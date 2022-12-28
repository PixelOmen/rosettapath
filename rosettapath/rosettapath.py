import re
from pathlib import Path

class RosettaPath:
    default_server_mount = r"\\192.168.10.1" + "\\"
    default_win_mount = "C:/mount/"
    default_linux_mount = "mnt/"
    default_mac_mount = "Volumes/"
    mounts_regex = {
        "windows": r"^\w:\\mount",
        "ip": r"\d+.\d+.\d+.\d+",
        "linux": r"^mnt",
        "mac": r"^volumes"
    }
    def __init__(self, userpath: str|Path):
        self.userpath = Path(userpath)
        if self.userpath.parts[0] == "\\" or self.userpath.parts[0] == "/":
            self.userpath = Path(*self.userpath.parts[1:])
        self.default_server_mount = RosettaPath.default_server_mount
        self.default_win_mount = RosettaPath.default_win_mount
        self.default_linux_mount = RosettaPath.default_linux_mount
        self.default_mac_mount = RosettaPath.default_mac_mount
        self.mounts_regex = RosettaPath.mounts_regex

    def server_path(self, usermount: str=..., platform: str="win") -> str:
        if usermount is ...:
            usermount = self.default_server_mount
        newpath = self._change_mount(self.userpath, usermount)
        if platform.lower() == "win":
            newpath = newpath.replace("/", "\\")
        else:
            newpath = newpath.replace("\\", "/")
        return newpath

    def win_path(self, usermount: str=...) -> str:
        if usermount is ...:
            usermount = self.default_win_mount
        newpath = self._change_mount(self.userpath, usermount)
        return newpath.replace("/", "\\")

    def mac_path(self, usermount: str=...) -> str:
        if usermount is ...:
            usermount = self.default_mac_mount
        newpath = self._change_mount(self.userpath, usermount)
        return newpath.replace("\\", "/")

    def linux_path(self, usermount: str=...) -> str:
        if usermount is ...:
            usermount = self.default_linux_mount
        newpath = self._change_mount(self.userpath, usermount)
        return newpath.replace("\\", "/")

    def nomount_path(self) -> str:
        newpath = self._change_mount(self.userpath)
        return newpath.replace("\\", "/")

    def _hasmount(self, regexstr: str, userpath: str|Path) -> tuple[bool, int]:
        userpath = Path(userpath)
        mountstart = re.search(regexstr, str(userpath), re.IGNORECASE)
        if not mountstart:
            return False, 0
        endindex = mountstart.span()[1]
        return True, endindex

    def _removemount(self, userpath: Path) -> Path:
        for regex in self.mounts_regex.values():
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