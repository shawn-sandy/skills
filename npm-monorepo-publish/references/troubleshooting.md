# NPM Publish Troubleshooting Guide

This reference provides detailed solutions for common errors encountered during npm package publishing in Lerna monorepos.

## OTP (One-Time Password) Issues

### Error: "Invalid OTP" or "OTP expired"

**Symptoms:**
```
npm ERR! code EOTP
npm ERR! This operation requires a one-time password.
npm ERR! You can provide a one-time password by passing --otp=<code> to the command you ran.
```

**Causes:**
- OTP code expired (codes valid for ~30 seconds)
- Typo in OTP code entry
- Clock drift on authenticator device
- Already used OTP code (single-use only)

**Solutions:**

1. **Get fresh OTP code:**
   - Open authenticator app (Google Authenticator, Authy, etc.)
   - Wait for code to refresh if near expiration
   - Enter new 6-digit code immediately

2. **Check clock synchronization:**
   ```bash
   # On macOS, verify system time is correct
   date

   # Ensure authenticator app clock is synced
   # (Check app settings for time sync option)
   ```

3. **Retry with new code:**
   ```bash
   lerna publish --otp <fresh-code>
   ```

4. **If persistent:**
   - Log out of npm: `npm logout`
   - Log back in: `npm login`
   - Verify 2FA is properly configured: Visit npmjs.com → Account Settings → Two-Factor Authentication

### Error: "OTP required but not provided"

**Symptoms:**
```
npm ERR! code EOTP
npm ERR! This operation requires a one-time password from your authenticator.
```

**Cause:**
- Forgot to include `--otp` flag in command
- 2FA enabled on npm account but OTP not provided

**Solution:**
Always use the `--otp` flag when publishing:
```bash
lerna publish --otp <6-digit-code>
```

## Authentication Issues

### Error: "You must be logged in to publish packages"

**Symptoms:**
```
npm ERR! code ENEEDAUTH
npm ERR! need auth This command requires you to be logged in.
```

**Cause:**
- Not authenticated with npm registry
- npm auth token expired

**Solutions:**

1. **Check current authentication:**
   ```bash
   npm whoami
   ```

   If this fails, you're not logged in.

2. **Log in to npm:**
   ```bash
   npm login
   ```

   Enter username, password, email, and OTP when prompted.

3. **Verify authentication:**
   ```bash
   npm whoami
   # Should return your npm username
   ```

### Error: "403 Forbidden - You do not have permission to publish"

**Symptoms:**
```
npm ERR! code E403
npm ERR! 403 Forbidden - PUT https://registry.npmjs.org/@fpkit/acss
npm ERR! You do not have permission to publish "@fpkit/acss"
```

**Causes:**
- Not a member of the npm organization (@fpkit)
- Package name already taken by another user
- Insufficient permissions in organization

**Solutions:**

1. **Check package ownership:**
   ```bash
   npm owner ls @fpkit/acss
   ```

2. **Check organization membership:**
   ```bash
   npm org ls @fpkit
   ```

3. **Request access:**
   - Contact organization owner to add you as member
   - Verify you have publish permissions for the package

4. **For scoped packages, verify publishConfig:**

   In `packages/fpkit/package.json`:
   ```json
   {
     "publishConfig": {
       "access": "public"
     }
   }
   ```

## Network Issues

### Error: "ETIMEDOUT" or "Network timeout"

**Symptoms:**
```
npm ERR! network request to https://registry.npmjs.org/@fpkit/acss failed, reason: socket hang up
npm ERR! network This is a problem related to network connectivity.
```

**Causes:**
- Slow or unstable internet connection
- npm registry temporarily unavailable
- Corporate firewall blocking npm registry
- VPN interference

**Solutions:**

1. **Check npm registry status:**
   - Visit https://status.npmjs.org/
   - Check for ongoing incidents or maintenance

2. **Test network connectivity:**
   ```bash
   ping registry.npmjs.org
   curl -I https://registry.npmjs.org
   ```

