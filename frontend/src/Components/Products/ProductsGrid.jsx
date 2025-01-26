import React from 'react';
import ProductItem from './ProductItem';

const ProductsGrid = ({ products, onDelete, onEdit }) => {
  return (
    <div className="products-row">
      {products.map((product) => (
        <ProductItem
          key={product.id}
          product={product}
          onDelete={onDelete}
          onEdit={onEdit}
        />
      ))}
    </div>
  );
};

export default ProductsGrid;
