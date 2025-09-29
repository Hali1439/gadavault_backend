# 🛡️ GadaVault Backend API

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat&logo=python)
![Django](https://img.shields.io/badge/Django-5.0-092E20?style=flat&logo=django)
![DRF](https://img.shields.io/badge/DRF-REST_Framework-red?style=flat)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/Auth-JWT-yellow?style=flat)
![Railway](https://img.shields.io/badge/Deployed%20on-Railway-0B3A48?style=flat&logo=railway)

---

## 🌟 Project Overview: GadaVault API

The GadaVault Backend is the secure, authoritative data layer for the GadaVault e-commerce application. It is a **RESTful API** built with **Django REST Framework (DRF)**, designed for scalability, security, and performance.

### Rationale & Purpose

As a core demonstration of backend competence, this project adheres to the **API-first** principle:
1.  **Decoupling:** Separate business logic from presentation, allowing the frontend (Next.js) to scale independently.
2.  **Security:** Implements **stateless authentication** using JWT tokens to secure all protected resources.
3.  **Scalability:** Utilizes PostgreSQL for robust data management and implements built-in pagination, search, and filtering to handle growing product catalogs efficiently.

## ✨ Key API Features

| Feature | Description | Technical Implementation |
| :--- | :--- | :--- |
| **Authentication** | Secure user registration, login, and profile access. | **JWT (djangorestframework_simplejwt)** |
| **API Documentation** | Interactive, self-documenting API schema. | **drf-yasg (Swagger UI & Redoc)** |
| **Core Resources** | Comprehensive CRUD operations for all e-commerce data. | **Designers, Products, Users** endpoints |
| **Data Efficiency** | Limits data payload size for faster client loading. | **Pagination & Search Filters** |
| **Configuration** | Separation of settings from the codebase. | **python-decouple** (12-Factor App) |

## 🛠️ Technology Stack

* **Framework:** Django 5.x
* **API:** Django REST Framework (DRF)
* **Database:** PostgreSQL
* **Security:** JWT (JSON Web Tokens)
* **Deployment:** Railway / Render
* **Documentation:** drf-yasg (Swagger/Redoc)
* **Configuration:** python-decouple

---

## 🚀 Getting Started (Local Development)

### Prerequisites

* Python 3.11+
* PostgreSQL
* pip

### Installation

1.  **Clone the repository:**
    

2.  **Create and activate a virtual environment:**
    

### Environment Configuration

This project requires sensitive settings to be stored in environment variables.

1.  Create a file named `.env` in the project root:

2.  **Security Note:** The `DJANGO_SECRET_KEY` must be generated, unique, and **NEVER** committed to Git. Use the key generation method discussed previously.

### Database Setup and Run

1.  **Run Migrations:**

2.  **Create a Superuser (Optional):**

3.  **Run the Server:**
    
## 👤 Author & Acknowledgements

* Author: Halima Muktar
* Program: ALX ProDev Backend (Nexus Project)