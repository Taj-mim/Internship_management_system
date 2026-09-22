# Internship Management System

A web-based **Internship Management System** built with **Django and Python** to simplify and organize the internship management process. The system is designed to connect students and companies while providing a centralized platform for managing internship-related activities.

## 📌 Overview

The Internship Management System provides a structured way to manage internship information and interactions between students, companies, and administrators.

The project focuses on applying Django's web development architecture, database management, authentication, CRUD operations, and role-based application workflows.

## ✨ Features

* Student management
* Company management
* Internship management
* Internship application management
* User authentication
* Role-based access
* Admin dashboard
* CRUD operations
* Database-driven application
* Responsive web interface

## 🏗️ Architecture

The project follows Django's **MVT (Model–View–Template)** architecture.

### Model

Handles the application's data structure and database interactions.

### View

Contains the application logic and processes user requests.

### Template

Provides the user interface and presents data to users.

### Application Flow

```text
User
  ↓
URL
  ↓
View
  ↓
Model
  ↓
Database
  ↓
View
  ↓
Template
  ↓
User
```

## 🛠️ Technologies Used

* **Python**
* **Django**
* **HTML5**
* **CSS3**
* **JavaScript**
* **SQL / Database**
* **Git & GitHub**

## 📂 Project Structure

```text
Internship_management_system/
│
├── internship/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   └── ...
│
├── manage.py
├── requirements.txt
└── README.md
```

> The exact structure may vary depending on the current project configuration.

## 🚀 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Taj-mim/Internship_management_system.git
```

### 2. Navigate to the project

```bash
cd Internship_management_system
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Apply migrations

```bash
python manage.py migrate
```

### 7. Create a superuser

```bash
python manage.py createsuperuser
```

### 8. Run the development server

```bash
python manage.py runserver
```

Open the application in your browser:

```text
http://127.0.0.1:8000/
```

## 🗄️ Database

The application uses Django's database framework to store and manage internship-related data.

Database configuration can be found in:

```text
settings.py
```

For local development, configure the database according to your environment before running migrations.

## 🔐 Authentication & Authorization

The system provides user authentication and access control for different types of users.

This helps ensure that users can access the functionality appropriate to their role.

## 🎯 Project Objectives

The main objectives of this project are:

* To digitize internship management.
* To simplify internship-related workflows.
* To provide centralized management of students, companies, and internships.
* To practice Django-based backend development.
* To implement database-driven web application development.
* To gain practical experience with authentication, CRUD operations, and MVC/MVT concepts.

## 📚 Learning Outcomes

Through this project, I practiced:

* Django project and app structure
* Models and database relationships
* Views and URL routing
* Django templates
* Forms and validation
* Authentication and authorization
* CRUD operations
* Database migrations
* Static files management
* Git and GitHub workflow
* Deployment configuration

## 🔮 Future Improvements

Possible future improvements include:

* Email notifications
* Advanced search and filtering
* Internship recommendation system
* Application status notifications
* Company and student profile enhancements
* REST API integration
* Improved analytics and reporting

## 👩‍💻 Author

**Fatema Taj Mim**

* GitHub: [Taj-mim](https://github.com/Taj-mim)

## 📄 License

This project is developed for educational and project-learning purposes.
