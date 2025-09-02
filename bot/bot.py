import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from bot_token import telegram_bot_token

API_BASE = "http://127.0.0.1:8000/api"
LOGIN_URL = f"{API_BASE}/accounts/login/"
PROJECT_URL = f"{API_BASE}/projects/"
TASK_URL = f"{API_BASE}/tasks/"

BOT_TOKEN = telegram_bot_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

user_tokens = {}

# --- Helper: Auth token olish ---
def get_headers(user_id):
    token = user_tokens.get(user_id)
    if not token:
        return None
    return {"Authorization": f"Bearer {token}"}

# --- Login ---
async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        username, password = context.args
    except ValueError:
        await update.message.reply_text("❌ To‘g‘ri format: /login username password")
        return

    r = requests.post(LOGIN_URL, json={"username": username, "password": password})
    if r.status_code == 200:
        token = r.json()["access"]
        user_tokens[update.effective_user.id] = token
        await update.message.reply_text("✅ Login muvaffaqiyatli!")
    else:
        await update.message.reply_text(f"❌ Login xato! {r.text}")


# --- Logout ---
async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in user_tokens:
        del user_tokens[update.effective_user.id]
        await update.message.reply_text("✅ Logout qilindi.")
    else:
        await update.message.reply_text("❌ Siz login qilmagansiz.")

# --- Quotes parser ---
import shlex

def parse_args(context_args, required_keys):
    """
    context_args: update yoki command context.args
    required_keys: list of required field names, masalan ["name", "description"]

    return: dict with values or None if format xato
    """
    args_text = " ".join(context_args)
    try:
        # shlex bilan split qiladi, quotes ichidagi stringlarni bir butun sifatida oladi
        parts = dict(pair.split("=", 1) for pair in shlex.split(args_text))
    except ValueError:
        return None

    # required_keys tekshir
    for key in required_keys:
        if key not in parts or not parts[key]:
            return None

    return parts


# --- Tasklar yoki bitta task ---
async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    headers = get_headers(update.effective_user.id)
    if not headers:
        await update.message.reply_text("❌ Avval /login qiling.")
        return

    # ID tekshirish
    if context.args:
        try:
            task_id = int(context.args[0])
        except ValueError:
            await update.message.reply_text("❌ Format: /tasks <id> (faqat raqam)")
            return
        url = f"{TASK_URL}{task_id}/"  # detail endpoint
    else:
        url = TASK_URL  # list endpoint

    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        data = r.json()
        # Bitta task
        if context.args:
            msg = "\n".join([f"{k}: {v}" for k, v in data.items()])
            await update.message.reply_text(f"📌 Task ma'lumotlari:\n{msg}")
        # Ro'yxat
        else:
            if not data:
                await update.message.reply_text("📭 Tasklar yo‘q.")
            else:
                msg = "\n".join([f"{t['id']}: {t['title']} [{t.get('status','')}]"
                                 for t in data])
                await update.message.reply_text(f"✅ Tasklar:\n{msg}")
    elif r.status_code == 404:
        await update.message.reply_text("❌ Bunday task topilmadi.")
    else:
        await update.message.reply_text(f"❌ Xatolik: {r.text}")


# --- Projects yoki bitta project ---
async def projects(update: Update, context: ContextTypes.DEFAULT_TYPE):
    headers = get_headers(update.effective_user.id)
    if not headers:
        await update.message.reply_text("❌ Avval /login qiling.")
        return

    # ID tekshirish
    if context.args:
        try:
            project_id = int(context.args[0])
        except ValueError:
            await update.message.reply_text("❌ Format: /projects <id> (faqat raqam)")
            return
        url = f"{PROJECT_URL}{project_id}/"  # detail endpoint
    else:
        url = PROJECT_URL  # list endpoint

    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        data = r.json()
        # Bitta project
        if context.args:
            msg = "\n".join([f"{k}: {v}" for k, v in data.items()])
            await update.message.reply_text(f"📌 Project ma'lumotlari:\n{msg}")
        # Ro'yxat
        else:
            if not data:
                await update.message.reply_text("📭 Projectlar yo‘q.")
            else:
                msg = "\n".join([f"{p['id']}: {p['name']}" for p in data])
                await update.message.reply_text(f"📋 Projectlar:\n{msg}")
    elif r.status_code == 404:
        await update.message.reply_text("❌ Bunday project topilmadi.")
    else:
        await update.message.reply_text(f"❌ Xatolik: {r.text}")


