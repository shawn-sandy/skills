# Claude Code Skills Repository

A collection of modular skill packages that extend Claude Code's capabilities with specialized knowledge, workflows, and tool integrations.

## What Are Skills?

Skills are self-contained packages that transform Claude from a general-purpose agent into a specialized agent equipped with procedural knowledge for specific domains or tasks. Think of them as "onboarding guides" that provide:

- **Specialized workflows** - Multi-step procedures for complex tasks
- **Tool integrations** - Instructions for working with specific file formats, APIs, or frameworks
- **Domain expertise** - Company-specific knowledge, schemas, and business logic
- **Bundled resources** - Scripts, references, templates, and assets for complex tasks

### How Skills Work

Skills use a progressive disclosure design with three loading levels:

1. **Metadata** (name + description) - Always loaded (~100 words)
2. **SKILL.md body** - Loaded when skill triggers (<5k words)
3. **Bundled resources** - Loaded as needed (scripts/, references/, assets/)

This approach minimizes context usage while providing Claude with the right information at the right time.

## Available Skills

### mcp-builder
**Version:** 1.0.0
**Purpose:** Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools.

Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).

**Features:**
- Agent-centric design principles
- Comprehensive implementation guides for Python and TypeScript
- Evaluation framework for testing effectiveness
- Best practices for tool design and error handling

### skill-creator
**Version:** 1.0.0
**Purpose:** Guide for creating effective skills for Claude Code.

Use when creating a new skill or updating an existing skill that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.

**Features:**
- Step-by-step skill creation process
- YAML frontmatter validation
- Bundled resource organization
- Skill packaging automation

### skill-packager
**Version:** 1.0.0
**Purpose:** Package custom skills into versioned distributable ZIP files with installation and user documentation.

Use when preparing a skill for sharing, distribution, or archival. Supports semantic versioning, automatic documentation generation, and version management.

**Features:**
- Semantic versioning support (MAJOR.MINOR.PATCH)
- Automatic validation before packaging
- Installation guide generation
- User documentation generation
- Version history management

### npm-monorepo-publish
**Version:** 0.1.0
**Purpose:** Orchestrate publishing monorepo packages to npm using Lerna with OTP handling, pre-publish validation, and post-publish verification.

Use when publishing, releasing, or deploying packages to npm registry. Designed for Lerna-managed monorepos with 2FA-enabled npm accounts.

**Features:**
- Pre-flight validation (build + lint)
- Dry-run preview before publishing
- Interactive OTP prompt handling
- Post-publish verification
- Error recovery and rollback guidance

### wcag-compliance-reviewer
**Version:** 1.0.0
**Purpose:** Review HTML/CSS and React/TypeScript code for WCAG 2.1 Level AA accessibility compliance.

Use when reviewing code for accessibility, checking WCAG compliance, identifying accessibility issues, or auditing components/pages for a11y standards.

**Features:**
- Systematic review by WCAG principle (Perceivable, Operable, Understandable, Robust)
- Specific code fixes with examples
- Severity categorization (Errors, Warnings, Recommendations)
- Automated testing tool recommendations
- Python script for static analysis

## Installation

### Prerequisites

