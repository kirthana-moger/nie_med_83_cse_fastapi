import { useState } from "react";
import api from "./api";

function Register() {

    const [form, setForm] = useState({
        username: "",
        password: "",
        name: "",
        email: "",
        phone: "",
        department: "",
        role: ""
    });


    const register = async () => {

        try {

            const response = await api.post(
                "/users",
                form
            );

            if (response.status === 201) {

                alert("User created successfully");

                setForm({
                    username: "",
                    password: "",
                    name: "",
                    email: "",
                    phone: "",
                    department: "",
                    role: ""
                });
            }

        } catch (error) {

            alert(
                error.response?.data?.detail ||
                "User creation failed"
            );
        }
    };


    return (
        <div className="container mt-4">

            <div
                className="card p-4 mx-auto"
                style={{ maxWidth: "500px" }}
            >

                <h2>Create User</h2>


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


                <label className="form-label">
                    Name
                </label>

                <input
                    className="form-control mb-3"
                    value={form.name}
                    onChange={(e) =>
                        setForm({
                            ...form,
                            name: e.target.value
                        })
                    }
                />


                <label className="form-label">
                    Email
                </label>

                <input
                    className="form-control mb-3"
                    value={form.email}
                    onChange={(e) =>
                        setForm({
                            ...form,
                            email: e.target.value
                        })
                    }
                />


                <label className="form-label">
                    Phone
                </label>

                <input
                    className="form-control mb-3"
                    value={form.phone}
                    onChange={(e) =>
                        setForm({
                            ...form,
                            phone: e.target.value
                        })
                    }
                />


                <label className="form-label">
                    Department
                </label>

                <select
                    className="form-select mb-3"
                    value={form.department}
                    onChange={(e) =>
                        setForm({
                            ...form,
                            department: e.target.value
                        })
                    }
                >
                    <option value="">Select Department</option>
                    <option value="HR">HR</option>
                    <option value="IT">IT</option>
                    <option value="Finance">Finance</option>
                    <option value="Sales">Sales</option>
                </select>


                <label className="form-label">
                    Role
                </label>

                <select
                    className="form-select mb-3"
                    value={form.role}
                    onChange={(e) =>
                        setForm({
                            ...form,
                            role: e.target.value
                        })
                    }
                >
                    <option value="">Select Role</option>
                    <option value="Employee">Employee</option>
                    <option value="Engineer">Engineer</option>
                    <option value="Lead">Lead</option>
                    <option value="HR Manager">HR Manager</option>
                    <option value="Admin">Admin</option>
                </select>


                <button
                    className="btn btn-primary"
                    onClick={register}
                >
                    Create User
                </button>

            </div>

        </div>
    );
}

export default Register;
