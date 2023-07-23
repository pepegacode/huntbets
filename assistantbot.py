import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events
import key
 
  
# get your api_id, api_hash, token
# from telegram as described above
api_id = key.api_id
api_hash = key.api_hash
token = key.botkey2
message = "/addteam"
 
# your phone number
phone = key.phone
  
# creating a telegram session and assigning
# it to a variable client
client = TelegramClient('session', api_id, api_hash)
  
# connecting and building the session
client.connect()
 
# in case of script ran first time it will
# ask either to input token or otp sent to
# number or sent or your telegram id
if not client.is_user_authorized():
  
    client.send_code_request(phone)
     
    # signing in the client
    client.sign_in(phone, input('Enter the code: '))
  
  
try:
    # receiver user_id and access_hash, use
    # my user_id and access_hash for reference
    dest_name = key.botname
    dest = client.get_entity(dest_name)
    
 
    # sending message using telegram client
    client.send_message(dest, message, parse_mode='html')
except Exception as e:
     
    # there may be many error coming in while like peer
    # error, wrong access_hash, flood_error, etc
    print(e)
 
# disconnecting the telegram session
client.disconnect()

