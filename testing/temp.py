import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent
if ROOT not in sys.path:
    sys.path.append(str(ROOT))

from rosettapath import RosettaPath
import testfiles


start = testfiles.MAC_PATH
rpath = RosettaPath(start)
server_result = rpath.server_path()
win_result = rpath.win_path()
mac_result = rpath.mac_path()
linux_result = rpath.linux_path()
nomount_result = rpath.nomount_path()
print(start)
print(server_result)
print(win_result)
print(mac_result)
print(linux_result)
print(nomount_result)