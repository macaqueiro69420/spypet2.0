import json
import os
from datetime import datetime

class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.messages = []
        self.load_existing_data()
    
    def load_existing_data(self):
        """Load existing data from the database file if it exists"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    self.messages = json.load(f)
                print(f"Loaded {len(self.messages)} existing messages from database")
            except Exception as e:
                print(f"Error loading database: {e}")
                self.messages = []
    
    def add_message(self, message_data):
        """Add a new message to the database"""
        self.messages.append(message_data)
    
    def save(self):
        """Save all messages to the database file"""
        try:
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(self.messages, f, indent=2, ensure_ascii=False)
            print(f"Successfully saved {len(self.messages)} messages to {self.db_file}")
            return True
        except Exception as e:
            print(f"Error saving database: {e}")
            return False
    
    def message_exists(self, message_id):
        """Check if a message already exists in the database"""
        return any(msg.get('id') == message_id for msg in self.messages)
    
    def get_latest_message_date(self, channel_id):
        """Get the date of the latest message for a channel"""
        channel_messages = [msg for msg in self.messages if msg.get('channel_id') == channel_id]
        if not channel_messages:
            return None
        
        # Find the message with the latest timestamp
        latest_message = max(channel_messages, key=lambda msg: msg.get('timestamp', 0))
        return latest_message.get('timestamp')
    
    def get_stats(self):
        """Get statistics about the database"""
        total_messages = len(self.messages)
        channels = set(msg.get('channel_id') for msg in self.messages)
        authors = set(msg.get('author_id') for msg in self.messages)
        
        return {
            'total_messages': total_messages,
            'unique_channels': len(channels),
            'unique_authors': len(authors),
            'last_updated': datetime.now().isoformat()
        }