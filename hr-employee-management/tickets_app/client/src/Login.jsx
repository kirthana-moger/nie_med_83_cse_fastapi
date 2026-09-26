import { useState } from "react";
import api from "./api";

function Login({ onLogin }) {

    const [form, setForm] = useState({
        username: "",
        password: ""
    });


    const login = async () => {

        try {

            const response = await api.post(
                "/login",
                form
            );

            if (response.status === 200) {

                alert("Login successful");

                onLogin();
            }

        } catch (error) {

            alert(
                error.response?.data?.detail ||
                "Login failed"
            );
        }
    };


    return (

        <div className="container mt-5">

            <div
                className="card p-4 mx-auto"
                style={{ maxWidth: "500px" }}
            >

                <h2>HR Management System</h2>


                <label className="form-label">
                    Username
                </label>

                <input
                    className="form-control mb-3"
                    value={form.username}
                    onChange={(e) =>
                        setForm({
                            ...form,
                            username: e.target.value
                        })
                    }
                />


                <label className="form-label">
                    Password
                </label>

                <input
                    type="password"
                    className="form-control mb-3"
                    value={form.password}
                    onChange={(e) =>
                        setForm({
                            ...form,
                            password: e.target.value
                        })
                    }
                />


                <button
                    className="btn btn-primary"
                    onClick={login}
                >
                    Login
                </button>

            </div>

        </div>
    );
}

export default Login;
