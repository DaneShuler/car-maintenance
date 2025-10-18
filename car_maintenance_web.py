from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import MySQLConnection

app = Flask(__name__)
app.secret_key = "your_secret_key"


def connect_to_db() -> MySQLConnection:
    """
    Connects to the MySQL database.

    Returns:
        MySQLConnection: The database connection object.
    """
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="RZX*Pcb$i5hVNySJg6^R#%^D",  # MySQL root password
        database="CarMaintenanceDB",
    )


# ---- Main Menu ----
@app.route("/")
def main_menu() -> str:
    """
    Displays the main menu for the Car Maintenance Tracker application.

    Returns:
        str: Rendered HTML template for the main menu.
    """
    return render_template("index.html")


# ---- View Submenu ----
# ---- View Submenu ----
@app.route("/view_menu")
def view_menu() -> str:
    """
    Displays the View submenu.

    Returns:
        str: Rendered HTML template for the view submenu.
    """
    return render_template("view_menu.html")


@app.route("/view/<string:record_type>")
def view_records(record_type: str) -> str:
    """
    Displays records of the specified type.

    Args:
        record_type (str): The type of records to view (vehicles, parts, maintenance).

    Returns:
        str: Rendered HTML template with the records.
    """
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)

    try:
        # Fetch records based on type
        if record_type == "vehicles":
            cursor.execute("SELECT * FROM Vehicle")
        elif record_type == "parts":
            cursor.execute("SELECT * FROM PartsInventory")
        elif record_type == "maintenance":
            cursor.execute("SELECT * FROM Maintenance")
        else:
            flash("Invalid record type!")
            return redirect(url_for("view_menu"))

        # Fetch the records and render the appropriate page
        records = cursor.fetchall()
        return render_template(
            f"view_records.html", records=records, record_type=record_type.capitalize()
        )
    finally:
        cursor.close()
        db.close()


@app.route("/view/parts_by_vehicle", methods=["GET", "POST"])
def view_parts_by_vehicle():
    """
    Displays parts associated with a specific vehicle.

    Returns:
        str: Rendered HTML template showing parts by vehicle.
    """
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        # Fetch selected vehicle parts
        vehicle_id = request.form.get("vehicle_id")
        cursor.execute(
            "SELECT * FROM PartsInventory WHERE VehicleID = %s", (vehicle_id,)
        )
        parts = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template(
            "view_parts_by_vehicle.html", parts=parts, vehicle_id=vehicle_id
        )

    # Fetch all vehicles for dropdown
    cursor.execute("SELECT VehicleID, Make, Model, Year FROM Vehicle")
    vehicles = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("view_parts_by_vehicle.html", vehicles=vehicles)


@app.route("/view/maintenance_by_vehicle", methods=["GET", "POST"])
def view_maintenance_by_vehicle():
    """
    Displays maintenance records for a specific vehicle.

    Returns:
        str: Rendered HTML template showing maintenance records by vehicle.
    """
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        # Fetch selected vehicle maintenance records
        vehicle_id = request.form.get("vehicle_id")
        cursor.execute("SELECT * FROM Maintenance WHERE VehicleID = %s", (vehicle_id,))
        maintenance_records = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template(
            "view_maintenance_by_vehicle.html",
            maintenance_records=maintenance_records,
            vehicle_id=vehicle_id,
        )

    # Fetch all vehicles for dropdown
    cursor.execute("SELECT VehicleID, Make, Model, Year FROM Vehicle")
    vehicles = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("view_maintenance_by_vehicle.html", vehicles=vehicles)


# ---- Add Submenu ----
@app.route("/add_menu")
def add_menu() -> str:
    """
    Displays the Add submenu.

    Returns:
        str: Rendered HTML template for the Add submenu.
    """
    return render_template("add_menu.html")


