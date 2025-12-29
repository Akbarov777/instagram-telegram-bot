from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp
import os

# ⬇️ Token to‘g‘ri
TOKEN = "8376760305:AAFyHndrBBqcsTqBIOopdMKeAbAUipYe-AU"

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Salom!\nInstagram linkini yubor — video va audio beraman."
    )

# Video + Audio (ffmpeg siz)
async def download_instagram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "instagram.com" not in url:
        await update.message.reply_text("❌ Bu Instagram link emas")
        return

    await update.message.reply_text("⏳ Video va audio yuklanmoqda, kut...")

    try:
        # ===== VIDEO =====
        video_opts = {
            'format': 'mp4',
            'outtmpl': 'video.%(ext)s',
            'quiet': True
        }

        with yt_dlp.YoutubeDL(video_opts) as ydl:
            ydl.download([url])

        for file in os.listdir():
            if file.startswith("video.") and file.endswith(".mp4"):
                await update.message.reply_video(video=open(file, 'rb'))
                os.remove(file)
                break

        # ===== AUDIO (FFmpeg YO‘Q) =====
        audio_opts = {
            'format': 'bestaudio',
            'outtmpl': 'audio.%(ext)s',
            'quiet': True
        }

        with yt_dlp.YoutubeDL(audio_opts) as ydl:
            ydl.download([url])

        for file in os.listdir():
            if file.startswith("audio."):
                await update.message.reply_audio(audio=open(file, 'rb'))
                os.remove(file)
                break

    except Exception as e:
        await update.message.reply_text("❌ Xatolik yuz berdi")
        print(e)

# Botni ishga tushirish
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_instagram))

print("🤖 Bot ishga tushdi...")
app.run_polling()
