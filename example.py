#!/usr/bin/env python3

import unarchives
import zc.lockfile

tmp = "/tmp/unarchive.lock"
try:
    lock = zc.lockfile.LockFile(tmp)
    _ue = unarchives.Extruct(["/home/zips", "/home/rars"])
    _ue.do()
except zc.lockfile.LockError:
    print('Already started.')