@app.route("/add/<string:record_type>", methods=["GET", "POST"])
def add_record(record_type: str) -> str:
    """
    Handles the addition of new records.

    Args:
        record_type (str): The type of record to add (vehicles, parts, maintenance).

    Returns:
        str: Rendered HTML template for the form or redirects after addition.
    """
    db = connect_to_db()
    cursor = db.cursor()

    if request.method == "POST":
        try:
            if record_type == "vehicles":
                make = request.form["make"]
                model = request.form["model"]
                year = request.form["year"]
                vin = request.form["vin"]
                cursor.execute(
                    "INSERT INTO Vehicle (Make, Model, Year, VIN) VALUES (%s, %s, %s, %s)",
                    (make, model, year, vin),
                )
            elif record_type == "parts":
                part_name = request.form["part_name"]
                quantity = request.form["quantity"]
                vehicle_id = request.form.get("vehicle_id", None)
                cursor.execute(
                    "INSERT INTO PartsInventory (PartName, Quantity, VehicleID) VALUES (%s, %s, %s)",
                    (part_name, quantity, vehicle_id),
                )
            elif record_type == "maintenance":
                vehicle_id = request.form["vehicle_id"]
                date_of_service = request.form["date_of_service"]
                type_of_service = request.form["type_of_service"]
                mileage = request.form["mileage"]
                next_service_date = request.form.get("next_service_date", None)
                next_service_mileage = request.form.get("next_service_mileage", None)
                cursor.execute(
                    "INSERT INTO Maintenance (VehicleID, DateOfService, TypeOfService, Mileage, NextServiceDate, NextServiceMileage) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (
                        vehicle_id,
                        date_of_service,
                        type_of_service,
                        mileage,
                        next_service_date,
                        next_service_mileage,
                    ),
                )
            else:
                flash("Invalid record type!")
                return redirect(url_for("add_menu"))

            db.commit()
            flash(f"{record_type.capitalize()} added successfully!")
            return redirect(url_for("add_menu"))
        except mysql.connector.Error as err:
            flash(f"Error adding record: {err.msg}")
        finally:
            cursor.close()
            db.close()

    # Fetch data needed for the forms (e.g., vehicle list for parts/maintenance dropdowns)
    if record_type == "parts" or record_type == "maintenance":
        cursor.execute("SELECT VehicleID, Make, Model, Year FROM Vehicle")
        vehicles = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template(
            "add_record.html", record_type=record_type.capitalize(), vehicles=vehicles
        )

    return render_template("add_record.html", record_type=record_type.capitalize())


@app.route("/add/vehicles", methods=["GET", "POST"])
def add_vehicle():
    """
    Handles adding a new vehicle to the database.

    Returns:
        str: Rendered HTML template for adding a vehicle.
    """
    if request.method == "POST":
        db = connect_to_db()
        cursor = db.cursor()

        try:
            # Get form data
            make = request.form["make"]
            model = request.form["model"]
            year = request.form["year"]
            vin = request.form["vin"]

            # Insert into database
            cursor.execute(
                "INSERT INTO Vehicle (Make, Model, Year, VIN) VALUES (%s, %s, %s, %s)",
                (make, model, year, vin),
            )
            db.commit()
            flash("Vehicle added successfully!")
            return redirect(url_for("add_menu"))
        except mysql.connector.Error as err:
            flash(f"Error: {err}")
        finally:
            cursor.close()
            db.close()

    return render_template("add_record.html", record_type="Vehicle")


@app.route("/add/parts", methods=["GET", "POST"])
def add_part():
    """
    Handles adding a new part to the database.

    Returns:
        str: Rendered HTML template for adding a part.
    """
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        cursor_insert = db.cursor()
        try:
            # Get form data
            part_name = request.form["part_name"]
            quantity = request.form["quantity"]
            vehicle_id = request.form.get("vehicle_id", None)

            # Insert into database
            cursor_insert.execute(
                "INSERT INTO PartsInventory (PartName, Quantity, VehicleID) VALUES (%s, %s, %s)",
                (part_name, quantity, vehicle_id),
            )
            db.commit()
            flash("Part added successfully!")
            return redirect(url_for("add_menu"))
        except mysql.connector.Error as err:
            flash(f"Error: {err}")
        finally:
            cursor_insert.close()
            db.close()

    # Fetch all vehicles for the dropdown
    try:
        cursor.execute("SELECT VehicleID, Make, Model, Year FROM Vehicle")
        vehicles = cursor.fetchall()
    finally:
        cursor.close()
        db.close()

    return render_template("add_record.html", record_type="Part", vehicles=vehicles)


