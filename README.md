# 🛠️ TaskHub

**TaskHub** — a task/project management system for teams and individual users. The project includes a backend (Django + DRF) and a Telegram bot interface.

---

## 📌 Project Overview
- Backend: Django + Django REST Framework API (projects, tasks, accounts, authentication).
- Telegram Bot: Provides login, project and task CRUD operations via commands through the API.
- Source code is organized into two main folders: backend/ and bot/.

---

## ✅ Key Features
- User registration and authentication with JWT (login/logout).
- Roles: admin, manager, user — each with different permissions.
- Project and Task CRUD APIs (DRF ViewSet + router).
- Task filtering (by status, assigned_to, title).
- Telegram bot commands: login, list projects, list tasks, create/update/delete projects and tasks.

---

## 🧾 Technologies
- Python 3.x
- Django
- Django REST Framework
- djangorestframework-simplejwt (JWT authentication)
- django-filter
- python-telegram-bot (or PyTelegramBotAPI)
- PostgreSQL (recommended for production)
- requirements.txt file included in the rep

---

## 📁 Project Structure
```
TaskHub/
├─ backend/        # Django project (settings, apps: accounts, projects, api ...)
├─ bot/            # Telegram bot code
├─ .gitignore
├─ requirements.txt
└─ README.md
```

---

## ⚙️ Local Setup (minimal)
> Inside the backend/ folder:

1. Clone the repository:
```bash
git clone https://github.com/DilmurodZK/TaskHub.git
cd TaskHub/backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

3. Install dependencies:
```bash
pip install -r ../requirements.txt
# yoki agar requirements.txt backend ichida bo'lsa:
# pip install -r requirements.txt
```

4. - Create .env or local_settings.py with:
```
SECRET_KEY=...
DEBUG=True
DB_NAME=...
DB_USER=...
DB_PASSWORD=...
DB_HOST=...
BOT_TOKEN=...
```

5. - Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Start the server
```bash
python manage.py runserver
```

8. Run the bot (in a separate terminal):
```bash
cd ../bot
python bot.py
```
⚠️ Note: The bot requires the Django server (runserver) or a deployed API to be running, since it communicates with the API.

---

## 🔌 API Examples (via DRF Router)
- GET /api/projects/ — list all projects
- POST /api/projects/ — create a new project (manager/admin only)
- GET /api/projects/<id>/ — project details
- GET /api/tasks/ — list tasks (filters: ?status=done, ?assigned_to=2)
- POST /api/tasks/ — create a new task (required: title, project, …)

---

## 🤖 Bot Commands (Examples)
The bot is command-based. Use /help inside the bot to see all commands. Main ones include:
```
/login <username> <password>
/logout

/projects                  # list all projects
/projects <id>             # project detail
/newproject name="..." description="..."

/tasks                    # list all tasks
/tasks <id>               # task detail
/newtask title="..." description="..." project=<project_id> assigned_to=<user_id>
/updatetask id=... title="..." description="..."
/deltask id
/help
```

---
