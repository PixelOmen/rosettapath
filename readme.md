# RosettaPath

RossetaPath objects translate network paths mounted to local volumes from one mount point to another across operating systems.
___

## Overview
####Usage
[Basic Usage](#basic-usage)
[Override Default OS Prefixes](#override-default-os-prefixes)
[Input Path Regex Override](#input-path-regex-override)
[Override Class Defaults](#override-class-defaults)
####Utility Functions
[Detect Image Sequences](#detect-image-sequences)

####[License](#license)

___

## Basic Usage
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


## Override Default OS Prefixes
``` python
from rosettapath import RosettaPath

rpath = RosettaPath("myshare/mydir/app.py")

# Permanently override
rpath.default_linux_prefix = "newMountPoint/"
rpath.linux_path()
# newMountPoint/myshare/mydir/app.py

# Temporarily override
rpath.linux_path(usermount="newMountPoint/")
# newMountPoint/myshare/mydir/app.py# 
```


## Input Path Regex Override
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


## Override Class Defaults
Default mount points and regex can be overridden on the class itself for all future instances.
``` python
from rosettapath import RosettaPath

RosettaPath.default_linux_prefix = "newMountPoint/"
rpath = RosettaPath("myshare/mydir/app.py")
rpath.linux_path()
# newMountPoint/myshare/mydir/app.py

RosettaPath.input_mount_patterns["linux"] = r"^otherMount"
rpath = RosettaPath("otherMount/myshare/mydir/app.py")
rpath.win_path()
# C:\mount\myshare\mydir\app.py

```

___
# Utility Functions:

## Detect Image Sequences
RosettaPath offers 2 utility functions for dealing with image sequences that have an arbitrary number of frames and padding. `is_seq()` checks if a file is a sequence and `contains_seq()` checks if a directory contains one. Both of these functions can detect an image sequence without scanning the entire image sequence.

They both return a 3 item tuple of (bool, int, str) where:
>bool: True if the path contains a sequence, False otherwise
int: The number of digits in the sequence
str: The sequence name with a format specifer in place of the frame number. E.g. my_image_seq.%04d.tif


``` python
from rosettapath import is_seq, contains_seq

# file
result = is_seq("myshare/mydir/my_image_seq.0001.tif")
print(result)
# (True, 4, 'my_image_seq.%04d.tif')

# directory
result = contains_seq("myshare/mydir")
print(result)
# (True, 4, 'my_image_seq.%04d.tif')
```


___
<br>

## License
[MIT](https://choosealicense.com/licenses/mit/)