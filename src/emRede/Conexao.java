/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package emRede;


import interfaces.Interface;
import java.net.UnknownHostException;
import java.io.ObjectOutputStream;
import java.io.ObjectInputStream;
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
    ObjectOutputStream objOut;
    ObjectInputStream objIn;
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

        objOut = new ObjectOutputStream(socket.getOutputStream());
        objIn = new ObjectInputStream(socket.getInputStream());
    }

    private void desconecta() throws IOException{
        socket.close();
    }

    // neste endereco sera o MultcastSocket do jogo
    private MemoryGame.Endereco recebeEndereco() throws IOException, ClassNotFoundException{
        MemoryGame.Endereco endereco;

        System.out.println("Enviado a string");
        // escreve o objeto para o servidor
        objOut.writeObject(novoJogo);
        // aguarda a resposta
        System.out.println("Recebendo a resposta");
        endereco = (MemoryGame.Endereco) objIn.readObject();
        System.out.println("Receeu");

        return endereco;
    }

    // cria um socket multcast neste endereco e se conecta
    private void conectaMultcast(MemoryGame.Endereco endereco) throws UnknownHostException, IOException{

        ipGrupo = endereco.getEndereco();
        portaGrupo = endereco.getPorta();

        id = endereco.getId();
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
                        continue;
                    }
                }
            }
        }.start();
    }

    public int Jogar(){

        try{
            conecta();
            MemoryGame.Endereco endereco = recebeEndereco();
            conectaMultcast(endereco);

            // @NEW + nick quer dizer que o jogador esta pronto
            enviaNoGrupo("@USER " + inte.getNick());

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
        MemoryGame.Endereco.Builder builder = MemoryGame.Endereco.newBuilder();
        // adicionando o que tiver de adicionar
        builder.setId(-1);
        builder.setEndereco("4499737489");
        builder.setPorta(2+1);

        // constroi seja lah o que ele estah construindo
        MemoryGame.Endereco contato = builder.build();

        // o que o servidor responder vai ser guardado aqui
        MemoryGame.Endereco response;
    }
}
