import asyncio
import config
from scraper import DiscordScraper
from colorama import Fore, Style, init

# Initialize colorama for colored console output
init()

def main():
    print(f"{Fore.CYAN}Discord Server Scraper (User Account Version){Style.RESET_ALL}")
    print(f"Target Server ID: {config.SERVER_ID}")
    print(f"Database file: {config.DATABASE_FILE}")
    print("-------------------------------\n")
    
    # Check for valid token
    if config.DISCORD_TOKEN == "YOUR_DISCORD_USER_TOKEN":
        print(f"{Fore.RED}Error: Please update the Discord user token in config.py{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Note: Using a user account (selfbot) may violate Discord's Terms of Service.{Style.RESET_ALL}")
        return
    
    # Check for valid server ID
    if config.SERVER_ID == 123456789012345678:
        print(f"{Fore.RED}Error: Please update the server ID in config.py{Style.RESET_ALL}")
        return
    
    # Initialize the Discord client - no intents needed for selfcord
    client = DiscordScraper(config.SERVER_ID, config.DATABASE_FILE)
    
    try:
        # Start the client with user token
        asyncio.run(client.run(config.DISCORD_TOKEN))
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Scraping interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()