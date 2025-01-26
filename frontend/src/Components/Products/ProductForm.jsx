import React, { useState, useEffect } from 'react';

const ProductForm = ({ onSave, editingProduct, companies }) => {
  const [form, setForm] = useState({
    code: '',
    name: '',
    description: '',
    price: '',
    quantity: '',  // Agregado campo quantity
    companyNit: '', 
  });

  useEffect(() => {
    if (editingProduct) {
      setForm({
        code: editingProduct.code,
        name: editingProduct.name,
        description: editingProduct.description,
        price: editingProduct.price,
        quantity: editingProduct.quantity,  // Ajustado para editar productos existentes
        companyNit: editingProduct.companyNit,
      });
    }
  }, [editingProduct]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Se ajusta para enviar todos los campos requeridos por el backend
    onSave({
      code: form.code,
      name: form.name,
      description: form.description, // Cambiado 'features' a 'description' para coincidir con el backend
      price: form.price,
      quantity: form.quantity,  // Asegurarse de que quantity se pase
      company_nit: form.companyNit, 
    });
    setForm({
      code: '',
      name: '',
      description: '',
      price: '',
      quantity: '',  // Reiniciar quantity
      companyNit: '', 
    });
  };

  return (
    <form className="product-form" onSubmit={handleSubmit}>
      <input
        name="code"
        value={form.code}
        onChange={handleChange}
        placeholder="Product Code"
        required
      />
      <input
        name="name"
        value={form.name}
        onChange={handleChange}
        placeholder="Product Name"
        required
      />
      <textarea
        name="description"
        value={form.description}
        onChange={handleChange}
        placeholder="Description"
        required
      />
      <input
        name="price"
        type="number"
        value={form.price}
        onChange={handleChange}
        placeholder="Price"
        required
      />
      <input
        name="quantity"
        type="number"
        value={form.quantity}
        onChange={handleChange}
        placeholder="Quantity"
        required
      />
      <select
        name="companyNit"
        value={form.companyNit}
        onChange={handleChange}
        required
      >
        <option value="">Select a Company</option>
        {companies.map((company) => (
          <option key={company.nit} value={company.nit}>
            {company.name}
          </option>
        ))}
      </select>
      <button type="submit">
        {editingProduct ? 'Update Product' : 'Add Product'}
      </button>
    </form>
  );
};

export default ProductForm;
