# MemoryGame-with-gRPC-protobuf

This is a project to Distributed System discipline. Simple Memory Game between two person in LAN.

The server is in Python3, and the exchange of the messages between server and client are using package Protobuf.

## Install Protobuf:
'''
sudo python3 -m pip install python3-protobuf
sudo python3 -m pip install --upgrade protobuf
'''

On cmd 'python3 Server/Server.py'. If you dont have 'ifconfig', use 'python3 Server/Server.py 192.168.0.105'. The 192.168.0.105 is the address of machine in the LAN and 5555 is a port to connect with server.

Have fun.