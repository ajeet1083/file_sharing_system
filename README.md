# file_sharing_system
# Django Secure File Sharing System

This is a secure file-sharing system built with Django REST framework. It supports two types of users: Ops Users and Client Users. Ops Users can upload files, while Client Users can download files securely.

## Features

- Ops Users can upload files (pptx, docx, xlsx).
- Client Users can download files via secure encrypted URLs.
- Email verification for Client Users.

## Requirements

- Python 3.8+
- Django 3.2+
- Django REST framework
- PostgreSQL or SQLite (for development)
- `django-allauth` for user authentication and email verification
- `django-rest-framework-simplejwt` for JWT authentication

## Setup Instructions

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/file_sharing_system.git
    cd file_sharing_system
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the database:**

    ```sh
    python manage.py migrate
    ```

5. **Create a superuser:**

    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server:**

    ```sh
    python manage.py runserver
    ```

## Running Tests

To run the tests, use the following command:

```sh
python manage.py test
