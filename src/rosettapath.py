import re
import os
import itertools
from pathlib import Path
from typing import Union

class RosettaPath:
    default_server_prefix = r"\\192.168.10.1" + "\\"
    default_win_prefix = "C:/mount/"
    default_linux_prefix = "mnt/"
    default_mac_prefix = "Volumes/"
    input_mount_patterns = {
        "windows": r"^\w:\\mount",
        "ip": r"\d+\.\d+\.\d+\.\d+",
        "linux": r"^mnt",
        "mac": r"^volumes"
    }
    
    def __init__(self, userpath: Union[str, Path]):
        self.userpath = Path(userpath)
        if self.userpath.parts[0] == "\\" or self.userpath.parts[0] == "/":
            self.userpath = Path(*self.userpath.parts[1:])
        self.server_prefix = RosettaPath.default_server_prefix
        self.win_prefix = RosettaPath.default_win_prefix
        self.linux_prefix = RosettaPath.default_linux_prefix
        self.mac_prefix = RosettaPath.default_mac_prefix
        self.input_mount_patterns = RosettaPath.input_mount_patterns

    def _hasmount(self, regexstr: str, userpath: Union[str, Path]) -> tuple[bool, int]:
        userpath = Path(userpath)
        mountstart = re.search(regexstr, str(userpath), re.IGNORECASE)
        if not mountstart:
            return False, 0
        endindex = mountstart.span()[1]
        return True, endindex

    def _removemount(self, userpath: Path) -> Path:
        for regex in self.input_mount_patterns.values():
            is_mount, startindex = self._hasmount(regex, userpath)
            if is_mount:
                newpath = Path(str(userpath)[startindex:])
                if newpath.parts[0] == "\\" or newpath.parts[0] == "/":
                    newpath = Path(*newpath.parts[1:])
                return newpath
        return userpath

    def _change_mount(self, userpath: Path, newmount: str="") -> str:
        nomountpath = self._removemount(userpath)
        if not newmount:
            return str(nomountpath)
        return str(Path(newmount + str(nomountpath)))

    def server_path(self, usermount: Union[str, None]=None, platform: str="win") -> str:
        if usermount is None:
            usermount = self.server_prefix
        newpath = self._change_mount(self.userpath, usermount)
        if platform.lower() == "win":
            newpath = newpath.replace("/", "\\")
        else:
            newpath = newpath.replace("\\", "/")
        return newpath

    def win_path(self, usermount: Union[str, None]=None) -> str:
        if usermount is None:
            usermount = self.win_prefix
        newpath = self._change_mount(self.userpath, usermount)
        return newpath.replace("/", "\\")

    def mac_path(self, usermount: Union[str, None]=None) -> str:
        if usermount is None:
            usermount = self.mac_prefix
        newpath = self._change_mount(self.userpath, usermount)
        return newpath.replace("\\", "/")

    def linux_path(self, usermount: Union[str, None]=None) -> str:
        if usermount is None:
            usermount = self.linux_prefix
        newpath = self._change_mount(self.userpath, usermount)
        return newpath.replace("\\", "/")

    def nomount_path(self) -> str:
        newpath = self._change_mount(self.userpath)
        return newpath.replace("\\", "/")



def _make_seq_name(filename: Path) -> tuple[int, str]:
    framestr = filename.name.split(".")[1]
    re_name = re.search(r".+?\.", str(filename.name))
    if not re_name:
        return (0, "")
    digits = len(framestr)
    return (digits, re_name.group()[:-1]+f".%{str(digits).zfill(2)}d"+filename.suffix)

def is_seq(userpath: Union[Path, str], seq_depth: int=10) -> tuple[bool, int, str]:
    """
    Returns a tuple of (bool, int, str) where:
    bool: True if the path is a sequence, False otherwise
    int: The number of digits in the sequence
    str: The sequence name with the correct number of digits
    """
    userpath = Path(userpath)
    if userpath.is_dir():
        return (False, 0, "")
    with os.scandir(userpath.parent) as iter:
        iterslice = itertools.islice(iter, seq_depth)
        firstfile = None
        secondfile = None
        for f in iterslice:
            if not firstfile:
                firstfile = Path(f.path)
                continue
            if not secondfile:
                secondfile = Path(f.path)
                break
        if not firstfile or not secondfile:
            return (False, 0, "")

    firstseq = re.search(r".*\.\d*\.", str(firstfile.name))
    secondseq = re.search(r".*\.\d*\.", str(secondfile.name))

    if firstseq and secondseq:
        return (True, *_make_seq_name(firstfile))
    else:
        return (False, 0, "")

def contains_seq(userpath: Union[str, Path]) -> tuple[bool, int, str]:
    """
    Returns a tuple of (bool, int, str) where:
    bool: True if the directory contains a sequence, False otherwise
    int: The number of digits in the sequence
    str: The sequence name with the correct number of digits
    """
    userpath = Path(userpath)
    if userpath.is_file():
        return (False, 0, "")
    for file in userpath.iterdir():
        return is_seq(file)
    return (False, 0, "")