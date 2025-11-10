# {{SKILL_NAME}} - User Guide

**Version:** {{SKILL_VERSION}}
**Last Updated:** {{INSTALLATION_DATE}}

## What is {{SKILL_NAME}}?

{{SKILL_DESCRIPTION}}

This skill extends Claude Code's capabilities by providing specialized knowledge and workflows tailored to specific tasks. When invoked, Claude can leverage this skill's expertise to help you accomplish your goals more efficiently.

## When to Use This Skill

Use **{{SKILL_NAME}}** when you need to:

- Accomplish tasks related to the skill's domain expertise
- Follow established workflows and best practices
- Access specialized knowledge and resources
- Leverage automation scripts and tools provided by the skill

**Tip:** Check the `SKILL.md` file in the skill directory for detailed information about when and how to invoke this skill.

## How to Use This Skill

### Basic Invocation

Simply describe what you want to accomplish in natural language. Claude will automatically determine if this skill is relevant and invoke it when appropriate.

**Example:**
```
You: [Describe your task that relates to this skill's domain]
```

Claude will:
1. Recognize that your request matches this skill's capabilities
2. Load the skill's knowledge and workflows
3. Guide you through the process step-by-step
4. Utilize any bundled resources (scripts, references, templates)

### Skill Resources

This skill may include additional resources to enhance its capabilities:

#### Scripts (`scripts/` directory)

If present, the `scripts/` directory contains executable code that the skill can run to perform specific tasks. These scripts are:

- **Token-efficient:** Can execute without loading full code into context
- **Deterministic:** Produce consistent, reliable results
- **Specialized:** Designed for specific operations related to the skill

**Check for scripts:**
```bash
ls ~/.claude/skills/{{SKILL_DIR_NAME}}/scripts/
```

#### References (`references/` directory)

If present, the `references/` directory contains detailed documentation that Claude can load as needed. These might include:

- API documentation
- Detailed guidelines and standards
- Troubleshooting guides
- Code examples and patterns

**Check for references:**
```bash
ls ~/.claude/skills/{{SKILL_DIR_NAME}}/references/
```

#### Assets (`assets/` directory)

If present, the `assets/` directory contains templates, boilerplates, or other files that the skill uses to generate output. These might include:

- Code templates
- Configuration file templates
- Images or design resources
- Boilerplate code

**Check for assets:**
```bash
ls ~/.claude/skills/{{SKILL_DIR_NAME}}/assets/
```

## Typical Workflow

While each skill has its own unique workflow, most follow a similar pattern:

1. **Invocation:** You describe your task or request
2. **Context Gathering:** Claude asks clarifying questions if needed
3. **Planning:** The skill outlines the steps to accomplish your goal
4. **Execution:** Claude follows the skill's workflow, using bundled resources
5. **Validation:** Results are checked and verified
6. **Completion:** Final output is delivered with next steps

## Best Practices

### 1. Be Specific

Provide clear, detailed descriptions of what you want to accomplish. The more context you provide, the better the skill can assist you.

**Good:**
```
I need to [specific task] for [specific context], ensuring [specific requirements].
```

**Less Helpful:**
```
Help me with [vague request].
```

### 2. Review the SKILL.md

The `SKILL.md` file in the skill directory contains the complete workflow and instructions. Reviewing it can help you understand:

- Exactly when to use the skill
- What the skill can and cannot do
- The step-by-step process the skill follows
- Any prerequisites or requirements

**View SKILL.md:**
```bash
cat ~/.claude/skills/{{SKILL_DIR_NAME}}/SKILL.md
```

### 3. Leverage Bundled Resources

If the skill includes scripts, references, or assets, understand what they provide. Claude will use these automatically, but knowing they exist helps you understand the skill's capabilities.

### 4. Provide Feedback

If something doesn't work as expected:
- Describe what went wrong
- Share any error messages
- Explain what you expected to happen

This helps Claude adjust and find alternative approaches.

## Common Use Cases

Check the `SKILL.md` file for specific use cases and examples relevant to this skill. Common patterns include:

- **Workflow-based tasks:** Multi-step processes with defined stages
- **Code generation:** Creating code following specific patterns
- **Analysis and review:** Evaluating code or content against standards
- **Documentation:** Generating documentation from code or templates
- **Automation:** Running scripts to perform repetitive tasks

## Troubleshooting

### Skill Not Triggering

**Problem:** Claude doesn't seem to be using the skill even though your task matches its description.

**Solutions:**
- Be more explicit in your request, mentioning keywords from the skill description
- Review the skill's description in SKILL.md to ensure your task aligns
- Try directly asking Claude to use the skill

### Unexpected Behavior

**Problem:** The skill doesn't work as you expected.

**Solutions:**
- Review the SKILL.md workflow to understand the intended process
- Check if your request matches the skill's designed use cases
- Provide more context about your specific situation

### Missing Resources

**Problem:** The skill references resources that don't seem to exist.

**Solutions:**
- Verify the skill was installed completely (check for scripts/, references/, assets/)
- Re-extract and reinstall the skill package
- Check the Download.md installation guide

## Advanced Usage

### Understanding Progressive Disclosure

Skills use "progressive disclosure" to manage context efficiently:

1. **Metadata** (~100 words): Always loaded - skill name and description
2. **SKILL.md Body** (<5k words): Loaded when skill is invoked
3. **Bundled Resources**: Loaded only when specifically needed

This means Claude always knows the skill exists but only loads detailed information when relevant.

### Combining with Other Skills

Skills can work together. You can use multiple skills in a single session if your task spans multiple domains.

**Example:**
```
You: Use skill-creator to build a new skill, then use skill-packager to distribute it.
```

Claude will invoke each skill in sequence, creating a seamless workflow.

### Customizing the Skill

Skills can be modified to fit your specific needs:

1. **Edit SKILL.md:** Adjust workflows or add domain-specific guidance
2. **Add scripts:** Include custom automation for your workflow
3. **Add references:** Supplement with your own documentation
4. **Update assets:** Customize templates for your use case

**Caution:** If you customize a skill, keep track of your changes. Re-installing from the original package will overwrite modifications.

## Version History

**Current Version:** {{SKILL_VERSION}}

To check for updates or newer versions of this skill, consult the original source or distribution channel where you obtained the package.

## Skill Information

- **Skill Name:** {{SKILL_NAME}}
- **Version:** {{SKILL_VERSION}}
- **Installation Directory:** `~/.claude/skills/{{SKILL_DIR_NAME}}/`

## Getting More Help

1. **Read SKILL.md:** Complete workflow and technical details
2. **Check References:** Detailed guides in `references/` (if present)
3. **Review Scripts:** See `scripts/` for automation tools (if present)
4. **Experiment:** Try the skill with simple tasks first to understand its behavior

## Related Resources

- **Claude Code Documentation:** https://docs.claude.com/claude-code
- **Skill Creation Guide:** See the `skill-creator` skill for building custom skills
- **Community Skills:** Check for community-contributed skills

---

**Ready to get started?**

Invoke this skill by describing your task to Claude in natural language. The skill will guide you through the process step-by-step.

**Example invocation:**
```
You: [Your task that relates to {{SKILL_NAME}}]
```

For installation help, see `{{SKILL_NAME}}-Download.md`.
