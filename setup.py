import sys
import traceback
import os
import shutil
import time
import click
from distutils.core import setup
from Cython.Build import cythonize

starttime = time.time()
build_dir = "build"
build_tmp_dir = build_dir + "/temp"


@click.command()
@click.option('-e', '--exclude', 'exclude', multiple=True, help='Directories to exclude.')
@click.argument('targets', nargs=-1, type=click.Path(exists=True))
@click.option('-d', '--delete', 'delC', is_flag=True, default=False, help='Delete C files')
def get(exclude: tuple, delC: bool, targets):
    exclude = set(list(exclude))
    del_list = []
    myself = sys.argv[0]  # equivalent to __file__

    if targets:
        for target in targets:
            try:
                setup(ext_modules=cythonize(target, compiler_directives={
                      'language_level': "3"}), script_args=["build_ext", "-b", os.path.dirname(target), "-t", build_tmp_dir])
            except Exception as ex:
                traceback.print_exc()
                continue
        return

    for root, dirs, files in os.walk(os.getcwd(), topdown=True):
        # feature to exclude certain directories, if specified in click option.
        dirs[:] = [d for d in dirs if d not in exclude]
        for file in files:
            path = os.path.join(root, file)
            if file.endswith(".py") or file.endswith(".pyx") and file != myself:
                try:
                    setup(ext_modules=cythonize(path, compiler_directives={
                        'language_level': "3"}), script_args=["build_ext", "-b", root, "-t", build_tmp_dir])
                except Exception as ex:
                    traceback.print_exc()
                    continue
    if delC:
        for root, __, files in os.walk(os.getcwd()):
            for file in files:
                path = os.path.join(root, file)
                if file.endswith(".c") and os.stat(path).st_mtime > starttime:
                    del_list.append(path)
                elif file.endswith(".so") and os.stat(path).st_mtime > starttime:
                    del_list.append(path)

    for f in del_list:
        os.remove(f)

    if os.path.exists(build_tmp_dir):
        shutil.rmtree(build_tmp_dir)

    print("Complete! Time:", time.time()-starttime, 's')


if __name__ == '__main__':
    get()
