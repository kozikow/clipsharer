Shares clipboard between computers.
Quick and dirty implementation in python.
Works between different OS and with more than one client.
Monitors for clipboard changes at each node and sends them to server or all clients via socket.

USAGE

python clipsharer.py [-h] (-s | -c) [-d] hostname port

positional arguments:
  hostname
  port

optional arguments:
  -h, --help    show this help message and exit
  -s, --server  Run as server
  -c, --client  Run as client
  -d, --debug   Run as debug
