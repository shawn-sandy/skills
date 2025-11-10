# Semantic Versioning Guide for Claude Code Skills

This guide explains how to apply semantic versioning (semver) principles to Claude Code skills, helping you choose the appropriate version number when packaging your skills.

## What is Semantic Versioning?

Semantic Versioning is a versioning scheme that uses a three-part number: `MAJOR.MINOR.PATCH`

```
1.2.3
│ │ │
│ │ └─ PATCH: Bug fixes, documentation updates
│ └─── MINOR: New features, backward-compatible changes
└───── MAJOR: Breaking changes, major refactors
```

## Version Number Components

### MAJOR Version (X.0.0)

Increment the MAJOR version when you make **incompatible or breaking changes** that require users to modify how they use the skill.

**Examples of MAJOR changes:**
- Complete workflow restructuring
- Removing or renaming required fields in frontmatter
- Changing the skill's core purpose or domain
- Removing bundled scripts or resources that users depend on
- Changing script interfaces (parameters, return values)
- Incompatible changes to asset templates
- Removing support for previously supported use cases

**Version Examples:**
- `0.9.0` → `1.0.0` (first stable release)
- `1.5.3` → `2.0.0` (breaking workflow change)
- `2.1.0` → `3.0.0` (removed critical script)

**When to bump MAJOR:**
```
❓ Will users need to change how they invoke or use the skill?
❓ Are existing users' workflows broken by this change?
❓ Did you remove functionality that users relied on?

✅ Yes to any? → MAJOR version bump
```

### MINOR Version (x.Y.0)

Increment the MINOR version when you add **new functionality** in a **backward-compatible** manner.

**Examples of MINOR changes:**
- Adding new workflow steps or options
- Adding optional fields to frontmatter
- Adding new scripts to the `scripts/` directory
- Adding new references to the `references/` directory
- Adding new templates to `assets/`
- Enhancing existing features without breaking them
- Adding new use cases to the skill's capabilities
- Improving validation or error handling

**Version Examples:**
- `1.0.0` → `1.1.0` (added new optional feature)
- `1.1.0` → `1.2.0` (added helper script)
- `2.3.1` → `2.4.0` (added new workflow option)

**When to bump MINOR:**
```
❓ Are you adding new capabilities or features?
❓ Will the skill do more than before?
❓ Are the changes completely optional?

✅ Yes to any? → MINOR version bump
```

### PATCH Version (x.y.Z)

Increment the PATCH version for **bug fixes** and **backward-compatible corrections** that don't add new features.

**Examples of PATCH changes:**
- Fixing typos in SKILL.md or documentation
- Correcting errors in workflow instructions
- Fixing bugs in scripts
- Improving error messages
- Updating references with corrections
- Performance improvements without feature changes
- Documentation updates and clarifications
- Fixing validation logic bugs

**Version Examples:**
- `1.0.0` → `1.0.1` (fixed typo in docs)
- `1.2.0` → `1.2.1` (fixed script bug)
- `2.3.4` → `2.3.5` (improved error message)

**When to bump PATCH:**
```
❓ Are you fixing something that was broken?
❓ Are you improving docs or error messages?
❓ Is the skill more correct but not more capable?

✅ Yes to any? → PATCH version bump
```

## Special Version Numbers

### Pre-1.0 Versions (0.y.z)

Initial development versions. Use these when the skill is still under active development and not yet considered stable.

**Characteristics:**
- Major changes can happen in MINOR versions
- Breaking changes are acceptable
- API/workflow is not yet stable
- For experimental or beta skills

**Progression:**
```
0.1.0 → Initial release
0.2.0 → Added features
0.3.0 → Major refactor (OK in 0.x)
0.9.0 → Release candidate
1.0.0 → First stable release
```

### Version 1.0.0

This is your first **stable, production-ready** release. Use 1.0.0 when:

- The skill is feature-complete for its primary use case
- The workflow is well-tested and stable
- You're confident in the skill's interface
- You're ready to maintain backward compatibility

**Don't rush to 1.0.0!** It's okay to stay in 0.x for a while during development.

## Decision Tree for Version Bumps

When packaging a skill, use this decision tree:

```
START: What changed since the last version?

1. Did you remove or break existing functionality?
   YES → MAJOR version bump (x.0.0)
   NO → Go to 2

2. Did you add new features or capabilities?
   YES → MINOR version bump (x.y.0)
   NO → Go to 3

3. Did you fix bugs or improve documentation?
   YES → PATCH version bump (x.y.z)
   NO → Keep current version (re-package)
```

