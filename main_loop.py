from setup_GUI import *
from load_operations import *


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
    if seq == [1,88]:

        """
        On pressing |continue| to login
        Parameters: gets values of username and password boxes
        Checks if user is in database with entered password, if so, logs in, otherwise displays
          the relevant error message
        """

        userBox, passBox, confirm_passBox = Data.get_boxes1()
        user_database, pass_database, salt_database = Data.get_databases()

        username = userBox.get_val()
        password = passBox.get_val()

        if username not in user_database:
            # incorrect username
            Widgets.seq([0,3,15])
        else:
            # Gets index of username, checks passwords
            index = user_database.index(username)
            passkey, s = ef.scrypt_pass(password, salt_database[index])
            hashed_passkey = ef.sha256_hash(passkey)

            if not hashed_passkey == pass_database[index]:
                # incorrect password
                Widgets.seq([0,3,16])
            else:
                # verifying account with signature
                data = fop.read_file()
                account = data["users"][index]
                material = json.dumps(account[0]).encode()
                signature = b64decode(account[1]["signature"].encode())
                if CA.verify(material, signature):
                    # hashed passwords match, account is verified, load account
                    # calculate the private key
                    enc_priv = b64decode(account[0]["enc_priv"].encode())
                    nonce = b64decode(account[0]["nonce"].encode())
                    priv = ef.aes_decrypt(passkey, enc_priv, nonce)
                    # load into Data class
                    Data.login(account, priv)
                    # Loads the user's chats (load_operations)
                    chat_load()
                else:
                    # verification error
                    Widgets.seq([0,3,22])
    

    if seq == [0,3,88]:

        """
        On pressing |continue| to create new user
        Parameters: gets values of username, password, and confirm password boxes
        Ensures proper format and no repeated username, then creates an account. Includes
          error handling
        """

        userBox, passBox, confirm_passBox = Data.get_boxes1()
        user_database = Data.get_databases()[0]

        username = userBox.get_val()
        password = passBox.get_val()
        confirm = confirm_passBox.get_val()

        empty = bool(password == "" or username == "")

        # if passwords match and are something
        if(password == confirm and not empty):
            if username in user_database:
                # error for matching usernames
                Widgets.seq([2,3,19])
            else:
                # create new account
                passkey, salt = ef.scrypt_pass(password)
                priv, pub = CA.generate_key_pair()
                enc_priv, nonce = ef.aes_encrypt(priv.decode('utf-8'), passkey)
                priv_int = int(CA.pem_to_hex(priv, 128), 0)
                Y = ef.generate_Y(priv_int)
                Y_signed = CA.sign(str(Y).encode(), priv)
                enc_priv, nonce = ef.aes_encrypt(priv.decode('utf-8'), passkey)
                hashed_passkey = ef.sha256_hash(passkey)
               
                fop.add_user(username, salt, hashed_passkey, pub, enc_priv, nonce, Y, Y_signed)
                fop.load_account_data()

        elif empty:
            # one of the fields is empty
            Widgets.seq([2,3,18])
        else:
            # passwords don't match
            Widgets.seq([2,3,17])


    if seq == [88,89]:

        """
        On pressing |send| to send a message
        Parameters: user-entered password, message in message box
        adds message to current chat
        """
        key = Data.get_chatdata()[2]

        message = get_message()

        enc_message, nonce = ef.aes_encrypt(message, key)
        fop.add_message(enc_message, nonce) # account includes information on the chat
                
        chat = fop.get_chat(Data.t_username, Data.c_other)
        if chat == -1:
            print("MAJOR LOGICAL ERROR IN load_chat")
            exit(-6)
        
        msg_load(chat)



    if seq == [88,90]:

        """
        On pressing |New Chat| to create a new chat
        Parameters: gets name of who to chat with, password of new chat
        Creates new chat between user logged in and user specified. Chat password
          is created from input specified password.
        """

        username = get_username()
        user_database = Data.get_databases()[0]

        if username == "":
            Widgets.seq(5)
        else:
            if not username in user_database:
                Widgets.seq([5,15])
            elif username == Data.t_username:
                Widgets.seq([5,20])
            else:
                # check if chat already exists
                flag = fop.get_chat(username, Data.t_username)
                if flag == -1:
                    x, salt = ef.scrypt_pass("only_using_salt")
                    fop.add_chat(username, salt)
                    # reload chats
                    chat_load()
                    msg_load(fop.get_chat(username, Data.t_username))
                else:
                    Widgets.seq([5,21])


    if seq == [88,91]:

        """
        On pressing |Back| to leave a chat
        No parameters
        Reloads chats to update the current chat. This supports the (encrypted) message
          data staying within the data of the chat button
        """

        chat_load()

    
    if seq == [88,92]:
        
        """
        On pressing Logout to log out
        clears Data class and brings user to login page
        """
        
        Data.session_clear()
        Widgets.seq([0,3])




