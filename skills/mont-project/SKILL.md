---
name: mont-project
description: Create and edit native Mont projects, run reusable Mont workflows and kinetic templates, validate portable workspaces, and render completed MP4s with Mont CLI.
license: Apache-2.0
---

# Native Mont projects and workflows

Use an authorized **Mont CLI 0.1.0-preview.5 or newer**. Run `mont --version`, `mont --help`, and the relevant subcommand's `--help` before acting. Older public releases do not implement `mont workflow`. Install or upgrade only with the user's authorization through the [official distribution](https://github.com/usemont/mont-cli): Homebrew on Apple Silicon/macOS 14+, signed APT on Debian 12 ARM64/amd64. Windows is not a public target yet. Never use an unsigned internal build or bypass platform trust checks.

Reusable `.mont` workflows and native templates belong in [usemont/awesome-workflows](https://github.com/usemont/awesome-workflows), not in this skill. Use Mont's workflow runtime rather than Python orchestration, browser capture, or direct FFmpeg command sequences. FFmpeg/ffprobe are separately installed runtime dependencies; Mont invokes them where needed.

## Safety and ownership

- Obtain an explicit output base, inputs and intended edits. Use fresh destinations; refuse existing paths and symlinks rather than overwrite them. Retain partial results on failure and report their paths.
- Use owned or authorized text and assets. Registration/bundling does not relicense media. Do not download third-party media implicitly.
- For existing workspaces, inspect `project.json`, `status`, `diff`, and `history` before editing. Stop on malformed state or unavailable originals. Do not delete `.mont/`, reset a workspace, or initialize over one.
- Preserve unrelated fields, metadata, originals and local files. Replacing `/metadata` replaces the entire value; read and merge approved changes first. Do not replace the full payload.
- Ask before destructive changes or remote publication. Do not run `pull`, `push`, `sync`, `clone`, or `init --git` as hidden side effects. Do not write concurrently with another editor.
- Workflows are trusted executable instructions, **not a sandbox**. Review their graph, assets, API endpoints and local file access. Provider-backed workflows may transmit inputs and incur charges. Supply credentials through environment references; never embed keys or tokens in templates, generated projects, logs or issues.
- Use absolute definition/config/input filenames. `-C` selects the workflow output base or workspace; it does not change the shell's working directory. Quote paths and JSON-encode values, never interpolate user text into commands.

## Run a published template

Check out the official workflow collection using an approved new destination. From its root:

```sh
template=stretch-row-repeater # or letter-inflate-swell / spiral-type
mont --json -C "$PWD/out/$template" workflow run \
  "$PWD/templates/kinetic/$template/template.mont" --run-id "$template"
```

The workflow creates `project/` and `preview.mp4` under the output base. It performs native scene creation, validation and rendering; no inference key is needed. Use a new output base and run ID for an independent generation. Non-embedded fonts need network access on first use.

All three templates accept top-level `width`, `height`, `text`, `workspace`, `output`, and `fps` inputs. Review each template's declared defaults and controls; do not invent fields. Save settings such as `{"width":1080,"height":1920,"text":"MAKE SPACE"}` in a local JSON file and append `--inputs "/absolute/settings.json"`. Use 1920×1080 for landscape, 1080×1920 for portrait, or 1080×1080 for square. Layouts adapt natively; do not stretch a baked video.

For narrated explainers, follow the collection's [explainer guide](https://github.com/usemont/awesome-workflows/tree/main/workflows/explainer) and configuration example. Preserve its visual-fidelity caveats; execution success does not certify reference pixel identity. Do not promise a free run, fixed provider availability, or automatic approval of visual results.

## Durable workflow control

```sh
mont --json -C "/absolute/output-base" workflow list
mont --json -C "/absolute/output-base" workflow status RUN_ID
mont --json -C "/absolute/output-base" workflow cancel RUN_ID
mont --json -C "/absolute/output-base" workflow resume RUN_ID
```

Run accepts `--inputs`, `--config`, and `--run-id`. Resume uses frozen definitions, inputs and configuration from `.mont-workflows`; editing a source file does not change an existing run. Reusing an ID with different content is rejected. Inspect a failed run before any retry; do not delete its journal or silently charge for a new generation.

## Native project edits

Except help/version, use `--json`; success requires exit 0 and `{"ok":true,"result":...}`. Failure is `{"ok":false,"error":{"code":"...","message":"..."}}`; inspect it and stop. Exit 2 is invalid input, 3 conflict/stale revision, 4 asset integrity, 5 permission denied, and 1 another runtime failure.

Use full native command envelopes, not bare commands. An approved title edit sent to `mont --json -C "/absolute/workspace" dispatch -` is:

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

IDs are idempotency keys: generate a fresh ID for each distinct edit, never reuse one with different content. Inspect the executable's supported command contract rather than inventing SDK commands. `asset add` registers an original; it is not timeline placement. `import` and `render` have their own explicit contracts.

## Verify and report

Validate the resulting workspace with `mont --json -C "/absolute/workspace" validate`. Confirm the intended edit while preserving unrelated values. For MP4 work, check completed output duration, dimensions and frame count with the installed `ffprobe`, fully decode with the installed `ffmpeg`, and visually inspect relevant moments. These tools verify the output; they do not replace native Mont workflow orchestration.

`export --bundle` creates an editable directory with project payload and originals, not a video. Reopen and validate portable bundles; review private data before sharing. No Flutter/mobile project roundtrip is promised. Report exact binary version, run ID, output paths and only checks actually performed. A queued render or nonempty file is not proof of completed video.
