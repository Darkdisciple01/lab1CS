exec(open("./lab_GUI.py").read())
from file_operations import *
from encryption_functions import *

#decrypt_file()

user_database, pass_database, key_database, init_vec_database = load_file_data()
account = []


"""
Main loop for GUI

"""


def mainfunc(seq):
    global userBox, passBox, user_database, pass_database, key_database, init_vec_database, account
    if seq == [1,88]:

        """On pressing |continue| to login"""

        username = userBox.get_val()
        password = passBox.get_val()

        if username not in user_database:
            Widgets.seq([0,3,15])
        else:
            # Gets index of username, checks passwords
            index = user_database.index(username)
            enc_password, n = aes_encrypt(password, key_database[index], init_vec_database[index])
            if not enc_password == pass_database[index]:
                Widgets.seq([0,3,16])
            account = [user_database[index], pass_database[index], key_database[index], init_vec_database[index]]
            print(account)

    if seq == [0,3,88]:

        """On pressing |continue| to create new user"""

        username = userBox.get_val()
        password = passBox.get_val()
        confirm = confirm_passBox.get_val()

        empty = bool(password == "" or username == "")

        if(password == confirm and not empty):
            key = Random.get_random_bytes(32)
            enc_password, init_vec = aes_encrypt(password, key)

            add_user(username, enc_password, key, init_vec)
            user_database, pass_database, key_database, init_vec_database = load_file_data()

            print("account created: " + str(username))
        elif empty:
            Widgets.seq([2,3,18])
        else:
            Widgets.seq([2,3,17])


    return



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
    print("Beginning Testing")

    username = "admin"
    password = "admin"

    #key = Random.get_random_bytes(32)
    #enc_password, init_vec = aes_encrypt(password, key)

    #add_user(username, enc_password, key, init_vec)

    remove_user("jswizz")


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


#encrypt_file()
