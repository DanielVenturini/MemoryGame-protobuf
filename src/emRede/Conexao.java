/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package emRede;

import java.util.concurrent.CountDownLatch;
import io.grpc.StatusRuntimeException;
import io.grpc.ManagedChannelBuilder;
import java.util.concurrent.TimeUnit;
import io.grpc.stub.StreamObserver;
import com.google.protobuf.Message;
import java.util.logging.Logger;
import java.util.logging.Logger;
import java.util.logging.Level;
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannel;
import java.io.IOException;
import java.util.Iterator;
import java.util.Random;
import java.util.Random;
import io.grpc.Status;
import java.util.List;

// Endereco.newBuilder();

/**
 *
 * @author venturini
 */
public class Conexao {

    private ManagedChannel channel;
    private Random random = new Random();

    public Conexao(String ip, int porta){
        this(ManagedChannelBuilder.forAddress(ip, porta).usePlaintext().build());

        //criaToco(criaConexao(ip, porta));
        
    }

    public MemoryGameOuterClass.Endereco Jogar(){
        MemoryGameOuterClass.Endereco endereco;

        //endereco = channel.
        //Endereco.newBuilder();
    }

    public void criaToco(ManagedChannelBuilder<?> channelBuilder){
        channel = channelBuilder.build();
        blockingStub = RouteGuideGrpc.newBlockingStub(channel);
        asyncStub = RouteGuideGrpc.newStub(channel);
    }

    // cria um canal para se conectar com o servidor
    private ManagedChannelBuilder<?> criaConexao(String ip, int porta){
        return ManagedChannelBuilder.forAddress(ip, porta).usePlaintext(true);
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


      /*try {
        response = blockingStub.sayHello(request);
      } catch (StatusRuntimeException e) {
        logger.log(Level.WARNING, "RPC failed: {0}", e.getStatus());
        return;
      }
      logger.info("Greeting: " + response.getMessage());
      try {
        response = blockingStub.sayHelloAgain(request);
      } catch (StatusRuntimeException e) {
        logger.log(Level.WARNING, "RPC failed: {0}", e.getStatus());
        return;
      }
      logger.info("Greeting: " + response.getMessage());*/
    }
}
