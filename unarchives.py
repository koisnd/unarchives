"""Unarchive main program."""

import os
import re
import yaml
from unarchives.unrar import unrar
from unarchives.unzip import unzip

class Extruct(object):
    """Initial values"""
    target_dirs = []
    target_files = []

    def __init__(self, dirs=None):
        """Initial settings"""
        self.read_and_store_config()
        if dirs:
            for _p in dirs:
                if type(_p) is dict:
                    self.target_dirs.insert(0, _p)
                elif type(_p) is str:
                    _d = dict(self.conf["default_behavior"])
                    _d["path"] = _p
                    self.target_dirs.insert(0, _d)
        else:
            self.target_dirs = self.conf["unarchive"]

    def read_and_store_config(self):
        """Read default configuration"""
        with open(os.path.dirname(__file__) + "/config.yaml") as fh:
            _config = yaml.load(fh.read(), Loader=yaml.Loader)
        for _p in _config["includes"]:
            _config = self.read_config_file(_p, _config)
        self.conf = _config

    def read_config_file(self, path="", conf=None):
        """Read optional configuration"""
        path = os.path.expanduser(path)
        _c = {}
        if os.path.isfile(path):
            with open(path) as fh:
                _c = yaml.load(fh.read(), Loader=yaml.Loader)
        return conf | _c

    def do(self):
        """Unarchive"""
        if not self.target_files:
            self.target_files = self.listing_targets()
        for _t in self.target_files:
            if _t.rsplit(".", 1)[-1].lower() == "rar":
                unrar(
                    path=_t,
                    delete_on_success=True,
                    rename_on_error=True,
                    error_stop=True,
                )
            if _t.rsplit(".", 1)[-1].lower() == "zip":
                unzip(
                    path=_t,
                    delete_on_success=True,
                    rename_on_error=True,
                    error_stop=True,
                )

    def check_path_should_do(self, path=None, conf=None):
        """Check path which should be extruct"""
        if not conf:
            return None
        if not os.path.isfile(path):
            return None
        _b = dict(conf)
        del _b['path']
        for _t in _b:
            if _b[_t]:
                if _b[_t]["ignore_case"]:
                    _r = re.search(_b[_t]["expression"], path, re.I,)
                else:
                    _r = re.search(_b[_t]["expression"], path)
                if _r:
                    return True
        return None

    def listing_targets(self):
        """Listing files from directory"""
        _l = []
        for _d in self.target_dirs:
            for _cd, _, _f in os.walk(_d["path"]):
                for _fp in _f:
                    _t = f'{_cd}/{_fp}'
                    if self.check_path_should_do(_t, _d):
                        _l.append(_t)
        return _l
