# -*- coding: ISO-8859-1 -*-

import random
import struct
import socket

class Endereco:

    def __init__(self, id):
        self.id = id
        self.ip = '224.1.2.3'
        # com probabilidade de 1 em 55535 obter o mesmo endereco
        # mas vale arriscar
        self.porta = random.randrange(10000, 65535)

    def getId(self):
        return self.id

    def getIp(self):
        return self.ip

    def getPorta(self):
        return self.porta