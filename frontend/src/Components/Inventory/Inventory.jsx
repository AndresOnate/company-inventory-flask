import React, { useState, useEffect } from 'react';
import jsPDF from 'jspdf';
import 'jspdf-autotable';
import './Inventory.css';
import { Link, useNavigate } from 'react-router-dom'; 
import { jwtDecode } from "jwt-decode";

const BASE_URL = 'http://127.0.0.1:5000/api/products/';
const COMPANIES_URL = 'http://127.0.0.1:5000/api/companies/';
const EMAIL_URL = 'http://127.0.0.1:5000/api/email/';

const getAuthHeaders = () => {
  const token = localStorage.getItem('jwt');
  if (!token) throw new Error('No token found');
  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`,
  };
};

const InventoryView = () => {
  const [products, setProducts] = useState([]);
  const [selectedCompany, setSelectedCompany] = useState('');
  const [companies, setCompanies] = useState([]);
  const [email, setEmail] = useState('');
  const [isAdmin, setIsAdmin] = useState(false); // Estado para verificar si es ADMIN
  const navigate = useNavigate();

  // Verifica el rol del usuario al cargar el componente
  useEffect(() => {
    const token = localStorage.getItem('jwt');
    if (!token) {
      navigate("/login"); // Redirige al login si no hay token
      return;
    }

    try {
      const decodedToken = jwtDecode(token);
      const roles = decodedToken.roles;
      
      // Verifica si el usuario tiene el rol 'ADMIN'
      if (roles.includes("ADMIN")) {
        setIsAdmin(true); // Si tiene rol ADMIN, se actualiza el estado
      } else {
        setIsAdmin(false); // Si no tiene rol ADMIN, se ocultan los botones
      }
    } catch (error) {
      console.error('Error al verificar el rol:', error);
      navigate("/login"); // Redirige si hay error con el token
    }

    fetchCompanies();
    fetchProducts();
  }, [navigate]);

  const fetchProducts = async (nit = '') => {
    try {
      const url = nit ? `${COMPANIES_URL}${nit}/products` : BASE_URL;
      const response = await fetch(url, {
        method: 'GET',
        headers: getAuthHeaders(),
      });
      if (!response.ok) throw new Error('Error fetching products');
      const data = await response.json();
      setProducts(data);
    } catch (error) {
      console.error('Error fetching products:', error);
    }
  };

  const fetchCompanies = async () => {
    try {
      const response = await fetch(COMPANIES_URL, {
        method: 'GET',
        headers: getAuthHeaders(),
      });
      if (!response.ok) throw new Error('Error fetching companies');
      const data = await response.json();
      setCompanies(data);
    } catch (error) {
      console.error('Error fetching companies:', error);
    }
  };

  const handleCompanyChange = (e) => {
    const nit = e.target.value;
    setSelectedCompany(nit);
    fetchProducts(nit);
  };

  const generatePDF = () => {
    const doc = new jsPDF();
    doc.text('Inventory Report', 14, 10);
    doc.autoTable({
      head: [['ID', 'Code', 'Name', 'Description', 'Price', 'Quantity', 'Company NIT', 'Company Name']],
      body: products.map((product) => [
        product.id,
        product.code,
        product.name,
        product.description,
        product.price,
        product.quantity,
        product.company_nit,
        product.company_name,
      ]),
    });
    doc.save('inventory_report.pdf');
  };

  const sendEmail = async () => {
    if (!email) {
      alert('Please enter a valid email address.');
      return;
    }

    try {
      const doc = new jsPDF();
      doc.text('Inventory Report', 14, 10);
      doc.autoTable({
        head: [['ID', 'Code', 'Name', 'Description', 'Price', 'Quantity', 'Company NIT', 'Company Name']],
        body: products.map((product) => [
          product.id,
          product.code,
          product.name,
          product.description,
          product.price,
          product.quantity,
          product.company_nit,
          product.company_name,
        ]),
      });

      const pdfBlob = doc.output('blob');
      const formData = new FormData();
      formData.append('file', pdfBlob, 'inventory_report.pdf');
      formData.append('email', email);

      const response = await fetch(`${EMAIL_URL}send-email`, {
        method: 'POST',
        headers: {
          Authorization: getAuthHeaders().Authorization,
        },
        body: formData,
      });

      if (!response.ok) throw new Error('Error sending email');
      alert('Email sent successfully!');
    } catch (error) {
      console.error('Error sending email:', error);
      alert('Failed to send email.');
    }
  };

  return (
    <div className="inventory-view">
      <div className="header-container">
        <div>Inventario</div>
        <div className="header-buttons">
          {isAdmin && (
            <>
              <Link to="/empresas">
                <button>Empresas</button>
              </Link>
              <Link to="/productos">
                <button>Productos</button>
              </Link>
            </>
          )}
        </div>
      </div>
      <div className="filters">
        <select value={selectedCompany} onChange={handleCompanyChange}>
          <option value="">All Companies</option>
          {companies.map((company) => (
            <option key={company.nit} value={company.nit}>
              {company.name}
            </option>
          ))}
        </select>
      </div>
      <table className="inventory-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Code</th>
            <th>Name</th>
            <th>Description</th>
            <th>Price</th>
            <th>Quantity</th>
            <th>Company NIT</th>
            <th>Company Name</th>
          </tr>
        </thead>
        <tbody>
          {products.map((product) => (
            <tr key={product.id}>
              <td>{product.id}</td>
              <td>{product.code}</td>
              <td>{product.name}</td>
              <td>{product.description}</td>
              <td>{product.price}</td>
              <td>{product.quantity}</td>
              <td>{product.company_nit}</td>
              <td>{product.company_name}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="actions">
        <button onClick={generatePDF}>Download PDF</button>
        <div>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <button onClick={sendEmail}>Send Email</button>
        </div>
      </div>
    </div>
  );
};

export default InventoryView;
