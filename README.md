# E-Commerce API

A RESTful E-Commerce API built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**. This project demonstrates authentication, shopping cart management, checkout, order management, database migrations, automated testing, logging, and Docker containerization.

---

## Features

### Authentication

* User registration
* JWT authentication
* Role-based authorization (Admin & User)

### Product Management

* Create product (Admin)
* Update product (Admin)
* Delete product (Admin)
* Get all products
* Get product details
* Filter products by category

### Shopping Cart

* Add product to cart
* Update cart quantity
* Remove product from cart
* View shopping cart

### Checkout

* Checkout a single product
* Checkout all products in cart
* Automatic stock deduction
* Order creation

### Order

* Get all user orders
* Get order details

---

## Tech Stack

* FastAPI
* SQLAlchemy ORM
* PostgreSQL
* Alembic
* JWT Authentication
* Pytest
* Docker
* Docker Compose
* Logging

---

## Project Structure

```text
ecommerce_api/
│
├── app/
│   ├── database/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── logger.py
│   └── main.py
│
├── utility/
├── alembic/
├── seeds/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## API Endpoints

### Authentication

| Method | Endpoint    | Description           |
| ------ | ----------- | --------------------- |
| POST   | `/register` | Register new user     |
| POST   | `/login`    | Login and receive JWT |

### Product

| Method | Endpoint                       | Description              |
| ------ | ------------------------------ | ------------------------ |
| POST   | `/product`                     | Create product (Admin)   |
| GET    | `/product`                     | Get all products         |
| GET    | `/product/{id_product}`        | Get product detail       |
| GET    | `/product/category/{category}` | Get products by category |
| PUT    | `/product/{id_product}`        | Update product (Admin)   |
| DELETE | `/product/{id_product}`        | Delete product (Admin)   |

### Cart

| Method | Endpoint                     | Description              |
| ------ | ---------------------------- | ------------------------ |
| POST   | `/cart/product`              | Add product to cart      |
| GET    | `/cart`                      | Get shopping cart        |
| PUT    | `/cart/product/{id_product}` | Update cart quantity     |
| DELETE | `/cart/product/{id_product}` | Remove product from cart |

### Checkout

| Method | Endpoint                 | Description                   |
| ------ | ------------------------ | ----------------------------- |
| POST   | `/checkout/{id_product}` | Checkout a single product     |
| POST   | `/checkout`              | Checkout all products in cart |

### Order

| Method | Endpoint            | Description      |
| ------ | ------------------- | ---------------- |
| GET    | `/order`            | Get user orders  |
| GET    | `/order/{id_order}` | Get order detail |

---

## Running with Docker

### 1. Clone Repository

```bash
git clone <repository-url>
cd ecommerce_api
```

### 2. Start Containers

```bash
docker compose up --build
```

### 3. Run Database Migration

```bash
docker compose exec app alembic upgrade head
```

### 4. Seed Initial Data

```bash
docker compose exec app python -m seeds.seeds
```

### 5. Open Swagger UI

```
http://localhost:8000/docs
```

---

## Running Without Docker

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Migration

```bash
alembic upgrade head
```

### Seed Database

```bash
python -m seeds.seeds
```

### Start FastAPI

```bash
uvicorn app.main:app --reload
```

---

## Testing

Run all tests:

```bash
pytest
```

---

## Logging

Application events are logged for important operations such as:

* User registration
* User login
* Product creation
* Product update
* Product deletion
* Checkout

---

## Database Migration

Alembic is used for schema versioning.

Create a migration:

```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:

```bash
alembic upgrade head
```

---

## Future Improvements

* Refresh Token Authentication
* Payment Gateway Integration (Stripe)
* Image Upload
* Email Verification
* CI/CD Pipeline
* Frontend Integration

---

## Author

**Muhammad Nur Muliadi**

Backend Developer | Python | FastAPI | PostgreSQL
