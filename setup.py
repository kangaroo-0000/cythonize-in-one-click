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
@click.option('-e', '--dir2exclude', multiple=True, help='Directories to exclude. ')
@click.option('-f', '--file2exclude', multiple=True, help='Files to exclude. ')
@click.option('-t', '--targets', type=click.Path(exists=True), multiple=True, help='Files to target. ')
@click.option('-d', '--delete', 'delC', is_flag=True, default=False, help='Delete C files.')
def get(dir2exclude, file2exclude, delC, targets):
    dir2exclude = set(list(dir2exclude))
    file2exclude = set(list(file2exclude))
    myself = 'setup.py'

    if targets:
        for target in targets:
            if os.path.isdir(target):
                for root, dirs, files in os.walk(target, topdown=True):
                    dirs[:] = [d for d in dirs if d not in dir2exclude]
                    files[:] = [f for f in files if f not in file2exclude]
                    for file in files:
                        path = os.path.join(root, file)
                        if file.endswith(".py") or file.endswith(".pyx") and file != myself:
                            try:
                                setup(ext_modules=cythonize(path, compiler_directives={
                                    'language_level': "3"}), script_args=["build_ext", "-b", root, "-t", build_tmp_dir])
                            except Exception as ex:
                                traceback.print_exc()
                                continue 
            elif os.path.isfile(target):     
                try:
                    setup(ext_modules=cythonize(target, compiler_directives={
                        'language_level': "3"}), script_args=["build_ext", "-b", os.path.dirname(target), "-t", build_tmp_dir])
                except Exception as ex:
                    traceback.print_exc()
                    continue
        if delC:
            delete()
        if os.path.exists(build_tmp_dir):
            shutil.rmtree(build_tmp_dir)
        return

    for root, dirs, files in os.walk(os.getcwd(), topdown=True):
        # feature to exclude certain directories/files, if specified in click option.
        dirs[:] = [d for d in dirs if d not in dir2exclude]
        files[:] = [f for f in files if f not in file2exclude]
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
        delete()

    if os.path.exists(build_tmp_dir):
        shutil.rmtree(build_tmp_dir)

    print("Complete! Time:", time.time()-starttime, 's')


def delete():
    del_list = []
    for root, __, files in os.walk(os.getcwd()):
        for file in files:
            path = os.path.join(root, file)
            if file.endswith(".c") and os.stat(path).st_mtime > starttime:
                del_list.append(path)
            # elif file.endswith(".so") and os.stat(path).st_mtime > starttime:
            #     del_list.append(path)
    for f in del_list:
        os.remove(f)


if __name__ == '__main__':
    get()