@app.route("/add/maintenance", methods=["GET", "POST"])
def add_maintenance():
    """
    Handles adding a new maintenance record to the database.

    Returns:
        str: Rendered HTML template for adding a maintenance record.
    """
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        cursor_insert = db.cursor()
        try:
            # Get form data
            vehicle_id = request.form["vehicle_id"]
            date_of_service = request.form["date_of_service"]
            type_of_service = request.form["type_of_service"]
            mileage = request.form["mileage"]
            next_service_date = request.form.get("next_service_date", None)
            next_service_mileage = request.form.get("next_service_mileage", None)

            # Insert into database
            cursor_insert.execute(
                """
                INSERT INTO Maintenance 
                (VehicleID, DateOfService, TypeOfService, Mileage, NextServiceDate, NextServiceMileage)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    vehicle_id,
                    date_of_service,
                    type_of_service,
                    mileage,
                    next_service_date,
                    next_service_mileage,
                ),
            )
            db.commit()
            flash("Maintenance record added successfully!")
            return redirect(url_for("add_menu"))
        except mysql.connector.Error as err:
            flash(f"Error: {err}")
        finally:
            cursor_insert.close()
            db.close()

    # Fetch all vehicles for the dropdown
    try:
        cursor.execute("SELECT VehicleID, Make, Model, Year FROM Vehicle")
        vehicles = cursor.fetchall()
    finally:
        cursor.close()
        db.close()

    return render_template(
        "add_record.html", record_type="Maintenance", vehicles=vehicles
    )


# ---- Remove Submenu ----
@app.route("/remove_menu")
def remove_menu() -> str:
    """
    Displays the Remove submenu.

    Returns:
        str: Rendered HTML template for the add submenu.
    """
    return render_template("remove_menu.html")


@app.route("/remove/<string:record_type>", methods=["GET", "POST"])
def remove_record(record_type: str):
    """
    Handles removing a record by ID.

    Args:
        record_type (str): The type of record to remove (vehicle, part, maintenance).

    Returns:
        str: Rendered HTML template for record removal or redirects after deletion.
    """
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        record_id = request.form["record_id"]
        try:
            if record_type.lower() == "vehicle":
                cursor.execute("DELETE FROM Vehicle WHERE VehicleID = %s", (record_id,))
            elif record_type.lower() == "part":
                cursor.execute(
                    "DELETE FROM PartsInventory WHERE PartID = %s", (record_id,)
                )
            elif record_type.lower() == "maintenance":
                cursor.execute(
                    "DELETE FROM Maintenance WHERE MaintenanceID = %s", (record_id,)
                )
            else:
                flash("Invalid record type!")
                return redirect(url_for("remove_menu"))

            db.commit()
            flash(f"{record_type.capitalize()} record removed successfully!")
            return redirect(url_for("remove_menu"))
        except mysql.connector.Error as err:
            flash(f"Error: {err.msg}")
        finally:
            cursor.close()
            db.close()

    # Fetch records for the dropdown menu
    try:
        if record_type.lower() == "vehicle":
            cursor.execute("SELECT VehicleID, Make, Model, Year FROM Vehicle")
        elif record_type.lower() == "part":
            cursor.execute(
                "SELECT PartID, PartName, Quantity, VehicleID FROM PartsInventory"
            )
        elif record_type.lower() == "maintenance":
            cursor.execute(
                "SELECT MaintenanceID, VehicleID, TypeOfService, DateOfService FROM Maintenance"
            )
        else:
            flash("Invalid record type!")
            return redirect(url_for("remove_menu"))

        records = cursor.fetchall()
        return render_template(
            "remove_record.html", records=records, record_type=record_type.capitalize()
        )
    finally:
        cursor.close()
        db.close()


# ---- Update Submenu ----
@app.route("/update_menu")
def update_menu() -> str:
    """
    Displays the Update submenu with options to update vehicles, parts, or maintenance records.

    Returns:
        str: Rendered HTML template for the Update submenu.
    """
    return render_template("update_menu.html")


@app.route("/update/<string:record_type>", methods=["GET", "POST"])
def update_record(record_type: str):
    """
    Handles updating a record dynamically based on the type.

    Args:
        record_type (str): The type of record to update (vehicle, part, maintenance).

    Returns:
        str: Rendered HTML template for updating the record.
    """
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        record_id = request.form["record_id"]

        if record_type.lower() == "vehicle":
            make = request.form.get("make")
            model = request.form.get("model")
            year = request.form.get("year")
            vin = request.form.get("vin")
            updates = []
            values = []
            if make:
                updates.append("Make = %s")
                values.append(make)
            if model:
                updates.append("Model = %s")
                values.append(model)
            if year:
                updates.append("Year = %s")
                values.append(year)
            if vin:
                updates.append("VIN = %s")
                values.append(vin)
            if updates:
                values.append(record_id)
                cursor.execute(
                    f"UPDATE Vehicle SET {', '.join(updates)} WHERE VehicleID = %s",
                    values,
                )

        elif record_type.lower() == "part":
            part_name = request.form.get("part_name")
            quantity = request.form.get("quantity")
            vehicle_id = request.form.get("vehicle_id")
            updates = []
            values = []
            if part_name:
                updates.append("PartName = %s")
                values.append(part_name)
            if quantity:
                updates.append("Quantity = %s")
                values.append(quantity)
            if vehicle_id:
                updates.append("VehicleID = %s")
                values.append(vehicle_id)
            if updates:
                values.append(record_id)
                cursor.execute(
                    f"UPDATE PartsInventory SET {', '.join(updates)} WHERE PartID = %s",
                    values,
                )

        elif record_type.lower() == "maintenance":
            date_of_service = request.form.get("date_of_service")
            type_of_service = request.form.get("type_of_service")
            mileage = request.form.get("mileage")
            next_service_date = request.form.get("next_service_date")
            next_service_mileage = request.form.get("next_service_mileage")
            updates = []
            values = []
            if date_of_service:
                updates.append("DateOfService = %s")
                values.append(date_of_service)
            if type_of_service:
                updates.append("TypeOfService = %s")
                values.append(type_of_service)
            if mileage:
                updates.append("Mileage = %s")
                values.append(mileage)
            if next_service_date:
                updates.append("NextServiceDate = %s")
                values.append(next_service_date)
            if next_service_mileage:
                updates.append("NextServiceMileage = %s")
                values.append(next_service_mileage)
            if updates:
                values.append(record_id)
                cursor.execute(
                    f"UPDATE Maintenance SET {', '.join(updates)} WHERE MaintenanceID = %s",
                    values,
                )

        else:
            flash("Invalid record type!")
            return redirect(url_for("update_menu"))

        db.commit()
        flash(f"{record_type.capitalize()} record updated successfully!")
        return redirect(url_for("update_menu"))

    # Fetch records for the form
    try:
        if record_type.lower() == "vehicle":
            cursor.execute("SELECT * FROM Vehicle")
        elif record_type.lower() == "part":
            cursor.execute("SELECT * FROM PartsInventory")
        elif record_type.lower() == "maintenance":
            cursor.execute("SELECT * FROM Maintenance")
        else:
            flash("Invalid record type!")
            return redirect(url_for("update_menu"))

        records = cursor.fetchall()
        return render_template(
            "update_record.html", records=records, record_type=record_type.capitalize()
        )
    finally:
        cursor.close()
        db.close()


if __name__ == "__main__":
    app.run(debug=True)
