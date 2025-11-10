# npm-monorepo-publish Skill

A Claude Code skill that orchestrates publishing monorepo packages to npm with intelligent automation, validation, and error handling.

## Overview

Publishing npm packages in a Lerna monorepo can be complex, especially when dealing with:
- Two-factor authentication (OTP codes)
- Build and lint validation
- Version bumping with conventional commits
- Git tagging and GitHub releases
- Network errors and recovery

This skill eliminates the friction by providing a guided workflow that handles all the complexity while keeping you in control.

## Features

- **Pre-flight Validation**: Automatically checks authentication, runs builds, and validates code quality
- **Dry-Run Preview**: Shows exactly what will be published before committing
- **Smart OTP Handling**: Prompts for and validates OTP codes with retry logic
- **Post-Publish Verification**: Confirms packages are live on npm registry
- **Error Recovery**: Provides guided rollback for failed publishes
- **Lerna Compatible**: Works seamlessly with existing Lerna configurations

## Quick Start

### Prerequisites

1. **Lerna-managed monorepo** with `lerna.json` in root
2. **npm authentication**: Run `npm login` if not already authenticated
3. **2FA enabled** on your npm account
4. **Conventional commits** configured in your Lerna setup

### Basic Usage

Simply ask Claude to publish your packages:

```
"Publish the updated packages to npm"
"Release a new version"
"Deploy to npm registry"
```

Claude will:
1. ✅ Validate your environment (auth, build, lint)
2. 📋 Show preview of what will be published
3. 🔐 Prompt for your OTP code
4. 🚀 Execute the publish
5. ✅ Verify packages are live on npm

## Workflow Deep Dive

### Step 1: Pre-Flight Validation

Before publishing, the skill runs comprehensive checks:

```bash
npm whoami              # Verify authentication
npm run build           # Ensure packages compile
npm run lint            # Validate code quality
```

**If validation fails**, Claude will:
- Stop the workflow immediately
- Show clear error messages
- Provide guidance on how to fix issues

### Step 2: Dry-Run Preview

Preview what will be published without actually publishing:

```bash
lerna publish --no-git-tag-version --no-push --yes
```

You'll see:
- List of packages to be published
- Current → new version for each package
- Summary of changes from conventional commits

Claude will ask for confirmation before proceeding.

### Step 3: OTP Collection

Claude prompts for your 6-digit OTP code:

```
Please enter your 6-digit OTP code from your authenticator app:
```

**Important OTP details:**
- Codes are exactly 6 digits
- Expire after ~30 seconds
- Single-use only
- Claude never guesses or caches OTP codes

### Step 4: Publish Execution

The actual publish happens with:

```bash
lerna publish --otp <your-code>
```

This command:
- Bumps versions in package.json
- Publishes to npm registry
- Creates git tags
- Commits version changes
- Pushes to remote
- Creates GitHub releases (if configured)

**Error handling is automatic:**
- OTP expired → Re-prompts for new code (up to 3 retries)
- Network error → Shows diagnostic info
- Permission error → Checks access and provides guidance

### Step 5: Post-Publish Verification

After successful publish:

```bash
npm view @fpkit/acss version    # Verify version
npm view @fpkit/acss time       # Check timestamp
```

Claude shows:
- ✅ Success message with version number
- 📦 npm package URL
- 🏷️ GitHub release URL (if created)
- 📊 Version diff (e.g., 0.6.1 → 0.6.2)

## Configuration

### Lerna Configuration

The skill works with standard Lerna configurations in `lerna.json`:

```json
{
  "version": "independent",
  "conventionalCommits": true,
  "command": {
    "publish": {
      "message": "chore(release): publish %s"
    }
  }
}
```

**Conventional commits mapping:**
- `feat:` → minor version bump (0.6.0 → 0.7.0)
- `fix:` → patch version bump (0.6.1 → 0.6.2)
- `BREAKING CHANGE:` → major version bump (0.6.0 → 1.0.0)

### GitHub Releases (Optional)

To auto-create GitHub releases, add to `lerna.json`:

```json
{
  "command": {
    "version": {
      "createRelease": "github"
    }
  }
}
```

Requires `GH_TOKEN` environment variable:

```bash
export GH_TOKEN="your-github-token"
```

### Package Configuration

In your package's `package.json`:

```json
{
  "name": "@fpkit/acss",
  "version": "0.6.2",
  "publishConfig": {
    "access": "public"
  }
}
```

## Examples

### Example 1: Standard Publish

**User asks:**
```
Publish the updated components to npm
```

**Claude executes:**
1. ✅ Pre-flight checks pass
2. 📋 Shows preview: "@fpkit/acss: 0.6.1 → 0.6.2"
3. 🔐 Prompts: "Please enter your 6-digit OTP code:"
4. 🚀 Publishes with OTP: `lerna publish --otp 123456`
5. ✅ Verifies and shows: "Published @fpkit/acss@0.6.2"

### Example 2: Build Failure

**User asks:**
```
Release the new version
```

**Claude responds:**
1. ✅ npm whoami succeeds
2. ❌ Build fails with TypeScript errors
3. 🛑 Workflow stops
4. 💬 Shows errors with file locations
5. ℹ️ Guidance: "Fix these errors before publishing"

### Example 3: OTP Expiration

**User asks:**
```
Publish to npm
```

