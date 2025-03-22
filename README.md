# Discord Bot Project

This project is a Discord bot that connects to a game server, retrieves player information, and sends updates to a Discord channel via a webhook.

## Project Structure

```
discord-bot
├── src
│   ├── bot.py          # Main logic for the Discord bot
│   └── utils
│       └── __init__.py # Utility functions for the bot
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd discord-bot
   ```

2. **Install dependencies:**
   Make sure you have Python installed. Then, run:
   ```
   pip install -r requirements.txt
   ```

3. **Run the bot:**
   Execute the following command to start the bot:
   ```
   python src/bot.py
   ```

## Usage

The bot will connect to the specified game server and send updates about the players online to the configured Discord channel every minute. You can modify the server IP and port in `src/bot.py` as needed.

## Contributing

Feel free to submit issues or pull requests if you have suggestions or improvements for the bot.