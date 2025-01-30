
# Telegram AI Chatbot

Welcome to the **Telegram AI Chatbot** project! This chatbot is powered by **Google Gemini AI**, connected to a **MongoDB database**, and includes functionality for **image analysis**, **web searches**, and **user registration**.

## Features

- **User Registration**: Users are prompted to share their phone number using Telegram's contact button.
- **Chatbot**: Powered by Gemini AI, the bot can respond to text-based queries.
- **Image Analysis**: Users can share images, and the bot will analyze them using Gemini AI.
- **Web Search**: Users can perform web searches directly within the Telegram chat using the `/websearch` command.
- **MongoDB Integration**: Chat history and user data are stored in MongoDB for future reference.

## Installation

### Prerequisites
- **Python 3.8+**
- **MongoDB Atlas** (for storing chat history and user data)
- **Telegram Bot Token** (from [BotFather](https://core.telegram.org/bots#botfather))
- **Gemini API Key** (from [Google Cloud](https://cloud.google.com/generative-ai))
- **SerpAPI Key** (for web searches)

### Steps to Set Up

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/telegram-ai-chatbot.git
   cd telegram-ai-chatbot
   ```

2. **Create a virtual environment** (optional, but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your environment variables**:
   Create a `.env` file in the root directory of the project and add the following:
   ```ini
   TELEGRAM_BOT_TOKEN=your-telegram-bot-token
   MONGODB_URI=your-mongodb-uri
   GEMINI_API_KEY=your-gemini-api-key
   SERPAPI_KEY=your-serpapi-key
   ```

5. **Run the bot**:
   ```bash
   python bot.py
   ```

   The bot will now be running and listening for user messages.

## How It Works

- **User Registration**: 
   When the bot receives the `/start` command, it will prompt the user to share their phone number via the Telegram contact sharing feature. The bot saves this information in MongoDB.

- **Text Messages**:
   If the user sends a text, the bot generates a response using **Google Gemini AI** and responds accordingly. The conversation is also saved in MongoDB for future reference.

- **Image Upload**:
   When an image is shared, the bot uses **Gemini's Vision model** to analyze the image and provide a description.

- **Web Search**:
   Using the `/websearch <query>` command, users can search the web. The bot uses **SerpAPI** to get search results and summarizes them using Gemini.

## MongoDB Setup

The bot requires a MongoDB database to store chat history, user data, and file metadata. Set up a **MongoDB Atlas** cluster and create a database named `telegram_bot` with collections for:
- `users`
- `chat_history`
- `file_metadata`

Make sure to create a MongoDB user with **read & write permissions** and configure your **MongoDB URI** in the `.env` file.

## Troubleshooting

- **MongoDB Connection Error**:
   If you see errors like `bad auth: authentication failed`, double-check your MongoDB credentials in the `.env` file. Ensure your database user has the correct permissions.

- **Telegram Bot Not Responding**:
   Ensure your **Telegram Bot Token** is correct and the bot is running with no errors.

- **Error Logs**:
   If any errors occur, the bot logs them with details, including the `error_handler` which sends an error message to users.

## Contributing

Feel free to fork the repository, submit issues, or create pull requests. Contributions are always welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
