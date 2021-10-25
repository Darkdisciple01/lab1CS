exec(open("./lab_GUI.py").read())
from file_operations import *
from encryption_functions import *

decrypt_file()

user_database, pass_database = load_account_data()
account = []
message_data = load_message_data()


"""
Main loop for GUI

"""


def mainfunc(seq):
    global userBox, passBox, user_database, pass_database, account, message_data
    if seq == [1,88]:

        """On pressing |continue| to login"""

        username = userBox.get_val()
        password = passBox.get_val()

        if username not in user_database:
            Widgets.seq([0,3,15])
        else:
            # Gets index of username, checks passwords
            index = user_database.index(username)
            hashed_password = sha256_hash(password.encode())
            if not hashed_password == pass_database[index]:
                Widgets.seq([0,3,16])
            else:
                account = [user_database[index], pass_database[index],{}]
                # Loads the user's chats
                chat_load(message_data, 2, account)
    

    if seq == [0,3,88]:

        """On pressing |continue| to create new user"""

        username = userBox.get_val()
        password = passBox.get_val()
        confirm = confirm_passBox.get_val()

        empty = bool(password == "" or username == "")

        if(password == confirm and not empty):
            if username in user_database:
                Widgets.seq([2,3,19])
            else:
                password = password.encode()
                hashed_password = sha256_hash(password)

                add_user(username, hashed_password)
                user_database, pass_database = load_account_data()

                print("account created: " + str(username))
        elif empty:
            Widgets.seq([2,3,18])
        else:
            Widgets.seq([2,3,17])


    if seq == [88,89]:

        """On pressing |send| to send a message"""

        password = get_password()

        if password == "":
            Widgets.seq(4)
        else:
            hashed_password = sha256_hash(password.encode())
            doubly_hashed_password = sha256_hash(hashed_password)

            compare_hash = b64decode(account[2]["hashed_key"])

            if not doubly_hashed_password == compare_hash:
                Widgets.seq([4,16])

            else:
                message = get_message()
                hashed_password = sha256_hash(password.encode())
                init_vec = b64decode(account[2]["init_vec"])

                enc_message, n = aes_encrypt(message, hashed_password, init_vec)
                add_message(enc_message, account) # account includes information on the chat
                
                message_data = load_message_data()
                reload_messages(account, hashed_password, init_vec)

        #reload messages (use function in lab_GUI.py)
        # - similar to other function

    if seq == [88,90]:

        """On pressing |New Chat| to create a new chat"""

        username, password = get_username()

        if username == "" or password == "":
            Widgets.seq(5)
        else:
            if not username in user_database:
                Widgets.seq([5,15])
            elif username == account[0]:
                Widgets.seq([5,20])
            else:
                # check if chat already exists
                flag = 0
                for chat in message_data:
                    if chat["user1"] == account[0] and chat["user2"] == username:
                        flag = 1
                        Widgets.seq([5,21])
                    if chat["user2"] == account[0] and chat["user1"] == username:
                        flag = 1
                        Widgets.seq([5,21])
                
                if flag == 0:
                    init_vec = Random.get_random_bytes(AES.block_size)
                    doubly_hashed_password = sha256_hash(sha256_hash(password.encode()))
                    add_chat(account, username, init_vec, doubly_hashed_password)
                    # reload chats
                    message_data = load_message_data()
                    chat_load(message_data, 2, account)
    
    if seq == [88,91]:

        """On pressing |Back| to leave a chat"""

        chat_load(load_message_data(), 2, account)




"""
Different operation modes
0 for GUI, 1 for Testing, 2 for Progress Display

"""


import sys
import time
x = (int)(sys.argv[1]) if (len(sys.argv)>1) else 0

if x == 0:
    print("Booting GUI")
    # initiation
    Widgets.seq([0, 3])
    root.mainloop()

if x == 1:
    root.withdraw()
    remove_chat("admin", "jon")

if x == 2:
    root.withdraw()
    print("Beginning Progress Display")
    print()
    key = Random.get_random_bytes(32)
    print("Generating key: " + str(key))
    print("Running AES Encrypt, please enter message to encrypt:")
    print()
    data = str(input())
    cipher_text, init_vec = aes_encrypt(data, key)
    time.sleep(2)
    print()
    print("Encrypted message: " + str(cipher_text))
    print()
    print("Attempting to decrypt message")
    new_data = aes_decrypt(key, cipher_text, init_vec)
    time.sleep(1)
    print()
    time.sleep(2)
    print("Decrypted message is: \"" + str(new_data) + "\"")
    print()


encrypt_file()
