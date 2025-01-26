import React, { useState, useEffect } from 'react';

const CompanyForm = ({ onSave, editingCompany }) => {
  const [form, setForm] = useState({
    nit: '',
    name: '',
    address: '',
    phone: '',
  });

  useEffect(() => {
    if (editingCompany) {
      setForm(editingCompany);
    }
  }, [editingCompany]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(form);
    setForm({
      nit: '',
      name: '',
      address: '',
      phone: '',
    });
  };

  return (
    <form className="company-form" onSubmit={handleSubmit}>
      <input
        name="nit"
        value={form.nit}
        onChange={handleChange}
        placeholder="NIT"
        required
      />
      <input
        name="name"
        value={form.name}
        onChange={handleChange}
        placeholder="Company Name"
        required
      />
      <input
        name="address"
        value={form.address}
        onChange={handleChange}
        placeholder="Address"
        required
      />
      <input
        name="phone"
        value={form.phone}
        onChange={handleChange}
        placeholder="Phone"
        required
      />
      <button type="submit">
        {editingCompany ? 'Update Company' : 'Add Company'}
      </button>
    </form>
  );
};

export default CompanyForm;
