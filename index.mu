#!/usr/bin/python
print("#!c=0")

import os
import secrets
from datetime import datetime
from utils import sanitize, format_message_time, find_name, initialize_db_if_needed, get_messages, insert_message, check_if_message_exists
from customizations import chat_name as custom_chat_name, footer as footer
import RNS

RNS.Reticulum()
RNS.Identity.load_known_destinations()

chat_name = custom_chat_name()
page_size = 100

initialize_db_if_needed()

id_hash = None
passed_name = ''
message_payload = None
inserting_message_nonce = None
nonce = None
for e in os.environ:
  if e == "remote_identity":
    id_hash = os.environ[e]
  if e == "field_messagepayload":
    message_payload = os.environ[e]
  if e == "field_namepayload":
    passed_name = os.environ[e]
  if e == "var_nonce":
    nonce = os.environ[e]
      
username = find_name(id_hash)
    
print("`r" + datetime.now().strftime("%A, %B %d, %Y - %H:%M"))

if id_hash == None:
  print("")
else:
  short_id_hash = id_hash[:8]
  namePart = f' ({username})' if username else ''
  print("Identified as " + short_id_hash + namePart)
  print("")

print("`!`F222`B7FD")
print('-~')
print('`c' + chat_name)
print('-~')
print('`a`b`f')
print("")

inserting_message_ts = None

if message_payload:
    message_payload = message_payload.strip()
    if len(message_payload) > 500: 
        message_payload = message_payload[:500] + "<message truncated>"
    
    if message_payload != "":
        if not check_if_message_exists(nonce):
          name_to_save = passed_name if passed_name else username
          inserting_message_ts = str(datetime.now().timestamp())
          new_message_id = nonce
          insert_message(new_message_id, message_payload, name_to_save, id_hash, inserting_message_ts)

message_count, message_records = get_messages(page_size, 0)

print("`F8ffRecent Messages:`f")
print("``")
print("")

if len(message_records) == 0:
    print("No messages yet. Be the first to chat!\n")
else:
    for message_record in reversed(message_records): 
        print("``")
        
        sent_at = format_message_time(message_record[3])
        name = message_record[1]
        sender_id = message_record[2]
        text = sanitize(message_record[0])
        
        print(f'`F8ff`!\\[{sent_at}]: `Ffff{name}: ``{text}')

print("``")
print("")

if username:
  initial_name = username
else:
  initial_name = passed_name if passed_name else "Guest"
  
print(f'`FfffName: `B333`<15|namepayload`{initial_name}>`` `FfffMessage: `B333`<50|messagepayload`>`` `Ffff`[SEND`:/page/index.mu`namepayload|messagepayload|nonce={secrets.token_hex(16) }]`f')

print(footer())
