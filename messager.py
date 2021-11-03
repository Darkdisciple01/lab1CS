exec(open("./lab_GUI.py").read())
from file_operations import *
from encryption_functions import *
from backup_protocol import *


corruption = check_corruption(root = root)
if corruption == 0:
    exit(0)


user_database, pass_database = load_account_data()
account = []
message_data = load_message_data()


"""
Main loop for GUI

GUI operates by displaying one or multiple pages of "Widget"s
Upon the pressing of a button, different pages can be displayed
Since the GUI operates in a loop, we must intercept the loop to perform operations

Parameters: pages displayed, in list format
Performs operations based on the pages displayed
No returns

"""


def mainfunc(seq):
    global userBox, passBox, user_database, pass_database, account, message_data
    if seq == [1,88]:

        """
        On pressing |continue| to login
        Parameters: gets values of username and password boxes
        Checks if user is in database with entered password, if so, logs in, otherwise displays
          the relevant error message
        """

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
                # hashed passwords match, load account
                account = [user_database[index], pass_database[index],{}]
                # Loads the user's chats
                chat_load(message_data, 2, account)
    

    if seq == [0,3,88]:

        """
        On pressing |continue| to create new user
        Parameters: gets values of username, password, and confirm password boxes
        Ensures proper format and no repeated username, then creates an account. Includes
          error handling
        """

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

        """
        On pressing |send| to send a message
        Parameters: user-entered password, message in message box
        Checks validity of password, adds message to current chat
        """

        password = get_password() # returns password, clears password field box

        if password == "":
            Widgets.seq(4) # ask for password
        else:
            hashed_password = sha256_hash(password.encode())
            doubly_hashed_password = sha256_hash(hashed_password)

            compare_hash = b64decode(account[2]["hashed_key"]) # account[2] stores current chat

            # ensures password is correct
            if not doubly_hashed_password == compare_hash:
                Widgets.seq([4,16])

            # if password is correct, encrypts message and adds message into the chat
            else:
                message = get_message()
                hashed_password = sha256_hash(password.encode())

                enc_message, nonce = aes_encrypt(message, hashed_password)
                add_message(enc_message, account, nonce) # account includes information on the chat
                
                message_data = load_message_data()
                reload_messages(account, hashed_password)



    if seq == [88,90]:

        """
        On pressing |New Chat| to create a new chat
        Parameters: gets name of who to chat with, password of new chat
        Creates new chat between user logged in and user specified. Chat password
          is created from input specified password.
        """

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
                    doubly_hashed_password = sha256_hash(sha256_hash(password.encode()))
                    add_chat(account, username, doubly_hashed_password)
                    # reload chats
                    message_data = load_message_data()
                    chat_load(message_data, 2, account)
    
    if seq == [88,91]:

        """
        On pressing |Back| to leave a chat
        No parameters
        Reloads chats to update the current chat. This supports the (encrypted) message
          data staying within the data of the chat button
        """

        chat_load(load_message_data(), 2, account)




"""
Different operation modes
0,NULL for GUI, 1 for Testing
"""

import sys
x = (int)(sys.argv[1]) if (len(sys.argv)>1) else 0

if x == 0:
    print("Booting GUI")
    # initiation
    Widgets.seq([0, 3])
    root.mainloop()

if x == 1:
    root.withdraw()
    remove_chat("a","j") 

add_backup()


