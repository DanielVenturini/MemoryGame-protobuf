from Agenda_pb2 import Contato
import Agenda_pb2_grpc
import grpc
import sys

def obterDados():
    nome = input("Digite o nome do Contato: ")
    telefone = input("Digite o numero do Contato: ")

    contato = Contato()
    contato.nome = nome
    contato.telefone = telefone

    return contato

def adicionar(stub):
    contato = obterDados()

    print("Enviando contato {} {} para adicionar ao servidor".format(contato.nome, contato.telefone))
    stub.Adicionar(contato)
    print("Contato adicionado\n")

def consultar(stub):
    contato = obterDados()

    print("Enviando contato {} {} para consupoolta no servidor\n".format(contato.nome, contato.telefone))
    contatoResposta = stub.Consultar(contato)
    print("Contato encontrado: {} {}.\n".format(contatoResposta.nome, contatoResposta.telefone))


def excluir(stub):
    contato = obterDados()

    print("Enviando contato {} {} para excluir no servidor\n".format(contato.nome, contato.telefone))
    contato = stub.Remover(contato)
    print("Removido o contato {} {}.\n".format(contato.nome, contato.telefone))


def run():

    if(sys.argv.__len__() != 2):
        print("Inicializacao incorreta. Use 'python3 Agenda_cliente.py IP:PORT' do servidor.")
        return

    #channel = grpc.insecure_channel('[::]:50051')
    channel = grpc.insecure_channel(sys.argv[1])
    stub = Agenda_pb2_grpc.AgendaStub(channel)

    while(True):
        opc = input("A para adicionar, C para consultar, E para excluir contatos ou Q para sair: ").lower()

        try:
            if(opc == 'a'):
                adicionar(stub)
            elif(opc == 'c'):
                consultar(stub)
            elif(opc == 'e'):
                excluir(stub)
            elif(opc == 'q'):
                return
        except:
            print("Server nao conectado.\n")


run()