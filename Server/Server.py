from Endereco import Endereco
from threading import Thread
#import MemoryGame_pb2
import Network
import random
import socket
import pickle
import sys

# para facilitar, o id da partida sera a semente para o embaralhamento
class MemoryGameServicer():

    def __init__(self, ip):
        # hash com o id da partida
        self.ip = ip
        self.partidas = {}
        self.partidas[0] = Endereco(-1)

        # quando o primeiro conectar, ele ficara esperando o proximo jogador
        # entao guarda o numero da partida
        self.partidaEsperando = None
        print("Tudo certo")

        self.noAr()

    def Jogar(self, request, context):

        if(self.partidaEsperando is not None):
            endereco = self.partidas[self.partidaEsperando] # recupera a  partida que falta um jogador
            self.partidaEsperando = None                    # marca dizendo que nao tem mais partida esperando
            return endereco                                 # retorna as informacoes da partida

        id = 0                                              # realmente ira comecar uma nova partida
        while(id in list(self.partidas.keys())):            # para pegar um id que nao esteja sendo usado
            id = random.randrange(362880)

        endereco = Endereco(id)                             # recupera um endereco para esta nova partida
        self.partidas[id] = endereco                        # guarda nas partidas ativas
        self.partidaEsperando = id                          # guarda o id para o proximo jogador que entrar

        return endereco

    def Assistir(self, request, context):
        try:
            return self.partidaEsperando[request[0]]        # se tiver uma partida com este id, retorna o endereco
        except KeyError:
            return None                                     # senao, retorna None

    def FimJogo(self, request, context):
        try:
            self.partidas.pop(request[0])                   # remove o endereco e o id da partida
        except KeyError:                                    # provavelmente nao dara este erro
            pass

    def criaSocket(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.bind((self.ip, 5555))
        except socket.error:
            self.s.bind((self.ip, 0))

        self.porta = self.s.getsockname()[1]
        self.s.listen(5)

    def processaRequisicao(self, conn):
        data = conn.recv(4096)          # recebe o dado

        opcao = pickle.loads(data)     # des-serializa o objeto, ou seja, transforma em uma string

        try:                            # tenta transformar em uma string
            opcao = str(opcao)
        except ValueError:              # se der excecao, nao faz mais nada
            return None

        print("Chegou o dado: " + opcao)


    def noAr(self):
        self.criaSocket()
        while True:  # ever on
            print("Wait for new connections on " + self.ip + ":" + str(self.porta))
            conn, addr = self.s.accept()
            args = []
            args.append(conn)
            thread = Thread(target=self.processaRequisicao, args=(args))
            thread.start()  # execute thread

            continue
# -------------------------------------------------------------------------------------

ip, bdcst = Network.getIP_BC()

# no caso de ser no windows
if (ip is None or ip.__eq__("'ifconfig'")):
    if(sys.argv.__len__() != 2):
        print("Impossivel obter o endereco IP. Use 'python3 Server.py IP")
    else:
        MemoryGameServicer(sys.argv[1])
else:
    print("Valor do ip: " + ip)
    MemoryGameServicer(ip)