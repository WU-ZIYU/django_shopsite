//alert("Hello");
import React, {useState} from 'react'
import {ProductPrice} from "./components/ProductPrice";
import ReactDom from 'react-dom'
import {ShoppingCart} from "./components/ShoppingCart";

//import {Example} from "./components/Example";
//document.addEventListener('DOMContentLoaded', (event) => {
//    ReactDom.render(<Example/>, document.getElementById('app'))
//});

document.addEventListener('DOMContentLoaded', (event) => {
    if (document.getElementById('product_price')){
        var element = document.getElementById('product_price');
        var productId = element.dataset.productId;
        ReactDom.render(<ProductPrice id={ productId } />, document.getElementById('product_price'));
    }

    //if (document.getElementById('shopping_cart')){
    //    ReactDom.render(<ShoppingCart />, document.getElementById('shopping_cart'));
    //}
});