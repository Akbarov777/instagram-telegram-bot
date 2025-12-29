from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp
import os

# BotFather tokeningizni shu yerga yozing
TOKEN = "8376760305:AAFyHndrBBqcsTqBIOopdMKeAbAUipYe-AU"

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Salom!\nInstagram video linkini yubor, men videoni beraman."
    )

# Instagram videoni olish funksiyasi
async def download_instagram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "instagram.com" not in url:
        await update.message.reply_text("❌ Bu Instagram link emas")
        return

    await update.message.reply_text("⏳ Video yuklanmoqda, kut...")

    try:
        # ===== VIDEO =====
        video_opts = {
            'outtmpl': 'video.%(ext)s',
            'format': 'mp4'
        }

        with yt_dlp.YoutubeDL(video_opts) as ydl:
            ydl.download([url])

        video_file = None
        for file in os.listdir():
            if file.startswith("video.") and file.endswith(".mp4"):
                video_file = file
                break

        if video_file:
            await update.message.reply_video(video=open(video_file, 'rb'))
            os.remove(video_file)

    except Exception as e:
        await update.message.reply_text("❌ Xatolik yuz berdi")
        print(e)

# Botni ishga tushirish
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_instagram))

print("🤖 Bot ishga tushdi...")
app.run_polling()
