import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
from pymongo import MongoClient
import google.generativeai as genai
import requests

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize MongoDB Connection
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
try:
    client.admin.command('ping')
    logger.info("✅ Connected to MongoDB successfully!")
except Exception as e:
    logger.error(f"❌ MongoDB Connection Failed: {e}")

db = client["telegram_bot"]
users_collection = db["users"]
chat_history_collection = db["chat_history"]
file_metadata_collection = db["file_metadata"]

# Configure Gemini AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
text_model = genai.GenerativeModel('gemini-pro')
vision_model = genai.GenerativeModel('gemini-pro-vision')

# START COMMAND
async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_data = {
        "first_name": user.first_name,
        "username": user.username,
        "chat_id": update.message.chat_id,
        "phone_number": None
    }
    users_collection.update_one({"chat_id": user_data["chat_id"]}, {"$set": user_data}, upsert=True)

    contact_keyboard = ReplyKeyboardMarkup([[KeyboardButton("📱 Share Contact", request_contact=True)]], resize_keyboard=True)
    await update.message.reply_text("Welcome! Please share your phone number.", reply_markup=contact_keyboard)

# HANDLE CONTACT SHARING
async def handle_contact(update: Update, context: CallbackContext):
    contact = update.message.contact
    users_collection.update_one(
        {"chat_id": update.message.chat_id},
        {"$set": {"phone_number": contact.phone_number}},
        upsert=True
    )
    await update.message.reply_text("✅ Contact saved successfully!")

# HANDLE TEXT INPUT & AI RESPONSE
async def handle_text(update: Update, context: CallbackContext):
    user_input = update.message.text
    response = text_model.generate_content(user_input)
    
    chat_history = {
        "chat_id": update.message.chat_id,
        "user_input": user_input,
        "bot_response": response.text,
        "timestamp": datetime.now()
    }
    chat_history_collection.insert_one(chat_history)
    
    await update.message.reply_text(response.text)

# HANDLE IMAGE UPLOAD & AI DESCRIPTION
async def handle_image(update: Update, context: CallbackContext):
    file = await update.message.photo[-1].get_file()
    file_path = await file.download()

    with open(file_path, "rb") as image_file:
        image_data = image_file.read()

    response = vision_model.generate_content(["Describe this image:", image_data])

    file_data = {
        "chat_id": update.message.chat_id,
        "filename": file_path.name,
        "description": response.text,
        "timestamp": datetime.now()
    }
    file_metadata_collection.insert_one(file_data)

    await update.message.reply_text(response.text)

# HANDLE WEB SEARCH
async def web_search(update: Update, context: CallbackContext):
    query = " ".join(context.args)
    search_url = f"https://api.serpapi.com/search?q={query}&api_key={os.getenv('SERPAPI_KEY')}"

    try:
        search_results = requests.get(search_url).json()
        snippet = search_results.get("organic_results", [{}])[0].get("snippet", "No summary available")
        
        summary = text_model.generate_content(f"Summarize this: {snippet}")
        top_links = "\n".join([res["link"] for res in search_results.get("organic_results", [])[:3]])

        await update.message.reply_text(f"🔎 **Summary:** {summary.text}\n\n🌐 **Top Links:**\n{top_links}")
    except Exception as e:
        logger.error(f"❌ Web search error: {e}")
        await update.message.reply_text("🚨 An error occurred while searching. Please try again.")

# ERROR HANDLING
async def error_handler(update: Update, context: CallbackContext):
    logger.error(f"❌ Update {update} caused error {context.error}")

    if update and update.message:
        await update.message.reply_text("⚠️ An error occurred. Please try again later.")

# MAIN FUNCTION
def main():
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    # Register Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))
    application.add_handler(CommandHandler("websearch", web_search))

    # Error Handler
    application.add_error_handler(error_handler)

    logger.info("🚀 Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
