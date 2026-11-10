
import hashlib
import re

from database import get_connection
from models import User
from matching import find_matching_items


# Password Hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# User Registration
def register_user():

    print("\n===== USER REGISTRATION =====")

    username = input("Enter Username: ").strip()
    email = input("Enter Email: ").strip()
    password = input("Enter Password: ").strip()

    if not username or not email or not password:
        print("All fields are required!")
        return

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        print("Invalid Email Address!")
        return

    if len(password) < 6:
        print("Password must contain at least 6 characters!")
        return

    user = User(username, email, hash_password(password))

    connection = get_connection()

    if connection is None:
        print("Database connection failed!")
        return

    cursor = connection.cursor()

    try:
        query = """
        INSERT INTO lf_users (username, email, password, role)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (user.username, user.email, user.password, user.role)
        )

        connection.commit()
        print("Registration Successful!")

    except Exception as e:
        connection.rollback()

        if "1062" in str(e):
            print("Email already registered!")
        else:
            print("Registration Error:", e)

    finally:
        cursor.close()
        connection.close()


# User Login
def login_user():

    print("\n===== USER LOGIN =====")

    email = input("Enter Email: ").strip()
    password = input("Enter Password: ").strip()

    if not email or not password:
        print("Email and Password are required!")
        return None

    connection = get_connection()

    if connection is None:
        print("Database connection failed!")
        return None

    cursor = connection.cursor(dictionary=True)

    try:
        query = """
        SELECT * FROM lf_users
        WHERE email = %s AND password = %s
        """

        cursor.execute(
            query,
            (email, hash_password(password))
        )

        user = cursor.fetchone()

        if user:
            print("\nLogin Successful!")
            print("Welcome", user["username"])
            print("Role:", user["role"])
            return user

        print("Invalid Email or Password!")
        return None

    except Exception as e:
        print("Login Error:", e)
        return None

    finally:
        cursor.close()
        connection.close()


# Automatic Item Matching
def check_matching_items(lost_item):

    connection = get_connection()

    if connection is None:
        print("Database connection failed!")
        return

    cursor = connection.cursor(dictionary=True)

    try:
        query = """
        SELECT * FROM lf_items
        WHERE report_type = 'FOUND'
        AND status = 'OPEN'
        """

        cursor.execute(query)
        found_items = cursor.fetchall()

        matches = find_matching_items(lost_item, found_items)

        if matches:
            print("\n===== AUTOMATIC MATCHING RESULT =====")
            print("Possible Match Found!")

            for item in matches:
                print("----------------------------")
                print("Found Item ID:", item["item_id"])
                print("Item Name:", item["item_name"])
                print("Category:", item["category"])
                print("Location:", item["location"])
                print("Description:", item["description"])

        else:
            print("\nNo Matching Items Found!")

    except Exception as e:
        print("Matching Error:", e)

    finally:
        cursor.close()
        connection.close()


# Lost Item Registration
def register_lost_item(user_id):

    print("\n===== LOST ITEM REGISTRATION =====")

    item_name = input("Enter Item Name: ").strip()
    category = input("Enter Category: ").strip()
    location = input("Enter Lost Location: ").strip()
    description = input("Enter Description: ").strip()

    if not item_name or not category or not location:
        print("Item Name, Category and Location are required!")
        return

    connection = get_connection()

    if connection is None:
        print("Database connection failed!")
        return

    cursor = connection.cursor()

    try:
        query = """
        INSERT INTO lf_items
        (user_id, item_name, category, location, description, report_type)
        VALUES (%s, %s, %s, %s, %s, 'LOST')
        """

        cursor.execute(
            query,
            (user_id, item_name, category, location, description)
        )

        connection.commit()
        print("Lost Item Registered Successfully!")

        lost_item = {
            "item_name": item_name,
            "category": category,
            "location": location
        }

        check_matching_items(lost_item)

    except Exception as e:
        connection.rollback()
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()


# Found Item Registration
def register_found_item(user_id):

    print("\n===== FOUND ITEM REGISTRATION =====")

    item_name = input("Enter Item Name: ").strip()
    category = input("Enter Category: ").strip()
    location = input("Enter Found Location: ").strip()
    description = input("Enter Description: ").strip()

    if not item_name or not category or not location:
        print("Item Name, Category and Location are required!")
        return

    connection = get_connection()

    if connection is None:
        print("Database connection failed!")
        return

    cursor = connection.cursor()

    try:
        query = """
        INSERT INTO lf_items
        (user_id, item_name, category, location, description, report_type)
        VALUES (%s, %s, %s, %s, %s, 'FOUND')
        """

        cursor.execute(
            query,
            (user_id, item_name, category, location, description)
        )

        connection.commit()
        print("Found Item Registered Successfully!")

    except Exception as e:
        connection.rollback()
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()


# Search Item by Name and Category
def search_item():

    print("\n===== SEARCH ITEM =====")

    item_name = input("Enter Item Name: ").strip()
    category = input("Enter Category: ").strip()

    if not item_name or not category:
        print("Item Name and Category are required!")
        return

    connection = get_connection()

    if connection is None:
        print("Database connection failed!")
        return

    cursor = connection.cursor(dictionary=True)

    try:
        query = """
        SELECT
            lf_items.item_id,
            lf_items.item_name,
            lf_items.category,
            lf_items.location,
            lf_items.description,
            lf_items.report_type,
            lf_items.status,
            lf_users.username
        FROM lf_items
        JOIN lf_users
        ON lf_items.user_id = lf_users.user_id
        WHERE LOWER(lf_items.item_name) = LOWER(%s)
        AND LOWER(lf_items.category) = LOWER(%s)
        """

        cursor.execute(query, (item_name, category))
        items = cursor.fetchall()

        if items:
            print("\n===== SEARCH RESULTS =====")

            for item in items:
                print("----------------------------")
                print("Item ID:", item["item_id"])
                print("Item Name:", item["item_name"])
                print("Category:", item["category"])
                print("Location:", item["location"])
                print("Description:", item["description"])
                print("Report Type:", item["report_type"])
                print("Status:", item["status"])
                print("Reported By:", item["username"])

        else:
            print("No Matching Items Found!")

    except Exception as e:
        print("Search Error:", e)

    finally:
        cursor.close()
        connection.close()


# Update Item Status
def update_item_status(user, is_admin=False):

    print("\n===== UPDATE ITEM STATUS =====")

    item_id = input("Enter Item ID: ").strip()

    if not item_id.isdigit():
        print("Invalid Item ID!")
        return

    print("\nAvailable Status:")
    print("1. OPEN")
    print("2. MATCHED")
    print("3. CLAIMED")
    print("4. CLOSED")

    choice = input("Select New Status: ").strip()

    status_options = {
        "1": "OPEN",
        "2": "MATCHED",
        "3": "CLAIMED",
        "4": "CLOSED"
    }

    if choice not in status_options:
        print("Invalid Status Choice!")
        return

    new_status = status_options[choice]

    connection = get_connection()

    if connection is None:
        print("Database connection failed!")
        return

    cursor = connection.cursor()

    try:
        if is_admin:
            check_query = """
            SELECT item_id FROM lf_items
            WHERE item_id = %s
            """
            cursor.execute(check_query, (int(item_id),))

        else:
            check_query = """
            SELECT item_id FROM lf_items
            WHERE item_id = %s AND user_id = %s
            """
            cursor.execute(
                check_query,
                (int(item_id), user["user_id"])
            )

        existing_item = cursor.fetchone()

        if existing_item is None:
            print("Item ID Not Found or You Cannot Update This Report!")
            return

        update_query = """
        UPDATE lf_items
        SET status = %s
        WHERE item_id = %s
        """

        cursor.execute(update_query, (new_status, int(item_id)))
        connection.commit()

        print("Item Status Updated Successfully!")
        print("New Status:", new_status)

    except Exception as e:
        connection.rollback()
        print("Status Update Error:", e)

    finally:
        cursor.close()
        connection.close()


# Delete Report
def delete_report(user, is_admin=False):

    print("\n===== DELETE ITEM REPORT =====")

    item_id = input("Enter Item ID to Delete: ").strip()

    if not item_id.isdigit():
        print("Invalid Item ID!")
        return

    connection = get_connection()

    if connection is None:
        print("Database connection failed!")
        return

    cursor = connection.cursor()

    try:
        if is_admin:
            query = """
            DELETE FROM lf_items
            WHERE item_id = %s
            """

            cursor.execute(query, (int(item_id),))

        else:
            query = """
            DELETE FROM lf_items
            WHERE item_id = %s AND user_id = %s
            """

            cursor.execute(
                query,
                (int(item_id), user["user_id"])
            )

        connection.commit()

        if cursor.rowcount > 0:
            print("Report Deleted Successfully!")
        else:
            print("Item ID Not Found or You Cannot Delete This Report!")

    except Exception as e:
        connection.rollback()
        print("Delete Error:", e)

    finally:
        cursor.close()
        connection.close()


# Admin Dashboard - View All Reports
def view_all_reports():

    print("\n===== ADMIN - ALL ITEM REPORTS =====")

    connection = get_connection()

    if connection is None:
        print("Database connection failed!")
        return

    cursor = connection.cursor(dictionary=True)

    try:
        query = """
        SELECT
            lf_items.item_id,
            lf_items.item_name,
            lf_items.category,
            lf_items.location,
            lf_items.description,
            lf_items.report_type,
            lf_items.status,
            lf_users.username,
            lf_users.email
        FROM lf_items
        JOIN lf_users
        ON lf_items.user_id = lf_users.user_id
        ORDER BY lf_items.item_id
        """

        cursor.execute(query)
        items = cursor.fetchall()

        if items:
            for item in items:
                print("----------------------------")
                print("Item ID:", item["item_id"])
                print("Item Name:", item["item_name"])
                print("Category:", item["category"])
                print("Location:", item["location"])
                print("Description:", item["description"])
                print("Report Type:", item["report_type"])
                print("Status:", item["status"])
                print("Reported By:", item["username"])
                print("User Email:", item["email"])

        else:
            print("No Item Reports Available!")

    except Exception as e:
        print("Admin View Error:", e)

    finally:
        cursor.close()
        connection.close()


# User Dashboard
def user_dashboard(user):

    while True:

        print("\n===== USER DASHBOARD =====")
        print("1. Register Lost Item")
        print("2. Register Found Item")
        print("3. Search Item")
        print("4. Update Item Status")
        print("5. Delete Report")
        print("6. Logout")

        choice = input("Enter Your Choice: ").strip()

        if choice == "1":
            register_lost_item(user["user_id"])

        elif choice == "2":
            register_found_item(user["user_id"])

        elif choice == "3":
            search_item()

        elif choice == "4":
            update_item_status(user)

        elif choice == "5":
            delete_report(user)

        elif choice == "6":
            print("Logged Out Successfully!")
            break

        else:
            print("Invalid Choice! Try Again.")


# Admin Dashboard
def admin_dashboard(user):

    while True:

        print("\n===== ADMIN DASHBOARD =====")
        print("1. View All Item Reports")
        print("2. Search Item")
        print("3. Update Item Status")
        print("4. Delete Report")
        print("5. Logout")

        choice = input("Enter Your Choice: ").strip()

        if choice == "1":
            view_all_reports()

        elif choice == "2":
            search_item()

        elif choice == "3":
            update_item_status(user, is_admin=True)

        elif choice == "4":
            delete_report(user, is_admin=True)

        elif choice == "5":
            print("Admin Logged Out Successfully!")
            break

        else:
            print("Invalid Choice! Try Again.")


# Main Menu
def main():

    while True:

        print("\n================================")
        print(" SMART LOST & FOUND MANAGEMENT ")
        print("================================")
        print("1. User Registration")
        print("2. User Login")
        print("3. Exit")

        choice = input("Enter Your Choice: ").strip()

        if choice == "1":
            register_user()

        elif choice == "2":
            user = login_user()

            if user:
                if user["role"] == "ADMIN":
                    admin_dashboard(user)
                else:
                    user_dashboard(user)

        elif choice == "3":
            print("Thank You!")
            break

        else:
            print("Invalid Choice! Try Again.")


if __name__ == "__main__":
    main()
