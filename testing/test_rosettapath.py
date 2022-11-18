import sys
import unittest
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent
if ROOT not in sys.path:
    sys.path.append(str(ROOT))

import testfiles
import rosettapath

class TestPaths(unittest.TestCase):
    def test_ip(self):
        pass