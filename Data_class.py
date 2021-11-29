from base64 import b64encode, b64decode
import time

"""
Class for storing all program data locally during the code's execution

"""
class Data:
    root = ""

    t_username = ""
    t_priv = ""
    t_pub = ""
    t_user = []

    user_database = []
    pass_database = []
    salt_database = []

    c_chat = {}
    c_other = ""
    c_salt = ""
    c_key = ""

    userBox = None
    passBox = None
    confirm_passBox = None
    msgBox = None
    chatUsrBox = None

    time_counter = 0.01

    @staticmethod
    def login(user, privkey):
        Data.t_username = user[0]["username"]
        Data.t_priv = privkey
        Data.t_pub = b64decode(user[0]["pub"].encode())
        Data.t_user = user

    @staticmethod
    def get_boxes1():
        return Data.userBox, Data.passBox, Data.confirm_passBox

    @staticmethod
    def get_boxes2():
        return Data.msgBox

    @staticmethod
    def get_boxes3():
        return Data.chatUsrBox

    @staticmethod
    def get_databases():
        return Data.user_database, Data.pass_database, Data.salt_database

    @staticmethod
    def get_chatdata():
        return Data.c_chat, Data.c_other, Data.c_key

    @staticmethod
    def set_databases(userdb, passdb, saltdb):
        Data.user_database = userdb
        Data.pass_database = passdb
        Data.salt_database = saltdb

    @staticmethod
    def set_boxes(uBox, pBox, cpBox, mBox, cuBox):
        Data.userBox = uBox
        Data.passBox = pBox
        Data.confirm_passBox = cpBox
        Data.msgBox = mBox
        Data.chatUsrBox = cuBox

    @staticmethod
    def load_chat_data(chat):
        Data.c_chat = chat
        # chat must contain logged in user - logically enforced in code
        other = chat["user1"] if not chat["user1"] == Data.t_username else chat["user2"] 
        Data.c_other = other
        Data.c_salt = b64decode(chat["salt"].encode())

    @staticmethod
    def load_chat_key(key):
        Data.c_key = key
    
    @staticmethod
    def wait(reset = 0):
        if not reset:
            time.sleep(Data.time_counter)
            Data.time_counter *= 2
        else:
            Data.time_counter = 0.01

    @staticmethod
    def session_clear():
        Data.t_username = ""
        Data.t_priv = ""
        Data.t_pub = ""
        Data.t_user = []
        Data.c_chat = {}
        Data.c_other = ""
        Data.c_salt = ""
        Data.c_key = ""
        Data.userBox.clear()
        Data.passBox.clear()
        Data.confirm_passBox.clear()
        Data.msgBox.clear()
        Data.chatUsrBox.clear()



