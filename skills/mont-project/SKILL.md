---
name: mont-project
description: Create or edit native Mont project values, register owned originals, validate, and export/reopen an offline project bundle using the Mont developer-preview CLI. Not for video rendering or timeline composition.
license: Apache-2.0
---

# Native Mont project editing

Use an authorized, existing `mont` executable. There is no generally downloadable
binary promised by this skill. The recipe targets the **developer-preview
contract `mont 0.1.0-preview.1`**, not a stable public release or compatibility
range. Run the chosen executable's `--version` and `--help` first; stop if its
identity/commands differ. Do not install unsigned evaluation artifacts, bypass
Gatekeeper, or download a substitute executable automatically.

This workflow edits native JSON project values, registers originals, and bundles
projects. **It does not render MP4, compose a timeline, decode media, or provide
Flutter/mobile project roundtrips.** Asset registration is not clip placement.

## Safety and rights

- Obtain an explicit workspace path and a new output-directory path. Resolve all
  asset/command/bundle paths explicitly: `-C` selects a workspace but does not
  change the invoking working directory. Quote paths; never interpolate user text
  into shell command strings.
- Use only original text/metadata and assets the user owns or has permission to
  use. Never fetch third-party media for this recipe. Asset rights stay with
  their owners; registration/bundling does not relicense them.
- For existing projects, inspect `project.json`, `status`, `diff`, and `history`
  before proposing edits. Stop on malformed state or unavailable originals;
  do not reset `.mont/`, repair files by deleting them, or initialize over a
  workspace. `status` may create local session state when reopening public files.
- Preserve every unrelated project field, metadata key, original, and local file.
  Never replace the full payload. Replacing `/metadata` replaces that entire
  value: read it first, retain unrelated keys, and apply only approved changes.
- Ask before destructive changes, replacing existing user-authored values, deleting
  anything, or any remote publication. Do not run `pull`, `push`, `sync`, `clone`,
  or `init --git` as a hidden side effect. This recipe is offline and uses no token.
- Do not edit concurrently with another writer. Refuse existing destinations,
  including symlinks. Retain partial outputs on failure and report their path;
  do not clean up user data or retry an overwrite automatically.

## Use the command contract

Except for help/version (plain text), request `--json` on every invocation. A
successful process must exit 0 **and** return `{"ok":true,"result":...}`. Failures
return `{"ok":false,"error":{"code":"...","message":"..."}}`; inspect the
message and stop. Exit 2 means invalid input, 3 conflict/stale revision, 4 asset
integrity failure, 5 permission denied, and 1 another runtime failure. Never
interpret failure output as a project result.

Use a complete native command envelope, not a bare command. For an approved title
edit, send this JSON through stdin to
`mont --json -C "/absolute/workspace" dispatch -`:

```json
{
  "commandId": "a-new-unique-id-for-this-intentional-edit",
  "command": {
    "type": "setProjectValue",
    "pointer": "/title",
    "value": "Autumn release brief"
  }
}
```

Generate a fresh ID for each intentional edit; command IDs are idempotency keys,
not labels to reuse for different values. The recipe generates UUID-based IDs.
JSON-encode values rather than concatenating shell/JSON text. For metadata, use
the same full envelope with pointer `/metadata` and the approved merged object.
Do not invent additional SDK commands or media/timeline semantics.

The supported offline sequence is:

```sh
mont --json init "/absolute/new-project"
mont --json -C "/absolute/new-project" status
mont --json -C "/absolute/new-project" dispatch "/absolute/command.json"
mont --json -C "/absolute/new-project" asset add "/absolute/owned-original.png"
mont --json -C "/absolute/new-project" validate
mont --json -C "/absolute/new-project" export --bundle "/absolute/new-bundle"
mont --json -C "/absolute/new-bundle" status
mont --json -C "/absolute/new-bundle" validate
```

Omit `asset add` when no original is supplied. Never reuse the example destination
paths without checking that they are new. An exported bundle is a directory with
project identity, native payload, a manifest, and pinned originals; it is not a
video file. Validate again after reopening, compare title/metadata/project
identity, and verify any supplied original's hash and bundled bytes.

## Release-brief recipe

The adjacent `release_brief.py` requires Python 3.11+ and creates only a **new**
output directory, containing `project/` and `bundle/`. It accepts parameterized
original title/metadata and an optional owned original. It cannot edit an
existing workspace. Locate it relative to this skill file; do not assume the
agent's working directory is the skill directory.

```sh
python3 "/absolute/skill-directory/release_brief.py" \
  --mont "/absolute/authorized/mont" \
  --output-dir "/absolute/new-release-brief" \
  --title "Autumn release brief" \
  --metadata '{"owner":"Your team","release":"Autumn","summary":"Your original release notes"}'
```

Optionally add `--original "/absolute/your-original.png"`. Registering an original
copies it; the source is not modified or removed. The script validates and reopens
the bundle, compares portable project state, and checks the original's checksum
and bundled bytes. It prints JSON paths only after these checks succeed. It
keeps all generated data on failure for inspection; choose a fresh output path
for another run. Report only checks actually performed, never claim rendering.
