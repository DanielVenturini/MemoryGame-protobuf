# -*- coding: ISO-8859-1 -*-

import random
import socket

class Endereco:

    def __init__(self, id):
        self.id = id
        self.ip = '224.1.2.3'
        self.porta = -1

        self.bind()

    # esta funcao ira tentar conectar a algum endereco
    def bind(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        s.bind((self.ip, 0))            # conecta somente para recuperar um endereco disponivel
        self.porta = s.getsockname()[1] # pega o endereco
        s.close()                       # fecha o socket

    def getId(self):
        return self.id

    def getIp(self):
        return self.ip

    def getPorta(self):
        return self.porta