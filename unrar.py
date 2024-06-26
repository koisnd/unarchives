"""Main program for rar file"""

import os
import shutil
import subprocess

import rarfile

def unrar(
        path="",
        delete_on_success=True,
        rename_on_error=True,
        error_stop=True,
        ):
    try:
        with rarfile.RarFile(path) as rf:
            ext_path_tmp = path.rsplit(".", 1)[0] + ".temp/"
            ext_path = path.rsplit(".", 1)[0] + "/"
            os.mkdir(ext_path_tmp)
            rf.extractall(path=ext_path_tmp)
            _l = os.listdir(ext_path_tmp)
            if len(_l) == 1 and os.path.isdir(ext_path_tmp + _l[0]):
                _only_one_dir_path = ext_path_tmp + _l[0]
                shutil.move(_only_one_dir_path, os.path.dirname(path))
                os.rmdir(ext_path_tmp)
            else:
                os.rename(ext_path_tmp, ext_path)
            if delete_on_success:
                os.remove(path)
    except rarfile.RarUnknownError:
        """
        rarfile.RarUnknownError: Unknown exit code [1]:
            b"bsdtar: Error opening archive: Failed to open '--'\n"
        """
        print(ext_path_tmp)
        os.rmdir(ext_path_tmp)
        if command_unrar(path) and error_stop:
            raise

    except:
        if rename_on_error:
            os.rename(path, path + ".error")
        if error_stop:
            raise

def command_unrar(path=None):
    _cd = os.getcwd()
    _wd = os.path.dirname(path)
    os.chdir(_wd)
    try:
        _st = subprocess.check_output(
            ['unrar', 'x', '-o+', path]).decode().rstrip()
    except:
        print(f'Error: extract error {path} .')
        os.rename(path, f'{path}.error')
        os.chdir(_cd)
        return True
    os.remove(path)
    os.chdir(_cd)
    return None
