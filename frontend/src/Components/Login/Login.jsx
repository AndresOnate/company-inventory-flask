import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import './Login.css';
import { login } from "../utils/authService"; 

const Login = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate(); 

    const handleLogin = async () => {
        if (!email || !password) {
            setError("Please fill in both fields.");
            return;
        }

        try {
            const token  = await login(email, password); 
            setError(""); 
            console.log("token:", token);
            const decodedToken = jwtDecode(token); 
            const roles = decodedToken.roles;
            if (roles.includes("ADMIN")) {
                navigate("/empresas");
            } else {
                navigate("/inventario");
            }

        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <div className="login-page"> 
            <div className="container">
                <div className="header">
                    <div className="text">Login</div>
                    <div className="underline"></div>
                </div>
                <div className="inputs">
                    <div className="input">
                        <input
                            type="email"
                            placeholder="Email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </div>
                    <div className="input">
                        <input
                            type="password"
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </div>
                    <div className="submit-container">
                        <div className="submit" onClick={handleLogin}>
                            Login
                        </div>
                    </div>
                </div>
                {error && <div className="error">{error}</div>}
            </div>
        </div>
    );
};

export default Login;
