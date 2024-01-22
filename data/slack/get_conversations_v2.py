import time
from slack_sdk import WebClient
import os

slack_token = os.environ.get("SLACK_API_TOKEN")
client = WebClient(token=slack_token)
# Your channel ID (retrieved from previous calls or known)
channel_id = "C062GUWL0UB"

# Initialize to an empty string to fetch the first batch of messages
next_cursor = ""

# List to hold all fetched messages
all_messages = []

# Fetch messages as long as there are more to fetch (next_cursor is present)
while True:
    # Fetch a batch of messages
    response = client.conversations_history(channel=channel_id, cursor=next_cursor)
    
    # Check if the request was successful
    if response["ok"]:
        # Extract messages from the response and add them to the all_messages list
        messages = response['messages']
        all_messages.extend(messages)
        
        # Check for next_cursor to fetch next batch of messages
        response_metadata = response.get('response_metadata', {})
        next_cursor = response_metadata.get('next_cursor', '')
        
        # Break the loop if there's no next_cursor, meaning no more messages to fetch
        if not next_cursor:
            break
        
        # Optional: Sleep to avoid hitting Slack's rate limits
        time.sleep(1)
    else:
        print(f"Error: {response['error']}")
        break

# At this point, all_messages contains all the messages from the channel
print(f"Total messages fetched: {len(all_messages)}")
