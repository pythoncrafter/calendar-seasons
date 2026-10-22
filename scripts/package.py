"""Package product sources without collecting arbitrary local workspace files."""
from pathlib import Path
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIRECTORIES = {".github", "shared", "chrome", "safari", "ios-app", "scripts", "tests", "docs", "fastlane"}
SOURCE_FILES = {"README.md", "LICENSE", "Gemfile", "Gemfile.lock", "package.json", "package-lock.json"}
EXCLUDED_DIRECTORIES = {"node_modules", ".git", ".venv", "venv", "test-results", "__pycache__", "DerivedData", "xcuserdata", "build"}
EXCLUDED_SUFFIXES = {".p8", ".p12", ".mobileprovision", ".cer", ".key", ".pem", ".xcuserstate", ".pyc", ".zip", ".ipa"}


def package_files(base, *, complete=False):
    for path in sorted(base.rglob("*")):
        relative = path.relative_to(base)
        if any((part.startswith(".") and not (index == 0 and part == ".github"))
               or part in EXCLUDED_DIRECTORIES for index, part in enumerate(relative.parts)):
            continue
        if any(parent.is_symlink() for parent in (path, *path.parents) if parent != base):
            continue
        if not path.is_file() or path.suffix.lower() in EXCLUDED_SUFFIXES:
            continue
        if path.name in {"SigningCertificate.base64.txt", "report.xml", "credentials.json"}:
            continue
        if complete and relative.parts[0] not in SOURCE_DIRECTORIES | SOURCE_FILES:
            continue
        yield path


def main():
    subprocess.run([sys.executable, str(ROOT / "scripts/build.py")], check=True)
    for name, base, prefix, complete in [
        ("Calendar-Seasons-complete.zip", ROOT, "calendar-seasons/", True),
        ("Calendar-Seasons-Chrome.zip", ROOT / "chrome", "", False),
    ]:
        destination = ROOT.parent / name
        with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
            for path in package_files(base, complete=complete):
                archive.write(path, prefix + path.relative_to(base).as_posix())
        print(destination)


if __name__ == "__main__":
    main()
