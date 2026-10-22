import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("packager", Path(__file__).resolve().parents[1] / "scripts/package.py")
packager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packager)


class PackageTests(unittest.TestCase):
    def test_product_files_without_local_builds_credentials_or_symlinks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            good = {"README.md", ".github/workflows/build.yml", "chrome/manifest.json", "shared/content.js", "docs/privacy.md",
                    "safari/CalendarSeasons.xcodeproj/project.pbxproj"}
            unwanted = {".env", "notes.txt", "ios-app/secret.p8", "fastlane/SigningCertificate.base64.txt",
                        "safari/DerivedData/product/app", "shared/.env.local", "scripts/__pycache__/x.pyc",
                        "chrome/credentials.json", "chrome/assets/certificate.P12"}
            for name in good | unwanted:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("fixture")
            (root / "shared/local-key").symlink_to(root / "ios-app/secret.p8")
            (root / "shared/local-directory").symlink_to(root / "ios-app", target_is_directory=True)
            actual = {p.relative_to(root).as_posix() for p in packager.package_files(root, complete=True)}
            self.assertEqual(actual, good)


if __name__ == "__main__":
    unittest.main()
