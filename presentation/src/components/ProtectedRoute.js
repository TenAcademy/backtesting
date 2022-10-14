import React from "react";
import { Navigate, Outlet } from "react-router-dom";

const ProtectedRoute = () => {

    const isAuthenticated = localStorage.getItem("user");


    return (
        isAuthenticated ? <Outlet/>: <Navigate to="/login"/>
       
    )
}

export default ProtectedRoute