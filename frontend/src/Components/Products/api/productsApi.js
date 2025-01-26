const BASE_URL = "http://127.0.0.1:5000/api/products/";
const COMPANIES_URL = "http://127.0.0.1:5000/api/companies/"

const getAuthHeaders = () => {
  const token = localStorage.getItem("jwt");
  if (!token) throw new Error("No token found");
  return {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`,
  };
};

export const fetchProducts = async () => {
  try {
    const response = await fetch(BASE_URL, {
      method: "GET",
      headers: getAuthHeaders(),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(
        `Error fetching products: ${response.status} - ${errorData.error || response.statusText}`
      );
    }

    return await response.json();
  } catch (error) {
    console.error("Fetch Products Error:", error.message);
    throw error; // Rethrow para que el consumidor maneje el error
  }
};

export const createProduct = async (product) => {
  const response = await fetch(BASE_URL, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(product),
  });
  if (!response.ok) throw new Error("Error creating product");
  return await response.json();
};

export const updateProduct = async (id, product) => {
  const response = await fetch(`${BASE_URL}${id}`, {
    method: "PUT",
    headers: getAuthHeaders(),
    body: JSON.stringify(product),
  });
  if (!response.ok) throw new Error("Error updating product");
  return await response.json();
};

export const deleteProduct = async (id) => {
  const response = await fetch(`${BASE_URL}${id}`, {
    method: "DELETE",
    headers: getAuthHeaders(),
  });
  if (!response.ok) throw new Error("Error deleting product");
};


export const fetchCompanies = async () => {
    try {
      const response = await fetch(COMPANIES_URL, {
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
      throw error; 
    }
  };