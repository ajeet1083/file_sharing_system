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



Postman Collection
A Postman collection is included in this repository for easy API testing.

Importing the Collection
Download the Postman collection file (file_sharing_system_postman_collection.json) from the root of this repository.
Open Postman.
Click on the "Import" button.
Select the downloaded file_sharing_system_postman_collection.json file and click "Open".
Using the Collection
Ensure your Django server is running locally or on a production server.
Open the imported collection in Postman.
Set the environment variables (if any) required for the API requests.
Execute the requests to interact with the file-sharing system.
Deployment
To deploy this application to a production environment, follow these steps:

Configure the settings for production:

Update the ALLOWED_HOSTS setting with your domain name.
Configure the database settings for your production database.
Set up email backend settings for sending verification emails.
Ensure DEBUG is set to False.
Set up a production-ready server:

Use a web server like Nginx or Apache to serve your application.
Use Gunicorn as the application server.
Secure your application:

Use HTTPS for secure communication.
Set up proper security settings like SECURE_HSTS_SECONDS, SECURE_SSL_REDIRECT, and SESSION_COOKIE_SECURE.
Run the production server:

sh
Copy code
gunicorn file_sharing_system.wsgi:application
Monitor the application:

Set up logging and monitoring for your application to ensure it runs smoothly in production.