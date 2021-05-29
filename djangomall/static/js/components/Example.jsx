import React, {useState} from 'react'

export function Example() {
    const [count, setcount] = useState(0);
    const [name, setname] = useState();

    return(
        <div>
            <p className="fa fa-cart-plus" aria-hidden="true"></p>
            <p>{count}  {name}</p>
            <input type="ratio" name="product" value="product1" onClick={(e) => setname(e.target.value)}/>
            <input type="ratio" name="product" value="product2" onClick={(e) => setname(e.target.value)}/>
            <button className="btn btn-success" onClick={() => setcount(count+1)}>
                Add to cart
            </button>

        </div>
    )
}