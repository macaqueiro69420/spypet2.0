# Discord Server Scraper (User Account Version)

This tool allows you to scrape all messages from a Discord server using a normal user account, save them to a JSON database, and detect Discord invite links.

## Features

- Works with normal Discord user accounts (selfbot)
- Scrapes all accessible text channels in a Discord server
- Saves all messages to a JSON database file, including author, content, and timestamp
- Detects and highlights Discord invite links (discord.com/invite or discord.gg)
- Colorized console output for better readability
- Handles errors gracefully and continues scraping

## Setup

1. Clone this repository
2. Install the required dependencies: `pip install -r requirements.txt`
3. Get your Discord user account token:
   - Log into Discord in your browser
   - Press F12 to open Developer Tools
   - Go to the Network tab
   - Refresh the page (F5)
   - Look for a request to "science" or "api"
   - Find the "authorization" header in the request headers
   - Copy the token value (it's a long string)
4. Update the `config.py` file with your user token and target server ID

## Configuration

Edit the `config.py` file to configure the scraper:

```python
# Discord Configuration
DISCORD_TOKEN = "YOUR_DISCORD_USER_TOKEN"  # Your user account token
SERVER_ID = 123456789012345678  # Target server ID

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
1. Connect to Discord using your user account token
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
    "author": {
      "id": "author_id",
      "name": "author_name",
      "display_name": "display_name",
      "discriminator": "1234"
    },
    "content": "message content",
    "timestamp": "2023-01-01T12:00:00.000000",
    "attachments": ["url1", "url2"],
    "embeds": [{...}]
  },
  ...
]
```

## Notes

- The scraper has detailed author information including ID, name, display name, and discriminator
- Each message includes its timestamp in ISO format
- Some channels might not be accessible due to permission settings
- The scraper will skip messages that are already in the database
- For large servers, scraping might take a long time

## Important Warning

**Using this tool with a user account (selfbot) may violate Discord's Terms of Service.** Use at your own risk. This tool is for educational purposes only.