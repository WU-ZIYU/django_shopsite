import React, {useEffect, useState} from 'react';

export const ShoppingCart = function () {
    const [initialied, setInitialized] = useState(false);
    const [cartLines, setCartLines] = useState([]);
    const headers = {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": window.csrf
    };

    useEffect(() => {
        if (!initialied) {
            fetch("/api/cartlines/", {headers, credentials: "include"})
                .then(response => response.json())
                .then(data => {
                    //console.log(data);
                    setCartLines(data);
                })
        }
        setInitialized(true);
    });

    const handleQuantity = (e, cartLineId) => {
        fetch(`/api/cartlines/${cartLineId}/`, {
            headers: headers,
            method: "PATCH",
            body: JSON.stringify({quantity: e.target.value})
        }).then(response => response.json()).catch(error => alert("Error"))
            .then(data => {
                if (data) {
                    const editedCartLines = cartLines.map(cartLine => {
                        if (cartLine.id == cartLineId) {
                            cartLine = data;
                        }
                        return cartLine;
                    });
                    setCartLines(editedCartLines);
                }
            });
    };

    const deleteCartLine = (e, cartLineId) => {
        e.preventDefault();
        fetch(`/api/cartlines/${cartLineId}/`, {
            headers: headers,
            method: "DELETE",
            body: JSON.stringify({ quantity: e.target.value })
        }).then(response => {
            if (response.status == 204){
                const editedLines = cartLines.filter(cartLine => {
                    return cartLine.id = cartLineId;
                });
                setCartLines(editedLines);
            }
        })
    };

    return (
        <div className="row">
            <div className="col-sm-9">
                <h4 className="subtitle-doc">Shopping cart</h4>
                <div className="card">
                    <table className="table table-hover shopping-cart-wrap">
                        <thead className="text-muted">
                            <tr>
                                <th scope="col">
                                    Product
                                </th>
                                <th scope="col" width="120">
                                    Quantity
                                </th>
                                <th scope="col" width="120">
                                    Price
                                </th>
                                <th scope="col" className="text-right" width="200">
                                    Action
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            {cartLines.map(cartLine => {
                                return (
                                    <tr key={cartLine.id}>
                                        <td>
                                            <figure className="media">
                                                <div className="img-wrap mr-3">
                                                    <img src={cartLine.product_variant_details.images}
                                                         className="img-thumbnail img-sm"/>
                                                </div>
                                                <figcaption className="media-body">
                                                    <h6 className="title text-truncate"></h6>
                                                        <dl className="dlist-inline small">
                                                            <dt>Product variant</dt>
                                                            <dd>
                                                                {cartLine.product_variant_details.product_name}
                                                                <small className="ml-1">
                                                                    {cartLine.product_variant.name}
                                                                </small>
                                                            </dd>
                                                        </dl>
                                                        <dl className="dlist-inline small">
                                                            <dt>SKU: </dt>
                                                            <dd>{cartLine.product_variant_details.sku}</dd>
                                                        </dl>
                                                </figcaption>
                                            </figure>
                                        </td>
                                        <td>
                                            <input
                                                type="number"
                                                name="quantity"
                                                className="form-control"
                                                value={cartLine.quantity}
                                                onChange={e => handleQuantity(e, cartLine.id)}
                                            />
                                        </td>
                                        <td>
                                            <div className="price-wrap">
                                                <var className="price">{cartLine.total}</var>
                                            </div>
                                        </td>
                                        <td className="text-right">
                                            <a href=""
                                               onClick={e => deleteCartLine(e, cartLine.id)}
                                               className="btn btn-outline-danger">
                                                {" "}
                                                ×{" "}
                                            </a>
                                        </td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    )
};

