# Backend Developer (Intern) – Project Assignment

## 📌 Overview

This project is a **Scalable REST API with Authentication & Role-Based Access**, built as part of the **Backend Developer Intern assignment**. The backend is implemented using **FastAPI**, with secure JWT-based authentication, role-based authorization (admin vs user), and CRUD APIs for a secondary entity (Posts). A **basic React frontend** is included to interact with and test the APIs.

The project is designed with **security, scalability, and clean architecture** in mind.

---

## 🛠 Tech Stack

### Backend

* **Python 3.10+**
* **FastAPI** (REST APIs)
* **SQLAlchemy** (ORM)
* **PostgreSQL / SQLite** (Database)
* **JWT (OAuth2)** Authentication
* **Passlib + Bcrypt** (Password hashing)
* **Pydantic** (Validation & schemas)
* **Uvicorn** (ASGI server)

### Frontend

* **React.js**
* **Tailwind CSS** (basic styling)
* **Fetch API** for backend integration

---

## ✨ Features Implemented

### ✅ Authentication & Authorization

* User registration with hashed passwords
* Secure login using JWT tokens
* Role-based access control:

  * **Admin**: Manage users, view all users
  * **User**: Access own data & posts
* JWT-protected routes

### ✅ CRUD APIs (Secondary Entity – Posts)

* Create Post
* Read Posts
* Update Post (owner/admin only)
* Delete Post (owner/admin only)

### ✅ API Design & Validation

* RESTful API structure
* Proper HTTP status codes
* Input validation using Pydantic schemas
* Centralized error handling

### ✅ API Versioning

* All APIs are versioned using `/api/v1`

### ✅ Logging

* Application-level logging using Python `logging`
* Logs written to `app.log`
* Logs include authentication events, API access, and errors

### ✅ API Documentation

* Swagger UI available at:

  ```
  http://localhost:8000/docs
  ```

### ✅ Frontend Integration

* Register & Login UI
* JWT-based protected dashboard
* Perform CRUD operations on Posts
* Display API success & error messages

---

## 📂 Project Structure

```
backend/
│── app/
│   ├── main.py
│   ├── database.py
│   ├── model/
│   │   └── models.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── user.py
│   │   └── post.py
│   ├── schema/
│   │   └── schemas.py
│   ├── core/
│   │   ├── oauth2.py
│   │   ├── utils.py
│   │   └── logging_config.py
│── app.log
│── requirements.txt
│── README.md

frontend/
│── src/
│── package.json
│── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Backend Setup

```bash
# Create virtual environment
python -m venv venv

# Activate environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload
```

Backend will be available at:

```
http://localhost:8000
```

---

### 2️⃣ Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend will run at:

```
http://localhost:3000
```

---

## 🔐 Authentication Flow

1. User registers via `/api/v1/users/create`
2. Password is securely hashed
3. JWT token is generated on login
4. Token is required in `Authorization: Bearer <token>` header
5. Protected routes validate JWT & role

---

## 📊 Scalability Considerations

* Modular FastAPI project structure for easy feature expansion
* Stateless JWT authentication enables horizontal scaling
* Database indexing on frequently queried fields (email, foreign keys)
* Role-based access control via dependency injection
* Logging system for observability & debugging
* Ready for Dockerization & cloud deployment
* Optional future enhancements:

  * Redis caching
  * Microservices split
  * Rate limiting

---

## 📑 Logs

* Application logs are stored in `app.log`
* Logs include:

  * Authentication events
  * API access logs
  * Error & exception traces
