import React, {useState, useEffect} from 'react';

export const ProductPrice = function ({ id }) {
    const [price, setPrice] = useState();
    const [variants, setVarients] = useState([]);
    const [initialized, setInitialized] = useState(false);

    useEffect(() => {
        if (!initialized){
            fetch(`/api/products/${id}`)
                .then(response => response.json())
                .then(data =>{
                    setPrice(data.price);
                    setVarients(data.variants);
                });
            setInitialized(true);
        }
    });

    return (
        <div>
            <var className="price h3 text-warning">
                <span>{ price }</span>
            </var>
        <dl className="dlist-inline">
            <dd>
            {/* 迭代返回的商品变种 */}
            { variants.map(variant => (
                <label key={ variant.id } className="form-check form-check-inline">
                    {/* 价格写到单选按钮的 dataset，绑定 onClick 事件，点击设置价格 */}
                    <input className="form-check-input" type="radio" name="product_variant"
                           value={ variant.sku }
                           data-price={ variant.base_price }
                           onClick={ (e) => setPrice(e.target.dataset.price) }
                    />
                    <span className="form-check-label">{ variant.name }</span>
                </label>
            ) ) }
            </dd>
        </dl>
    </div>
    );
};