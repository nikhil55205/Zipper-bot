
import telebot
import zipfile
import os

TOKEN = "8837053657:AAFxFitiZHKZylhe833iyM2b8LLq-YLobZs"

bot = telebot.TeleBot(
    TOKEN,
    threaded=True,
    num_threads=10
)

DOWNLOAD_FOLDER = "downloads"
EXTRACT_FOLDER = "extracted"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
os.makedirs(EXTRACT_FOLDER, exist_ok=True)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Bot online ⚡")

@bot.message_handler(content_types=['document'])
def unzip_file(message):

    try:

        file_name = message.document.file_name

        if not file_name.endswith(".zip"):
            bot.reply_to(message, "ZIP file bhejo 😅")
            return

        bot.reply_to(message, "Processing ⚡")

        file_info = bot.get_file(message.document.file_id)

        downloaded_file = bot.download_file(file_info.file_path)

        zip_path = os.path.join(DOWNLOAD_FOLDER, file_name)

        with open(zip_path, "wb") as f:
            f.write(downloaded_file)

        extract_path = os.path.join(
            EXTRACT_FOLDER,
            file_name.replace(".zip", "")
        )

        os.makedirs(extract_path, exist_ok=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        for root, dirs, files in os.walk(extract_path):

            for file in files:

                full_path = os.path.join(root, file)

                with open(full_path, "rb") as send_file:
                    bot.send_document(message.chat.id, send_file)

        bot.send_message(message.chat.id, "Done 🔥")

    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

print("Fast bot running ⚡")

bot.infinity_polling(
    timeout=5,
    long_polling_timeout=1
)
