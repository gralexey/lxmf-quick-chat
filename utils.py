from datetime import datetime
import RNS
import os
import sqlite3

def sanitize(p):
  p = p.replace("`=","")
  p = p.replace("`","")
  return p

def format_message_time(timestamp):
  msg_time = datetime.fromtimestamp(float(timestamp))
  now = datetime.now()
  if msg_time.date() == now.date():
      return msg_time.strftime("%H:%M")
  else:
      return msg_time.strftime("%d.%m.%Y %H:%M") 

def find_name(id_hash):
    if id_hash == None:
        return None
    identity = RNS.Identity.recall(bytes.fromhex(id_hash), from_identity_hash=True)
    if not identity:
        return
    pub_key = identity.get_public_key()
    for key in RNS.Identity.known_destinations:
        v = RNS.Identity.known_destinations[key]
        if v[2] == pub_key:
            ad = extract_name(key.hex()) if (len(v) > 3 and v[3]) else None
            if ad:
                return ad

def extract_name(dest_hash):
    if not dest_hash:
        return '?'
    dest = RNS.Identity.known_destinations.get(bytes.fromhex(dest_hash), None)
    if not dest:
        return '?'
    return ''.join(c for c in dest[3].decode('utf-8', errors='ignore') if c.isprintable())

def get_database_path():
    board_directory = "nomadnetwork"
    userdir = os.path.expanduser("~")

    if os.path.isdir("/etc/" + board_directory) and os.path.isfile("/etc/" + board_directory + "/config"):
        configdir = "/etc/" + board_directory
    else:
        configdir = userdir + "/." + board_directory

    storagepath = configdir + "/storage"
    if not os.path.isdir(storagepath):
        os.makedirs(storagepath)

    return storagepath + "/chat.db"

def initialize_db_if_needed():
    databasepath = get_database_path()
    
    if not os.path.isfile(databasepath):
        conn = sqlite3.connect(databasepath)
        cur = conn.cursor()
        query = "CREATE TABLE chat_messages (id INTEGER PRIMARY KEY AUTOINCREMENT, message TEXT, creator TEXT, sender_id TEXT, timestamp TEXT, deleted INTEGER DEFAULT 0)"
        cur.execute(query)
        conn.commit()
        conn.close()

def get_messages(page_size=100, offset=0):
    databasepath = get_database_path()
    conn = sqlite3.connect(databasepath)
    cur = conn.cursor()
    
    query = "SELECT COUNT(*) FROM chat_messages WHERE deleted = 0"
    cur.execute(query)
    messagecount = cur.fetchall()[0][0]
    
    query = "SELECT message, creator, sender_id, timestamp FROM chat_messages WHERE deleted = 0 ORDER BY timestamp DESC LIMIT ? OFFSET ?"
    cur.execute(query, (page_size, offset))
    message_records = cur.fetchall()
    
    conn.close()
    
    return messagecount, message_records

def insert_message(message, creator, sender_id, timestamp):
    databasepath = get_database_path()
    conn = sqlite3.connect(databasepath)
    cur = conn.cursor()
    
    query = "INSERT INTO chat_messages (message, creator, sender_id, timestamp) VALUES (?, ?, ?, ?)"
    cur.execute(query, (message, creator, sender_id, timestamp))
    conn.commit()
    conn.close()

databasepath = get_database_path()