import React from 'react';

const ProductItem = ({ product, onDelete, onEdit }) => {
  return (
    <div className="product-item">
      <h2>{product.name}</h2>
      <p><strong>Code:</strong> {product.code}</p>
      <p><strong>Description:</strong> {product.description}</p>
      <p><strong>Price:</strong> {product.price}</p>
      <p><strong>Quantity:</strong> {product.quantity}</p>
      <p><strong>Company:</strong> {product.company_name}</p>
      <div className="product-header">
        <button onClick={() => onEdit(product.id)}>✏️</button>
        <button onClick={() => onDelete(product.id)}>🗑️</button>
      </div>
    </div>
  );
};

export default ProductItem;
