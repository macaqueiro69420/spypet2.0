import time
import re
from colorama import Fore, Style, init
from discord_api import DiscordAPI
from database import Database

# Initialize colorama for colored console output
init()

class DiscordScraper:
    def __init__(self, token, server_id, database_file):
        self.api = DiscordAPI(token)
        self.server_id = server_id
        self.db = Database(database_file)
        self.invite_pattern = re.compile(r'(discord\.com\/invite\/[a-zA-Z0-9-_]+|discord\.gg\/[a-zA-Z0-9-_]+)')
    
    def scrape(self):
        """Main method to scrape all messages from a server"""
        print(f"{Fore.CYAN}Starting Discord Server Scraper{Style.RESET_ALL}")
        
        # Get user info
        user = self.api.get_current_user()
        if not user:
            print(f"{Fore.RED}Failed to authenticate with Discord. Check your token.{Style.RESET_ALL}")
            return False
        
        print(f"{Fore.GREEN}Logged in as {user['username']}#{user['discriminator']} ({user['id']}){Style.RESET_ALL}")
        
        # Get server info
        server = self.api.get_guild(self.server_id)
        if not server:
            print(f"{Fore.RED}Failed to access server with ID {self.server_id}. Check permissions or server ID.{Style.RESET_ALL}")
            return False
        
        print(f"{Fore.CYAN}Scraping server: {server['name']} ({server['id']}){Style.RESET_ALL}")
        
        # Get channels
        channels = self.api.get_guild_channels(self.server_id)
        if not channels:
            print(f"{Fore.RED}Failed to get channels for server {server['name']}.{Style.RESET_ALL}")
            return False
        
        # Filter to text channels only
        text_channels = [c for c in channels if c['type'] == 0]  # 0 is TEXT_CHANNEL
        print(f"Found {len(text_channels)} text channels to scrape")
        
        # Statistics tracking
        total_channels = len(text_channels)
        processed_channels = 0
        total_messages = 0
        total_invite_links = 0
        
        # Scrape each channel
        for channel in text_channels:
            processed_channels += 1
            channel_name = channel.get('name', 'unknown-channel')
            channel_id = channel['id']
            
            print(f"\nScraping channel: #{channel_name} (ID: {channel_id})")
            print(f"Progress: {processed_channels}/{total_channels} channels")
            
            try:
                # Define a progress callback
                def progress_callback(count, batch_count):
                    print(f"  - {count} messages scraped from #{channel_name} (in {batch_count} API requests)")
                
                # Get all messages from the channel
                messages, invite_count = self.api.get_all_messages(channel_id, progress_callback)
                
                # Update stats
                channel_message_count = len(messages)
                total_messages += channel_message_count
                total_invite_links += invite_count
                
                # Save messages to database
                new_messages = 0
                for message in messages:
                    # Skip if message already exists
                    if self.db.message_exists(message['id']):
                        continue
                    
                    # Add to database
                    self.db.add_message({
                        'id': message['id'],
                        'channel_id': channel_id,
                        'channel_name': channel_name,
                        'author': {
                            'id': message['author']['id'],
                            'username': message['author']['username'],
                            'discriminator': message['author']['discriminator'],
                            'avatar': message['author'].get('avatar')
                        },
                        'content': message.get('content', ''),
                        'timestamp': message['timestamp'],
                        'attachments': [a['url'] for a in message.get('attachments', [])],
                        'embeds': message.get('embeds', [])
                    })
                    new_messages += 1
                
                print(f"Completed scraping #{channel_name} - {channel_message_count} messages found, {new_messages} new messages, {invite_count} invite links")
                
                # Save periodically to avoid data loss
                if processed_channels % 5 == 0 or processed_channels == total_channels:
                    self.db.save()
                    print(f"Database saved (checkpoint)")
                
            except Exception as e:
                print(f"{Fore.RED}Error scraping channel #{channel_name}: {str(e)}{Style.RESET_ALL}")
                continue
        
        # Final save
        self.db.save()
        
        # Print final statistics
        print(f"\n{Fore.GREEN}=== Scraping Complete ==={Style.RESET_ALL}")
        print(f"Processed: {processed_channels}/{total_channels} channels")
        print(f"Total messages scraped: {total_messages}")
        print(f"Discord invite links found: {total_invite_links}")
        print(f"Data saved to {self.db.db_file}")
        
        return True