- [Claude Code](https://claude.com/claude-code) installed and configured
- Skills directory at `~/.claude/skills/` (created automatically by Claude Code)

### Installing Skills

1. Clone this repository or download individual skill packages:

```bash
# Clone the entire repository
git clone https://github.com/yourusername/claude-skills.git ~/.claude/skills/

# Or copy individual skill directories
cp -r /path/to/skill-name ~/.claude/skills/
```

2. Verify installation by checking that skills appear in Claude Code's available skills list.

### Installing from ZIP Packages

If you received a skill as a ZIP file:

1. Extract the ZIP file:
```bash
unzip skill-name-v1.0.0.zip
```

2. Copy the extracted directory to your skills folder:
```bash
cp -r skill-name ~/.claude/skills/
```

3. Verify the skill appears in Claude Code's available skills.

## Skill Structure

Every skill follows this standard directory structure:

```
skill-name/
├── SKILL.md (required)           # Main skill prompt with YAML frontmatter
├── LICENSE.txt (optional)        # License information
├── scripts/                      # Executable code (Python/Bash)
│   └── example_script.py
├── references/                   # Documentation loaded as needed
│   └── detailed_guide.md
├── templates/                    # Output templates
│   └── example_template.md
└── assets/                       # Files used in output
    └── logo.png
```

### SKILL.md Requirements

Every SKILL.md must include:

**YAML Frontmatter:**
```yaml
---
name: skill-name                  # Required: lowercase, hyphen-case, max 40 chars
description: Clear description    # Required: when to use this skill
version: X.Y.Z                    # Optional: defaults to 0.1.0
license: Complete terms in LICENSE.txt  # Optional
---
```

**Markdown Content:**
- Purpose and overview
- When to use the skill
- Step-by-step workflow
- References to bundled resources

### Bundled Resources

**scripts/** - Executable code for deterministic tasks:
- Use when code is repeatedly rewritten or reliability is critical
- Common languages: Python, Bash
- Should include proper shebang and be executable
- May include dependencies (requirements.txt, package.json)

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

## Creating New Skills

### Quick Start

1. Use the `skill-creator` skill in Claude Code:
   - Describe what the skill should do
   - Provide concrete usage examples
   - Claude will guide you through the creation process

2. Or initialize manually using the included script:

```bash
python skill-creator/scripts/init_skill.py my-new-skill --path ~/.claude/skills/
```

3. Edit the generated SKILL.md and add bundled resources as needed.

### Validation

Validate your skill structure before distribution:

```bash
python skill-creator/scripts/quick_validate.py ~/.claude/skills/my-new-skill/
```

This checks:
- YAML frontmatter format and required fields
- Naming conventions
- Description quality
- File organization

## Packaging for Distribution

Use the `skill-packager` skill to create distributable ZIP files:

```bash
python skill-packager/scripts/package_and_document.py \
  --skill-path ~/.claude/skills/my-skill \
  --version 1.0.0 \
  --output-dir ~/.claude/downloads/my-skill
```

This generates:
- **my-skill-v1.0.0.zip** - Versioned skill package
- **my-skill-Download.md** - Installation instructions
- **my-skill-doc.md** - User documentation

### Semantic Versioning

Skills use semantic versioning (MAJOR.MINOR.PATCH):

- **Patch** (X.Y.Z+1) - Bug fixes, documentation updates
- **Minor** (X.Y+1.0) - New features, backward-compatible changes
- **Major** (X+1.0.0) - Breaking changes, major refactors

## Development Workflow

### Creating a New Skill

1. **Understand the use case** - Gather concrete examples
2. **Plan resources** - Identify needed scripts, references, assets
3. **Initialize** - Create skill directory and SKILL.md
4. **Implement** - Write SKILL.md and add bundled resources
5. **Test** - Use the skill with real tasks
6. **Iterate** - Refine based on performance
7. **Package** - Create distributable ZIP for sharing

### Updating an Existing Skill

1. **Make changes** - Edit SKILL.md or bundled resources
2. **Increment version** - Update version in SKILL.md frontmatter
3. **Test** - Verify improvements with real tasks
4. **Re-package** - Generate new versioned ZIP

### Best Practices

1. **Single Responsibility** - Each skill should have one clear purpose
2. **Self-Contained** - Skills should work independently
3. **Clear Triggers** - Description should make it obvious when to use
4. **Lean SKILL.md** - Move detailed content to reference files
5. **Validation** - Always validate before distribution
6. **Versioning** - Increment version on any changes
7. **Documentation** - Keep README.md and docs up to date

## Project-Specific Configuration

This repository includes a `CLAUDE.md` file with project-specific instructions for Claude Code. This ensures Claude understands:

- Repository structure and conventions
- Skill development best practices
- Validation requirements
- Packaging workflows

## Git Workflow

### Tracked Skills

The following skills are tracked in version control:
- All skills currently in the repository

### Untracked Skills

Some skills may be gitignored for personal use. Check `.gitignore` for excluded skill directories.

### Committing Changes

When making changes to skills:

1. Update version in SKILL.md frontmatter
2. Document changes in commit message
3. Follow conventional commit format:
   - `feat:` - New features
   - `fix:` - Bug fixes
   - `docs:` - Documentation updates
   - `refactor:` - Code refactoring

## Scripts and Automation

### Skill Creator Scripts

**init_skill.py** - Initialize a new skill directory
```bash
python skill-creator/scripts/init_skill.py <skill-name> --path <output-directory>
```

**quick_validate.py** - Validate skill structure
```bash
python skill-creator/scripts/quick_validate.py <path/to/skill>
```

**package_skill.py** - Package skill into ZIP
```bash
python skill-creator/scripts/package_skill.py <path/to/skill> [output-dir]
```

### Skill Packager Scripts

**package_and_document.py** - Package with documentation and versioning
```bash
python skill-packager/scripts/package_and_document.py \
  --skill-path <path/to/skill> \
  --version <X.Y.Z> \
  --output-dir <output-directory>
```

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

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-skill`)
3. Develop your skill following the structure guidelines
4. Validate your skill using the validation scripts
5. Test thoroughly with real-world use cases
6. Submit a pull request with clear description

### Contribution Guidelines

- Follow the standard skill structure
- Include comprehensive SKILL.md with frontmatter
- Add appropriate bundled resources
- Validate before submitting
- Increment version appropriately
- Update this README if adding new skills

## Resources

### Documentation

- [Claude Code Documentation](https://docs.claude.com/claude-code)
- [MCP Protocol Documentation](https://modelcontextprotocol.io/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

### Related Projects

- [Model Context Protocol](https://github.com/modelcontextprotocol) - Protocol for LLM integrations
- [Lerna](https://lerna.js.org/) - Monorepo management tool
- [axe DevTools](https://www.deque.com/axe/devtools/) - Accessibility testing

## License

Individual skills may have their own licenses. Check the LICENSE.txt file in each skill directory for specific terms.

## Support

For issues, questions, or feedback:

- Open an issue in this repository
- Refer to the [Claude Code documentation](https://docs.claude.com/claude-code)
- Check individual skill documentation for skill-specific questions

## Acknowledgments

Built for [Claude Code](https://claude.com/claude-code) by Anthropic.

Skills leverage the progressive disclosure design pattern to efficiently manage context while providing specialized expertise.

---

**Last Updated:** 2025-11-10
**Repository Structure Version:** 1.0.0
