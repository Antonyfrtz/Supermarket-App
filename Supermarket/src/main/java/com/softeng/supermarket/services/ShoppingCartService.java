package com.softeng.supermarket.services;

import com.softeng.supermarket.models.Cart;
import com.softeng.supermarket.models.CartItem;
import com.softeng.supermarket.models.Product;
import com.softeng.supermarket.repositories.ProductRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Service
public class ShoppingCartService {
    @Autowired
    ProductRepository productRepository;
    public Cart addToCartFirstTime(long id, Integer quantity,String storeId,Integer maxStock) throws Exception{
        try{
        Cart cart=new Cart(new ArrayList<CartItem>());
        Optional<Product> p=productRepository.findById(id);
        if(p.isPresent()) cart.addItem(new CartItem(p.get(),quantity,storeId,maxStock));
        return cart;
        }
        catch (Exception e){
            e.printStackTrace();
            return null;
        }
    }
    public Cart addToExistingCart(long id,Integer quantity,String storeId,Integer maxStock,Cart existingCart){
        Optional<Product> p=productRepository.findById(id);
        if(existingCart.containsProduct(id)){
            existingCart.updateQuantity(id,quantity);
        }
        else {
            CartItem cartItem=new CartItem(p.get(),quantity,storeId,maxStock);
            existingCart.addItem(cartItem);
        }
        return existingCart;
    }
    public Cart updateCart(Cart cart, List<CartItem> updatedCartItems) {
        for (CartItem updatedCartItem : updatedCartItems) {
            long itemId = updatedCartItem.getId();
            int quantity = updatedCartItem.getQuantity();
            if(quantity<=updatedCartItem.getMaxStock()) {
                cart.updateQuantity(itemId, quantity);
            }
        }
        // Save the updated cart in the database or perform any necessary calculations
        // For simplicity, we assume the cart object already contains the updated cart items.
        return cart;
    }

}
