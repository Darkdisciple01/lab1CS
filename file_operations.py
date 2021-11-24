import json
from base64 import b64encode, b64decode
import cert_auth.certificate_authority as CA
from Data_class import *
from datetime import date


"""
Reads 'data.json'
returns a dictionary

"""
def read_file():
    # Opening JSON file
    with open('data.json') as json_file:
        data = json.load(json_file)
        return data


"""
Adds user with username to 'data.json'
Description of arguments:
  username: name of user to be added
  salt: salt used in key derivation
  password: hashed with sha256 after using scrypt
  pub: public key
  enc_priv: private key encrypted with AES
  nonce: nonce used in encrypting private key
  Y: g^a mod p, intermediate step in diffie hellman associated with the private key
  Y_signed: signature of Y, to prevent impersonation attacks in chat
For variables which it is necessary, base64 encoding will be performed
"""
def add_user(username, salt, password, pub, enc_priv, nonce, Y, Y_signed, filename='data.json'):
    
    js  = json.load(open(filename))
    # Creating the dictionary
    
    salt_b64 = b64encode(salt).decode('utf-8')
    password_b64 = b64encode(password).decode('utf-8')
    pub_b64 = b64encode(pub).decode('utf-8')
    enc_priv_b64 = b64encode(enc_priv).decode('utf-8')
    nonce_b64 = b64encode(nonce).decode('utf-8')
    Y_signed_b64 = b64encode(Y_signed).decode('utf-8')

    new_data = {"username": str(username), "salt": salt_b64, "password": password_b64, "enc_priv": enc_priv_b64, "pub": pub_b64, "nonce": nonce_b64, "Y": Y, "Y_signed": Y_signed_b64}

    signature = CA.sign(json.dumps(new_data).encode())
    signature_b64 = b64encode(signature).decode('utf-8')
    todays_date = date.today().strftime("%m/%d/%y")

    new_data2 = {"name": str(username), "signature": signature_b64, "authority": "ROOT", "date_created": todays_date}

    union = [0,0]
    union[0] = new_data
    union[1] = new_data2

    with open(filename, 'r+') as file:
        # First we load existing data into a dictionary
        file_data = json.load(file)
        # Join new_data with file_data inside users
        file_data["users"].append(union)  # "users" is the domain where all users' data is stored
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)

"""
Finds and removes user with given username
"""
def remove_user(username, filename='data.json'):

    js  = json.load(open("data.json"))

    # Iterate through the objects in the JSON and pop (remove)
    # the obj once we find it.
    for i in range(len(js["users"])):
        flag = 1
        if js["users"][i][0]["username"] == str(username):
            js["users"].pop(i)
            flag = 0
            break
    if flag == 1:
        raise TypeError(str(username) + " not found in database")

    with open(filename, 'r+') as file:
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(js, file, indent=4)
        file.truncate()


"""
returns databases for "users" part of data
each index of either database represents a user
"""
def load_account_data():
    data = read_file()

    user_database = []
    salt_database = []
    pass_database = []

    for account in data["users"]:
        user_database.append(account[0]["username"])
        salt_database.append(b64decode(account[0]["salt"].encode('utf-8')))
        pass_database.append(b64decode(account[0]["password"].encode('utf-8')))

    Data.set_databases(user_database, pass_database, salt_database)



"""
returns "messages" part of data
"""
def load_message_data():
    data = read_file()
    return data["messages"]





"""
adds message to the chat opened in "account"
message must be encrypted
"""

def add_message(message, nonce, filename='data.json'):

    b64message = b64encode(message).decode()
    b64nonce = b64encode(nonce).decode()
    new_data = {"sent_by": Data.t_username, "msg": b64message, "nonce": b64nonce}

    js = json.load(open(filename))
    index = -1

    chat = Data.c_chat

    for i in range(len(js["messages"])):
        if js["messages"][i]["user1"] == chat["user1"] and js["messages"][i]["user2"] == chat["user2"]:
            index = i

    if not index == -1:
        with open(filename, 'r+') as file:
            # First we load existing data into a dictionary
            file_data = json.load(file)
            # Join new_data with file_data inside users
            file_data["messages"][index]["msg_data"].append(new_data)  # "users" is the domain where all users' data is stored
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent=4)
    else:
        print("error adding message to database, chat not found")
    

"""
creates a new chat with given specifications
key must already be hashed
"""
def add_chat(username, salt, filename='data.json'):

    js = json.load(open(filename))
    salt_b64 = b64encode(salt).decode()

    new_data = {"user1": Data.t_username, "user2": username, "salt": salt_b64, "msg_data":[]}
    Data.load_chat_data(new_data)

    with open(filename, 'r+') as file:
        # First we load existing data into a dictionary
        file_data = json.load(file)
        # Join new_data with file_data inside users
        file_data["messages"].append(new_data)  # "users" is the domain where all users' data is stored
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)



"""
Deletes the chat between user1 and user2, if it exists

"""
def remove_chat(user1, user2, filename = 'data.json'):

    js = json.load(open(filename))

    index = -1

    for i in range(len(js["messages"])):
        if js["messages"][i]["user1"] == user1 and js["messages"][i]["user2"] == user2:
            index = i
        if js["messages"][i]["user1"] == user2 and js["messages"][i]["user2"] == user1:
            index = i

    if index >= 0:
        with open(filename, 'r+') as file:
            # First we load existing data into a dictionary
            file_data = json.load(file)
            # Join new_data with file_data inside users
            file_data["messages"].pop(index)  # "users" is the domain where all users' data is stored
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent=4)
            file.truncate()




"""
Removes the user from the database and deletes all of his current chats

"""
def delete_user(user):
    user_database = Data.user_database
    for other_user in user_database:
        remove_chat(user, other_user)
    remove_user(user)



"""
Gets and returns Y value from specified username
"""
def get_Y(username):
    users = read_file()["users"]
    for user in users:
        if user[0]["username"] == username:
            return user[0]["Y"]
    return -1


"""
Finds chat corresponding to two usernames
returns chat
"""
def get_chat(user1, user2):
    chats = load_message_data()
    ret = -1
    for chat in chats:
        if chat["user1"] == user1 and chat["user2"] == user2:
            ret = chat
        if chat["user2"] == user1 and chat["user1"] == user2:
            ret = chat
    return ret








