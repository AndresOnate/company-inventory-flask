import React from "react";
import { BrowserRouter as Router, Route, Routes,  Navigate } from "react-router-dom";
import Login from "./Components/Login/Login";
import Companies from "./Components/Companies/Companies";
import Products from "./Components/Products/Products";
import InventoryView from "./Components/Inventory/Inventory";

function App() {
    return (
        <Router>
            <Routes basename="/">
            <Route path="/" element={<Navigate to="/login" />} />
            <Route path="/login" element={<Login />} />
            <Route path="/empresas" element={<Companies />} />
            <Route path="/productos" element={<Products />} />
            <Route path="/inventario" element={<InventoryView />} />
            </Routes>
        </Router>
    );
}

export default App;