3. **Increase timeout:**
   ```bash
   npm config set fetch-timeout 300000
   npm config set fetch-retry-mintimeout 20000
   npm config set fetch-retry-maxtimeout 120000
   ```

4. **Check npm configuration:**
   ```bash
   npm config list
   ```

   Verify registry URL is correct:
   ```
   registry = "https://registry.npmjs.org/"
   ```

5. **Retry publish:**
   ```bash
   lerna publish --otp <code>
   ```

### Error: "ENOTFOUND registry.npmjs.org"

**Symptoms:**
```
npm ERR! code ENOTFOUND
npm ERR! errno ENOTFOUND
npm ERR! network request to https://registry.npmjs.org failed
```

**Causes:**
- DNS resolution failure
- No internet connection
- Corporate DNS blocking npm registry

**Solutions:**

1. **Check internet connection:**
   ```bash
   ping google.com
   ```

2. **Try alternative DNS:**
   ```bash
   # Temporarily use Google DNS
   networksetup -setdnsservers Wi-Fi 8.8.8.8 8.8.4.4
   ```

3. **Check npm registry setting:**
   ```bash
   npm config get registry
   ```

   Should return: `https://registry.npmjs.org/`

## Build and Validation Issues

### Error: "Build failed before publish"

**Symptoms:**
```
npm ERR! Missing script: "build"
npm ERR!
npm ERR! To see a list of scripts, run:
npm ERR!   npm run
```

**Causes:**
- Build script doesn't exist
- Build script has errors
- Dependencies not installed

**Solutions:**

1. **Verify build script exists:**
   ```bash
   cat packages/fpkit/package.json | grep "build"
   ```

2. **Install dependencies:**
   ```bash
   npm install
   lerna bootstrap
   ```

3. **Test build manually:**
   ```bash
   npm run build --prefix packages/fpkit
   ```

4. **Fix build errors:**
   - Check TypeScript errors
   - Verify all dependencies are installed
   - Ensure tsconfig.json is correct

### Error: "Lint failed"

**Symptoms:**
```
npm ERR! Exit code 1
npm ERR! Failed at the lint script
```

**Cause:**
- ESLint errors in code
- Code style violations

**Solutions:**

1. **Run lint to see errors:**
   ```bash
   npm run lint
   ```

2. **Auto-fix if possible:**
   ```bash
   npm run lint-fix
   ```

3. **Fix remaining errors manually**

4. **Retry publish after fixes**

## Version and Git Issues

### Error: "Tag already exists"

**Symptoms:**
```
fatal: tag 'v0.6.2' already exists
```

**Cause:**
- Git tag already created from previous failed publish attempt
- Trying to publish same version twice

**Solutions:**

1. **Check existing tags:**
   ```bash
   git tag -l
   ```

2. **Remove local tag:**
   ```bash
   git tag -d v0.6.2
   ```

3. **Remove remote tag:**
   ```bash
   git push origin :refs/tags/v0.6.2
   ```

4. **Retry publish:**
   ```bash
   lerna publish --otp <code>
   ```

### Error: "Version not bumped" or "No changed packages"

**Symptoms:**
```
lerna info No changed packages to publish
```

**Causes:**
- No commits since last publish
- Commits don't follow conventional commit format
- All changes are in non-published packages

**Solutions:**

1. **Check for changes:**
   ```bash
   git log --oneline v0.6.1..HEAD
   ```

2. **Verify conventional commit format:**
   ```bash
   git log --oneline -10
   ```

   Commits should start with: `feat:`, `fix:`, `chore:`, etc.

3. **Force specific version:**
   ```bash
   lerna publish patch --otp <code>
   # or
   lerna publish minor --otp <code>
   # or
   lerna publish major --otp <code>
   ```

### Error: "Working tree is not clean"

**Symptoms:**
```
error: Working tree has uncommitted changes
```

**Cause:**
- Uncommitted files in working directory
- Lerna requires clean working tree before publish