# --- Yangi project ---
async def newproject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    headers = get_headers(update.effective_user.id)
    if not headers:
        await update.message.reply_text("❌ Avval login qiling.")
        return

    parts = parse_args(context.args, ["name", "description"])
    if not parts:
        await update.message.reply_text(
            "❌ Format: /newproject name=\"nomi\" description=\"tavsifi\""
        )
        return

    r = requests.post(
        PROJECT_URL,
        json={"name": parts["name"], "description": parts["description"]},
        headers=headers
    )

    if r.status_code == 201:
        await update.message.reply_text("✅ Project qo‘shildi!")
    else:
        await update.message.reply_text(f"❌ Xatolik: {r.text}")


# --- Yangi task ---
async def newtask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    headers = get_headers(update.effective_user.id)
    if not headers:
        await update.message.reply_text("❌ Avval login qiling.")
        return

    parts = parse_args(context.args, ["title", "description", "project", "assigned_to"])
    if not parts:
        await update.message.reply_text(
            "❌ Format: /newtask title=\"sarlavha\" description=\"tavsifi\""
        )
        return

    r = requests.post(
        TASK_URL,
        json={"title": parts["title"], "description": parts["description"], "project":int(parts['project']), "assigned_to":int(parts["assigned_to"])},
        headers=headers
    )

    if r.status_code == 201:
        await update.message.reply_text("✅ Task qo‘shildi!")
    else:
        await update.message.reply_text(f"❌ Xatolik: {r.text}")



# --- Taskni yangilash ---
async def updatetask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    headers = get_headers(update.effective_user.id)
    if not headers:
        await update.message.reply_text("❌ Avval /login qiling.")
        return

    # faqat id required
    parts = parse_args(context.args, ["id"])
    if not parts:
        await update.message.reply_text(
            "❌ Format: /updatetask id=<id> [title=\"sarlavha\"] [description=\"tavsifi\"]"
        )
        return

    task_id = parts.pop("id")  # IDni alohida olamiz
    payload = {}  # faqat berilgan maydonlar

    if "title" in parts:
        payload["title"] = parts["title"]
    if "description" in parts:
        payload["description"] = parts["description"]

    if not payload:
        await update.message.reply_text("❌ Hech narsa yangilanmadi, title yoki description kiriting.")
        return

    r = requests.patch(f"{TASK_URL}{task_id}/", json=payload, headers=headers)

    if r.status_code in (200, 204):
        await update.message.reply_text("✅ Task yangilandi!")
    else:
        await update.message.reply_text(f"❌ Xatolik: {r.text}")


# --- Taskni o‘chirish ---
async def deltask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    headers = get_headers(update.effective_user.id)
    if not headers:
        await update.message.reply_text("❌ Avval login qiling.")
        return

    if len(context.args) != 1:
        await update.message.reply_text("❌ Format: /deltask id")
        return

    task_id = context.args[0]
    url = f"{TASK_URL}{task_id}/"
    r = requests.delete(url, headers=headers)

    if r.status_code == 204:
        await update.message.reply_text("✅ Task o‘chirildi!")
    else:
        await update.message.reply_text(f"❌ Xatolik: {r.text}")

# --- Help komandasi ---
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📌 Mavjud komandalar:\n\n"
        
        '🔹 /login username password – tizimga kirish'
        '🔹 /logout – tizimdan chiqish'
        '🔹 /tasks – barcha tasklarni ko‘rish'
        '🔹 /tasks <id> – ID bo‘yicha bitta taskni ko‘rish'
        '🔹 /newtask title="sarlavha" description="tavsifi" – yangi task yaratish'
        '🔹 /projects – barcha projectlarni ko‘rish'
        '🔹 /projects <id> – ID bo‘yicha bitta projectni ko‘rish'
        '🔹 /newproject name="nomi" description="tavsifi" – yangi project yaratish'

        '🔹 /updatetask id field=value ... – taskni yangilash\n'
        '🔹 /deltask id – taskni o‘chirish\n\n'
        "ℹ️ Misol:\n"
        "/newtask title=BotTest description=TestDesc\n"
        "/updatetask 3 task_status=done title=YangiTitle"
    )
    await update.message.reply_text(text)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("login", login))
    app.add_handler(CommandHandler("logout", logout))
    app.add_handler(CommandHandler("projects", projects))
    app.add_handler(CommandHandler("newproject", newproject))
    app.add_handler(CommandHandler("tasks", tasks))
    app.add_handler(CommandHandler("newtask", newtask))
    app.add_handler(CommandHandler("updatetask", updatetask))
    app.add_handler(CommandHandler("deltask", deltask))
    app.add_handler(CommandHandler("help", help_command))


    app.run_polling()

if __name__ == "__main__":
    main()
