# --- start AI code --
import sys
import unittest
from pathlib import Path


def main():
    unitTestFolder = Path(__file__).parent / "unitTests"
    tests = unittest.defaultTestLoader.discover(unitTestFolder, pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    if not result.wasSuccessful():
        sys.exit(1)


if __name__ == "__main__":
    main()
# --- end AI code --