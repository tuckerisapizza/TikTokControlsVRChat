from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent, ConnectEvent, GiftEvent, FollowEvent

from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server, udp_client

# FOR EASY SETUP, GO LIVE, REPLACE MY USERNAME WITH YOURS AND TOGGLE ON THE TTS COMPONENTS YOU WANT
username = "@creamsicletucky" # REPLACE THIS WITH YOURS (RUN AFTER YOU GO LIVE)

# Instantiate's objects
client: TikTokLiveClient = TikTokLiveClient(unique_id=username)


# the actual speaking words function
def sendmessages(message):
    
    client = udp_client.SimpleUDPClient("127.0.0.1", 9000)
    if message == "gift":
        client.send_message("/avatar/parameters/TiktokLive", 1)
    if message == "!hoodie":
        client.send_message("/avatar/parameters/TiktokLive", 2)
    if message == "!sweater":
        client.send_message("/avatar/parameters/TiktokLive", 3)
    if message == "!pants":
        client.send_message("/avatar/parameters/TiktokLive", 4)
    if message == "!harness":
        client.send_message("/avatar/parameters/TiktokLive", 5)
    if message == "!fishnets":
        client.send_message("/avatar/parameters/TiktokLive", 6)
      
     # SENDS DATA TO VRCHAT OVER PARAMS FOCUS, FOCUSLEFT AND FOCUSRIGHT
    
  


# Define how you want to handle specific events via decorator

@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    print("Connected to Room ID:", client.room_id)
    
# Notice no decorator?
@client.on(CommentEvent)
async def on_comment(event: CommentEvent):
    print(f"{event.user.unique_id} says {event.comment}")
    if not event.comment == "gift":
        sendmessages(event.comment)

    
    
@client.on(GiftEvent)
async def on_gift(event: GiftEvent):
    # Streakable gift & streak is over
    sendmessages("gift")
    if event.gift.streakable:
        print(f"{event.user.unique_id} sent x \"{event.gift.name}\"")
        
        
    # Non-streakable gift
    elif not event.gift.streakable:
        print(f"{event.user.unique_id} sent \"{event.gift.name}\"")
        
        
@client.on(FollowEvent)
async def on_follow(event: FollowEvent):
    print(f"@{event.user.unique_id} just followed!")
    # writetofile(event.user.unique_id + "\n")
    
    
     
# Define handling an event via a "callback"
client.add_listener("comment", on_comment)
client.add_listener("gift", on_gift)
client.add_listener("follow", on_follow)

if __name__ == '__main__':
    client.run()
