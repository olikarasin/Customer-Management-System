# Customer Management System

## Description

The **Customer Management System** is a Django-based web application that helps businesses efficiently manage their customers, contracts, timesheets, and payments. The application includes a user authentication system for secure access to customer and admin views, contract management, timesheet tracking, and reporting functionalities.

The system allows users to:
- Manage customer profiles and associated contracts
- Track customer timesheets, including working hours and approvals
- Generate and review reports
- Administer customer payments and contract statuses

## Features

- User authentication for admins and customers
- Timesheet management with approval workflows
- Contract management with easy updates and tracking
- Reporting functionality for customer hours and contract status
- Secure password storage and login system
- PostgreSQL database support for efficient data handling

## Installation

### Prerequisites

- Python 3.x
- PostgreSQL
- Django
- Virtual environment (optional, but recommended)

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/olikarasin/Customer-Management-System
    ```

2. Navigate to the project directory:

    ```bash
    cd CmsApp
    ```

3. Create and activate a virtual environment:

    ```bash
    python -m venv myvenv
    source myvenv/bin/activate  # On Windows, use myvenv\Scripts\activate
    ```

4. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Configure the PostgreSQL database:
   - Create a PostgreSQL database and user.
   - Update the `DATABASES` setting in `Cms/settings.py` with your database credentials.

6. Apply migrations:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

7. Create a superuser to access the admin interface:

    ```bash
    python manage.py createsuperuser
    ```

8. Run the development server:

    ```bash
    python manage.py runserver
    ```

9. Access the application at `http://127.0.0.1:8000`.

## Usage

- **Admin Dashboard**: Accessible to admins to manage customers, timesheets, and contracts.
- **Customer Dashboard**: Customers can view their contracts and timesheets.

### Admin Functionality:

- Add and update customer profiles
- View and approve timesheets
- Manage contract details and status
- Generate reports for customer activities

### Customer Functionality:

- View their active contracts and timesheets
- Monitor time worked and report issues with timesheets

## License

This project is licensed under the MIT License. See the LICENSE file for details.
