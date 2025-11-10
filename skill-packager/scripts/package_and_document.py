#!/usr/bin/env python3
"""
Skill Packager with Versioning and Documentation Generator

Creates distributable ZIP files of skills with semantic versioning,
generates installation and user documentation.

Usage:
    python package_and_document.py --skill-path <path> --version <version> --output-dir <dir>

Example:
    python package_and_document.py \\
        --skill-path /Users/user/.claude/skills/my-skill \\
        --version 1.0.0 \\
        --output-dir /Users/user/.claude/downloads/my-skill
"""

import sys
import os
import zipfile
import argparse
import hashlib
import re
from pathlib import Path
from datetime import datetime


def validate_skill_extended(skill_path):
    """
    Extended validation of a skill including version field check.

    Returns:
        tuple: (is_valid: bool, message: str, metadata: dict)
    """
    skill_path = Path(skill_path)

    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found", {}

    # Read and validate frontmatter
    content = skill_md.read_text()
    if not content.startswith('---'):
        return False, "No YAML frontmatter found", {}

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format", {}

    frontmatter = match.group(1)

    # Check required fields
    if 'name:' not in frontmatter:
        return False, "Missing 'name' in frontmatter", {}
    if 'description:' not in frontmatter:
        return False, "Missing 'description' in frontmatter", {}

    metadata = {}

    # Extract name
    name_match = re.search(r'name:\s*(.+)', frontmatter)
    if name_match:
        name = name_match.group(1).strip()
        metadata['name'] = name

        # Check naming convention
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"Name '{name}' should be hyphen-case", {}
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"Name '{name}' has invalid hyphen placement", {}

    # Extract description
    desc_match = re.search(r'description:\s*(.+)', frontmatter)
    if desc_match:
        description = desc_match.group(1).strip()
        metadata['description'] = description

        # Check for angle brackets
        if '<' in description or '>' in description:
            return False, "Description cannot contain angle brackets", {}

    # Extract version (optional, will be added if missing)
    version_match = re.search(r'version:\s*(.+)', frontmatter)
    if version_match:
        version = version_match.group(1).strip()
        metadata['version'] = version
    else:
        metadata['version'] = None

    # Extract license if present
    license_match = re.search(r'license:\s*(.+)', frontmatter)
    if license_match:
        metadata['license'] = license_match.group(1).strip()

    return True, "Skill is valid!", metadata


def validate_semver(version):
    """
    Validate semantic version format.

    Args:
        version: Version string to validate

    Returns:
        bool: True if valid semver format
    """
    pattern = r'^\d+\.\d+\.\d+$'
    return re.match(pattern, version) is not None


