import MemoryGame_pb2_grpc
import Network
import Random
import grpc
import time
import sys

# para facilitar, o id da partida sera a semente para o embaralhamento
class MemoryGameServicer(MemoryGame_pb2_grpc.MemoryGameServicer):

    def __init__(self):
        # hash com o id da partida
        self.partidas = {}

    def Jogar(self, Id):
        pass

    def Assistir(self, Id):
        pass

    def FimJogo(self, Id):
        pass


def server():
    ip, broadcast = Network.getIP_BC()

    if(ip == None and sys.argv.__len__() != 2):
        print("Nao foi possivel obter o endereco IP. Use 'python3 Agenda_server.py IP")
        return

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    MemoryGame_pb2_grpc.add_MemoryGameServicer_to_server(MemoryGameServicer(), server)
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