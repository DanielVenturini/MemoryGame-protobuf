# MemoryGame-with-protobuf

This is a project to Distributed System discipline. Simple Memory Game between two person in LAN and any watchers.

![Screen](https://i.ibb.co/LkX5Dkq/screen.jpg)

The server is in Python3, and the exchange of the messages between server and client are using protocols Protobuf.

## Install:
To install, clone this repository and install the required packages:

```
git clone https://github.com/danielventurini/memorygame-with-protobuf
sudo python3 -m pip install python3-protobuf
sudo python3 -m pip install --upgrade protobuf
```

## Run Server
On terminal type:

`python3 Server/Server.py`.

Or directly, type:

`python3 Server/Server.py 192.168.0.105`.

The `192.168.0.105` is the address of machine in the LAN.

## Run game
Open the folder with NetBeans and run.

## Watch Mach
It's also can watch any match in the same LAN. To do this, use the ID, shown in the game screen.

Have fun.
