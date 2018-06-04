from MemoryGame_pb2 import Conecta
from MemoryGame_pb2 import Resolvido
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
        self.resolvidos = {}
        self.enderecos = EnderecoOperacoes()

        self.partidaEsperando = None
        print("Tudo certo")

        self.noAr()

    def Jogar(self):

        if(self.partidaEsperando is not None):
            endereco = self.partidas[self.partidaEsperando] # recupera a  partida que falta um jogador
            self.partidaEsperando = None                    # marca dizendo que nao tem mais partida esperando
            return endereco                                 # retorna as informacoes da partida

        self.partidaEsperando, endereco = self.enderecos.criaEndereco() # recupera um endereco para esta nova partida
        self.partidas[self.partidaEsperando] = endereco     # guarda nas partidas ativas
        self.resolvidos[self.partidaEsperando] = []         # cria um array para guardar os objetos resolvidos

        return endereco

    # tem que retornar tambem o historico das pecas
    def Assistir(self, id):
        try:
            end = Endereco()
            end.ParseFromString(self.partidas[int(id)])
            return self.partidas[int(id)]                   # se tiver uma partida com este id, retorna o endereco
        except KeyError:
            print("Me derrubaram aqui O, denovo")
            return None                                     # senao, retorna None

    # simplesmente remove o id da hash
    def FimJogo(self, id):
        try:
            self.partidas.pop(int(id))                      # remove o endereco e o id da partida
        except KeyError:
            print("Me derrubaram aqui O")

    def Resolve(self, botao, id):
        try:
            print(self.resolvidos)
            b = self.resolvidos[int(id)]
            b.append(botao)
            print(self.resolvidos)
            print("Adicionado o botao com sucesso")
            print(self.resolvidos)
        except:
            print("Me derrubaram aqui O, na ora de resolver")

    # retorna todas os botoes que ja foram resolvidos
    def pegaTodosResolvidos(self, id, conn):
        try:
            resolvidos = self.resolvidos[int(id)]
            print("Resolvidos: ", resolvidos)

            for botao in resolvidos:
                botaoResolvido = Resolvido()
                botaoResolvido.idJogo = id              # tecnicamente o cliente nao vai usar este id
                botaoResolvido.botao = botao            # tecnicamente o cliente nao vai usar este id
                conn.send(botao.SerializeToString())    # envia o botao
        except:
            print("Me derrubaram aqui O, na hora de devolver os resolvidos")
            return None

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

        # tenta se for mensagem
        try:
            conecta = Conecta()
            conecta.ParseFromString(data)       # transforma em um objeto conecta

            if(conecta.mensagem.__eq__('')):    # se vir vazio eh um resolvido entao
                raise ValueError

            print("Chegou o Conecta: " + conecta.mensagem)
            self.opcoesConecta(conecta.mensagem, conn)
        except:                             # entao eh um resolvido
            resolvido = Resolvido()
            resolvido.ParseFromString(data) # transforma em um objeto resolvido

            print("Chegou o Botao: " + resolvido.botao + " do jogo " + str(resolvido.idJogo))
            self.Resolve(resolvido.botao, resolvido.idJogo)

        conn.shutdown(socket.SHUT_RDWR)     # avisando que vai fechar
        conn.close()
        print("Tudo enviado")

    def opcoesConecta(self, mensagem, conn):
        # envia um novo endereco
        if(mensagem.__eq__('@NOVO')):
            conn.send(self.Jogar())

        elif(mensagem.startswith('@FIMJOGO')):
            # '@FIMJOGO IDJOGO'
            id = mensagem.split(' ')[1]
            self.FimJogo(id)

        elif(mensagem.startswith('@GETREVELADOS')):
            # '@FIMJOGO IDJOGO'
            id = mensagem.split(' ')[1]
            self.pegaTodosResolvidos(id, conn)

        elif(mensagem.startswith('@ASSISTIR')):
            id = mensagem.split(' ')[1]
            conn.send(self.Assistir(id))

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
    MemoryGameServicer(ip)