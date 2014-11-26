RTP-3251
========

Networking protocol

Current Status:
i) I can run files like tester1.py (in src/client) using eclipse but not in command line. 
b) I followed tutorials such as the following to set up the __init__ files in src, src/client and src/server:

	https://docs.python.org/2/tutorial/modules.html#packages
	https://stackoverflow.com/questions/448271/what-is-init-py-for
	
3) Currently, the RTP-3251 and src are both set as source directories, so be aware of that. 
4) If for some reason this directory doesn't work out, just move all files back to src and run.

==============
Run instructions:

1. Run NetEmu as specified in the ReadMe.txt given with the emulator. (i.e. NetEmu 8000 -options)
2. Run "python serverApplication.py" in the directory with the server application. This file is set up to run with python 2.7
3. Run "python clientApplication.py" in the diector with the client application. This file also uses 2.7.
4. To add more files, simply create the files in the directories with the respective application. Change the client application's main method
	to use the method "postF" and "getF" to interacte with these files.
	
	
