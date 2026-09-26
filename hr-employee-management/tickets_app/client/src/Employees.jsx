import { useEffect, useState } from "react";
import api from "./api";


function Employees() {

    const [employees, setEmployees] = useState([]);


    const getEmployees = async () => {

        try {

            const response = await api.get("/users");

            setEmployees(response.data);

        } catch (error) {

            alert("Could not load employees");

        }
    };


    useEffect(() => {

        getEmployees();

    }, []);


    const deleteEmployee = async (id) => {

        if (!window.confirm("Delete this employee?")) {
            return;
        }


        try {

            await api.delete(`/users/${id}`);

            alert("Employee deleted");

            getEmployees();

        } catch (error) {

            alert("Delete failed");

        }
    };


    return (

        <div className="container mt-4">

            <h2>
                Employees
            </h2>


            <div className="card p-3 mt-3">

                <table className="table">

                    <thead>

                        <tr>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Phone</th>
                            <th>Department</th>
                            <th>Role</th>
                            <th>Action</th>
                        </tr>

                    </thead>


                    <tbody>

                        {employees.map((employee) => (

                            <tr key={employee.id}>

                                <td>
                                    {employee.name}
                                </td>

                                <td>
                                    {employee.email}
                                </td>

                                <td>
                                    {employee.phone}
                                </td>

                                <td>
                                    {employee.department}
                                </td>

                                <td>
                                    {employee.role}
                                </td>

                                <td>

                                    <button
                                        className="btn btn-danger btn-sm"
                                        onClick={() =>
                                            deleteEmployee(
                                                employee.id
                                            )
                                        }
                                    >
                                        Delete
                                    </button>

                                </td>

                            </tr>

                        ))}

                    </tbody>

                </table>

            </div>

        </div>
    );
}


export default Employees;
