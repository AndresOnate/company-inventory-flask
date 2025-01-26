import React from 'react';

const CompanyItem = ({ company, onDelete, onEdit }) => {
  return (
    <div className="company-item">
      <h2>{company.name}</h2>
      <p><strong>NIT:</strong> {company.nit}</p>
      <p><strong>Address:</strong> {company.address}</p>
      <p><strong>Phone:</strong> {company.phone}</p>
      <div className="company-header">
        <button onClick={() => onEdit(company.nit)}>✏️</button>
        <button onClick={() => onDelete(company.nit)}>🗑️</button>
      </div>
    </div>
  );
};

export default CompanyItem;