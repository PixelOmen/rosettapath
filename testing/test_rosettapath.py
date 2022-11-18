import sys
import unittest
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent
if ROOT not in sys.path:
    sys.path.append(str(ROOT))

import testfiles
from rosettapath import RosettaPath

class TestPaths(unittest.TestCase):
    def test_ip(self):
        rpath = RosettaPath(testfiles.WINDOWS_IP_PATH)
        is_ip, _ = rpath._isipmount(rpath.userpath)
        self.assertTrue(is_ip)
        for path in testfiles.ALL_PATHS:
            if path == testfiles.WINDOWS_IP_PATH:
                continue
            rpath = RosettaPath(path)
            is_ip, _ = rpath._isipmount(rpath.userpath)
            self.assertFalse(is_ip)

    def test_server(self):
        for path in testfiles.ALL_PATHS:
            if path == testfiles.WINDOWS_IP_PATH:
                continue
            win_path = RosettaPath(path).server_path()
            self.assertEqual(win_path, testfiles.WINDOWS_IP_PATH)

    def test_win(self):
        for path in testfiles.ALL_PATHS:
            if path == testfiles.WINDOWS_PATH:
                continue
            win_path = RosettaPath(path).win_path()
            self.assertEqual(win_path, testfiles.WINDOWS_PATH)

    def test_mac(self):
        for path in testfiles.ALL_PATHS:
            if path == testfiles.MAC_PATH:
                continue
            win_path = RosettaPath(path).mac_path()
            self.assertEqual(win_path, testfiles.MAC_PATH)

    def test_linux(self):
        for path in testfiles.ALL_PATHS:
            if path == testfiles.LINUX_PATH:
                continue
            win_path = RosettaPath(path).linux_path()
            self.assertEqual(win_path, testfiles.LINUX_PATH)
            

if __name__ == "__main__":
    unittest.main()