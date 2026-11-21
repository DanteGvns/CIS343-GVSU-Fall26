import sys
import unittest
from pathlib import Path


if __name__ == "__main__":
    unitTestFolder = Path(__file__).resolve().parent / "unitTests"
    tests = unittest.defaultTestLoader.discover(unitTestFolder, pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    sys.exit(0 if result.wasSuccessful() else 1)