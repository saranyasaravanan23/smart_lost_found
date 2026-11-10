# Smart Lost & Found Management System

## Project Description

The Smart Lost & Found Management System is a Python and MySQL-based application used to manage lost and found item reports.

It allows users to register, log in, report lost and found items, search for items, and automatically identify possible matches.

An Admin Dashboard is provided to manage all item reports.

## Technologies Used

- Python
- MySQL
- MySQL Connector
- Object-Oriented Programming
- SQL

## Project Features

1. User Registration
2. User Login
3. Lost Item Registration
4. Found Item Registration
5. Search Items by Name and Category
6. Automatic Item Matching
7. Update Item Status
8. Delete Item Reports
9. Admin Dashboard
10. View All Item Reports

## Database Tables

### 1. lf_users

Stores user information:
- user_id
- username
- email
- password
- role

### 2. lf_items

Stores lost and found item information:
- item_id
- user_id
- item_name
- category
- location
- description
- report_type
- status
- report_date

## Item Status

- OPEN
- MATCHED
- CLAIMED
- CLOSED

## Project Structure

```text
smart_lost_found/
│
├── main.py
├── database.py
├── models.py
├── matching.py
├── requirements.txt
└── README.md
```

## Installation

### Step 1: Create Virtual Environment

```bash
python -m venv venv
```

### Step 2: Activate Virtual Environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Required Package

```bash
python -m pip install mysql-connector-python
```

### Step 4: Configure MySQL

Create the required database tables and configure the MySQL connection details in `database.py`.

### Step 5: Run the Application

```bash
python main.py
```

## Admin Dashboard

The Admin Dashboard provides the following operations:

- View All Item Reports
- Search Item
- Update Item Status
- Delete Report
- Logout

## Conclusion

This project provides an efficient way to manage lost and found items using Python and MySQL. It demonstrates database connectivity, CRUD operations, automatic item matching, input validation and exception handling.
