# 🛠️ TaskHub

**TaskHub** — jamoa va foydalanuvchilar uchun vazifa boshqarish (task/project) tizimi. Loyiha backend (Django + DRF) va Telegram bot orqali interfeysga ega.

---

## 📌 Loyihaning qisqacha tavsifi
- Backend: Django + Django REST Framework API (projects, tasks, accounts, auth).
- Telegram bot: API orqali login, project va task CRUD amallarini command orqali bajaradi.
- Loyihaning kodi `backend/` va `bot/` papkalarida joylashgan.

---

## ✅ Asosiy imkoniyatlar
- Foydalanuvchi ro‘yxatdan o‘tishi, JWT bilan autentifikatsiya (login/logout).
- Role’lar: `admin`, `manager`, `user` — har biri uchun turli huquqlar.
- Project va Task CRUD APIlari (DRF ViewSet + router).
- Tasklarni filterlash (status, assigned_to, title).
- Telegram bot orqali: login, projects ro‘yxati, tasks ro‘yxati, task yaratish, project yaratish, update va delete komandalar.

---

## 🧾 Texnologiyalar
- Python 3.x
- Django
- Django REST Framework
- djangorestframework-simplejwt (JWT)
- django-filter
- python-telegram-bot (yoki PyTelegramBotAPI — bot kodida ishlatilgan kutubxona)
- PostgreSQL (production uchun tavsiya etiladi)
- `requirements.txt` fayli repoda mavjud.

---

## 📁 Loyiha tuzilmasi (muqaddima)
```
TaskHub/
├─ backend/        # Django project (settings, apps: accounts, projects, api ...)
├─ bot/            # Telegram bot kodi
├─ .gitignore
├─ requirements.txt
└─ README.md
```

---

## ⚙️ Tizimni mahalliy ishga tushirish (minimal)
> Quyidagi ko‘rsatmalar `backend/` papkasi ichida bajarilishi nazarda tutilgan.

1. Repozitoriyani klonlash:
```bash
git clone https://github.com/DilmurodZK/TaskHub.git
cd TaskHub/backend
```

2. Virtual muhit yaratish va faollashtirish:
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

3. Kutubxonalarni o‘rnatish:
```bash
pip install -r ../requirements.txt
# yoki agar requirements.txt backend ichida bo'lsa:
# pip install -r requirements.txt
```

4. `.env` yoki `local_settings.py` yarating va quyidagilarni qo‘shing (hech qachon ularni repo-ga push qilmang):
```
SECRET_KEY=...
DEBUG=True
DB_NAME=...
DB_USER=...
DB_PASSWORD=...
DB_HOST=...
BOT_TOKEN=...
```

5. Migratsiyalarni bajarish:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Superuser yaratish:
```bash
python manage.py createsuperuser
```

7. Serverni ishga tushirish:
```bash
python manage.py runserver
```

8. Botni ishga tushirish (alohida terminalda):
```bash
cd ../bot
python bot.py
```
> Eslatma: bot ishlashi uchun Django server (`runserver`) yoki deployed API orqali mavjud bo‘lishi kerak — bot API ga murojaat qiladi.

---

## 🔌 API misollar (DRF router orqali)
- `GET  /api/projects/` — barcha projectlar
- `POST /api/projects/` — yangi project yaratish (manager/admin)
- `GET  /api/projects/<id>/` — project detali
- `GET  /api/tasks/` — tasklar (filter: `?status=done`, `?assigned_to=2`)
- `POST /api/tasks/` — task yaratish (required: `title`, `project`, ...)

(Exact endpoint pathlar sizning `api/urls.py` ga mos).

---

## 🤖 Bot komandalar (misol)
Bot command-based ishlaydi. `/help` orqali komandalarning shakli bot ichida ko‘rsatiladi. Asosiylari:
```
/login <username> <password>
/logout

/projects                  # barcha projectlar
/projects <id>             # project detali
/newproject name="..." description="..."

/tasks                    # barcha tasklar
/tasks <id>               # task detali
/newtask title="..." description="..." project=<project_id> assigned_to=<user_id>
/updatetask id=... title="..." description="..."
/deltask id
/help
```

---