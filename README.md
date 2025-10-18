<h1>SOCIAL MEDIA</h1>
# 🧠 Social Media Backend (Django + Docker + PostgreSQL)

This project is a **social media platform** similar to Instagram — built with **Django** as the backend framework.  
It is designed to include all major social media features such as:

- 🧍 **Accounts & Authentication**
- 🖼️ **Posts & Media Upload**
- 💬 **Comments**
- 📚 **Stories**
- ✉️ **Direct Messages**
- ❤️ **Likes & Notifications**

The project is fully **containerized with Docker**, and uses **PostgreSQL** as its main database.

---

## 🚀 Features

- Modular Django architecture (apps for each domain)
- RESTful API ready for frontend or mobile apps
- JWT authentication system
- Scalable with Docker & Docker Compose
- Environment variables via `.env`
- PostgreSQL as relational DB
- Ready to extend with Redis, Celery, or any async features

---

## 🧩 Tech Stack

| Component     | Technology |
|----------------|-------------|
| Backend        | Django 4.x (Python 3.11) |
| Database       | PostgreSQL |
| Containerization | Docker & Docker Compose |
| Authentication | JWT |
| Caching (optional) | Redis |
| Environment Management | `.env` file |

---

## ⚙️ Project Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/social_media.git
cd social_media
```
### 2. Create and configure the environment file
```commandline
cp .env-example .env
```
Then open .env and set your own values if needed: 
```commandline
DEBUG=True
SECRET_KEY=your-secret-key
POSTGRES_DB=socialdb
POSTGRES_USER=user
POSTGRES_PASSWORD=pass
POSTGRES_HOST=db
POSTGRES_PORT=5432
```
💡 Note: .env-example is included in the repository as a template.

### 3. Build and run the project using Docker Compose
```commandline
sudo docker-compose up --build
```
This will:
  - Build the Django backend image
  - Start the PostgreSQL database
  - Launch the Django server on port 8000

### 4. Access the app
After all services are up, open your browser and go to:
```commandline
http://localhost:8000
```
### 5. Running commands inside the container
If you need to run migrations or create a superuser, use:
```commandline
sudo docker exec -it social_app python manage.py migrate
sudo docker exec -it social_app python manage.py createsuperuser
```
---


### 👨‍💻 Author

**Javad Hoseinzade
_Backend Developer | Python & Django |

- 📧 Email: [javadhoseinzde80@gmail.com]  
- 🌐 LinkedIn: [https://www.linkedin.com/in/javad-hoseinzade-33b979220/]  
