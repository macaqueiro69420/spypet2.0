# Discord Server Scraper (Direct API Version)

This tool allows you to scrape all messages from a Discord server using the Discord API directly, save them to a JSON database, and detect Discord invite links.

## Features

- Uses the Discord REST API directly, without any third-party wrappers
- Works with normal Discord user accounts
- Scrapes all accessible text channels in a Discord server
- Saves all messages to a JSON database file, including author, content, and timestamp
- Detects and highlights Discord invite links (discord.com/invite or discord.gg)
- Colorized console output for better readability
- Handles rate limits and errors gracefully

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
      "username": "author_username",
      "discriminator": "1234",
      "avatar": "avatar_hash"
    },
    "content": "message content",
    "timestamp": "2023-01-01T12:00:00.000Z",
    "attachments": ["url1", "url2"],
    "embeds": [{...}]
  },
  ...
]
```

## How It Works

This scraper:
1. Makes direct HTTP requests to Discord's API endpoints
2. Handles rate limiting automatically (waits when Discord limits are hit)
3. Processes channels and messages using the raw JSON responses
4. Detects invite links using regex pattern matching
5. Stores messages with complete author, content, and timestamp information

## Important Warning

**Using this tool with a user account token may violate Discord's Terms of Service.** Use at your own risk. This tool is for educational purposes only.