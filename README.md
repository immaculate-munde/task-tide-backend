# 🌊 TaskTide - School Management API

TaskTide is a modern backend API for managing academic cohorts, designed with a community-first approach similar to Discord servers. 

Unlike traditional rigid school portals, TaskTide allows Class Representatives to create dynamic "Servers" (classrooms) where students can join via unique codes, access units (subjects), and collaborate in assignment groups.

## 🚀 Key Features

* **Role-Based Access Control (RBAC):** Distinct permissions for Admins, Class Reps, Lecturers, and Students.
* **Server System:** Dynamic classroom creation with unique 6-digit join codes.
* **Authentication:** Secure User Registration and Login using **JWT (JSON Web Tokens)**.
* **Scalable Architecture:** Built on Django REST Framework with a normalized database schema.

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Framework:** Django & Django REST Framework (DRF)
* **Authentication:** SimpleJWT
* **Database:** SQLite (Dev) / PostgreSQL (Prod)

---

## 💻 Local Development Setup

Follow these steps to set up the project locally on your machine.

### 1. Clone the Repository

```bash
git clone <https://github.com/immaculate-munde/task-tide-backend.git>
cd task-tide-backend
```

### 2. Create a Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

**Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**

```bash
python3 -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations

Set up the local SQLite database and apply the custom user models.

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (Admin)

To access the Django Admin panel:

```bash
python manage.py createsuperuser
```

### 6. Run the Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

---

## 🔗 API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register a new user (Student/ClassRep/Lecturer) |
| POST | `/api/auth/login/` | Login and receive Access/Refresh Tokens |
| POST | `/api/auth/token/refresh/` | Refresh an expired Access Token |

### Servers (Classrooms)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/servers/` | List servers you have created or joined |
| POST | `/api/servers/` | Create a new server (Class Reps only) |
| POST | `/api/servers/join/` | Join a server using a 6-digit code |

---

## 👤 Author

**Immaculate Munde** - [GitHub Profile](https://github.com/immaculate-munde)