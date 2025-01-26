import React from 'react';
import CompanyItem from './CompanyItem';

const CompaniesGrid = ({ companies, onDelete, onEdit }) => {
  return (
    <div className="companies-row">
      {companies.map((company) => (
        <CompanyItem
          key={company.nit}
          company={company}
          onDelete={onDelete}
          onEdit={onEdit}
        />
      ))}
    </div>
  );
};

export default CompaniesGrid;