## Practical Examples for Skills

### Example 1: Documentation Fix

**Changes:**
- Fixed typo in SKILL.md
- Updated example in references/

**Version Decision:**
- Current: `1.2.3`
- New: `1.2.4` (PATCH)

**Reasoning:** Bug fix, no new features, no breaking changes.

### Example 2: Adding Helper Script

**Changes:**
- Added new script to automate validation
- Updated SKILL.md to mention new script
- Script is optional, doesn't change existing workflow

**Version Decision:**
- Current: `1.2.4`
- New: `1.3.0` (MINOR)

**Reasoning:** New feature (script), backward-compatible, existing workflows still work.

### Example 3: Workflow Restructure

**Changes:**
- Completely reorganized the workflow steps
- Changed how the skill is invoked
- Users must adapt their usage

**Version Decision:**
- Current: `1.3.0`
- New: `2.0.0` (MAJOR)

**Reasoning:** Breaking change, existing users must update how they use the skill.

### Example 4: First Stable Release

**Changes:**
- Tested thoroughly in 0.9.x
- Confident in workflow stability
- Ready to commit to backward compatibility

**Version Decision:**
- Current: `0.9.5`
- New: `1.0.0` (MAJOR)

**Reasoning:** First stable release, signal production readiness.

## Best Practices

### 1. Start with 0.1.0

For new skills, start with version `0.1.0` rather than `1.0.0`. This signals that the skill is still under development.

### 2. Document Changes

Keep track of what changed between versions. Consider maintaining a changelog in your skill directory (though not strictly required).

### 3. Reset Lower Numbers

When incrementing a higher number, reset lower numbers to zero:
- `1.2.3` → `2.0.0` (not `2.2.3`)
- `1.2.3` → `1.3.0` (not `1.3.3`)

### 4. Don't Skip Numbers

Increment by 1 only. Don't jump from `1.0.0` to `1.5.0` or `3.0.0`.

### 5. Be Conservative with MAJOR

Don't bump MAJOR version unnecessarily. If you can make a change backward-compatible, do so and use MINOR instead.

### 6. When in Doubt, Ask

If you're unsure whether a change is MAJOR or MINOR:
- Think about existing users
- Would they need to change anything?
- If yes → MAJOR
- If no → MINOR

### 7. Pre-release Tags (Optional)

For advanced use, you can use pre-release tags:
- `1.0.0-alpha`
- `1.0.0-beta.1`
- `1.0.0-rc.1`

These are considered less stable than the release version.

## Version Lifecycle Example

Here's a realistic version progression for a skill:

```
0.1.0  - Initial release, basic functionality
0.2.0  - Added validation script
0.2.1  - Fixed bug in validation
0.3.0  - Added reference documentation
0.3.1  - Updated docs with examples
0.9.0  - Feature-complete, testing phase
0.9.1  - Bug fixes from testing
1.0.0  - First stable release
1.0.1  - Documentation improvements
1.1.0  - Added optional helper script
1.1.1  - Fixed script bug
1.2.0  - Added new workflow option
2.0.0  - Major workflow restructure
```

## Versioning SKILL.md Frontmatter

Always keep the version in your SKILL.md frontmatter in sync with your package version:

```yaml
---
name: my-skill
description: Does something useful
version: 1.2.3
---
```

The skill-packager tool will update this automatically when packaging.

## FAQ

**Q: I forgot to bump the version. What do I do?**
A: Package with the correct new version. The old version remains in the downloads directory.

**Q: Can I go backwards in version numbers?**
A: No, version numbers should always increase. If you need to "undo" changes, create a new version.

**Q: What if I have multiple changes (bug fix + new feature)?**
A: Use the highest applicable version bump (MINOR in this case, since new feature > bug fix).

**Q: Should I version the templates?**
A: No, templates are part of the skill-packager skill itself. Version the packaged skill.

**Q: What about build metadata (+)?**
A: For simplicity, stick to MAJOR.MINOR.PATCH for skills. Build metadata is optional.

## Summary

**Quick Reference:**
- **MAJOR** (x.0.0): Breaking changes
- **MINOR** (x.y.0): New features, backward-compatible
- **PATCH** (x.y.z): Bug fixes, documentation

**Decision Process:**
1. Breaking changes? → MAJOR
2. New features? → MINOR
3. Bug fixes/docs? → PATCH
4. No changes? → Keep version

**Start at:** `0.1.0`
**First stable:** `1.0.0`
**Always increment:** By 1 only

---

For more information on semantic versioning, see https://semver.org/