def calculate_file_hash(file_path):
    """Calculate SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def should_exclude_file(file_path):
    """
    Determine if a file should be excluded from the package.

    Args:
        file_path: Path object of the file

    Returns:
        bool: True if file should be excluded
    """
    exclude_patterns = [
        '.DS_Store',
        '__pycache__',
        '*.pyc',
        '*.pyo',
        '.git',
        '.gitignore',
        'Thumbs.db',
        '.vscode',
        '.idea',
        '*.swp',
        '*.swo',
        '*~'
    ]

    file_name = file_path.name

    # Check exact matches
    if file_name in exclude_patterns:
        return True

    # Check pattern matches
    for pattern in exclude_patterns:
        if pattern.startswith('*.'):
            extension = pattern[1:]
            if file_name.endswith(extension):
                return True

    # Check if in excluded directory
    parts = file_path.parts
    excluded_dirs = {'__pycache__', '.git', '.vscode', '.idea'}
    if any(part in excluded_dirs for part in parts):
        return True

    return False


def load_template(template_path, skill_metadata, version, skill_dir_name):
    """
    Load and process a template file with variable substitution.

    Args:
        template_path: Path to the template file
        skill_metadata: Dictionary of skill metadata
        version: Version string
        skill_dir_name: Directory name of the skill

    Returns:
        str: Processed template content
    """
    if not template_path.exists():
        return None

    template_content = template_path.read_text()

    # Prepare substitution variables
    substitutions = {
        '{{SKILL_NAME}}': skill_metadata.get('name', 'Unknown'),
        '{{SKILL_VERSION}}': version,
        '{{SKILL_DESCRIPTION}}': skill_metadata.get('description', 'No description'),
        '{{INSTALLATION_DATE}}': datetime.now().strftime('%Y-%m-%d'),
        '{{SKILL_DIR_NAME}}': skill_dir_name,
    }

    # Perform substitutions
    result = template_content
    for placeholder, value in substitutions.items():
        result = result.replace(placeholder, value)

    return result


def create_package(skill_path, version, output_dir):
    """
    Create a versioned ZIP package of the skill.

    Args:
        skill_path: Path to the skill directory
        version: Version string for the package
        output_dir: Directory where package will be created

    Returns:
        tuple: (success: bool, zip_path: Path or None, metadata: dict)
    """
    skill_path = Path(skill_path).resolve()
    output_dir = Path(output_dir).resolve()

    # Validate skill
    print("🔍 Validating skill structure...")
    valid, message, metadata = validate_skill_extended(skill_path)
    if not valid:
        print(f"❌ Validation failed: {message}")
        return False, None, {}

    print(f"✅ {message}")
    print(f"   Skill: {metadata['name']}")
    print(f"   Description: {metadata['description'][:60]}...")
    print()

    # Validate version format
    if not validate_semver(version):
        print(f"❌ Invalid version format: {version}")
        print("   Version must be in semver format (e.g., 1.0.0)")
        return False, None, metadata

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Determine zip filename
    skill_name = metadata['name']
    zip_filename = output_dir / f"{skill_name}-v{version}.zip"

    print(f"📦 Creating package: {zip_filename.name}")

    # Create the ZIP file
    try:
        file_count = 0
        total_size = 0

        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Walk through the skill directory
            for file_path in skill_path.rglob('*'):
                if file_path.is_file() and not should_exclude_file(file_path):
                    # Calculate the relative path within the zip
                    arcname = file_path.relative_to(skill_path.parent)
                    zipf.write(file_path, arcname)

                    file_size = file_path.stat().st_size
                    total_size += file_size
                    file_count += 1

                    print(f"   Added: {arcname} ({file_size:,} bytes)")

        # Calculate package size and hash
        package_size = zip_filename.stat().st_size
        package_hash = calculate_file_hash(zip_filename)

        print()
        print(f"✅ Package created successfully!")
        print(f"   Files: {file_count}")
        print(f"   Size: {package_size:,} bytes ({package_size / 1024:.1f} KB)")
        print(f"   SHA-256: {package_hash[:16]}...")

        # Warn if package is very large
        if package_size > 10 * 1024 * 1024:  # 10 MB
            print(f"⚠️  Warning: Package is large ({package_size / 1024 / 1024:.1f} MB)")
            print("   Consider checking for unnecessary files (node_modules, .git, etc.)")

        return True, zip_filename, {
            **metadata,
            'package_size': package_size,
            'package_hash': package_hash,
            'file_count': file_count
        }

    except Exception as e:
        print(f"❌ Error creating package: {e}")
        return False, None, metadata


def generate_documentation(skill_path, version, output_dir, metadata):
    """
    Generate Download.md and {SkillName}-doc.md from templates.

    Args:
        skill_path: Path to the skill directory
        version: Version string
        output_dir: Directory where docs will be created
        metadata: Skill metadata dictionary

    Returns:
        tuple: (success: bool, doc_paths: list)
    """
    skill_path = Path(skill_path).resolve()
    output_dir = Path(output_dir).resolve()
    skill_name = metadata['name']
    skill_dir_name = skill_path.name

    # Find template directory (relative to this script)
    script_dir = Path(__file__).parent
    templates_dir = script_dir.parent / 'templates'

    doc_paths = []

    print()
    print("📝 Generating documentation...")

    # Generate Download.md
    download_template_path = templates_dir / 'download_template.md'
    if download_template_path.exists():
        download_content = load_template(
            download_template_path,
            metadata,
            version,
            skill_dir_name
        )

        download_output_path = output_dir / f"{skill_name}-Download.md"
        download_output_path.write_text(download_content)
        doc_paths.append(download_output_path)
        print(f"   ✅ Created: {download_output_path.name}")
    else:
        print(f"   ⚠️  Template not found: {download_template_path}")

    # Generate {SkillName}-doc.md
    doc_template_path = templates_dir / 'doc_template.md'
    if doc_template_path.exists():
        doc_content = load_template(
            doc_template_path,
            metadata,
            version,
            skill_dir_name
        )

        doc_output_path = output_dir / f"{skill_name}-doc.md"
        doc_output_path.write_text(doc_content)
        doc_paths.append(doc_output_path)
        print(f"   ✅ Created: {doc_output_path.name}")
    else:
        print(f"   ⚠️  Template not found: {doc_template_path}")

    return len(doc_paths) > 0, doc_paths


def main():
    parser = argparse.ArgumentParser(
        description='Package a skill with versioning and documentation'
    )
    parser.add_argument(
        '--skill-path',
        required=True,
        help='Path to the skill directory'
    )
    parser.add_argument(
        '--version',
        required=True,
        help='Semantic version for this package (e.g., 1.0.0)'
    )
    parser.add_argument(
        '--output-dir',
        required=True,
        help='Directory where package and docs will be created'
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Skill Packager - Version and Documentation Generator")
    print("=" * 60)
    print()

    # Create package
    success, zip_path, metadata = create_package(
        args.skill_path,
        args.version,
        args.output_dir
    )

    if not success:
        sys.exit(1)

    # Generate documentation
    doc_success, doc_paths = generate_documentation(
        args.skill_path,
        args.version,
        args.output_dir,
        metadata
    )

    # Summary
    print()
    print("=" * 60)
    print("📋 Packaging Summary")
    print("=" * 60)
    print(f"Skill Name: {metadata['name']}")
    print(f"Version: v{args.version}")
    print(f"Output Directory: {args.output_dir}")
    print()
    print("Generated Files:")
    if zip_path:
        print(f"  • {zip_path.name} ({metadata['package_size']:,} bytes)")
    for doc_path in doc_paths:
        print(f"  • {doc_path.name}")
    print()
    print("✅ Packaging complete!")
    print("=" * 60)

    sys.exit(0)


if __name__ == "__main__":
    main()
