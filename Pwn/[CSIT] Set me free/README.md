# [CSIT] Set me free
- 1000 points
- did not solve

Description
---
We found a mysterious note and a binary in one of the computers of an abandoned lab previously used by APOCALYPSE.

The note reads, "Be free of the structures and repoint me elsewhere."

Use the binary to get a flag from the challenge server

Interact with the service using:
nc chals.cyberthon22f.ctf.sg 10101
```
Helpful tips!

Windows Platform
===============
To run the .exe binary provided, you just need to double click the provided binary. 

Helpful tools:
	• windbg
		1. Download the installer at https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/
		2. After installing, head over to C:\Program Files (x86)\Windows Kits\10\Debuggers\x64 and
		   find windbg.exe

Kali Linux Platform
===============
To run the .exe binary provided, you will have to install wine on your kali linux 
machine in order to run it. The following are the steps to perform to get the binary
running on your local kali linux machine.

Run the following commands to install wine:
	1. sudo apt-get update
	2. sudo apt-get install wine 

After the installation of wine, run the following command to get the binary working:
	1. wine uaf_challenge.exe

Helpful tools:
	• gdb
```
Files: [uaf_challenge.exe](./uaf_challenge.exe)

Solution
---
kiv
