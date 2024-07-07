import gzip 
import os # + Change working directories
import os.path # + Resolve relative paths to absolute and vice versa
import re # +
import subprocess # + Execute system commands, packages etc
import shutil # + Copy and move files
import tarfile

s = input("Type in a path to your deb-packages: ")

if s != None and "~" in s[0]: 
    workingDir = os.path.join(
        os.path.expanduser("~"),
        s[2:]
    )
elif s != None and "/" in s[0]:
    workingDir = s
elif s != None and "~" not in s[0] and "/" not in s[0]:
    workingDir = os.path.join(
    os.getcwd(),
    s)

os.chdir(workingDir)
print("\nThe working dir is " + os.getcwd() + "\n")

regex = re.compile(r"\.deb$")
debPkgs = list(filter(regex.search, os.listdir()))
for i in debPkgs:
    print(i)
    if str(i).removesuffix(".deb") not in os.listdir():
        os.mkdir(str(i).removesuffix(".deb"))
    if str(i).removesuffix(".deb") is empty:
        shutil.move(str(i), str(i).removesuffix(".deb"))
        os.chdir(str(i).removesuffix(".deb"))
        subprocess.run(["ar", "pxv" "??Popen Constructor"]check=True, capture_output=True)
print("\n\nThe cwd contains " + str(len(debPkgs)) + " deb packages.\n")


# /home/mdk/Documents/Experiments/Docker/Cryptopro/cryptopro-linux-amd64-deb
