### About tool
On one hand, sam dumping tools are widely used, but surprisingly not much automated. On the other hand, WINHELLO pin dumping tools barely exists.
This simple and lightweight python script is made to automate the process of credentials dumping for both of these cases.

### Requirements
Requires the following conditions :
 - To be run from a GNU/linux's terminal (`python wcreddump.py`)
 - pypykatz installed on system (`apt install pypykatz`)
 - python >=3.10 with the following libs installed : dpapick3, PyCryptodome (`pip install dpapick3 PyCryptodome`)
 - `WINHELLO2hashcat.py` in the same directory as `wcreddump.py` (https://github.com/Banaanhangwagen/WINHELLO2hashcat)
 - A mounted drive with a windows os on it

### Now with parser !
<img alt="wcreddump help / parser" src="https://github.com/truerustyy/wcreddump/blob/main/wcreddump%20help.png">
Usage: wcreddump [-h] [--save | --no-save] [--os | --no-os] [-p P] [-d D] [-m {0,1,2}]
All default parser options can be changed directly in the source code for more automation

### Usage exemple
<img alt="Exemple usage of wcreddump on a kali linux." src="https://github.com/truerustyy/wcreddump/blob/main/wcreddump%20exemple3.png">

If used with all default settings, dumped data will be printed in terminal and saved automatically in the folder `outputs` with name of the drive and current unix time. `outputs` folder will be automatically created in the working directory if inexistent.
Dumped hashes can be cracked using JTR or hashcat with `-m 1000` for NTLM.s from SAM hive, and `-m 28100` for pin.s from WINHELLO (https://hashcat.net/wiki/doku.php?id=example_hashes)

### Other infos
Tool tested on Windows 10 22H2 build 19045.4170, Windows 10 pro 22H2 build 19045.5131, Windows 11 family 22H2 22621.2215.
As said in https://github.com/Banaanhangwagen/WINHELLO2hashcat?tab=readme-ov-file#remarks, systems with a TPM won't work as they are protected.

Provided "as is" without any warranty of any kind. Do not use for illegal purposes and use at your own risks.
Feel free to report bugs/mistakes or make suggesetions.
Good luck on your crackings !
