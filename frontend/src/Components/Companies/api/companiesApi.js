const BASE_URL = "http://127.0.0.1:5000/api/companies/";

const getAuthHeaders = () => {
  const token = localStorage.getItem("jwt");
  if (!token) throw new Error("No token found");
  return {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`,
  };
};

export const fetchCompanies = async () => {
  try {
    const response = await fetch(BASE_URL, {
      method: "GET",
      headers: getAuthHeaders(),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(
        `Error fetching companies: ${response.status} - ${errorData.error || response.statusText}`
      );
    }

    return await response.json();
  } catch (error) {
    console.error("Fetch Companies Error:", error.message);
    throw error; // Rethrow para que el consumidor maneje el error
  }
};

export const createCompany = async (company) => {
  const response = await fetch(BASE_URL, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(company),
  });
  if (!response.ok) throw new Error("Error creating company");
  return await response.json();
};

export const updateCompany = async (id, company) => {
  const response = await fetch(`${BASE_URL}/${id}`, {
    method: "PUT",
    headers: getAuthHeaders(),
    body: JSON.stringify(company),
  });
  if (!response.ok) throw new Error("Error updating company");
  return await response.json();
};

export const deleteCompany = async (id) => {
  const response = await fetch(`${BASE_URL}/${id}`, {
    method: "DELETE",
    headers: getAuthHeaders(),
  });
  if (!response.ok) throw new Error("Error deleting company");
};

export const fetchActiveCompanies = async () => {
  const response = await fetch(`${BASE_URL}/active`, {
    headers: getAuthHeaders(),
  });
  if (!response.ok) throw new Error("Error fetching active companies");
  return response.json();
};
