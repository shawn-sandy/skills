# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a skills repository for Claude Code, containing modular skill packages that extend Claude's capabilities with specialized knowledge, workflows, and tool integrations. Each skill is self-contained with its own documentation and bundled resources.

## Skill Structure

Every skill follows this standard structure:

```
skill-name/
├── SKILL.md (required)           # Main skill prompt with YAML frontmatter
├── README.md (optional)          # User documentation
├── LICENSE.txt (optional)        # License information
├── scripts/                      # Executable code (Python/Bash)
├── references/                   # Documentation loaded as needed
├── templates/                    # Output templates
└── assets/                       # Files used in output
```

## Working with Skills

### SKILL.md Requirements

Every SKILL.md must have:

1. **YAML Frontmatter** (required):
   ```yaml
   ---
   name: skill-name
   description: Clear description of when to use this skill
   version: X.Y.Z (optional, defaults to 0.1.0)
   license: Complete terms in LICENSE.txt (optional)
   ---
   ```

2. **Validation Rules**:
   - Name: lowercase, hyphen-case, max 40 chars
   - Description: specific, third-person, no angle brackets
   - Version: semantic versioning (MAJOR.MINOR.PATCH)

3. **Content Guidelines**:
   - Focus on procedural instructions and workflows
   - Keep core content lean (<5k words)
   - Move detailed reference material to `references/` directory
   - Avoid duplication between SKILL.md and reference files

### Bundled Resources

**scripts/** - Executable code for deterministic tasks:
- Use when code is repeatedly rewritten or reliability is critical
- Common languages: Python, Bash
- Should be executable with proper shebang
- May include requirements.txt or package.json for dependencies

**references/** - Documentation loaded into context as needed:
- Database schemas, API docs, detailed guides
- Loaded only when Claude determines it's needed
- For large files (>10k words), include grep patterns in SKILL.md

**templates/** - Files used to generate output:
- Markdown templates with variable substitution
- Use `{{VARIABLE_NAME}}` for substitution points

**assets/** - Files copied/used in output:
- Not loaded into context
- Images, fonts, boilerplate code, sample documents

### Current Skills in Repository

1. **mcp-builder** - Create MCP (Model Context Protocol) servers
2. **npm-monorepo-publish** - Publish Lerna monorepo packages to npm
3. **skill-creator** - Create new Claude Code skills
4. **skill-packager** - Package skills into distributable ZIP files
5. **wcag-compliance-reviewer** - Review code for WCAG 2.1 AA compliance

## Common Development Tasks

### Creating a New Skill

1. Create directory: `mkdir skill-name/`
2. Create SKILL.md with YAML frontmatter and instructions
3. Add bundled resources as needed (scripts/, references/, etc.)
4. Validate structure before distribution

### Packaging a Skill for Distribution

Use the skill-packager skill or run the packaging script directly:

```bash
python skill-packager/scripts/package_and_document.py \
  --skill-path /path/to/skill \
  --version X.Y.Z \
  --output-dir /Users/shawnsandy/.claude/downloads/skill-name
```

This generates:
- Versioned ZIP file: `skill-name-vX.Y.Z.zip`
- Installation documentation: `Download.md`
- User documentation: `{SkillName}-doc.md`

### Testing Skills

Skills are loaded by Claude Code based on their frontmatter metadata. To test:

1. Ensure skill directory is in `~/.claude/skills/`
2. Verify SKILL.md has valid frontmatter
3. Trigger by using phrases matching the description
4. Check that bundled resources are accessible

## Version Management

Skills use semantic versioning (MAJOR.MINOR.PATCH):

- **Patch** (X.Y.Z+1): Bug fixes, documentation updates
- **Minor** (X.Y+1.0): New features, backward-compatible changes
- **Major** (X+1.0.0): Breaking changes, major refactors

Update version in SKILL.md frontmatter when making changes.

## Progressive Disclosure Design

Skills use a three-level loading system to manage context efficiently:

1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - Loaded when skill triggers (<5k words)
3. **Bundled resources** - Loaded as needed by Claude (variable size)

Keep SKILL.md lean by moving detailed content to reference files.

## File Naming Conventions

- Skill directories: `lowercase-hyphen-case/`
- SKILL.md: Always uppercase
- Scripts: `snake_case.py` or `kebab-case.sh`
- References: `lowercase-hyphen-case.md`
- Templates: `descriptive_template.md`

## Git Workflow

The repository tracks skills but may gitignore some skill directories. Check `.gitignore` for excluded skills.

Current untracked skills (per git status):
- mcp-builder/
- npm-monorepo-publish/
- skill-packager/
- wcag-compliance-reviewer/

These may be project/gitignored skills for personal use.

## Best Practices

1. **Single Responsibility**: Each skill should have one clear purpose
2. **Self-Contained**: Skills should work independently without cross-dependencies
3. **Clear Triggers**: Description should make it obvious when to use the skill
4. **Documentation**: Include README.md for user-facing documentation
5. **Validation**: Always validate SKILL.md frontmatter before distribution
6. **Versioning**: Increment version on any changes
7. **License**: Include LICENSE.txt if distributing publicly

## Scripts and Automation

### Python Scripts

Most skills use Python 3 for automation. Common patterns:

- Argument parsing with `argparse`
- Path handling with `pathlib.Path`
- YAML/frontmatter parsing with regex
- ZIP file creation with `zipfile`
- Input validation with clear error messages

### Script Execution

Scripts in `scripts/` directories may be executed directly or loaded into context for review/modification. They should:

- Include docstrings explaining purpose and usage
- Accept command-line arguments for flexibility
- Provide clear error messages
- Exit with appropriate status codes
- Include example usage in comments/docstrings

## Troubleshooting

### Skill Not Loading

- Verify SKILL.md exists in skill directory
- Check YAML frontmatter is valid (proper `---` delimiters)
- Ensure `name` and `description` fields are present
- Verify skill directory is in `~/.claude/skills/`

### Packaging Errors

- Validate SKILL.md structure before packaging
- Check version format is valid (X.Y.Z)
- Ensure all referenced files exist
- Verify output directory has write permissions

### Script Execution Issues

- Check script has execute permissions (`chmod +x script.sh`)
- Verify Python version (>=3.7 recommended)
- Install dependencies if requirements.txt exists
- Check shebang points to correct interpreter