**Claude handles:**
1. ✅ Pre-flight checks pass
2. 📋 Preview shown
3. 🔐 User provides OTP: "123456"
4. ❌ OTP expired error
5. 🔄 Re-prompts: "OTP expired. Please enter fresh code:"
6. 🔐 User provides new OTP: "789012"
7. ✅ Publish succeeds

## Error Recovery

### Rollback Git Tags

If publish fails after creating git tags:

```bash
# Remove local tag
git tag -d v0.6.2

# Remove remote tag
git push origin :refs/tags/v0.6.2

# Reset version changes
git reset --hard HEAD~1
```

### Partial Publish (Multi-Package)

If some packages published but others failed:

```bash
# Publishes only packages where local version > npm version
lerna publish from-package --otp <code>
```

### Deprecate Instead of Unpublish

To undo a publish (safer than unpublishing):

```bash
npm deprecate @fpkit/acss@0.6.2 "Accidental publish, use 0.6.1 instead"
```

**Note:** npm unpublish has severe restrictions:
- Only within 72 hours
- Cannot have dependents
- Permanently removes package

## Troubleshooting

### Common Issues

| Error | Solution |
|-------|----------|
| "Invalid OTP" | Wait for new code, ensure clock sync |
| "Not logged in" | Run `npm login` |
| "403 Forbidden" | Check package ownership with `npm owner ls` |
| "Network timeout" | Check https://status.npmjs.org/ |
| "Tag already exists" | Delete tag: `git tag -d v0.6.2` |
| "No changed packages" | Verify conventional commit format |

### Detailed Troubleshooting

See [`references/troubleshooting.md`](./references/troubleshooting.md) for comprehensive error solutions covering:
- OTP handling issues
- Authentication problems
- Network errors
- Build failures
- Version conflicts
- Recovery procedures

## Development Notes

### Skill Structure

```
npm-monorepo-publish/
├── SKILL.md                      # Main skill prompt (loaded by Claude)
├── README.md                     # This file (for developers)
└── references/
    └── troubleshooting.md        # Comprehensive error reference
```

### How It Works

1. **Skill Activation**: User mentions "publish", "release", or "deploy"
2. **Prompt Loading**: Claude loads `SKILL.md` with workflow instructions
3. **Workflow Execution**: Step-by-step validation → preview → OTP → publish → verify
4. **Error Handling**: Automatic retries, clear messages, guided recovery

### Extending the Skill

To add custom validation steps, edit `SKILL.md`:

```markdown
### Step 1: Pre-Flight Validation

# 1. Run your custom validation
npm run custom-check

# 2. Continue with standard checks
npm whoami
...
```

### Testing the Skill

**Dry-run mode** (preview without publishing):

```bash
lerna publish --no-git-tag-version --no-push --yes
```

**Local registry testing** (before production):

```bash
# Use Verdaccio local registry
npm config set registry http://localhost:4873/
lerna publish --otp 123456
```

## Requirements

### Environment
- **Node.js**: >= 20.9.0
- **Lerna**: >= 6.0.0 (globally or locally installed)
- **npm**: Latest stable version

### npm Account
- Active npm account with publish permissions
- 2FA enabled (OTP required)
- Member of organization (for scoped packages like `@fpkit/acss`)

### Repository
- Git repository with remote configured
- Conventional commits for version bumping
- Clean working tree before publishing

## Best Practices

### Before Publishing

1. **Commit all changes**: `git status` should be clean
2. **Run tests**: `npm test` to ensure quality
3. **Update changelog**: Document changes (if using manual changelog)
4. **Review commits**: Verify conventional commit format
5. **Check branch**: Usually publish from `main` or `master`

### During Publishing

1. **Use dry-run first**: Preview changes before committing
2. **Have OTP ready**: Open authenticator app before starting
3. **Watch for errors**: Read error messages carefully
4. **Don't retry blindly**: Network errors shouldn't auto-retry

### After Publishing

1. **Verify on npm**: Visit package page to confirm
2. **Test installation**: `npm install @fpkit/acss@latest` in test project
3. **Check GitHub release**: Ensure release notes are correct
4. **Update documentation**: If API changed

## Resources

### Official Documentation
- [Lerna Publishing](https://lerna.js.org/docs/features/version-and-publish)
- [npm Publishing](https://docs.npmjs.com/packages-and-modules/contributing-packages-to-the-registry)
- [Conventional Commits](https://www.conventionalcommits.org/)

### npm Registry
- [Status Page](https://status.npmjs.org/)
- [Package Search](https://www.npmjs.com/)
- [Organization Management](https://www.npmjs.com/settings)

### Support
- [npm Community](https://npm.community/)
- [Lerna GitHub Issues](https://github.com/lerna/lerna/issues)
- [Claude Code Docs](https://docs.claude.com/claude-code)

## License

This skill is part of Claude Code user skills and follows the same license as your project configuration.

## Contributing

This skill can be customized for your specific workflow:

1. Fork/copy the skill directory
2. Modify `SKILL.md` with your requirements
3. Add custom validation or post-publish steps
4. Update `references/troubleshooting.md` with project-specific issues

## Changelog

### Version History

- **Initial Release**: Core workflow with OTP handling, validation, and verification
- Supports Lerna independent versioning
- Compatible with conventional commits
- GitHub releases integration

---

**Made for Claude Code** - Simplifying npm publishing for monorepo developers
