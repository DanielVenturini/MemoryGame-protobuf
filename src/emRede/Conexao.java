/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package emRede;


import java.net.UnknownHostException;
import java.io.ObjectOutputStream;
import java.io.ObjectInputStream;
import java.net.MulticastSocket;
import java.net.DatagramPacket;
import java.net.InetAddress;
import java.io.IOException;
import java.net.Socket;

// Endereco.newBuilder();

/**
 *
 * @author venturini
 */
public class Conexao {

    private String ip;
    private int porta;

    private String ipGrupo;
    private int portaGrupo;
    private int id;     // id do jogo no servidor

    // objetos para trocar objetos e mensagens em rede
    MulticastSocket multcastSocket;
    ObjectOutputStream objOut;
    ObjectInputStream objIn;
    InetAddress group;
    Socket socket;

    // protocolo de troca de mensagem com o servidor
    String assistir = "@ASSISTIR";  // + id do jogo
    String fimJogo = "@FIMJOGO";    // + id jogo
    String novoJogo = "@NOVO";

    public Conexao(String ip, int porta){
        this.ip = ip;
        this.porta = porta;
    }

    private void conecta() throws UnknownHostException, IOException {
        System.out.println("Criando objetos de socket, leitura e escrita");
        socket = new Socket(InetAddress.getByName(ip), porta);

        objOut = new ObjectOutputStream(socket.getOutputStream());
        objIn = new ObjectInputStream(socket.getInputStream());
    }

    private void desconecta() throws IOException{
        socket.close();
    }

    // neste endereco sera o MultcastSocket do jogo
    private MemoryGameOuterClass.Endereco recebeEndereco() throws IOException, ClassNotFoundException{
        MemoryGameOuterClass.Endereco endereco;

        // escreve o objeto para o servidor
        objOut.writeObject(novoJogo);
        // aguarda a resposta
        endereco = (MemoryGameOuterClass.Endereco) objIn.readObject();

        return endereco;
    }

    // cria um socket multcast neste endereco e se conecta
    private void conectaMultcast(MemoryGameOuterClass.Endereco endereco) throws UnknownHostException, IOException{

        ipGrupo = endereco.getEndereco();
        portaGrupo = endereco.getPorta();

        id = endereco.getId();
        // cria, se ja nao houver, e conecta
        group = InetAddress.getByName(ipGrupo);
        multcastSocket = new MulticastSocket(portaGrupo);
        multcastSocket.joinGroup(group);
    }

    // pode ter um cliente esperando para comecar o jogo, entao envia uma mensagem avisando
    private void enviaNoGrupo(String mensagem) throws IOException{

        byte[] mensagemBytes = mensagem.getBytes();
        DatagramPacket messageOut = new DatagramPacket(mensagemBytes, mensagemBytes.length, group, portaGrupo);
	/* envia o datagrama como multicast */
	multcastSocket.send(messageOut);
    }

    private void ouve(){
        new Thread(){
            @Override
            public void run(){
                while(true){
                    try{
                        byte[] buffer = new byte[1024];
                        DatagramPacket messageIn = new DatagramPacket(buffer, buffer.length);
                        multcastSocket.receive(messageIn);
                    } catch (Exception ex) {
                        System.out.println("Erro na thread ouve multcast");
                        continue;
                    }
                }
            }
        }.start();
    }

    public int Jogar(){

        try{
            conecta();
            MemoryGameOuterClass.Endereco endereco = recebeEndereco();
            conectaMultcast(endereco);

            // @NEW quer dizer que o jogador esta pronto
            enviaNoGrupo("@NEW");

            // comeca a ouvir as mensagens no grupo
            ouve();
        } catch (Exception ex) {
            System.out.println("Erro ao inicializar o jogo");
            // -1 quer dizer que o jogo nao foi iniciado
            id = -1;
        }

        // semente do embaralhamento
        return id;
    }

    public void greet(String name) {
        System.out.println("Will try to greet " + name + " ...");

        // cria um builder
        MemoryGameOuterClass.Endereco.Builder builder = MemoryGameOuterClass.Endereco.newBuilder();
        // adicionando o que tiver de adicionar
        builder.setId(-1);
        builder.setEndereco("4499737489");
        builder.setPorta(2+1);

        // constroi seja lah o que ele estah construindo
        MemoryGameOuterClass.Endereco contato = builder.build();

        // o que o servidor responder vai ser guardado aqui
        MemoryGameOuterClass.Endereco response;
    }
}
