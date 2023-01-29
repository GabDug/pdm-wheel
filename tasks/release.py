import argparse
import subprocess
import sys
from pathlib import Path

import parver

PROJECT_DIR = Path(__file__).parent.parent


def get_current_version():
    cmd = ["git", "describe", "--tags", "--abbrev=0"]
    return subprocess.check_output(cmd).decode("utf-8").strip()


def bump_version(pre=None, major=False, minor=False, patch=True):
    if not any([major, minor, patch]):
        patch = True
    if len([v for v in [major, minor, patch] if v]) != 1:
        print(
            "Only one option should be provided among " "(--major, --minor, --patch)",
            file=sys.stderr,
        )
        sys.exit(1)
    current_version = parver.Version.parse(get_current_version())
    if not pre:
        version_idx = [major, minor, patch].index(True)
        version = current_version.bump_release(index=version_idx).replace(
            pre=None, post=None
        )
    else:
        version = current_version.bump_pre(pre)
    version = version.replace(local=None, dev=None)
    return str(version)


def release(dry_run=False, commit=True, pre=None, major=False, minor=False, patch=True):
    new_version = bump_version(pre, major, minor, patch)
    print(f"Bump version to: {new_version}")
    if dry_run:
        subprocess.check_call(["towncrier", "--version", new_version, "--draft"])
    else:
        subprocess.check_call(["towncrier", "--yes", "--version", new_version])
        subprocess.check_call(["git", "add", "."])
        if commit:
            subprocess.check_call(["git", "commit", "-m", f"Release {new_version}"])
            subprocess.check_call(
                ["git", "tag", "-a", new_version, "-m", f"v{new_version}"]
            )
            subprocess.check_call(["git", "push"])
            subprocess.check_call(["git", "push", "--tags"])


def parse_args(argv=None):
    parser = argparse.ArgumentParser("release.py")

    parser.add_argument("--dry-run", action="store_true", help="Dry run mode")
    parser.add_argument(
        "--no-commit",
        action="store_false",
        dest="commit",
        default=True,
        help="Do not commit to Git",
    )
    group = parser.add_argument_group(title="version part")
    group.add_argument("--pre", help="Pre tag")
    group.add_argument("--major", action="store_true", help="Bump major version")
    group.add_argument("--minor", action="store_true", help="Bump minor version")
    group.add_argument("--patch", action="store_true", help="Bump patch version")

    return parser.parse_args(argv)


if __name__ == "__main__":
    args = parse_args()
    release(args.dry_run, args.commit, args.pre, args.major, args.minor, args.patch)