**Solutions:**

1. **Check git status:**
   ```bash
   git status
   ```

2. **Commit changes:**
   ```bash
   git add .
   git commit -m "chore: prepare for publish"
   ```

3. **Or stash changes:**
   ```bash
   git stash
   lerna publish --otp <code>
   git stash pop
   ```

## Package-Specific Issues

### Error: "Package name already exists"

**Symptoms:**
```
npm ERR! 403 Forbidden - PUT https://registry.npmjs.org/@fpkit/acss
npm ERR! Package name too similar to existing package
```

**Cause:**
- Package name conflicts with existing npm package
- npm prevents publishing packages with similar names

**Solution:**
- Choose a different package name
- Update `name` field in package.json
- Verify name availability: `npm view @new-scope/new-name`

### Error: "Version already published"

**Symptoms:**
```
npm ERR! 403 Forbidden - PUT https://registry.npmjs.org/@fpkit/acss
npm ERR! You cannot publish over the previously published version
```

**Cause:**
- Trying to publish a version that already exists on npm
- Version was successfully published but local git failed

**Solutions:**

1. **Check published version:**
   ```bash
   npm view @fpkit/acss version
   ```

2. **If version matches what you wanted:**
   ```bash
   # Just tag and push git changes
   git tag v0.6.2
   git push origin main --tags
   ```

3. **If version needs to be higher:**
   ```bash
   # Manually bump version
   lerna version patch --no-push
   # Then publish
   lerna publish from-package --otp <code>
   ```

## Recovery and Rollback

### Scenario: Publish succeeded but git push failed

**Symptoms:**
- Package visible on npm
- Git tags not pushed to remote
- No GitHub release

**Solution:**

1. **Verify publish succeeded:**
   ```bash
   npm view @fpkit/acss version
   ```

2. **Push git changes manually:**
   ```bash
   git push origin main
   git push origin --tags
   ```

3. **Create GitHub release manually:**
   ```bash
   gh release create v0.6.2 --generate-notes
   ```

### Scenario: Partial publish (multi-package monorepo)

**Symptoms:**
- Some packages published successfully
- Others failed
- Inconsistent state

**Solution:**

Use `from-package` to publish remaining packages:
```bash
lerna publish from-package --otp <code>
```

This will only publish packages where the version in package.json doesn't match what's on npm.

### Scenario: Need to undo a publish

**Important:** npm unpublish has restrictions:
- Can only unpublish within 72 hours of publishing
- Cannot unpublish if package has dependents
- Permanently removes package (not recommended)

**Better solution - Deprecate:**
```bash
npm deprecate @fpkit/acss@0.6.2 "Accidental publish, use 0.6.1 instead"
```

**Then publish correct version:**
```bash
lerna publish patch --otp <code>
```

## Preventive Measures

### Pre-Publish Checklist

Always verify before publishing:

1. ✅ **Authentication:**
   ```bash
   npm whoami
   ```

2. ✅ **Clean working tree:**
   ```bash
   git status
   ```

3. ✅ **Build succeeds:**
   ```bash
   npm run build --prefix packages/fpkit
   ```

4. ✅ **Lint passes:**
   ```bash
   npm run lint
   ```

5. ✅ **Tests pass:**
   ```bash
   npm test
   ```

6. ✅ **On correct branch:**
   ```bash
   git branch --show-current
   ```

7. ✅ **Conventional commits:**
   ```bash
   git log --oneline -10
   ```

### Dry-Run First

Always preview changes before publishing:
```bash
lerna publish --no-git-tag-version --no-push --yes
```

This shows what will be published without actually publishing.

## Getting Help

If you encounter an error not covered here:

1. **Check npm status:** https://status.npmjs.org/
2. **Check Lerna docs:** https://lerna.js.org/docs/features/version-and-publish
3. **npm support:** https://npm.community/
4. **Lerna GitHub issues:** https://github.com/lerna/lerna/issues
