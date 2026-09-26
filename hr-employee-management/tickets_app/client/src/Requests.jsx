import { useEffect, useState } from "react";
import api from "./api";


function Requests() {

    const [requests, setRequests] = useState([]);

    const [form, setForm] = useState({
        title: "",
        description: "",
        category: "Leave",
        status: "Pending",
        user: ""
    });


    const getRequests = async () => {

        const response = await api.get("/requests");

        setRequests(response.data);
    };


    useEffect(() => {

        getRequests();

    }, []);


    const createRequest = async () => {

        try {

            await api.post("/requests", form);

            alert("Request created");

            setForm({
                title: "",
                description: "",
                category: "Leave",
                status: "Pending",
                user: ""
            });

            getRequests();

        } catch (error) {

            alert("Request creation failed");

        }
    };


    return (

        <div className="container mt-4">

            <h2>
                HR Service Requests
            </h2>


            <div className="card p-4 mt-3">

                <input
                    className="form-control mb-2"
                    placeholder="Request title"
                    value={form.title}
                    onChange={(e) =>
                        setForm({
                            ...form,
                            title: e.target.value
                        })
                    }
                />


                <textarea
                    className="form-control mb-2"
                    placeholder="Description"
                    value={form.description}
                    onChange={(e) =>
                        setForm({
                            ...form,
                            description: e.target.value
                        })
                    }
                />


                <select
                    className="form-select mb-2"
                    value={form.category}
                    onChange={(e) =>
                        setForm({
                            ...form,
                            category: e.target.value
                        })
                    }
                >

                    <option value="Leave">
                        Leave
                    </option>

                    <option value="Salary">
                        Salary
                    </option>

                    <option value="Attendance">
                        Attendance
                    </option>

                    <option value="Other">
                        Other
                    </option>

                </select>


                <input
                    className="form-control mb-2"
                    placeholder="Employee name"
                    value={form.user}
                    onChange={(e) =>
                        setForm({
                            ...form,
                            user: e.target.value
                        })
                    }
                />


                <button
                    className="btn btn-primary"
                    onClick={createRequest}
                >
                    Create Request
                </button>

            </div>


            <div className="mt-4">

                {requests.map((request) => (

                    <div
                        className="card p-3 mb-2"
                        key={request.id}
                    >

                        <h5>
                            {request.title}
                        </h5>

                        <p>
                            {request.description}
                        </p>

                        <p>
                            Employee: {request.user}
                        </p>

                        <span>
                            Category: {request.category}
                        </span>

                        <span>
                            Status: {request.status}
                        </span>

                    </div>

                ))}

            </div>

        </div>
    );
}


export default Requests;
