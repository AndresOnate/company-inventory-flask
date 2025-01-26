import axios from "axios";

/**
 * Realiza la solicitud de inicio de sesión al backend.
 * @param {string} email - Correo electrónico del usuario.
 * @param {string} password - Contraseña del usuario.
 * @returns {Promise<string>} - Retorna el JWT si la solicitud es exitosa.
 */
export const login = async (email, password) => {
    try {
        const response = await axios.post("http://127.0.0.1:5000/api/auth", { email, password });
        const { token } = response.data;
        localStorage.setItem("jwt", token);
        return token;
    } catch (error) {
        // Mejorar el manejo del error para obtener un mensaje más específico
        const errorMessage = error.response?.data?.message || "Invalid email or password. Please try again.";
        throw new Error(errorMessage);
    }
};

