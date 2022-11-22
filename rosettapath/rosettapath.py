import re
from pathlib import Path

from .shares import SHARES

class RosettaPath:
    default_server = r"\\10.0.20.175" + "\\"
    
    def __init__(self, userpath: str|Path):
        self.userpath = Path(userpath)
        self.servermount = RosettaPath.default_server

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

    def _isipmount(self, userpath: str|Path) -> tuple[bool, int]:
        userpath = Path(userpath)
        mountstart = re.search(r"[a-z]", str(userpath), re.IGNORECASE)
        if not mountstart:
            raise ValueError(f"Malformed mount point for filepath: {str(userpath)}")
        startindex = mountstart.span()[0]
        is_ip = True if startindex > 4 else False
        return is_ip, startindex

    def _removemount(self, userpath: Path) -> Path:
        is_ip, startindex = self._isipmount(userpath)
        if is_ip:
            return Path(str(userpath)[startindex:])

        if userpath.parts[0][0].lower() == "c" and userpath.parts[1].lower() == "mount":
            return Path(*userpath.parts[2:])

        is_share = (False, None)
        for vol in SHARES:
            for index, part in enumerate(userpath.parts):
                if part.lower() == vol:
                    is_share = (True, index)
                    break
            if is_share[0]:
                break
            
        if is_share[0]:
            return Path(*userpath.parts[is_share[1]:])
        raise ValueError(f"Malformed mount point for filepath: {str(userpath)}")

    def _change_mount(self, userpath: Path, newmount: str="") -> str:
        nomountpath = self._removemount(userpath)
        if not newmount:
            return str(nomountpath)
        if self._isipmount(newmount+"test")[0]:
            newmount = newmount + nomountpath.parts[0]
            nomountpath = Path(*nomountpath.parts[1:])
        else:
            newmount = newmount
        return str(Path(newmount, nomountpath))