"""Main program for zip file"""

import os
import shutil

import zipfile

def unzip(
        path="",
        delete_on_success=True,
        rename_on_error=True,
        error_stop=True,
        ):
    try:
        with zipfile.ZipFile(path) as zf:
            ext_path_tmp = path.rsplit(".", 1)[0] + ".temp/"
            ext_path = path.rsplit(".", 1)[0] + "/"
            os.mkdir(ext_path_tmp)
            zf.extractall(path=ext_path_tmp)
            _l = os.listdir(ext_path_tmp)
            if len(_l) == 1 and os.path.isdir(ext_path_tmp + _l[0]):
                _only_one_dir_path = ext_path_tmp + _l[0]
                shutil.move(_only_one_dir_path, os.path.dirname(path))
                os.rmdir(ext_path_tmp)
            else:
                os.rename(ext_path_tmp, ext_path)
            if delete_on_success:
                os.remove(path)
    except:
        if rename_on_error:
            os.rename(path, path + ".error")
        if error_stop:
            raise
