from slack_sdk import WebClient
import flytekit


token = flytekit.current_context().secrets.get("slack-api", "token")
client = WebClient(token=token)
client.chat_postMessage(channel="demo", text="test")

