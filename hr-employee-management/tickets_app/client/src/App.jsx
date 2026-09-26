import { useState } from "react";

import Login from "./Login";
import Register from "./Register";
import Employees from "./Employees";
import Requests from "./Requests";


function App() {

    const [loggedIn, setLoggedIn] = useState(false);

    const [page, setPage] = useState("dashboard");


    if (!loggedIn) {
        return (
            <Login
                onLogin={() => setLoggedIn(true)}
            />
        );
    }


    return (
        <>

            {/* Navigation */}

            <nav className="navbar navbar-dark bg-dark px-4">

                <span className="navbar-brand">
                    HR Management System
                </span>


                <div>

                    <button
                        className="btn btn-outline-light me-2"
                        onClick={() => setPage("dashboard")}
                    >
                        Dashboard
                    </button>


                    <button
                        className="btn btn-outline-light me-2"
                        onClick={() => setPage("employees")}
                    >
                        Employees
                    </button>


                    <button
                        className="btn btn-outline-light me-2"
                        onClick={() => setPage("register")}
                    >
                        Add Employee
                    </button>


                    <button
                        className="btn btn-outline-light me-2"
                        onClick={() => setPage("requests")}
                    >
                        HR Requests
                    </button>


                    <button
                        className="btn btn-danger"
                        onClick={() => setLoggedIn(false)}
                    >
                        Logout
                    </button>

                </div>

            </nav>


            {/* Pages */}

            {page === "dashboard" && (

                <div className="container mt-4">

                    <h2>HR Dashboard</h2>

                    <p>
                        Welcome to HR Management System
                    </p>

                </div>

            )}


            {page === "employees" && (
                <Employees />
            )}


            {page === "register" && (
                <Register />
            )}


            {page === "requests" && (
                <Requests />
            )}

        </>
    );
}


export default App;

