/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package emRede;

/**
 *
 * @author Daniel
 */
public class teste {

    public static void main(String[] args){
        Conexao c = new Conexao("192.168.0.105", 5555, "Daniel", null);
        c.Jogar();
    }
}
