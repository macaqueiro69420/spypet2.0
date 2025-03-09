import discord
import asyncio
import re
import json
import datetime
from colorama import Fore, Style, init
from database import Database

# Initialize colorama for colored console output
init()

class DiscordScraper(discord.Client):
    def __init__(self, server_id, database_file, *args, **kwargs):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(intents=intents, *args, **kwargs)
        
        self.server_id = server_id
        self.db = Database(database_file)
        self.invite_pattern = re.compile(r'(discord\.com\/invite\/[a-zA-Z0-9-_]+|discord\.gg\/[a-zA-Z0-9-_]+)')

    async def on_ready(self):
        print(f"{Fore.GREEN}Logged in as {self.user} ({self.user.id}){Style.RESET_ALL}")
        print(f"Starting to scrape messages from server ID: {self.server_id}")
        
        # Start the scraping process
        await self.scrape_server()
        
        # After scraping is done, exit the bot
        await self.close()

    async def scrape_server(self):
        # Get the server object
        server = self.get_guild(self.server_id)
        
        if not server:
            print(f"{Fore.RED}Error: Could not find server with ID {self.server_id}{Style.RESET_ALL}")
            return
        
        print(f"{Fore.CYAN}Starting to scrape server: {server.name}{Style.RESET_ALL}")
        
        # Get all channels in the server
        channels = [channel for channel in server.channels if isinstance(channel, discord.TextChannel)]
        print(f"Found {len(channels)} text channels to scrape")
        
        # Track statistics
        total_channels = len(channels)
        processed_channels = 0
        total_messages = 0
        invite_links_found = 0
        
        # Start scraping each channel
        for channel in channels:
            try:
                channel_messages, channel_invites = await self.scrape_channel(channel)
                total_messages += channel_messages
                invite_links_found += channel_invites
                processed_channels += 1
                
                # Save periodically to avoid data loss
                if processed_channels % 5 == 0 or processed_channels == total_channels:
                    self.db.save()
                    
                print(f"{Fore.CYAN}Progress: {processed_channels}/{total_channels} channels processed {Style.RESET_ALL}")
                
            except discord.Forbidden:
                print(f"{Fore.YELLOW}No access to channel #{channel.name}{Style.RESET_ALL}")
                processed_channels += 1
            except Exception as e:
                print(f"{Fore.RED}Error scraping channel #{channel.name}: {e}{Style.RESET_ALL}")
                processed_channels += 1
        
        # Final save
        self.db.save()
        
        # Print final statistics
        print(f"\n{Fore.GREEN}=== Scraping Complete ==={Style.RESET_ALL}")
        print(f"Processed: {processed_channels}/{total_channels} channels")
        print(f"Total messages scraped: {total_messages}")
        print(f"Discord invite links found: {invite_links_found}")

    async def scrape_channel(self, channel):
        print(f"\nScraping channel: #{channel.name} (ID: {channel.id})")
        
        message_count = 0
        invite_count = 0
        
        # Get messages in batches of 100 (Discord API limit)
        try:
            async for message in channel.history(limit=None, oldest_first=False):
                # Skip if message already exists in database
                if self.db.message_exists(message.id):
                    continue
                
                # Convert message to storable format
                message_data = {
                    'id': message.id,
                    'channel_id': channel.id,
                    'channel_name': channel.name,
                    'author_id': message.author.id,
                    'author_name': message.author.name,
                    'content': message.content,
                    'timestamp': message.created_at.isoformat(),
                    'attachments': [att.url for att in message.attachments],
                    'embeds': [embed.to_dict() for embed in message.embeds]
                }
                
                # Check for Discord invite links
                invite_links = self.invite_pattern.findall(message.content)
                if invite_links:
                    invite_count += len(invite_links)
                    print(f"{Fore.RED}Invite link found in #{channel.name}:{Style.RESET_ALL}")
                    print(f"Author: {message.author.name} ({message.author.id})")
                    print(f"Content: {message.content}")
                    print(f"Timestamp: {message.created_at.isoformat()}")
                    print(f"Links: {', '.join(invite_links)}\n")
                
                # Add to database
                self.db.add_message(message_data)
                message_count += 1
                
                # Simple progress indicator
                if message_count % 100 == 0:
                    print(f"  - {message_count} messages scraped from #{channel.name}")
                
        except discord.Forbidden:
            print(f"{Fore.YELLOW}No access to read message history in #{channel.name}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error reading messages from #{channel.name}: {e}{Style.RESET_ALL}")
        
        print(f"Completed scraping #{channel.name} - {message_count} messages scraped, {invite_count} invite links found")
        return message_count, invite_count