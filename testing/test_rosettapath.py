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

from src.rosettapath import RosettaPath, is_seq, contains_seq

IMG_SEQ_DIR = HERE / "test_image_seq"
IMG_SEQ = IMG_SEQ_DIR / "my_image_seq.0001.tif"

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
            win_path = RosettaPath(path).win_path()
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

    def test_custom_mount(self):
        RosettaPath.default_linux_prefix = "newMountPoint/"
        rpath = RosettaPath("myshare/mydir/app.py")
        rpath.linux_path()
        self.assertEqual(rpath.linux_path(), "newMountPoint/myshare/mydir/app.py")
        RosettaPath.default_linux_prefix = "mnt/"

    def test_windows_local_mount(self):
        RosettaPath.default_win_prefix = testpaths.WINDOWS_PATH[:3]
        RosettaPath.input_mount_patterns["windows"] = r"^\w:\\"
        rpath = RosettaPath(testpaths.WINDOWS_PATH)
        self.assertEqual(rpath.win_path(), testpaths.WINDOWS_PATH)

    def test_is_seq(self):
        expected_positive = (True, 4, 'my_image_seq.%04d.tif')
        expected_negative = (False, 0, '')

        result_postive = is_seq(IMG_SEQ)
        self.assertEqual(result_postive, expected_positive)

        result_negative = is_seq(IMG_SEQ_DIR)
        self.assertEqual(result_negative, expected_negative)

    def test_contains_seq(self):
        expected_positive = (True, 4, 'my_image_seq.%04d.tif')
        expected_negative = (False, 0, '')

        result_postive = contains_seq(IMG_SEQ_DIR)
        self.assertEqual(result_postive, expected_positive)

        result_negative = contains_seq(IMG_SEQ)
        self.assertEqual(result_negative, expected_negative)


if __name__ == "__main__":
    unittest.main()