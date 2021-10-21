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



def load_file_data():
    data = read_file()

    user_database = []
    pass_database = []

    for account in data["users"]:
        user_database.append(account["username"])
        pass_database.append(b64decode(account["password"].encode('utf-8')))

    return user_database, pass_database






"""
def add_user(username, password, key, init_vec, filename='data.json'):

    # Searching for coincidences
    js  = json.load(open(filename))

    for user in js["users"]:
        if user["username"] == str(username):
            raise TypeError(str(username) + " is already used as a name account")
            break

    # Creating the dictionary

    password_b64 = b64encode(password).decode('utf-8')
    key_b64 = b64encode(key).decode('utf-8')
    init_vec_b64 = b64encode(init_vec).decode('utf-8')

    new_data = {"username": str(username),
            "password": (password_b64), "key": (key_b64), "init_vec": (init_vec_b64)}

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


