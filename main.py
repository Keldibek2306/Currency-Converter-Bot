import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

CBU_URL = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/USD/"
from config import TOKEN

def calculate_currency(direction: str, amount: float) -> float:
    data = requests.get(CBU_URL, timeout=10).json()
    rate = float(str(data[0]["Rate"]).replace(",", "."))
    return amount * rate if direction == "USD-UZS" else amount / rate

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! UZS USD bot.\nFormat: USD-UZS:100 yoki UZS-USD:125000\n/ rate — 1 USD kursi"
    )

async def rate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = requests.get(CBU_URL, timeout=10).json()
    rate = float(str(data[0]["Rate"]).replace(",", "."))
    await update.message.reply_text(f"1 USD = {int(round(rate))} UZS")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = (update.message.text or "").strip().upper().replace(" ", "")
        if ":" not in text: 
            await update.message.reply_text("Format: USD-UZS:100 yoki UZS-USD:125000")
            return
        direction, amt = text.split(":", 1)
        if direction not in ("USD-UZS", "UZS-USD"):
            await update.message.reply_text("Yo'nalish: USD-UZS yoki UZS-USD")
            return
        amount = float(amt.replace(",", "."))
        result = calculate_currency(direction, amount)
        if direction == "USD-UZS":
            await update.message.reply_text(f"Natija: {result:,.0f} UZS".replace(",", " "))
        else:
            await update.message.reply_text(f"Natija: ${result:,.2f}")
    except:
        await update.message.reply_text("Xato. Masalan: USD-UZS:100 yoki UZS-USD:125000")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("rate", rate_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()

if __name__ == "__main__":
    main()
