import re
from pathlib import Path

class RosettaPath:
    default_server = r"\\10.0.20.175" + "\\"
    mounts_regex = {
        "ip": r"\d+.\d+.\d+.\d+",
        "linux": r"^mnt",
        "mac": r"^volumes",
    }
    
    def __init__(self, userpath: str|Path, win_mount_regex: str=r"^\w:\\mount"):
        self.userpath = Path(userpath)
        self.servermount = RosettaPath.default_server
        self._win_regex = win_mount_regex

    def server_path(self, usermount: str=..., platform: str="win") -> str:
        if usermount is ...:
            usermount = self.servermount
        newpath = self._change_mount(self.userpath, usermount)
        if platform.lower() == "win":
            newpath = newpath.replace("/", "\\")
        else:
            newpath = newpath.replace("\\", "/")
        return newpath

    def win_path(self, usermount: str="C:/mount/") -> str:
        newpath = self._change_mount(self.userpath, usermount)
        return newpath.replace("/", "\\")

    def mac_path(self, usermount: str="Volumes/") -> str:
        newpath = self._change_mount(self.userpath, usermount)
        return newpath.replace("\\", "/")

    def linux_path(self, usermount: str="mnt/") -> str:
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
        for regex in (list(RosettaPath.mounts_regex.values()) + [self._win_regex]):
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