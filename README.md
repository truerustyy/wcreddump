### About tool
On one hand, sam dumping tools are widely used, but surprisingly not much automated. On the other hand, WINHELLO pin dumping tools barely exists.
This simple and lightweight python script is made to automate the process of credentials dumping for both of these cases.

### Requirements
Requires the following conditions :
 - To be ran from a GNU/linux's terminal (`python wcreddump.py`)
 - samdump2 (`apt install samdump2`)
 - python >3.10 with the following libs installed : dpapick3, PyCryptodome
 - `WINHELLO2hashcat.py` in the same directory as `wcreddump.py` (https://github.com/Banaanhangwagen/WINHELLO2hashcat)
 - A mounted drive with a windows os on it

### Other infos
Tool tested on windows 10  21H1.
As said in https://github.com/Banaanhangwagen/WINHELLO2hashcat?tab=readme-ov-file#remarks, systems with a TPM won't work as they are protected.

Dumped hashes can be cracked using JTR or hashcat with `-m 1000` for NTLMs from SAM hive, and `-m 28100` for pins from WINHELLO (https://hashcat.net/wiki/doku.php?id=example_hashes)

Provided "as is" without any warranty of any kind. Feel free to report bugs/mistakes.
Good luck on your crackings !
