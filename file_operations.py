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
        ----------------------------------------------------------
        Printing nested dictionary as a key-value pair:
        ----------------------------------------------------------
        
                for i in data:
                    print("Username:", i['username'])
                    print("Password", i['password'])
                    print()
        
        ----------------------------------------------------------
        username, password are examples of values in the JSON file
        ----------------------------------------------------------    
        """
        return data


"""
Adds user with username, password to 'data.json'
Password and key will be base64 encoded before insertion
Password must be hashed before called as argument
"""
def add_user(username, password, filename='data.json'):

    # Searching for coincidences
    js  = json.load(open(filename))

    for user in js["users"]:
        if user["username"] == str(username):
            raise TypeError(str(username) + " is already used as a name account")
            break

    # Creating the dictionary

    password_b64 = b64encode(password).decode('utf-8')

    new_data = {"username": str(username), 
            "password": (password_b64)}

    with open(filename, 'r+') as file:
        # First we load existing data into a dictionary
        file_data = json.load(file)
        # Join new_data with file_data inside users
        file_data["users"].append(new_data)  # "users" is the domain where all users' data is stored
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)



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
    pass_database = []

    for account in data["users"]:
        user_database.append(account["username"])
        pass_database.append(b64decode(account["password"].encode('utf-8')))

    return user_database, pass_database



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

def add_message(message, account, filename='data.json'):

    b64message = b64encode(message).decode()
    new_data = {"sent_by": account[0], "msg": b64message}

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

"messages": [
        {
            "user1": "admin",
            "user2": "admin2",
            "init_vec": "iy23o8y4ow3iuho==",
            "hashed_key":"2972dhfioauhe3i2h=",
            "msg_data": [
                {
                    "sent_by": "admin",
                    "msg": "oiwuerioho8734yoig3287=="
                },
                {
                    "sent_by": "admin2",
                    "msg": "p9823y8og2o8t4=="
                }
            ]
        }
    ]

"""



