import React, { useState, useEffect, useCallback } from 'react';
import ProductForm from './ProductForm';
import ProductsGrid from './ProductsGrid';
import { Link, useNavigate } from 'react-router-dom';
import { jwtDecode } from "jwt-decode";
import { fetchProducts, createProduct, updateProduct, deleteProduct, fetchCompanies } from './api/productsApi';
import './Products.css';

const Products = () => {
  const [products, setProducts] = useState([]);
  const [companies, setCompanies] = useState([]); // Agregado estado para compañías
  const [editingId, setEditingId] = useState(null);
  const navigate = useNavigate();


  useEffect(() => {
    const token = localStorage.getItem("jwt"); 
    if (!token) {
      navigate("/login"); 
      return;
    }

    try {
      const decodedToken = jwtDecode(token); 
      const roles = decodedToken.roles;
      if (!roles.includes("ADMIN")) {
        navigate("/inventario"); 
      }
    } catch (error) {
      console.error('Error al verificar el rol:', error);
      navigate("/login");
    }
  }, [navigate]);

  const loadProducts = useCallback(async () => {
    try {
      const data = await fetchProducts();
      setProducts(data);
    } catch (error) {
      console.error('Error loading products:', error);
    }
  }, []);

  const loadCompanies = useCallback(async () => {
    try {
      const data = await fetchCompanies(); // Suponiendo que tienes un endpoint para obtener las compañías
      setCompanies(data);
    } catch (error) {
      console.error('Error loading companies:', error);
    }
  }, []);

  useEffect(() => {
    loadProducts();
    loadCompanies();
  }, [loadProducts, loadCompanies]);

  const addOrUpdateProduct = async (product) => {
    try {
      let updatedProduct;
  
      if (editingId !== null) {
        updatedProduct = await updateProduct(editingId, product);
        console.log('updatedProduct:', updatedProduct);
        if (updatedProduct && updatedProduct.id) {
          setProducts((prev) =>
            prev.map((p) => (p.id === editingId ? updatedProduct : p))
          );
        } else {
          console.error('El producto actualizado no tiene el formato esperado.');
        }

        setEditingId(null);
      } else {
        const newProduct = await createProduct(product);

        if (newProduct && newProduct.id) {
          setProducts((prev) => [...prev, newProduct]);
        } else {
          console.error('El producto creado no tiene el formato esperado.');
        }
      }
    } catch (error) {
      console.error('Error al guardar el producto:', error);
    }
  };

  const deleteProductHandler = async (id) => {
    try {
      await deleteProduct(id);
      setProducts((prev) => prev.filter((product) => product.id !== id));
    } catch (error) {
      console.error('Error deleting product:', error);
    }
  };

  const editProductHandler = (id) => {
    setEditingId(id);
  };

  return (
    <div className="products-view">
      <div className="header-container">
        <div>Productos</div>
        <div className="header-buttons">
          <Link to="/empresas">
            <button>Empresas</button>
          </Link>
          <Link to="/inventario">
            <button>Inventario</button>
          </Link>
        </div>
      </div>
      <div className="content-container">
        <ProductForm
          onSave={addOrUpdateProduct}
          editingProduct={products.find((p) => p.id === editingId)}
          companies={companies} // Pasamos las compañías al formulario
        />
        <ProductsGrid
          products={products}
          onDelete={deleteProductHandler}
          onEdit={editProductHandler}
        />
      </div>
    </div>
  );
};

export default Products;
