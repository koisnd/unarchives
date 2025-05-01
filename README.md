# Unarchive files

* This program unarchives recurcively. Supported file type is below.
  * zip
  * rar

## Requirements

* python3-rarfile
* python3-zc.lockfile
* unrar

## Installation

### On Ubuntu

```
# apt update
# apt install -qy python3-rarfile unrar
# cd /usr/local/lib/python3*/dist-packages
/usr/local/lib/python3.x/dist-packages# git clone https://github.com/koisnd/unarchives.git
```

## Usage

```
import unarchives

_ue = unarchives.Extruct(["/home/zips", "/home/rars"])
_ue.do()
```
