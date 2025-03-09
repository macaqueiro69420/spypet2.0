import requests
import re
import time
from colorama import Fore, Style

class DiscordAPI:
    """Class to interact directly with Discord API endpoints"""
    
    BASE_URL = "https://discord.com/api/v10"
    
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        # This regex matches discord.gg/xyz or discord.com/invite/xyz
        self.invite_pattern = re.compile(r'(discord\.com\/invite\/[a-zA-Z0-9-_]+|discord\.gg\/[a-zA-Z0-9-_]+)')
    
    def _request(self, method, endpoint, params=None, data=None, rate_limit_retry=True):
        """Make a request to Discord API with rate limit handling"""
        url = f"{self.BASE_URL}{endpoint}"
        
        response = requests.request(
            method,
            url,
            headers=self.headers,
            params=params,
            json=data
        )
        
        # Handle rate limiting
        if response.status_code == 429 and rate_limit_retry:
            retry_after = response.json().get('retry_after', 1)
            print(f"{Fore.YELLOW}Rate limited. Waiting {retry_after} seconds...{Style.RESET_ALL}")
            time.sleep(retry_after + 0.5)  # Add a small buffer
            return self._request(method, endpoint, params, data)
        
        # Handle other errors
        if not response.ok:
            print(f"{Fore.RED}Error {response.status_code}: {response.text}{Style.RESET_ALL}")
            return None
        
        # Return JSON data if available, otherwise return the response
        try:
            return response.json()
        except:
            return response
    
    def get_current_user(self):
        """Get the current user (me) details"""
        return self._request("GET", "/users/@me")
    
    def get_guild(self, guild_id):
        """Get details about a guild/server"""
        return self._request("GET", f"/guilds/{guild_id}")
    
    def get_guild_channels(self, guild_id):
        """Get all channels in a guild/server"""
        return self._request("GET", f"/guilds/{guild_id}/channels")
    
    def get_channel(self, channel_id):
        """Get details about a channel"""
        return self._request("GET", f"/channels/{channel_id}")
    
    def get_messages(self, channel_id, limit=100, before=None):
        """Get messages from a channel with pagination support"""
        params = {"limit": limit}
        if before:
            params["before"] = before
        
        return self._request("GET", f"/channels/{channel_id}/messages", params=params)
    
    def get_all_messages(self, channel_id, progress_callback=None):
        """Fetch all messages from a channel using pagination"""
        all_messages = []
        last_id = None
        invite_count = 0
        
        while True:
            # Get a batch of messages
            messages = self.get_messages(channel_id, limit=100, before=last_id)
            
            # If no messages or API error, break the loop
            if not messages or len(messages) == 0:
                break
                
            # Process messages (check for invites)
            for message in messages:
                # Check for invite links
                if message.get('content'):
                    invite_links = self.invite_pattern.findall(message['content'])
                    if invite_links:
                        invite_count += len(invite_links)
                        channel_name = f"Channel ID: {channel_id}"
                        print(f"{Fore.RED}Invite link found in {channel_name}:{Style.RESET_ALL}")
                        print(f"Author: {message['author']['username']} ({message['author']['id']})")
                        print(f"Content: {message['content']}")
                        print(f"Timestamp: {message['timestamp']}")
                        print(f"Links: {', '.join(invite_links)}\n")
            
            # Add this batch to our collection
            all_messages.extend(messages)
            
            # Call progress callback if provided
            if progress_callback:
                progress_callback(len(all_messages))
            
            # If we got fewer messages than the limit, we're at the end
            if len(messages) < 100:
                break
                
            # Update the last_id for pagination
            last_id = messages[-1]['id']
            
            # Small delay to avoid hitting rate limits too hard
            time.sleep(0.5)
        
        return all_messages, invite_count