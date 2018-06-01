from concurrent import futures
from Endereco import Endereco
import MemoryGame_pb2_grpc
import MemoryGame_pb2
import Network
import random
import grpc
import time
import sys

# para facilitar, o id da partida sera a semente para o embaralhamento
class MemoryGameServicer(MemoryGame_pb2_grpc.MemoryGameServicer):

    def __init__(self, ip):
        # hash com o id da partida
        self.ip = ip
        self.partidas = {}
        self.partidas[0] = Endereco(-1, ip)

        # quando o primeiro conectar, ele ficara esperando o proximo jogador
        # entao guarda o numero da partida
        self.partidaEsperando = None
        print("Tudo certo")

    def Jogar(self, request, context):

        if(self.partidaEsperando is not None):
            endereco = self.partidas[self.partidaEsperando] # recupera a  partida que falta um jogador
            self.partidaEsperando = None                    # marca dizendo que nao tem mais partida esperando
            return endereco                                 # retorna as informacoes da partida

        id = 0                                              # realmente ira comecar uma nova partida
        while(id in list(self.partidas.keys())):            # para pegar um id que nao esteja sendo usado
            id = random.randrange(362880)

        endereco = Endereco(id, self.ip)                    # recupera um endereco para esta nova partida
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


def server():
    ip, broadcast = Network.getIP_BC()

    if(ip is None and sys.argv.__len__() != 2):
        print("Nao foi possivel obter o endereco IP. Use 'python3 Agenda_server.py IP")
        return

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    MemoryGame_pb2_grpc.add_MemoryGameServicer_to_server(MemoryGameServicer(ip), server)
    #server.add_insecure_port('[::]:50051')
    server.add_insecure_port(ip + ':50051')
    server.start()
    print("Server inicializado em " + ip + ":50051")

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

server()