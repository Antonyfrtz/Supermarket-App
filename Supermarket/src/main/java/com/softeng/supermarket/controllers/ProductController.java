package com.softeng.supermarket.controllers;

import ch.qos.logback.core.model.Model;
import com.softeng.supermarket.foreign_keys.SupermarketProductKey;
import com.softeng.supermarket.models.Product;
import com.softeng.supermarket.models.Stock;
import com.softeng.supermarket.repositories.ProductRepository;
import com.softeng.supermarket.repositories.StockRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.Optional;


@Controller
public class ProductController {
    @Autowired
    ProductRepository productRepository;

    @GetMapping("/product")
    public String productPage(Model model){
        //model.addAttribute("product",new Product());
        return "productPage";
    }


    @GetMapping(value = "/productPage")
    public String singleproductPage(@RequestParam(value = "id") String id){

        return "productPage";

    }

    // For testing
    // curl http://localhost:8080/add -d name=Γαλα -d desc=Γαλα ελληνικό -d catID=Γαλακτοκομικά -d price=3
    @PostMapping(path="/add") // Map ONLY POST Requests
    public @ResponseBody String addNewProduct (@RequestParam String name, @RequestParam String desc, @RequestParam String catID, @RequestParam String price, @RequestParam String imageSource) {
        // @ResponseBody means the returned String is the response, not a view name
        // @RequestParam means it is a parameter from the GET or POST request

        Product p = new Product();
        p.setName(name);
        p.setDescription(desc);
        p.setCategoryID(catID);
        p.setPrice(price);
        p.setImageSource(imageSource);
        productRepository.save(p);
        return "Saved";
    }


    @GetMapping(path = "/all", produces = "application/json")
    public @ResponseBody Iterable<Product> getAllProducts(@RequestParam(value = "type", required = false) String productType) {
        Iterable<Product> products;

        if (productType == null || productType.equals("all")) {
            products = productRepository.findAll();
        } else {
            products = productRepository.findByCategoryID(productType);
        }

        return products;
    }


    @GetMapping(path="/all/prods", produces = "application/json")
    public @ResponseBody Iterable<Product> getPriceProducts(@RequestParam(required = false) String price) {
        if (price != null) {
            // Retrieve products with price less than or equal to the specified price
            return productRepository.findByPriceLessThanEqual(price);
        } else {
            // Return all products
            return productRepository.findAll();
        }
    }

    @GetMapping(path = "/allbyid", produces = "application/json")
    public @ResponseBody Iterable<Product> getAllProductsById(@RequestParam(value = "id") String productId) {
       // Iterable<Product> products;

        return productRepository.findById(productId);
        //return "redirect:/productPage";
    }

    // http://localhost:8080/stock?supermarket_id=1&product_id=1
    @Autowired
    StockRepository stockRepository;
    @GetMapping(path="/stock", produces = "application/json")
    public @ResponseBody Stock getStock(@RequestParam(value = "supermarket_id") Long supermarketId, @RequestParam(value = "product_id" ) Long productId){
        SupermarketProductKey key = new SupermarketProductKey(supermarketId, productId);
        Optional<Stock> optionalProduct = stockRepository.findById(key);
        if (optionalProduct.isPresent()) {
           return optionalProduct.get();
            // Handle the retrieved SupermarketProduct entity
        } else {
            return null;
            // SupermarketProduct not found
        }
    }

}
