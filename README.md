# 💬 Django ChatApp

A **real-time chat application** built using Django, Django REST Framework, and WebSockets. This app allows users to sign up, log in, and communicate instantly — all without refreshing the page. Built with scalability, responsiveness, and clean architecture in mind.

---

## 🚀 Features

- 🔐 User authentication (Sign up, Login, Logout)
- 🧵 Real-time 1-to-1 chat using Django Channels & WebSockets
- 📬 Message history and chat persistence (stored in database)
- 🟢 Online user status indicator
- 🎨 Clean & responsive UI (HTML, CSS, JS)
- 🌐 API endpoints built with Django REST Framework (for future frontend support)

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Django, Django REST Framework |
| Real-Time | Django Channels, WebSockets |
| Frontend | HTML5, CSS3, JavaScript |
| Database | SQLite (default) or PostgreSQL (production-ready) |
| Auth | Django's built-in Authentication system |
| Deployment Ready | Yes (with Gunicorn + Daphne/ASGI setup) |

---

## 📸 Screenshots

> *(Insert screenshots or a GIF demo of the app in action)*

![ChatApp Screenshot](./screenshots/chat-sample.png)

---

## 🔧 Installation & Setup

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/django-chatapp.git
cd django-chatapp

# 2. Create and activate virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
