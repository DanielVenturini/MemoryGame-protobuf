from MemoryGame_pb2 import Conecta
from MemoryGame_pb2 import Endereco

from EnderecoOperacoes import EnderecoOperacoes
from threading import Thread
import Network
import socket
import sys

# para facilitar, o id da partida sera a semente para o embaralhamento
class MemoryGameServicer():

    def __init__(self, ip):
        # hash com o id da partida
        self.ip = ip
        self.partidas = {}
        self.enderecos = EnderecoOperacoes()

        self.partidaEsperando = None
        print("Tudo certo")

        self.noAr()

    def Jogar(self):

        if(self.partidaEsperando is not None):
            endereco = self.partidas[self.partidaEsperando] # recupera a  partida que falta um jogador
            self.partidaEsperando = None                    # marca dizendo que nao tem mais partida esperando
            print("Partida fechada")
            return endereco                                 # retorna as informacoes da partida

        endereco = self.enderecos.criaEndereco()            # recupera um endereco para esta nova partida
        self.partidas[id] = endereco                        # guarda nas partidas ativas
        self.partidaEsperando = id                          # guarda o id para o proximo jogador que entrar

        print("Retornando endereco")
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
        data = conn.recv(4096)              # recebe o dado

        conecta = Conecta()
        conecta.ParseFromString(data)       # transforma em um objeto conecta

        print("Chegou o dado: " + conecta.mensagem)
        self.opcoes(conecta.mensagem, conn)

        conn.shutdown(socket.SHUT_RDWR)     # avisando que vai fechar
        conn.close()
        print("Tudo enviado")

    def opcoes(self, mensagem, conn):
        # envia um novo endereco
        if(mensagem.__eq__('@NOVO')):
            print("Vai enviar um novo endereco para o cliente")
            conn.send(self.Jogar())

        elif(mensagem.__eq__('@FIMJOGO')):
            pass
        elif(mensagem.__eq__('@ASSISTIR')):
            pass

    def noAr(self):
        self.criaSocket()

        while True:  # ever on
            print("Conectado em " + self.ip + ":" + str(self.porta))
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