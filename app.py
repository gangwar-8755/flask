from flask import Flask, request, jsonify
import database

app = Flask(__name__)





@app.route("/")
def home():
    return "Employee Management API is running"


# Get all employees
@app.route("/employees", methods=["GET"])
def get_employees():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(employees)


# Get employee by ID
@app.route("/employees/<int:id>", methods=["GET"])
def get_employee(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM employees WHERE id = %s",
        (id,)
    )

    employee = cursor.fetchone()

    cursor.close()
    conn.close()

    if employee:
        return jsonify(employee)

    return jsonify({"message": "Employee not found"}), 404


# Add employee
@app.route("/employees", methods=["POST"])
def add_employee():

    data = request.json

    name = data["name"]
    email = data["email"]
    department = data["department"]
    salary = data["salary"]

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO employees
        (name, email, department, salary)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (name, email, department, salary)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Employee added successfully"
    }), 201


# Update employee
@app.route("/employees/<int:id>", methods=["PUT"])
def update_employee(id):

    data = request.json

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        UPDATE employees
        SET name=%s,
            email=%s,
            department=%s,
            salary=%s
        WHERE id=%s
    """

    cursor.execute(
        query,
        (
            data["name"],
            data["email"],
            data["department"],
            data["salary"],
            id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Employee updated successfully"
    })


# Delete employee
@app.route("/employees/<int:id>", methods=["DELETE"])
def delete_employee(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM employees WHERE id=%s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Employee deleted successfully"
    })


if __name__ == "__main__":
    app.run(debug=True)