/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package interfaces;

import javax.swing.ImageIcon;

/**
 *
 * @author Daniel
 */
public class IconeControle {

    private final ImageIcon icone;
    private boolean resolvido;

    public IconeControle(ImageIcon icone) {
        this.icone = icone;
        resolvido = false;
    }

    public ImageIcon getIcone() {
        return icone;
    }

    public boolean isResolvido() {
        return resolvido;
    }

    public void setResolvido(){
        resolvido = true;
    }
}
