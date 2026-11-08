# --- start AI code --
import sys
import unittest
from pathlib import Path


def main():
    unitTestFolder = Path(__file__).resolve().parent / "unitTests"
    tests = unittest.defaultTestLoader.discover(unitTestFolder, pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
# --- end AI code --
