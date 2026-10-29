# Mont native project skill

An original agent skill and a small release-brief recipe for native Mont project
editing, original registration, validation, and offline bundling. This is **not a
video-rendering or timeline-composition tool**. Bundle export produces a project
directory, not MP4. No Flutter/mobile project interoperability is promised.

## Availability

The signed and Apple-notarized **Mont CLI 0.1.0-preview.1** is available for
**Apple Silicon (ARM64), macOS 14 or newer**:

```sh
brew install usemont/tap/mont
```

See the [official release](https://github.com/usemont/mont-cli/releases/tag/v0.1.0-preview.1)
for the archive, checksums, and proprietary Nauchu AB preview terms. This skills
repository contains no executable distribution, SDK, or private source.

Check your executable with `mont --version` and `mont --help`. The recipe requires
the exact identity `mont 0.1.0-preview.1`, not a stable compatibility range; it
refuses another identity rather than guessing. Use only official signed releases;
never bypass platform security or redistribute an internal evaluation executable.

## Install the agent skill

From this repository's root, copy the self-contained skill directory to your
agent's normal skill location. For an agent using the `.claude/skills` convention:

```sh
mkdir -p "$HOME/.claude/skills"
mkdir "$HOME/.claude/skills/mont-project" && \
  cp -n skills/mont-project/SKILL.md skills/mont-project/release_brief.py \
    "$HOME/.claude/skills/mont-project/"
```

The second `mkdir` intentionally fails if that skill already exists; stop instead
of replacing an existing installation. This is an ordinary file copy, not a Mont
installer. Other agents can use their own documented skill directory or load
`skills/mont-project/SKILL.md` explicitly. Keep the recipe beside `SKILL.md`.

## Create a release brief

Requirements: Python **3.11+** (standard library only), an authorized Mont preview
executable, and an already-existing parent directory for a **new** output path.
No account, network, SDK checkout, Rust toolchain, or media download is needed.

```sh
python3 skills/mont-project/release_brief.py \
  --mont /absolute/path/to/mont \
  --output-dir /absolute/path/to/new-release-brief \
  --title "Autumn release brief" \
  --metadata '{"owner":"Your team","release":"Autumn","summary":"Your original release notes"}'
```

Optionally append `--original /absolute/path/to/your-original.png` for an asset
you own or have permission to use. An original is registered and bundled, **not**
placed on a timeline. Asset registration does not decode or validate media format.

The recipe creates `project/` and `bundle/` inside the specified output directory.
It dispatches full native envelopes with unique command IDs, sets title/metadata,
optionally registers the original, validates, exports, then reopens and validates
the bundle. It compares portable project state and verifies original checksums
and retained bytes. On success it prints a JSON object with absolute project and
bundle paths and the binary identity. Source data is never deleted or overwritten.
Existing output paths (even empty directories or dangling symlinks) are refused.
Preflight failures create no output; failures after creation retain partial output
for inspection. There is no automatic deletion, overwrite, remote sync, or retry.

This recipe creates new projects only. For existing projects, follow the skill's
inspection and targeted-edit instructions; retain unrelated fields and metadata,
and obtain permission before destructive changes or replacing authored values.

## Focused real-binary check

From this repository's root, choose another **nonexistent** output directory:

```sh
python3 tests/verify_release_brief.py \
  --mont /absolute/path/to/mont \
  --output-dir /absolute/path/to/new-skill-check
```

This runnable standard-library check invokes the actual CLI, not a mock. It
constructs original two-pixel artwork, checks recipe output and bundled bytes,
renames its own source/original to demonstrate reopening without their former
paths, checks targeted edits preserve unrelated metadata, and checks refused
operations do not change existing data. It exercises existing/symlink output,
missing-original and invalid-metadata rejection, invalid native commands, and
refused self-overwrite export. Every generated file is retained under the
explicit check directory; nothing is removed. A `Passed` line is emitted only
when this check is actually run and all assertions succeed. Shipping the check
is not evidence that it has passed on a particular binary.

## License and contribution boundary

The original skill text, recipe, and verification script in this repository are
licensed under **Apache-2.0**. Submit only original contributions or material for
which you can grant that license. No third-party media is included. The tiny
verification artwork is generated from original pixel values by the script.

The Mont CLI executable, private SDK/engine, monorepo, existing private examples,
and third-party components are **not** included or relicensed by this repository.
Their separate terms/notices still apply. User-supplied text and assets keep their
own rights: using this recipe does not publish them or grant anyone a license to
them. Review generated project payloads, metadata, and originals for confidential
material before sharing a bundle; bundles contain originals, not just references.

## Support and contributions

Use [issues](https://github.com/usemont/skills/issues) for bugs and proposals.
See [CONTRIBUTING.md](CONTRIBUTING.md) for original contributions and real-binary
verification, or [SECURITY.md](SECURITY.md) to report a vulnerability privately.
