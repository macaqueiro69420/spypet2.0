# Discord Server Scraper

This tool allows you to scrape all messages from a Discord server, save them to a JSON database, and detect Discord invite links.

## Features

- Scrapes all accessible text channels in a Discord server
- Saves all messages to a JSON database file
- Detects and highlights Discord invite links (discord.com/invite or discord.gg)
- Colorized console output for better readability
- Handles errors gracefully and continues scraping

## Setup

1. Clone this repository
2. Install the required dependencies: `pip install -r requirements.txt`
3. Create a Discord bot and get its token:
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application
   - Go to the Bot tab and create a bot
   - Copy the token
4. Enable the following Privileged Gateway Intents:
   - Message Content Intent
   - Server Members Intent
5. Invite the bot to your server with the following permissions:
   - Read Messages/View Channels
   - Read Message History
6. Update the `config.py` file with your bot token and server ID

## Configuration

Edit the `config.py` file to configure the scraper:

```python
# Discord Configuration
DISCORD_TOKEN = "YOUR_DISCORD_TOKEN"  # Your bot token
SERVER_ID = 123456789012345678  # Your server ID

# Database settings
DATABASE_FILE = "database.json"  # Where to save the data

# Other settings
DEBUG_MODE = True  # Set to False to disable verbose logging
```

## Usage

Run the scraper with:

```
python main.py
```

The scraper will:
1. Connect to Discord using your bot token
2. Access the specified server
3. Scrape all accessible text channels
4. Save all messages to the database file
5. Print Discord invite links to the console

## Output

All messages are saved to `database.json` in the following format:

```json
[
  {
    "id": "message_id",
    "channel_id": "channel_id",
    "channel_name": "channel_name",
    "author_id": "author_id",
    "author_name": "author_name",
    "content": "message content",
    "timestamp": "2023-01-01T12:00:00.000000",
    "attachments": ["url1", "url2"],
    "embeds": [{...}]
  },
  ...
]
```

## Notes

- The bot needs appropriate permissions to access channels and read message history
- Some channels might not be accessible due to permission settings
- The scraper will skip messages that are already in the database
- For large servers, scraping might take a long time

## Legal Notice

This tool is for educational purposes only. Always ensure you have proper authorization to scrape Discord servers. Using this tool may violate Discord's Terms of Service.