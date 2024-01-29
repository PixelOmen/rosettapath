# RosettaPath

RossetaPath objects translate network paths mounted to local volumes from one mount point to another across operating systems.
___



## Usage
```python
from rosettapath import RosettaPath

rpath = RosettaPath("myshare/mydir/app.py")

rpath.win_path()
# C:\mount\myshare\mydir\app.py

rpath.linux_path()
# mnt/myshare/mydir/app.py

rpath.mac_path()
# Volumes/myshare/mydir/app.py

rpath.server_path()
# \\192.168.10.1\myshare\mydir\app.py

rpath.nomount_path()
# myshare/mydir/app.py
```


## Override default mount points
``` python
from rosettapath import RosettaPath

rpath = RosettaPath("myshare/mydir/app.py")

# Permanently override
rpath.default_linux_mount = "newMountPoint/"
rpath.linux_path()
# newMountPoint/myshare/mydir/app.py

# Temporarily override
rpath.linux_path(usermount="newMountPoint/")
# newMountPoint/myshare/mydir/app.py# 
```

## Custom Default Mount Points
RosettaPath uses regex to search for input mount points. These regex search expressions can be overridden for non-standard mount points.

``` python
from rosettapath import RosettaPath

RosettaPath.default_linux_mount = "newMountPoint/"
rpath = RosettaPath("myshare/mydir/app.py")
rpath.linux_path()
# newMountPoint/myshare/mydir/app.py
```


## Input Regex Override
RosettaPath uses regex to search for input mount points. These regex search expressions can be overridden for non-standard mount points.

``` python
from rosettapath import RosettaPath

rpath = RosettaPath("otherMount/myshare/mydir/app.py")

# -- Before ---
rpath.win_path()
# C:\mount\otherMount\myshare\mydir\app.py

# -- After ---
rpath.input_mount_patterns["linux"] = r"^otherMount"
rpath.win_path()
# C:\mount\myshare\mydir\app.py
```


## Override class defaults
Default mount points and regex can be overridden on the class itself for all future instances.
``` python
from rosettapath import RosettaPath

RosettaPath.default_linux_mount = "newMountPoint/"
rpath = RosettaPath("myshare/mydir/app.py")
rpath.linux_path()
# newMountPoint/myshare/mydir/app.py

RosettaPath.input_mount_patterns["linux"] = r"^otherMount"
rpath = RosettaPath("otherMount/myshare/mydir/app.py")
rpath.win_path()
# C:\mount\myshare\mydir\app.py

```
___
<br>

## License
[MIT](https://choosealicense.com/licenses/mit/)