# Hospital Management System

![Technology](https://img.shields.io/badge/Built%20with-Python%20%7C%20Django-green)
![License](https://img.shields.io/badge/License-MIT-blue)
![Version](https://img.shields.io/badge/Version-1.0.0-orange)

## 📋 Project Description

The **Hospital Management System** is a comprehensive web-based application designed to streamline hospital operations. It provides features for managing patients, doctors, appointments, billing, and medical records, ensuring efficient communication and organization within a hospital.

## 🎯 Features

### Core Features
- **Patient Management:** Add, update, and view patient details
- **Doctor Management:** Manage doctor profiles and specializations
- **Appointment Scheduling:** Book, reschedule, and cancel appointments
- **Medical Records:** Store and access patient history and test results
- **User Roles:** Admin, Doctor, and Patient dashboards with role-specific functionalities

### Advanced Features
- **Real-time Notifications:** Email and in-app notifications for appointment updates
- **Secure Authentication:** Two-factor authentication and role-based access control
- **Password Reset:** Secure email-based password reset with strong validation
- **SEO & Accessibility:** Meta tags, OpenGraph, and accessible HTML for public pages
- **Medical History Tracking:** Comprehensive patient medical history management
- **Prescription Management:** Digital prescription creation and management
- **Billing System:** Automated billing and payment tracking
- **Reporting:** Generate detailed reports and analytics

## 🛠️ Tech Stack

### Frontend
- HTML5, CSS3, JavaScript
- Bootstrap 5
- Font Awesome Icons
- jQuery

### Backend
- Python 3.9+
- Django 4.2.6
- Django REST Framework
- Django AllAuth
- PyMySQL (MySQL database connector, no C headers needed)
- django-axes (login attempt limiting)
- phonenumbers (phone number validation)

### Database
- MySQL 8.0+

### Additional Tools
- Gunicorn (WSGI Server)
- Whitenoise (Static Files)
- Pillow (Image Processing)
- Django Debug Toolbar
- Django Crispy Forms

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- Git
- MySQL Server 8.0+

### Installation

1. Clone the repository:
```bash
git clone https://github.com/abdelrahman-a99/Hospital-Management-System.git
cd hospital-management-system
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```
> **Note:** On Windows, you do NOT need to install MySQL C/C++ headers. The project uses PyMySQL, a pure Python MySQL client.

4. Set up MySQL database:
```bash
mysql -u root -p
CREATE DATABASE hospital_management;
CREATE USER 'hospital_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON hospital_management.* TO 'hospital_user'@'localhost';
FLUSH PRIVILEGES;
```

5. Set up environment variables:
```bash
# Create a .env file in the project root with the following content:
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=hospital
DB_USER=hospital_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

# Security settings (for production, set these to True)
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SECURE_SSL_REDIRECT=False
```

6. Run migrations:
```bash
python manage.py migrate
```

7. Create superuser:
```bash
python manage.py createsuperuser
```

8. Run development server:
```bash
python manage.py runserver
```

### Development Setup

1. Install development dependencies:
```bash
pip install -r requirements.txt
```

2. Run tests:
```bash
python manage.py test
```

3. Check code style:
```bash
flake8
black .
```

## 📚 Documentation

- [API Documentation](docs/api.md)
- [User Guide](docs/user-guide.md)
- [Development Guide](docs/development.md)
- [Deployment Guide](docs/deployment.md)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Abdelrahman Ahmed - Initial work - [YourGitHub](https://github.com/abdelrahman-a99)

## 🙏 Acknowledgments

- List any acknowledgments here
- Thanks to all contributors
- Special thanks to the open-source community
