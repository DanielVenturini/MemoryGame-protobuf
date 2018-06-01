from concurrent import futures
from Agenda_pb2 import Contato
import Agenda_pb2_grpc
import Network
import grpc
import time
import sys

class AgendaServicer(Agenda_pb2_grpc.AgendaServicer):

    def __init__(self):
        self.Agenda = []

    def Adicionar(self, contato, context):
        print("Adicionando contato: " + contato.nome + " " + contato.telefone)

        self.Agenda.append(contato)
        return contato


    def Remover(self, contato, context):
        print("Removendo o contato {} {}".format(contato.nome, contato.telefone))

        for contatoLista in self.Agenda:
            if(contatoLista.nome == contato.nome or contatoLista.telefone == contato.telefone):
                print("Encontrado contato para remover: " + contato.nome + " " + contato.telefone)
                self.Agenda.remove(contatoLista)
                return contatoLista

        return self.contatoVazio(contato)


    def Consultar(self, contato, context):
        print("Procurando o contato {} {}".format(contato.nome, contato.telefone))

        for contatoLista in self.Agenda:
            if(contatoLista.nome == contato.nome or contatoLista.telefone == contato.telefone):
                print("Encontrado contato: " + contato.nome + " " + contato.telefone)
                return contatoLista

        return self.contatoVazio(contato)

    def contatoVazio(self, contato):
        print("Nenhum contato " + contato.nome + " " + contato.telefone + ". Retornano contato vazio.")
        contato = Contato()
        contato.nome = "Nao encontrado"
        contato.telefone = "Nao encontrado"
        return contato

def server():
    ip, broadcast = Network.getIP_BC()

    if(ip == None and sys.argv.__len__() != 2):
        print("Nao foi possivel obter o endereco IP. Use 'python3 Agenda_server.py IP")
        return

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Agenda_pb2_grpc.add_AgendaServicer_to_server(AgendaServicer(), server)
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