\# ShopAPI - E-Commerce REST API



A backend E-Commerce REST API built with Python, Django REST Framework and PostgreSQL.



\## Features



\- JWT Authentication

\- User Registration and Login

\- User Profile API

\- Product Management

\- Category Management

\- Shopping Cart

\- Order Creation and Order History

\- Automatic Stock Reduction

\- Search and Filtering

\- Pagination

\- PostgreSQL Database

\- Swagger / OpenAPI Documentation

\- RESTful API Architecture



\## Tech Stack



\- Python

\- Django

\- Django REST Framework

\- PostgreSQL

\- Simple JWT

\- Django Filter

\- drf-spectacular

\- Swagger / OpenAPI

\- Git \& GitHub



\## Project Structure



```text

ShopAPI-E-Commerce-REST-API/

│

├── accounts/

├── products/

├── cart/

├── orders/

├── config/

├── manage.py

├── requirements.txt

├── .env

├── .gitignore

└── README.md

API Endpoints

Authentication

POST /api/auth/register/

POST /api/auth/login/

POST /api/auth/token/refresh/

GET  /api/auth/profile/

Products

GET    /api/products/

POST   /api/products/

GET    /api/products/{id}/

PUT    /api/products/{id}/

PATCH  /api/products/{id}/

DELETE /api/products/{id}/

Categories

GET    /api/categories/

POST   /api/categories/

GET    /api/categories/{id}/

PUT    /api/categories/{id}/

PATCH  /api/categories/{id}/

DELETE /api/categories/{id}/

Cart

GET    /api/cart/

POST   /api/cart/

PATCH  /api/cart/{id}/

DELETE /api/cart/{id}/

Orders

GET  /api/orders/

POST /api/orders/

GET  /api/orders/{id}/

Swagger Documentation



After starting the Django server, open:



http://127.0.0.1:8000/api/docs/



Swagger provides an interactive interface for testing the API endpoints.



Installation



Clone the repository:



git clone https://github.com/DevKumarBhatt/ShopAPI-E-Commerce-REST-API.git

cd ShopAPI-E-Commerce-REST-API



Create a virtual environment:



python -m venv venv



Activate it on Windows:



.\\venv\\Scripts\\Activate.ps1



Install dependencies:



pip install -r requirements.txt

Environment Variables



Create a .env file in the project root:



DB\_NAME=shopapi\_db

DB\_USER=postgres

DB\_PASSWORD=your\_password

DB\_HOST=localhost

DB\_PORT=5432

DJANGO\_SECRET\_KEY=your\_secret\_key



Never commit the .env file to GitHub.



Database Setup



Run migrations:



python manage.py makemigrations

python manage.py migrate



Create an admin user:



python manage.py createsuperuser



Start the development server:



python manage.py runserver

Order Workflow



The order workflow follows these steps:



User logs in using JWT authentication.

User adds products to the cart.

User creates an order.

The API calculates the order total.

Product stock is reduced automatically.

The cart is cleared after successful order creation.

The order is stored in PostgreSQL.

User can view order history and order details.

API Testing



The API can be tested using:



Swagger UI

Postman

Browser for GET endpoints

Django Admin

Database



PostgreSQL is used as the primary database.



The project uses Django ORM for database operations and transaction handling for order creation.



Security

JWT-based authentication

Password hashing using Django authentication

Environment variables for database credentials

.env excluded from Git

Authenticated API access using DRF permissions

Future Improvements

Razorpay payment integration

Product image storage

Wishlist

User reviews and ratings

Email notifications

Redis and Celery

Docker deployment

React frontend

Cloud deployment

Seller and delivery modules



Author



Dev Kumar Bhatt



MCA | Python Developer | Data Analyst



GitHub: https://github.com/DevKumarBhatt



LinkedIn: https://linkedin.com/in/dev-kumar-bhatt-b74540347

