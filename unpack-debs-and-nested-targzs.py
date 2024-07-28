# These tools were used:
# - pycodestyle;
# - pyflakes;
# - McCabe complexity checker in Flake8;

# These conventions were used:
# - line length to 88 chars (see 'Black' explanation);
# - global variables instead of classes: I can't see a reason why I should
# complicate a simple-minded script with OOP

import os
import os.path
import re
import shutil
import subprocess
import sys
import tarfile
import traceback


def path_to_deb_pkgs():
    global working_dir
    path = input("Type in a path to a directory with deb-packages: ")

    match list(path):
        case ("/", *_) if path is not None:
            working_dir = path
        case ("~", *_) if path is not None:
            working_dir = os.path.join(os.path.expanduser("~"), path[2:])
        case (_, *_) if path is not None:
            working_dir = os.path.join(os.getcwd(), path)
        case _:
            raise NotADirectoryError

    os.chdir(working_dir)


def unpack_deb_pkgs():
    global deb_pkgs, dirs_for_deb_pkg

    re_deb = re.compile(r"\.deb$")
    deb_pkgs = list(filter(re_deb.search, os.listdir()))
    dirs_for_deb_pkg = [str(i).removesuffix(".deb") for i in deb_pkgs]

    print("\n\nThe cwd contains " + str(len(deb_pkgs)) + " debian packages.\n")

    # Make direcrories
    for package in deb_pkgs:
        for directory in dirs_for_deb_pkg:
            if str(package).removesuffix(".deb") == directory:
                if directory not in os.listdir():
                    os.mkdir(directory)
                    print(
                            "Made a directory where "
                            + str(package)
                            + " will be unpacked"
                    )
                if any(os.scandir(directory)) is False:
                    shutil.move(package, directory)
                    subprocess.run(
                        [
                            shutil.which("ar"), "xv", "--output", directory,
                            directory + "/" + package
                        ],
                        check=True
                    )
                    os.remove(directory + "/" + package)


def unpack_archives_in_unpacked_debs():
    re_tar_gz = re.compile(r"\.tar\.gz$")

    for directory, _, files in os.walk(working_dir):
        for file in filter(re_tar_gz.search, files):
            try:
                tarfile.open(
                    name=os.path.join(directory, file),
                    mode='r:gz'
                    ).extractall(path=directory, filter='tar')
            except Exception:
                print("Short exception:")
                print(sys.exc_info())

                print("\nLong exception:")
                traceback.print_exc()
            else:
                os.remove(os.path.join(directory, file))


path_to_deb_pkgs()
unpack_deb_pkgs()
unpack_archives_in_unpacked_debs()
