#!/usr/bin/env python3
"""Safely validate, preview, apply, and restore unified Git patches.

Install this file as tools/apply_agent_patch.py in a Git repository.

Preview a patch (default; no files are changed):
    python tools/apply_agent_patch.py patches/my-change.patch

Apply after reviewing the patch:
    python tools/apply_agent_patch.py patches/my-change.patch --apply

Read patch contents from stdin:
    git diff | python tools/apply_agent_patch.py - --apply

Restore a pre-apply backup (preview first, then add --apply):
    python tools/apply_agent_patch.py --restore .git/agent-patch-backups/<backup-id>
    python tools/apply_agent_patch.py --restore .git/agent-patch-backups/<backup-id> --apply

Requires Python 3.10+ and Git. No third-party Python packages are required.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Iterable

APP_NAME = "apply_agent_patch.py"
MANIFEST_NAME = "manifest.json"


class PatchToolError(RuntimeError):
    """Expected user-facing failure."""


def run_git(args: list[str], *, cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    try:
        result = subprocess.run(
            ["git", *args], cwd=str(cwd), text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
    except FileNotFoundError as exc:
        raise PatchToolError("Git was not found. Install Git and make sure `git` is on PATH.") from exc
    if check and result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise PatchToolError(detail or f"Git command failed with exit code {result.returncode}.")
    return result


def discover_root(explicit_root: Path | None) -> Path:
    if explicit_root is not None:
        candidate = explicit_root.expanduser().resolve()
    else:
        # Resolve from this script's directory so invoking it from tools/ works.
        candidate = Path(__file__).resolve().parent
    result = run_git(["rev-parse", "--show-toplevel"], cwd=candidate, check=False)
    if result.returncode != 0:
        raise PatchToolError(
            f"Could not find a Git repository from {candidate}. Run this inside the repository, "
            "or pass --root PATH."
        )
    git_root = Path(result.stdout.strip()).resolve()
    if explicit_root is not None and candidate != git_root:
        raise PatchToolError(f"--root must be the repository root: {git_root}")
    return git_root


def load_patch(patch_arg: str) -> tuple[str, Path | None]:
    """Return patch content and optional temporary path that must be cleaned up."""
    if patch_arg == "-":
        content = sys.stdin.read()
        if not content.strip():
            raise PatchToolError("Patch input from stdin is empty.")
        temp = tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", suffix=".patch", delete=False)
        try:
            temp.write(content)
        finally:
            temp.close()
        return content, Path(temp.name)

    patch_path = Path(patch_arg).expanduser().resolve()
    if not patch_path.is_file():
        raise PatchToolError(f"Patch file not found: {patch_path}")
    try:
        content = patch_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise PatchToolError("Patch file is not UTF-8 text. This utility expects a text unified diff.") from exc
    if not content.strip():
        raise PatchToolError(f"Patch file is empty: {patch_path}")
    return content, patch_path


def clean_patch_path(value: str) -> str | None:
    """Convert a Git diff path (a/foo, b/foo, /dev/null) to a safe repo-relative path."""
    value = value.strip()
    if not value or value == "/dev/null":
        return None
    # Backslashes can be path separators on Windows. Normalize, then validate.
    value = value.replace("\\", "/")
    if value.startswith("/") or (len(value) >= 2 and value[1] == ":"):
        raise PatchToolError(f"Absolute path in patch is not allowed: {value!r}")
    if value.startswith("a/") or value.startswith("b/"):
        value = value[2:]
    p = PurePosixPath(value)
    if not value or any(part in ("", ".", "..") for part in p.parts):
        raise PatchToolError(f"Unsafe path in patch: {value!r}")
    return p.as_posix()


def parse_patch_paths(patch_text: str) -> list[str]:
    """Extract file paths from standard `git diff`/`git format-patch` unified patches."""
    found: set[str] = set()
    for line in patch_text.splitlines():
        if not line.startswith("diff --git "):
            continue
        payload = line[len("diff --git "):]
        try:
            parts = shlex.split(line, posix=True)
        except ValueError as exc:
            raise PatchToolError(f"Cannot parse a diff header safely: {line}") from exc
        if len(parts) == 4 and parts[0] == "diff" and parts[1] == "--git":
            raw_paths = parts[2:4]
        else:
            # Some Git configurations leave spaces in paths unquoted. In that
            # case the header is ambiguous to shlex; locate the ` b/` boundary.
            # Prefer the split where old/new names are identical (ordinary edit).
            candidates: list[tuple[str, str]] = []
            start = 0
            while True:
                split_at = payload.find(" b/", start)
                if split_at < 0:
                    break
                old_raw, new_raw = payload[:split_at], payload[split_at + 1:]
                if old_raw.startswith("a/") and new_raw.startswith("b/"):
                    candidates.append((old_raw, new_raw))
                start = split_at + 1
            same_name = [pair for pair in candidates if pair[0][2:] == pair[1][2:]]
            if len(same_name) == 1:
                raw_paths = list(same_name[0])
            elif len(candidates) == 1:
                raw_paths = list(candidates[0])
            else:
                raise PatchToolError(f"Unsupported or ambiguous diff header: {line}")
        for raw in raw_paths:
            rel = clean_patch_path(raw)
            if rel:
                found.add(rel)

    # Fallback for simple unified diffs that omit `diff --git` headers.
    if not found:
        lines = patch_text.splitlines()
        i = 0
        while i + 1 < len(lines):
            if lines[i].startswith("--- ") and lines[i + 1].startswith("+++ "):
                try:
                    old_parts = shlex.split(lines[i][4:], posix=True)
                    new_parts = shlex.split(lines[i + 1][4:], posix=True)
                except ValueError as exc:
                    raise PatchToolError("Cannot safely parse unified diff file headers.") from exc
                if old_parts and new_parts:
                    old = clean_patch_path(old_parts[0].split("\t", 1)[0])
                    new = clean_patch_path(new_parts[0].split("\t", 1)[0])
                    if old:
                        found.add(old)
                    if new:
                        found.add(new)
                i += 2
            else:
                i += 1

    if not found:
        raise PatchToolError(
            "No file paths found in the patch. Supply a standard unified diff generated by `git diff` "
            "or `git format-patch`."
        )
    return sorted(found)


def ensure_safe_targets(root: Path, relatives: Iterable[str]) -> None:
    root_resolved = root.resolve()
    for rel in relatives:
        candidate = root / Path(*PurePosixPath(rel).parts)
        # Reject symlinks: a backup/restore must not silently replace a link with a file.
        cur = candidate
        while cur != root and cur != cur.parent:
            if cur.is_symlink():
                raise PatchToolError(f"Refusing to patch a path containing a symlink: {rel}")
            cur = cur.parent
        resolved = candidate.resolve(strict=False)
        if resolved != root_resolved and root_resolved not in resolved.parents:
            raise PatchToolError(f"Patch target escapes repository root: {rel}")
        if candidate.exists() and candidate.is_dir():
            raise PatchToolError(f"Patch target is a directory, not a file: {rel}")


def git_patch_args(*, check_only: bool, reverse: bool, strip: int, whitespace: str, patch_path: Path) -> list[str]:
    args = ["apply"]
    if check_only:
        args.append("--check")
    if reverse:
        args.append("--reverse")
    args.extend([f"--whitespace={whitespace}", "-p", str(strip), str(patch_path)])
    return args


def git_backup_root(root: Path) -> Path:
    result = run_git(["rev-parse", "--git-path", "agent-patch-backups"], cwd=root)
    location = Path(result.stdout.strip())
    if not location.is_absolute():
        location = root / location
    return location.resolve()


def make_backup(root: Path, relatives: list[str], patch_text: str, *, reverse: bool) -> Path:
    base = git_backup_root(root)
    base.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(patch_text.encode("utf-8")).hexdigest()[:8]
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = base / f"{stamp}-{digest}"
    suffix = 1
    while backup.exists():
        backup = base / f"{stamp}-{digest}-{suffix}"
        suffix += 1
    backup.mkdir(parents=True)
    files_dir = backup / "files"
    manifest_items: list[dict[str, object]] = []
    for rel in relatives:
        target = root / Path(*PurePosixPath(rel).parts)
        existed = target.is_file()
        manifest_items.append({"path": rel, "existed": existed})
        if existed:
            snapshot = files_dir / Path(*PurePosixPath(rel).parts)
            snapshot.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, snapshot)
    manifest = {
        "format": 1,
        "created_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "repository_root": str(root),
        "patch_sha256": hashlib.sha256(patch_text.encode("utf-8")).hexdigest(),
        "direction": "reverse" if reverse else "forward",
        "files": manifest_items,
    }
    (backup / MANIFEST_NAME).write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return backup


def restore_backup(root: Path, backup_path: Path, *, apply: bool) -> int:
    backup = backup_path.expanduser().resolve()
    manifest_path = backup / MANIFEST_NAME
    if not manifest_path.is_file():
        raise PatchToolError(f"Backup manifest not found: {manifest_path}")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PatchToolError(f"Cannot read backup manifest: {exc}") from exc
    if manifest.get("format") != 1 or Path(str(manifest.get("repository_root", ""))).resolve() != root:
        raise PatchToolError("Backup format or repository root does not match this repository.")
    files = manifest.get("files")
    if not isinstance(files, list) or not files:
        raise PatchToolError("Backup manifest contains no files.")
    paths: list[str] = []
    for item in files:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str) or not isinstance(item.get("existed"), bool):
            raise PatchToolError("Backup manifest contains an invalid file entry.")
        safe = clean_patch_path(item["path"])
        if not safe:
            raise PatchToolError("Backup manifest contains an invalid path.")
        paths.append(safe)
    ensure_safe_targets(root, paths)
    print(f"Backup: {backup}")
    print("Files that would be restored:")
    for item in files:
        print(f"  {'restore' if item['existed'] else 'remove'}  {item['path']}")
    if not apply:
        print("Preview only: no files were changed. Add --apply to restore this backup.")
        return 0

    files_dir = backup / "files"
    for item in files:
        rel = str(item["path"])
        target = root / Path(*PurePosixPath(rel).parts)
        if item["existed"]:
            snapshot = files_dir / Path(*PurePosixPath(rel).parts)
            if not snapshot.is_file():
                raise PatchToolError(f"Backup copy is missing for {rel}; restore stopped.")
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists() or target.is_symlink():
                if target.is_dir():
                    raise PatchToolError(f"Refusing to overwrite a directory: {rel}")
                target.unlink()
            shutil.copy2(snapshot, target)
        else:
            if target.exists() or target.is_symlink():
                if target.is_dir():
                    raise PatchToolError(f"Refusing to remove a directory: {rel}")
                target.unlink()
    print(f"Restored {len(files)} file path(s). Review with: git status --short && git diff")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("patch", nargs="?", help="path to a unified diff file, or '-' to read from stdin")
    parser.add_argument("--root", type=Path, help="repository root; auto-detected by default")
    parser.add_argument("--apply", action="store_true", help="write changes; without this flag only validate/preview")
    parser.add_argument("--reverse", action="store_true", help="apply the patch in reverse")
    parser.add_argument("--strip", type=int, default=1, help="path components to strip from diff paths (default: 1)")
    parser.add_argument("--whitespace", choices=("error-all", "warn", "nowarn", "fix"), default="error-all",
                        help="Git whitespace handling (default: error-all)")
    parser.add_argument("--no-backup", action="store_true", help="do not create automatic backups before applying")
    parser.add_argument("--restore", type=Path, help="preview/restore a backup directory created by this script")
    args = parser.parse_args()

    if args.strip < 0:
        parser.error("--strip must be >= 0")
    if args.restore is not None and (args.patch is not None or args.reverse or args.no_backup):
        parser.error("--restore cannot be combined with patch input, --reverse, or --no-backup")
    if args.restore is None and args.patch is None:
        parser.error("provide a patch file (or '-') or use --restore BACKUP_DIR")

    try:
        root = discover_root(args.root)
        if args.restore is not None:
            return restore_backup(root, args.restore, apply=args.apply)

        patch_text, patch_path = load_patch(args.patch)
        temp_to_remove: Path | None = patch_path if args.patch == "-" else None
        try:
            assert patch_path is not None
            relatives = parse_patch_paths(patch_text)
            ensure_safe_targets(root, relatives)

            check = run_git(
                git_patch_args(check_only=True, reverse=args.reverse, strip=args.strip,
                               whitespace=args.whitespace, patch_path=patch_path),
                cwd=root, check=False,
            )
            if check.returncode != 0:
                detail = (check.stderr or check.stdout).strip()
                raise PatchToolError("Patch validation failed; no changes were applied.\n" + detail)

            print(f"Repository: {root}")
            print(f"Patch SHA-256: {hashlib.sha256(patch_text.encode('utf-8')).hexdigest()}")
            print("Affected paths:")
            for rel in relatives:
                print(f"  {rel}")
            print("Validation: OK (git apply --check)")

            if not args.apply:
                print("Preview only: no files were changed. Add --apply after reviewing the patch.")
                return 0

            backup: Path | None = None
            if not args.no_backup:
                backup = make_backup(root, relatives, patch_text, reverse=args.reverse)
                print(f"Backup created: {backup}")

            applied = run_git(
                git_patch_args(check_only=False, reverse=args.reverse, strip=args.strip,
                               whitespace=args.whitespace, patch_path=patch_path),
                cwd=root, check=False,
            )
            if applied.returncode != 0:
                detail = (applied.stderr or applied.stdout).strip()
                if backup is not None:
                    try:
                        restore_backup(root, backup, apply=True)
                        raise PatchToolError("Patch application failed; original files were restored automatically.\n" + detail)
                    except PatchToolError as restore_exc:
                        if "original files were restored automatically" in str(restore_exc):
                            raise
                        raise PatchToolError(
                            "Patch application failed and automatic restore also failed. "
                            f"Manual recovery backup: {backup}\nApply error: {detail}\nRestore error: {restore_exc}"
                        ) from restore_exc
                raise PatchToolError("Patch application failed. No automatic backup was requested.\n" + detail)

            print(f"Applied patch to {len(relatives)} path(s).")
            if backup is not None:
                print(f"Rollback backup: {backup}")
                print(f"To preview rollback: python {APP_NAME} --restore \"{backup}\"")
                print(f"To execute rollback: python {APP_NAME} --restore \"{backup}\" --apply")
            print("Review the result with: git diff --check && git diff")
            return 0
        finally:
            if temp_to_remove is not None:
                try:
                    temp_to_remove.unlink(missing_ok=True)
                except OSError:
                    pass
    except PatchToolError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"ERROR: file operation failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
