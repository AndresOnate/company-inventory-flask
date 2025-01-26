import React, { useState, useEffect, useCallback } from 'react';
import { Link, useNavigate } from 'react-router-dom'; 
import { jwtDecode } from "jwt-decode";
import CompanyForm from './CompanyForm';
import CompaniesGrid from './CompaniesGrid';
import {
  fetchCompanies,
  createCompany,
  updateCompany,
  deleteCompany,
} from './api/companiesApi';
import './Companies.css';

const Companies = () => {
  const [companies, setCompanies] = useState([]);
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

  const loadCompanies = useCallback(async () => {
    try {
      const data = await fetchCompanies();
      setCompanies(data);
    } catch (error) {
      console.error('Error loading companies:', error);
    }
  }, []);

  useEffect(() => {
    loadCompanies();
  }, [loadCompanies]);

  const addOrUpdateCompany = async (company) => {
    try {
      if (editingId !== null) {
        const updatedCompany = await updateCompany(editingId, company);
        setCompanies((prev) =>
          prev.map((c) => (c.nit === editingId ? updatedCompany : c))
        );
        setEditingId(null);
      } else {
        const newCompany = await createCompany(company);
        setCompanies((prev) => [...prev, newCompany]);
      }
    } catch (error) {
      console.error('Error saving company:', error);
    }
  };

  const deleteCompanyHandler = async (nit) => {
    try {
      await deleteCompany(nit);
      setCompanies((prev) => prev.filter((company) => company.nit !== nit));
    } catch (error) {
      console.error('Error deleting company:', error);
    }
  };

  const editCompanyHandler = (nit) => {
    setEditingId(nit);
  };

  return (
    <div className="companies-view">
      <div className="header-container">
        <div>Empresas</div>
        <div className="header-buttons">
          <Link to="/productos">
            <button>Productos</button>
          </Link>
          <Link to="/inventario">
            <button>Inventario</button>
          </Link>
        </div>
      </div>
      <div className="content-container">
        <CompanyForm
          onSave={addOrUpdateCompany}
          editingCompany={companies.find((c) => c.nit === editingId)}
        />
        <CompaniesGrid
          companies={companies}
          onDelete={deleteCompanyHandler}
          onEdit={editCompanyHandler}
        />
      </div>
    </div>
  );
};

export default Companies;
