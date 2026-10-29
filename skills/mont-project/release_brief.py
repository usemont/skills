#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Create a new native release brief and a verified offline bundle; never render video."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import uuid


PREVIEW_IDENTITY = "mont 0.1.0-preview.1"


def invoke(binary, workspace, *command, envelope=None):
    process = subprocess.run(
        [binary, "--json", "-C", str(workspace), *map(str, command)],
        input=json.dumps(envelope) if envelope is not None else None,
        text=True, capture_output=True, check=False,
    )
    try:
        response = json.loads(process.stdout)
    except ValueError as error:
        raise RuntimeError(f"Mont did not return JSON: {process.stdout}\n{process.stderr}") from error
    if process.returncode != 0 or response.get("ok") is not True:
        raise RuntimeError(f"Mont {' '.join(map(str, command))}: {response}\n{process.stderr}")
    return response["result"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mont", required=True, help="Authorized existing Mont executable path or PATH name")
    parser.add_argument("--output-dir", required=True, type=Path, help="New directory; its parent must already exist")
    parser.add_argument("--title", required=True)
    parser.add_argument("--metadata", required=True, type=json.loads, help="JSON object containing your release brief metadata")
    parser.add_argument("--original", type=Path, help="Optional original asset you own or have permission to use")
    args = parser.parse_args()
    if not args.title.strip() or not isinstance(args.metadata, dict):
        parser.error("Provide a nonempty title and a JSON object for --metadata")
    output = args.output_dir.expanduser().absolute()
    if os.path.lexists(output):
        parser.error("--output-dir must not exist (including a symlink); choose a fresh path")
    if not output.parent.is_dir():
        parser.error("The output parent directory must already exist")
    original = None
    original_digest = None
    if args.original is not None:
        original = args.original.expanduser().resolve(strict=True)
        if not original.is_file():
            parser.error("--original must be a readable file")
        with original.open("rb") as stream:
            original_digest = hashlib.file_digest(stream, "sha256").hexdigest()
    binary = shutil.which(args.mont)
    if binary is None:
        parser.error("Mont executable not found; this repository does not install a binary")
    binary = str(Path(binary).resolve())
    identity = subprocess.run([binary, "--version"], text=True, capture_output=True, check=True).stdout.strip()
    if identity != PREVIEW_IDENTITY:
        parser.error(f"This developer-preview recipe requires {PREVIEW_IDENTITY!r}; received {identity!r}")
    subprocess.run([binary, "--help"], text=True, capture_output=True, check=True)

    # Atomic reservation: an existing output is never reused, even in a race.
    output.mkdir()
    project = output / "project"
    bundle = output / "bundle"
    invoke(binary, project, "init", project, "--project-id", "release-brief-" + uuid.uuid4().hex)
    for key, value in (("title", args.title), ("metadata", args.metadata)):
        invoke(binary, project, "dispatch", "-", envelope={
            "commandId": "release-brief-" + uuid.uuid4().hex,
            "command": {"type": "setProjectValue", "pointer": "/" + key, "value": value},
        })
    if original is not None:
        invoke(binary, project, "asset", "add", original)
    invoke(binary, project, "validate")
    invoke(binary, project, "export", "--bundle", bundle)
    invoke(binary, bundle, "status")
    invoke(binary, bundle, "validate")
    for name in ("project.json", "mont.json", "assets/manifest.json"):
        if json.loads((project / name).read_text()) != json.loads((bundle / name).read_text()):
            raise RuntimeError(f"Reopened bundle changed {name}; output retained for inspection")
    payload = json.loads((bundle / "project.json").read_text())
    if payload.get("title") != args.title or payload.get("metadata") != args.metadata:
        raise RuntimeError("Reopened bundle lost requested values; output retained for inspection")
    if original_digest is not None:
        with original.open("rb") as stream:
            if hashlib.file_digest(stream, "sha256").hexdigest() != original_digest:
                raise RuntimeError("Original changed during this run")
        manifest = json.loads((bundle / "assets/manifest.json").read_text())
        if original_digest not in json.dumps(manifest):
            raise RuntimeError("Bundle manifest does not pin the supplied original")
        found = False
        for blob in (bundle / "assets/local").rglob("*"):
            if blob.is_file():
                with blob.open("rb") as stream:
                    found = found or hashlib.file_digest(stream, "sha256").hexdigest() == original_digest
        if not found:
            raise RuntimeError("Bundle does not contain the supplied original bytes")
    print(json.dumps({"project": str(project), "bundle": str(bundle), "binary": identity}))


if __name__ == "__main__":
    main()
