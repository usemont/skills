# Mont agent skills

Teach your agent to edit native Mont videos and render completed MP4s.

<table>
  <tr>
    <td width="33%"><a href="https://github.com/usemont/awesome-workflows/tree/main/templates/kinetic/stretch-row-repeater"><img src="https://raw.githubusercontent.com/usemont/awesome-workflows/main/assets/previews/stretch-row-repeater-square.gif" alt="Stretch Row Repeater animation" width="100%"></a></td>
    <td width="33%"><a href="https://github.com/usemont/awesome-workflows/tree/main/templates/kinetic/letter-inflate-swell"><img src="https://raw.githubusercontent.com/usemont/awesome-workflows/main/assets/previews/letter-inflate-swell-square.gif" alt="Letter Inflate Swell animation" width="100%"></a></td>
    <td width="33%"><a href="https://github.com/usemont/awesome-workflows/tree/main/templates/kinetic/spiral-type"><img src="https://raw.githubusercontent.com/usemont/awesome-workflows/main/assets/previews/spiral-type-square.gif" alt="Spiral Type animation" width="100%"></a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/usemont/awesome-workflows/tree/main/templates/kinetic/stretch-row-repeater">Stretch Row Repeater</a></td>
    <td align="center"><a href="https://github.com/usemont/awesome-workflows/tree/main/templates/kinetic/letter-inflate-swell">Letter Inflate Swell</a></td>
    <td align="center"><a href="https://github.com/usemont/awesome-workflows/tree/main/templates/kinetic/spiral-type">Spiral Type</a></td>
  </tr>
</table>

Native Mont renders · [Templates and workflow quickstart](https://github.com/usemont/awesome-workflows)

## Install the skill

Install [Mont CLI](https://github.com/usemont/mont-cli/blob/main/docs/install.md) **0.1.0-preview.5 or newer** ([Linux](https://github.com/usemont/mont-cli/blob/main/docs/install.md#linux)), then clone this repository. From its root, for Claude Code:

```sh
mkdir -p "$HOME/.claude/skills"
mkdir "$HOME/.claude/skills/mont-project" && \
  cp -n skills/mont-project/SKILL.md "$HOME/.claude/skills/mont-project/"
```

An existing skill is never overwritten; review updates deliberately. Other agents can load [SKILL.md](skills/mont-project/SKILL.md) directly.

[Apache-2.0 license](LICENSE) · [Contribute](CONTRIBUTING.md) · [Security](SECURITY.md)
