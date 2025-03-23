# Library Management System

A Django-based Library Management System that allows admins to perform CRUD operations on books and provides a student view to list all books.

---

## Features

- **Admin Operations:**

  - Signup: Create a new admin account.
  - Login: Authenticate admins using email and password.
  - Logout: Invalidate the admin's authentication token.

- **Book Management:**

  - Create: Add new books.
  - Read: Retrieve a list of all books.
  - Update: Modify book details.
  - Delete: Remove a book record.

- **Student View:**
  - View a list of all available books.

---

## Technical Specifications

- **Framework:** Django 5.0
- **API:** Django REST Framework (DRF)
- **Database:** MySQL
- **Authentication:** Token-based authentication for admin endpoints.
- **Front-End:** Optional (Django templates used for the student view).

---

## Setup Instructions

### Prerequisites

- Python 3.8+
- MySQL
- Django
- Django REST Framework

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/library-management-system.git
   cd library-management-system
   ```

2. **Set Up a Virtual Environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Database:**

   - Create a MySQL database named library_db.

   - Update the database settings in settings.py:

   ```python
       DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'library_db',
           'USER': 'root',
           'PASSWORD': 'yourpassword',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

5. **Apply Migrations:**

   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser:**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server:**

   ```bash
   python manage.py runserver

   ```

8. **Access the Application:**
   - Admin Interface: http://127.0.0.1:8000/admin/
   - API Endpoints: http://127.0.0.1:8000/api/
   - Student View: http://127.0.0.1:8000/

## API Endpoints

    **Admin Operations**

        -   Signup: POST /api/admin/signup/

        -   Login: POST /api/admin/login/

        -   Logout: POST /api/admin/logout/

    **Book Management**

        -   List Books: GET /api/books/

        -   Add Book: POST /api/books/add/

        -   Update Book: PUT /api/books/update/<uuid:pk>/

        -   Delete Book: DELETE /api/books/delete/<uuid:pk>/

## Assumptions

    -   Admins are uniquely identified by their email
    -   Books by ISBN
    -   The student view is read-only and does not require authentication.
