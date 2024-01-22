from slack_sdk import WebClient
import flytekit
"""
References:
slack conversation api: https://api.slack.com/methods/conversations.list
slack conversation history api: https://api.slack.com/methods/conversations.history

Channels:
1. Channel Name: demo
   - ID: C062E57C3CM
   - Created: 1698135166
   - Is Archived: False
   - Is General: False
   - Number of Members: 2
   - Purpose: This channel is for everything #demo. Hold meetings, share docs, and make decisions together with your team.
   - Creator: U063622JCSC

2. Channel Name: random
   - ID: C062GUWL0UB
   - Created: 1698134887
   - Is Archived: False
   - Is General: False
   - Number of Members: 2
   - Purpose: This channel is for... well, everything else. It’s a place for team jokes, spur-of-the-moment ideas, and funny GIFs. Go wild!
   - Creator: U063622JCSC

3. Channel Name: general
   - ID: C062VM35VSM
   - Created: 1698134886
   - Is Archived: False
   - Is General: True
   - Number of Members: 2
   - Purpose: This is the one channel that will always include everyone. It’s a great spot for announcements and team-wide conversations.
   - Creator: U063622JCSC

4. Channel Name: youtube-summary
   - ID: C063M7QD7HA
   - Created: 1698742728
   - Is Archived: False
   - Is General: False
   - Number of Members: 2
   - Purpose: [No purpose set]
   - Creator: U063622JCSC

"""

import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Your OAuth Access Token
slack_token = os.environ.get("SLACK_API_TOKEN")
# ID of the channel you want to send the message to
channel_id = "C062E57C3CM"

client = WebClient(token=slack_token)

try:
    # Call the conversations.history method using the built-in WebClient
    result = client.conversations_history(channel=channel_id)

    # Print message text
    messages = result["messages"]
    for message in messages:
        print(message["text"])

except SlackApiError as e:
    print(f"Error: {e.response['error']}")

# Store conversation history
conversation_history = []
# ID of the channel you want to send the message to
# channel_id = "C123ABC456"

try:
    # Call the conversations.history method using the WebClient
    # conversations.history returns the first 100 messages by default
    # These results are paginated, see: https://api.slack.com/methods/conversations.history
    result = client.groups_history(channel=channel_id)

    conversation_history = result["messages"]

    # Print results
    print("{} messages found in {}".format(len(conversation_history), channel_id))

except SlackApiError as e:
    print("Error creating conversation: {}".format(e))




# token = flytekit.current_context().secrets.get("slack-api", "token")
client = WebClient(token=token)
# client.chat_postMessage(channel="demo", text="test")

response = client.conversations_list()
print("conversations_list:", response)
channels = response['channels']
demo_channel_id = next((c['id'] for c in channels if c['name'] == 'demo'), None)

# if demo_channel_id is None:
#     print("Channel 'demo' not found")
# else:
#     # Fetch messages from the "demo" channel
#     messages = []
#     cursor = None
#     while True:
#         response = client.conversations_history(channel=demo_channel_id, cursor=cursor)
#         messages.extend(response['messages'])

#         # Check if there's more data to fetch
#         cursor = response['response_metadata']['next_cursor'] if 'response_metadata' in response else None
#         if not cursor:
#             break

#     # Now, messages list contains all the messages from the "demo" channel
#     for message in messages:
#         print(message['text'])

#     # If you need to handle the messages further, they are all in the `messages` list.
