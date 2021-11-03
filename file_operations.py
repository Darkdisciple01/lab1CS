import json
from base64 import b64encode, b64decode


"""
Reads 'data.json'
returns a dictionary

"""
def read_file():

    # Opening JSON file

    with open('data.json') as json_file:
        data = json.load(json_file)

        """
        Basic structure of the data.json file 
        -------------------------------------------
        {
        "users": [],
        "messages":[]
        }
        -------------------------------------------
        """
        return data


"""
Adds user with username, password to 'data.json'
Password and key will be base64 encoded before insertion
Password must be hashed before called as argument
"""
def add_user(username, salt, password, filename='data.json'):

    js  = json.load(open(filename))
    # Creating the dictionary
    
    salt_b64 = b64encode(salt).decode('utf-8')
    password_b64 = b64encode(password).decode('utf-8')

    new_data = {"username": str(username), "salt": salt_b64, "password": password_b64}

    with open(filename, 'r+') as file:
        # First we load existing data into a dictionary
        file_data = json.load(file)
        # Join new_data with file_data inside users
        file_data["users"].append(new_data)  # "users" is the domain where all users' data is stored
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
        if js["users"][i]["username"] == str(username):
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
        user_database.append(account["username"])
        salt_database.append(b64decode(account["salt"].encode('utf-8')))
        pass_database.append(b64decode(account["password"].encode('utf-8')))

    return user_database, salt_database, pass_database



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

def add_message(message, account, nonce, filename='data.json'):

    b64message = b64encode(message).decode()
    b64nonce = b64encode(nonce).decode()
    new_data = {"sent_by": account[0], "msg": b64message, "nonce": b64nonce}

    js = json.load(open(filename))

    index = -1

    for i in range(len(js["messages"])):
        if js["messages"][i]["user1"] == account[2]["user1"] and js["messages"][i]["user2"] == account[2]["user2"]:
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
def add_chat(account, username, salt, hashed_key, filename='data.json'):

    js = json.load(open(filename))

    b64salt = b64encode(salt).decode()
    b64hashed_key = b64encode(hashed_key).decode()

    new_data = {"user1": account[0], "user2": username, "salt": b64salt, "hashed_key": b64hashed_key, "msg_data":[]}

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
def delete_user(user, user_database):
    for other_user in user_database:
        remove_chat(user, other_user)
    remove_user(user)





"""

"messages": [
        {
            "user1": "admin",
            "user2": "admin2",
            "salt": "16byteso823y4o92hgog23"
            "hashed_key":"2972dhfioauhe3i2h=",
            "msg_data": [
                {
                    "sent_by": "admin",
                    "msg": "oiwuerioho8734yoig3287==",
                    "nonce": "ukyfu65ryvcg="
                },
                {
                    "sent_by": "admin2",
                    "msg": "p9823y8og2o8t4==",
                    "nonce": "lit7etrxtt87="
                }
            ]
        }
    ]

"""



