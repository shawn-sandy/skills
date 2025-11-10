# {{SKILL_NAME}} - Installation Guide

**Version:** {{SKILL_VERSION}}
**Package Date:** {{INSTALLATION_DATE}}

## Overview

This package contains the **{{SKILL_NAME}}** skill for Claude Code. This skill provides:

> {{SKILL_DESCRIPTION}}

## Prerequisites

Before installing this skill, ensure you have:

- **Claude Code** installed and configured
- Access to your Claude configuration directory (`~/.claude/`)
- Unzip utility (built into most operating systems)

## Installation Steps

### 1. Download the Package

You should have the following file:
```
{{SKILL_NAME}}-v{{SKILL_VERSION}}.zip
```

### 2. Extract the Archive

**On macOS/Linux:**
```bash
unzip {{SKILL_NAME}}-v{{SKILL_VERSION}}.zip -d /tmp/
```

**On Windows:**
- Right-click the ZIP file
- Select "Extract All..."
- Choose a temporary location

### 3. Install to Claude Skills Directory

**Option A: User-Level Installation (Recommended)**

Install for the current user, making the skill available across all projects:

```bash
# Create skills directory if it doesn't exist
mkdir -p ~/.claude/skills/

# Copy the extracted skill folder
cp -r /tmp/{{SKILL_DIR_NAME}} ~/.claude/skills/
```

**Option B: Project-Level Installation**

Install for a specific project only:

```bash
# Navigate to your project directory
cd /path/to/your/project

# Create skills directory if needed
mkdir -p skills/

# Copy the extracted skill folder
cp -r /tmp/{{SKILL_DIR_NAME}} skills/
```

### 4. Verify Installation

To confirm the skill is installed correctly:

1. Open Claude Code in your terminal or project
2. Type `/` to see available commands
3. Look for **{{SKILL_NAME}}** in the available skills list

Alternatively, check the skills directory:

```bash
# For user-level installation
ls ~/.claude/skills/{{SKILL_DIR_NAME}}

# You should see:
# SKILL.md  (required)
# scripts/  (if present)
# references/  (if present)
# assets/  (if present)
```

## Verification Checklist

- [ ] ZIP file extracted successfully
- [ ] Skill folder copied to `~/.claude/skills/` or project `skills/` directory
- [ ] SKILL.md file exists in the skill folder
- [ ] Skill appears in Claude Code's available skills
- [ ] No error messages when Claude Code starts

## Compatibility

- **Claude Code Version:** Any recent version with skill support
- **Operating Systems:** macOS, Linux, Windows
- **Dependencies:** Check SKILL.md for any additional requirements

## Troubleshooting

### Skill Not Appearing

**Problem:** The skill doesn't show up in Claude Code's available skills.

**Solutions:**
1. Verify the skill folder is in the correct location (`~/.claude/skills/`)
2. Check that SKILL.md exists and has valid YAML frontmatter
3. Restart Claude Code
4. Check Claude Code logs for errors

### Permission Errors

**Problem:** Cannot copy files to skills directory.

**Solutions:**
1. Ensure you have write permissions to `~/.claude/`
2. Try using `sudo` on Unix systems (not recommended, check permissions first)
3. Verify the directory path is correct

### Invalid Frontmatter

**Problem:** Skill validation fails.

**Solutions:**
1. Open `{{SKILL_DIR_NAME}}/SKILL.md`
2. Verify YAML frontmatter starts with `---` and ends with `---`
3. Check that `name:` and `description:` fields are present
4. Ensure no angle brackets (`<` or `>`) in the description

## Next Steps

1. **Read the Documentation:** See `{{SKILL_NAME}}-doc.md` for usage instructions and examples
2. **Explore the Skill:** Check the SKILL.md file for detailed workflow information
3. **Try It Out:** Invoke the skill in Claude Code to see it in action
4. **Review Resources:** If the skill includes `scripts/`, `references/`, or `assets/`, explore these for additional capabilities

## File Structure

After installation, your skill directory should contain:

```
~/.claude/skills/{{SKILL_DIR_NAME}}/
├── SKILL.md           # Main skill definition (required)
├── LICENSE.txt        # License information (optional)
├── scripts/           # Executable scripts (optional)
├── references/        # Documentation and guides (optional)
└── assets/            # Templates and resources (optional)
```

## Getting Help

If you encounter issues:

1. **Check the documentation:** Review `{{SKILL_NAME}}-doc.md`
2. **Validate the skill:** Ensure SKILL.md has proper frontmatter
3. **Review logs:** Check Claude Code output for error messages
4. **Reinstall:** Try removing and reinstalling the skill

## Uninstallation

To remove this skill:

```bash
# For user-level installation
rm -rf ~/.claude/skills/{{SKILL_DIR_NAME}}

# For project-level installation
rm -rf /path/to/project/skills/{{SKILL_DIR_NAME}}
```

## Version Information

- **Skill Name:** {{SKILL_NAME}}
- **Version:** {{SKILL_VERSION}}
- **Installation Date:** {{INSTALLATION_DATE}}

---

**Thank you for installing {{SKILL_NAME}}!**

For usage instructions and examples, see `{{SKILL_NAME}}-doc.md`.
