# Mont CLI agent skills

Agent instructions for native Mont project editing, reusable workflows, and completed MP4 exports. Workflows and templates live in **[usemont/workflows](https://github.com/usemont/workflows)**; this repository teaches agents to use them rather than duplicating their assets or implementing orchestration in Python.

## Install Mont

Use **Mont CLI 0.1.0-preview.5 or newer**. Earlier public previews cannot run `mont workflow`.

On Apple Silicon, macOS 14 or newer:

```sh
brew install usemont/tap/mont
# Existing installation:
brew update && brew upgrade usemont/tap/mont
mont --version
```

For Debian 12 ARM64/amd64, use the [official signed APT instructions](https://github.com/usemont/mont-cli#linux-signed-apt-preview-channel). Updates use `apt-get update` and `apt-get install --only-upgrade mont`. Homebrew and APT install external FFmpeg/ffprobe; they are not bundled into Mont. Windows is not a public preview target yet. Never install unsigned internal artifacts or bypass platform security.

The CLI and SDK remain proprietary under Nauchu AB's preview terms; this repository contains neither executable distributions nor private source. See the [versioned release](https://github.com/usemont/mont-cli/releases/tag/v0.1.0-preview.5) for checksums, provenance, notices and terms.

## Install the agent skill

From this repository's root, copy the skill into your agent's documented skill location. For the `.claude/skills` convention:

```sh
mkdir -p "$HOME/.claude/skills"
mkdir "$HOME/.claude/skills/mont-project" && \
  cp -n skills/mont-project/SKILL.md "$HOME/.claude/skills/mont-project/"
```

The second `mkdir` intentionally refuses an existing installation. Review and update an existing skill deliberately; do not overwrite it silently. Other agents can load `skills/mont-project/SKILL.md` directly. No Python helper is needed.

## Run an editable kinetic template

```sh
git clone https://github.com/usemont/workflows.git
cd workflows
template=stretch-row-repeater # or letter-inflate-swell / spiral-type
mont --json -C "$PWD/out/$template" workflow run \
  "$PWD/templates/kinetic/$template/template.mont" --run-id "$template"
```

Use a new output directory and run ID for a new generation. The workflow writes an editable `project/` and `preview.mp4`. It requires no inference account or API key. First use of a non-embedded font requires network access. To select portrait or square, follow the collection's [input and aspect-ratio instructions](https://github.com/usemont/workflows#kinetic-typography); canvas dimensions are inputs, not separate template copies.

For Markdown → narrated explainer, follow the [workflow's configuration and recovery guide](https://github.com/usemont/workflows/tree/main/workflows/explainer). It calls real inference APIs, incurs costs, and retains an experimental visual-fidelity warning. Review local endpoint/model settings and credential environment references before running. Never put keys in workflow source, project files, issues or logs.

## Verify a change

Run `mont --version` and `mont --help`, then exercise the changed instructions with an authorized installed binary and fresh output paths. Check `workflow status RUN_ID`, validate the resulting editable workspace, and inspect/decode the completed MP4. Record the binary version, workflow revision, inputs, output dimensions and observed result; shipping instructions alone is not evidence they passed.

For local edits, retain unrelated project fields and originals. `export --bundle` produces an editable directory, **not** an MP4; `render` produces an MP4. No Flutter/mobile roundtrip is promised. CLI command and packaged-workflow verification belongs to the runtime release; workflow/template behavior checks belong in the workflow collection.

## License, safety and contributions

Skill text is **Apache-2.0**. Submit only original material you can license under those terms. The proprietary CLI/SDK and user assets are not relicensed. Workflows are trusted executable instructions, not a sandbox; inspect them before execution and review bundles for private originals before sharing.

Use [issues](https://github.com/usemont/skills/issues) for skill bugs and proposals. See [CONTRIBUTING.md](CONTRIBUTING.md) for real-binary verification and [SECURITY.md](SECURITY.md) for private vulnerability reporting. Runtime bugs belong in [usemont/mont-cli](https://github.com/usemont/mont-cli/issues); workflows and templates belong in [usemont/workflows](https://github.com/usemont/workflows/issues).
