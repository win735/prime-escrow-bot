import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

ADMIN_ID = int(os.getenv("ADMIN_ID"))
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Start Escrow", callback_data="start_escrow")],
        [InlineKeyboardButton("How It Works", callback_data="how_it_works")],
        [InlineKeyboardButton("Contact Admin", url="https://t.me/me_0041")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🔐 *Welcome to the Official Escrow Bot!*\n\n"
        "I help protect buyers and sellers during trades.\n"
        "Choose an option below to begin:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "start_escrow":
        await query.edit_message_text(
            "📝 *Escrow Request Started!*\n\n"
            "Please send the following details in one message:\n"
            "- Buyer Username\n"
            "- Seller Username\n"
            "- Item/Service\n"
            "- Amount\n"
            "- Conditions\n\n"
            "After you send it, the admin will review.",
            parse_mode="Markdown"
        )

    elif query.data == "how_it_works":
        await query.edit_message_text(
            "📘 *How Escrow Works:*\n\n"
            "1️⃣ Buyer & Seller agree to a deal.\n"
            "2️⃣ Buyer sends payment to the escrow admin.\n"
            "3️⃣ Seller delivers the product/service.\n"
            "4️⃣ Buyer confirms receipt.\n"
            "5️⃣ Admin releases payment to the seller.\n\n"
            "This system protects both parties.",
            parse_mode="Markdown"
        )

async def handle_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📥 *New Escrow Request:*\n\n{user_message}",
        parse_mode="Markdown"
    )

    await update.message.reply_text(
        "✅ Your escrow request has been submitted.\n"
        "The admin will contact you shortly."
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_details))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
