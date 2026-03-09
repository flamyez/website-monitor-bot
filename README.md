# 🌐 Website Monitor Bot

A Telegram bot for monitoring website availability with support for 5 languages.

## ✨ Features

- ✅ Check availability of any website
- 📨 Automatic notifications when site goes down or comes back online
- 🌐 Multi-language support: English, Russian, Ukrainian, German, French
- ⚙️ Flexible settings for each user
- 🔄 Customizable check intervals

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/flamyez/website-monitor-bot.git
cd website-monitor-bot
```

2. Create virtual environment:
```bash
python -m venv .venv

# Windows:
.venv\Scripts\activate

# Linux/Mac:
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure the bot:

Edit `config.json` and add your bot token from [@BotFather](https://t.me/BotFather)

5. Run the bot:
```bash
python main.py
```

## 📁 Project Structure
```
website-monitor-bot/
├── main.py              # Main bot file
├── translate.py         # Translation system
├── config.json          # Configuration (not committed)
├── requirements.txt     # Dependencies
├── database/
│   └── main.py         # Database operations
├── handlers/
│   └── check.py        # Automatic website checking
├── request/
│   └── main.py         # HTTP requests
└── lang/               # Translation files
    ├── en.json
    ├── ru.json
    ├── ua.json
    ├── de.json
    └── fr.json
```

## 🛠️ Tech Stack

- Python 3.10+
- [aiogram](https://github.com/aiogram/aiogram) 3.x
- [aiohttp](https://github.com/aio-libs/aiohttp)
- SQLite

## ⚙️ Configuration

Edit `config.json`:
```json
{
  "bot_token": "YOUR_BOT_TOKEN",
  "check_interval": 300,
  "default_language": "en"
}
```

- `bot_token` - Your Telegram bot token from [@BotFather](https://t.me/BotFather)
- `check_interval` - Check interval in seconds (default: 300 = 5 minutes)
- `default_language` - Default language (en/ru/ua/de/fr)

## 📝 Usage

1. Start a chat with your bot
2. Use `/start` to begin
3. Configure your website URL in settings
4. Enable notifications to receive alerts

## 📄 License

MIT License - feel free to use this project for learning or commercial purposes.

## 🤝 Contributing

Pull requests are welcome! Feel free to open issues if you find bugs.

## 👨‍💻 Author

Created as a learning project for practicing Python, aiogram, and async programming.