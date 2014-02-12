Shares clipboard between computers.
Quick and dirty implementation in python.
Works between different OS and with more than one client.
Monitors for clipboard changes at each node and sends them to server or all clients via socket.

USAGE
```
python clipsharer.py [-h] (-s | -c) [-d] hostname port

positional arguments:
  hostname
  port

optional arguments:
  -h, --help    show this help message and exit
  -s, --server  Run as server
  -c, --client  Run as client
  -d, --debug   Run as debug
```
On linux it have to be run from xorg aware terminal.
Since whole package is supposed to be used with virtual machine/remote desktop setup just
open gnome, kde or similiar terminal on the Linux system and run server from this console.

Tested on linux server and mac client.
Should work elsewhere, since I use platform agnostic python packages.

Todo:
 - Close sockets on kill
 - Moar security
 - More transparent error if Linux user do not runs it from terminal that do not have access to xserver.
