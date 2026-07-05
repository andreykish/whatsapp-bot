from neonize.client import NewClient
from neonize.events import ConnectedEv, MessageEv, event
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_http():
    port = int(os.getenv("PORT", 8000))
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()

Thread(target=run_http, daemon=True).start()

# дальше запускаешь своего neonize-бота

client = NewClient("my_bot")
banned_words = ["fuck", "shit", "motherfucker", "блять", "хуй", "жопа", "сука"]


@client.event(ConnectedEv)
def on_connected(client: NewClient, evt: ConnectedEv):
    print("connected")


@client.event(MessageEv)
def on_message(client: NewClient, evt: MessageEv):
    global banned_words
    text = evt.Message.conversation or ""
    sender = client.get_pn_from_lid(evt.Info.MessageSource.Sender)
    if "/addbannedword" in text.lower():
        parameters = text.split(",")
        if parameters[2] == "8396":
            banned_words.append(parameters[1].strip())
            print(banned_words)

    if "/removebannedword" in text:
        parameters = text.split(",")
        if parameters[2] == "8396":
            banned_words.remove(parameters[1])

    for word in banned_words:
        if word.lower() in text.lower():
            client.revoke_message(
                evt.Info.MessageSource.Chat,
                evt.Info.MessageSource.Sender,
                evt.Info.ID
                )


client.connect()
event.wait()
