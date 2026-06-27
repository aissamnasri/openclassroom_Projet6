import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()

ANGULAR_PROJECT = ROOT / "G-rez-l-int-gration-et-la-livraison-continue-Application-Angular"

SPRING_PROJECT = (
    ROOT /
    "projet 6_exercice1-partie2" /
    "G-rez-l-int-gration-et-la-livraison-continue-Workshop-Organizer"
)

TEST_RESULTS = ROOT / "test-results"


def run(command, cwd):
    print(f"\nRunning: {' '.join(command)}")
    result = subprocess.run(command, cwd=cwd)
    return result.returncode


def clean_reports():
    if TEST_RESULTS.exists():
        shutil.rmtree(TEST_RESULTS)

    TEST_RESULTS.mkdir(parents=True, exist_ok=True)


def test_angular():
    print("\n=== Angular Tests ===")

    if not (ANGULAR_PROJECT / "package.json").exists():
        print("package.json introuvable")
        return 1

    return run(["npm", "test"], ANGULAR_PROJECT)


def test_spring():
    print("\n=== Spring Tests ===")

    if not (SPRING_PROJECT / "build.gradle").exists():
        print("build.gradle introuvable")
        return 1

    if sys.platform.startswith("win"):
        cmd = ["gradlew.bat", "clean", "test"]
    else:
        cmd = ["./gradlew", "clean", "test"]

    return run(cmd, SPRING_PROJECT)


def main():

    clean_reports()

    angular_code = test_angular()

    spring_code = test_spring()

    if angular_code != 0 or spring_code != 0:
        print("\nTests FAILED")
        sys.exit(1)

    print("\nTests PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()