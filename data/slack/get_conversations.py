from slack_sdk import WebClient
import flytekit


token = flytekit.current_context().secrets.get("slack-api", "token")
client = WebClient(token=token)
# client.chat_postMessage(channel="demo", text="test")

response = client.conversations_list()
print("conversations_list:", response)
channels = response['channels']
demo_channel_id = next((c['id'] for c in channels if c['name'] == 'demo'), None)

if demo_channel_id is None:
    print("Channel 'demo' not found")
else:
    # Fetch messages from the "demo" channel
    messages = []
    cursor = None
    while True:
        response = client.conversations_history(channel=demo_channel_id, cursor=cursor)
        messages.extend(response['messages'])

        # Check if there's more data to fetch
        cursor = response['response_metadata']['next_cursor'] if 'response_metadata' in response else None
        if not cursor:
            break

    # Now, messages list contains all the messages from the "demo" channel
    for message in messages:
        print(message['text'])

    # If you need to handle the messages further, they are all in the `messages` list.
