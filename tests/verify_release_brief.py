#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exercise the recipe with a real Mont binary; retain all output in a new directory."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import zlib


RECIPE = Path(__file__).resolve().parents[1] / "skills/mont-project/release_brief.py"
sys.path.insert(0, str(RECIPE.parent))
from release_brief import invoke


def snapshot(root):
    state = {}
    for path in root.rglob("*"):
        key = str(path.relative_to(root))
        if path.is_symlink():
            state[key] = ("link", os.readlink(path))
        elif path.is_file():
            with path.open("rb") as stream:
                state[key] = ("file", hashlib.file_digest(stream, "sha256").hexdigest())
        else:
            state[key] = ("directory",)
    return state


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mont", required=True, type=Path, help="Path to a real, authorized existing executable")
    parser.add_argument("--output-dir", required=True, type=Path, help="New directory; never removed by this script")
    args = parser.parse_args()
    binary = str(args.mont.expanduser().resolve(strict=True))
    root = args.output_dir.expanduser().absolute()
    if os.path.lexists(root) or not root.parent.is_dir():
        parser.error("--output-dir must not exist and its parent must already exist")
    root.mkdir()
    sentinel = root / "unrelated.txt"
    sentinel.write_text("Unrelated user material must survive.\n")
    original = root / "original.png"

    # Original two-pixel artwork, constructed here rather than downloaded or copied.
    chunks = []
    for kind, data in (
        (b"IHDR", struct.pack(">IIBBBBB", 2, 1, 8, 2, 0, 0, 0)),
        (b"IDAT", zlib.compress(bytes([0, 210, 40, 70, 25, 180, 115]))),
        (b"IEND", b""),
    ):
        chunks.append(struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data)))
    artwork = b"\x89PNG\r\n\x1a\n" + b"".join(chunks)
    original.write_bytes(artwork)
    metadata = {"owner": "Original contributor", "release": "Autumn notes", "notes": "Native project, not video"}
    title = 'Release brief: "Autumn" — original work'

    def recipe(destination, asset=original, metadata_json=json.dumps(metadata)):
        return subprocess.run(
            [sys.executable, str(RECIPE), "--mont", binary, "--output-dir", str(destination),
             "--title", title, "--metadata", metadata_json, "--original", str(asset)],
            text=True, capture_output=True, check=False,
        )

    destination = root / "brief"
    result = recipe(destination)
    assert result.returncode == 0, (result.stdout, result.stderr)
    report = json.loads(result.stdout)
    project = destination / "project"
    bundle = destination / "bundle"
    assert report["bundle"] == str(bundle)
    payload = json.loads((bundle / "project.json").read_text())
    assert payload["title"] == title and payload["metadata"] == metadata
    assert original.read_bytes() == artwork
    assert sentinel.read_text() == "Unrelated user material must survive.\n"
    assert any(path.is_file() and path.read_bytes() == artwork for path in (bundle / "assets/local").rglob("*"))

    text_only = root / "text-only"
    result = subprocess.run(
        [sys.executable, str(RECIPE), "--mont", binary, "--output-dir", str(text_only),
         "--title", title, "--metadata", json.dumps(metadata)],
        text=True, capture_output=True, check=False,
    )
    assert result.returncode == 0, (result.stdout, result.stderr)
    assert json.loads((text_only / "bundle/project.json").read_text())["metadata"] == metadata

    before = snapshot(root)
    result = recipe(destination)
    assert result.returncode != 0 and snapshot(root) == before, "Existing output was modified"
    for name, asset, metadata_json in (
        ("missing-original", root / "absent.png", json.dumps(metadata)),
        ("invalid-metadata", original, "[]"),
    ):
        result = recipe(root / name, asset, metadata_json)
        assert result.returncode != 0 and snapshot(root) == before, "Invalid input created or changed files"
    link = root / "occupied-link"
    link.symlink_to(root / "nonexistent-target")
    before = snapshot(root)
    result = recipe(link)
    assert result.returncode != 0 and snapshot(root) == before, "Symlink destination was not preserved"

    # Rename only our own source/original: reopen must not depend on their former paths.
    project.rename(destination / "source-retained")
    original.rename(root / "original-retained.png")
    invoke(binary, bundle, "status")
    invoke(binary, bundle, "validate")
    for command_id, pointer, value in (
        ("verify-unrelated", "/contributorNotes", {"keep": [1, "untouched"]}),
        ("verify-title", "/title", "Reopened release brief"),
    ):
        invoke(binary, bundle, "dispatch", "-", envelope={
            "commandId": command_id,
            "command": {"type": "setProjectValue", "pointer": pointer, "value": value},
        })
    payload = json.loads((bundle / "project.json").read_text())
    assert payload["title"] == "Reopened release brief"
    assert payload["contributorNotes"] == {"keep": [1, "untouched"]}
    assert payload["metadata"] == metadata
    invoke(binary, bundle, "validate")
    before = snapshot(root)
    rejection = subprocess.run(
        [binary, "--json", "-C", str(bundle), "dispatch", "-"],
        input=json.dumps({"commandId": "verify-rejection", "command": {"type": "notACommand"}}),
        text=True, capture_output=True, check=False,
    )
    assert rejection.returncode == 2 and json.loads(rejection.stdout)["ok"] is False
    assert snapshot(root) == before, "Rejected command changed project or unrelated data"
    rejection = subprocess.run(
        [binary, "--json", "-C", str(bundle), "export", "--bundle", str(bundle)],
        text=True, capture_output=True, check=False,
    )
    assert rejection.returncode != 0 and json.loads(rejection.stdout)["ok"] is False
    assert snapshot(root) == before, "Refused export changed existing data"
    print(f"Passed real-CLI recipe, offline reopen, original retention, targeted edits, and failure preservation; retained {root}")


if __name__ == "__main__":
    main()
