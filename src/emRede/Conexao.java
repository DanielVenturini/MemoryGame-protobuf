/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package emRede;


import interfaces.Interface;
import java.io.DataInputStream;
import java.net.UnknownHostException;
import java.net.MulticastSocket;
import java.net.DatagramPacket;
import java.net.InetAddress;
import java.io.IOException;
import java.net.Socket;
import java.util.HashMap;

// Endereco.newBuilder();

/**
 *
 * @author venturini
 */
public class Conexao {

    private String nick;
    private String ip;
    private int porta;

    private String ipGrupo;
    private int portaGrupo;
    private int id;     // id do jogo no servidor

    // objetos para trocar objetos e mensagens em rede
    MulticastSocket multcastSocket;
    InetAddress group;
    Socket socket;

    // protocolo de troca de mensagem com o servidor
    String assistir = "@ASSISTIR";  // + id do jogo
    String fimJogo = "@FIMJOGO";    // + id jogo
    String novoJogo = "@NOVO";

    // troca de mensagem entre os clientes
    String revela = "@REVELA";
    String comeca = "@NEW";

    Interface inte;

    private static HashMap<javax.swing.JButton, String> botoesNomes = new HashMap<>();

    public Conexao(String ip, int porta, String nick, Interface inte){
        this.porta = porta;
        this.inte = inte;
        this.ip = ip;
    }

    private void conecta() throws UnknownHostException, IOException {
        System.out.println("Criando objetos de socket, leitura e escrita");
        socket = new Socket(InetAddress.getByName(ip), porta);
    }

    private void desconecta() throws IOException{
        socket.close();
    }

    // neste endereco sera o MultcastSocket do jogo
    private void recebeEndereco(String stringParaServidor) throws IOException, ClassNotFoundException{

        System.out.println("Enviado a string");
        // cria uma mensagem para o servidor
        MemoryGame.Conecta mensagem = criaMensagem(stringParaServidor);
        System.out.println("Crou a mensagem, agora vamos enviar");
        // escreve o objeto para o servidor
        mensagem.writeTo(socket.getOutputStream());

        DataInputStream recebe = new DataInputStream(socket.getInputStream());

        // recebe o compromisso do servidor e faz o Parse

        MemoryGame.Endereco endereco = MemoryGame.Endereco.parseFrom(recebe);
        System.out.println("Endereco: " + endereco.getEndereco() + ". Id: " + endereco.getId() + ". Porta: " + endereco.getPorta());

        ipGrupo = endereco.getEndereco();
        portaGrupo = endereco.getPorta();
        id = endereco.getId();
    }

    // cria um socket multcast neste endereco e se conecta
    private void conectaMultcast() throws UnknownHostException, IOException{

        // cria, se ja nao houver, e conecta
        group = InetAddress.getByName(ipGrupo);
        multcastSocket = new MulticastSocket(portaGrupo);
        multcastSocket.joinGroup(group);
    }

    // pode ter um cliente esperando para comecar o jogo, entao envia uma mensagem avisando
    public void enviaNoGrupo(String mensagem) throws IOException{

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
                    }
                }
            }
        }.start();
    }

    public int Assistir(int id){
        return returnIdEmbaralhamento(assistir + " " + Integer.toString(id));
    }

    public int Jogar(){
        return returnIdEmbaralhamento(novoJogo);
    }

    // string complemento do comando, por exemplo, para assistir precisamos do @ASSISTIR + id
    // entao o Id sera este complemento
    public int returnIdEmbaralhamento(String stringParaServidor){
        try{
            conecta();
            recebeEndereco(stringParaServidor);
            desconecta();
            conectaMultcast();

            // @NEW + nick quer dizer que o jogador esta pronto
            enviaNoGrupo("@USER " + inte.getNick());

            // comeca a ouvir as mensagens no grupo
            ouve();
        } catch (Exception ex) {
            System.out.println("Erro ao inicializar o jogo: " + ex);
            // -1 quer dizer que o jogo nao foi iniciado
            id = -1;
        }

        // semente do embaralhamento
        return id;
    }
    public MemoryGame.Conecta criaMensagem(String msg) {
        System.out.println("Will try to greet " + msg + " ...");

//        // cria um builder
//        MemoryGame.Endereco.Builder builder = MemoryGame.Endereco.newBuilder();
//        // adicionando o que tiver de adicionar
//        builder.setId(-1);
//        builder.setEndereco("4499737489");
//        builder.setPorta(2+1);
//
//        // constroi seja lah o que ele estah construindo
//        MemoryGame.Endereco contato = builder.build();

        MemoryGame.Conecta.Builder builder = MemoryGame.Conecta.newBuilder();
        builder.setMensagem(msg);
        builder.setId(-1);          // id simbolico

        MemoryGame.Conecta conecta = builder.build();
        return conecta;
    }
}
