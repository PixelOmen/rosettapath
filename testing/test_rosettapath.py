import sys
import unittest
from pathlib import Path

import testpaths

HERE = Path(__file__).parent
ROOT = HERE.parent
if ROOT not in sys.path:
    sys.path.append(str(ROOT))
ROOT_PARENT = ROOT.parent
if ROOT_PARENT not in sys.path:
    sys.path.append(str(ROOT_PARENT))

from rosettapath import RosettaPath

class TestPaths(unittest.TestCase):
    def test_ip(self):
        rpath = RosettaPath(testpaths.WINDOWS_IP_PATH)
        is_ip, _ = rpath._hasmount(rpath.input_mount_patterns["ip"], rpath.userpath)
        self.assertTrue(is_ip)
        for path in testpaths.ALL_PATHS:
            if path == testpaths.WINDOWS_IP_PATH:
                continue
            rpath = RosettaPath(path)
            is_ip, _ = rpath._hasmount(rpath.input_mount_patterns["ip"], rpath.userpath)
            self.assertFalse(is_ip)

    def test_server(self):
        for path in testpaths.ALL_PATHS:
            if path == testpaths.WINDOWS_IP_PATH:
                continue
            win_path = RosettaPath(path).server_path()
            self.assertEqual(win_path, testpaths.WINDOWS_IP_PATH)

    def test_win(self):
        for path in testpaths.ALL_PATHS:
            if path == testpaths.WINDOWS_PATH:
                continue
            win_path = RosettaPath(path).win_path(f"{testpaths.WINDOWS_PATH[0]}:/mount/")
            self.assertEqual(win_path, testpaths.WINDOWS_PATH)

    def test_mac(self):
        for path in testpaths.ALL_PATHS:
            if path == testpaths.MAC_PATH:
                continue
            win_path = RosettaPath(path).mac_path()
            self.assertEqual(win_path, testpaths.MAC_PATH)

    def test_linux(self):
        for path in testpaths.ALL_PATHS:
            if path == testpaths.LINUX_PATH:
                continue
            win_path = RosettaPath(path).linux_path()
            self.assertEqual(win_path, testpaths.LINUX_PATH)

    def test_nomount(self):
        for path in testpaths.ALL_PATHS:
            if path == testpaths.NOMOUNT_PATH:
                continue
            win_path = RosettaPath(path).nomount_path()
            self.assertEqual(win_path, testpaths.NOMOUNT_PATH)
            

if __name__ == "__main__":
    unittest.main()