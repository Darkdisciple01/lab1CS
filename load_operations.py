import json
from GUI_class import *
from Data_class import *
import database.file_operations as fop
import encryption_functions as ef
import cert_auth.certificate_authority as CA


"""
Loads chats and displays them on the screen
Upon selection of a chat, loads messages
no returns
"""

def chat_load():
    # loading all the chats on Widgets seq 100-108, data = json["messages"]
    username = Data.t_username
    data = fop.load_message_data()

    for i in range(100,109):
        Widgets.rem_seq(i)

    page = 100
    Widgets.add(100,Button("^",x=550,y=40,wide=70,com=[1,100]))

    # add a button for each chat
    new_button = ""
    i = 0
    for chat in data:
        if username == chat["user1"] or username == chat["user2"]:
            name = chat["user1"] if not chat["user1"] == username else chat["user2"]
            new_button = Button(name,x=40,y=75+65*(int(i)%5),wide=200,msgload=1,com= lambda chat=chat: msg_load(chat))
            new_button.configure(wide=35,high=1)
            Widgets.add(int(100+i/5),new_button)
            i+=1
            if not page == int(100+i/5):
                page += 1
                Widgets.rem_seq(page)
                Widgets.add(page-1,Button("v",x=550,y=350,wide=70,com=[1,page]))
                Widgets.add(page,Button("^",x=550,y=40,wide=70,com=[1,page-1]))
            if i >= 45:
                print("Please expand chat database")
                exit(-3)

    Widgets.add(page,Button("v",x=550,y=350,wide=70,com=[1,page]))

    # if no chats
    if i == 0:
        Widgets.add(100,Message("Sorry, you have no chats at this time",190,175,wide=200,fs=18))

    # display first page of chats
    Widgets.seq([100,1])




"""
Loads all messages in the chat provided
Verifies the validity of other user's account and Y value
"""
def msg_load(chat):
    new_message = Data.get_boxes2()
    Data.load_chat_data(chat)

    # calc value for key for Diffie Hellman
    a = int(CA.pem_to_hex(Data.t_priv, 128), 0)
    
    # validate other user's account with their signature
    other_account = fop.get_u(Data.c_other) 
    if other_account == -1:
        print("Could not find correspondant's account")
        exit(-9)

    material = json.dumps(other_account[0]).encode()
    signature = b64decode(other_account[1]["signature"].encode())
    if not CA.verify(material, signature):
        print("Correspondant's account could not be validated")
        chat_load()
        return

    Y_other = fop.get_Y(Data.c_other)

    # validate Y with other's public key
    other_pub = b64decode(other_account[0]["pub"].encode())
    material = str(Y_other).encode()
    signature = b64decode(other_account[0]["Y_signed"].encode())

    if not CA.verify(material, signature, other_pub):
        print("Correspondant's Y value could not be validated")
        exit(-9)

    shared_key = ef.generate_Y(a, Y_other)

    #turn shared_key into bytes
    salt = Data.c_salt
    key, s = ef.scrypt_pass(str(shared_key), salt)
    Data.load_chat_key(key)

    for i in range(110,130):
        Widgets.rem_seq(i)
    page = 110
    line = 50
    start = 1
    index = -1

    Widgets.add(110,Button("^",x=550,y=40,wide=70,com=[110]))
    js = json.load(open('database/data.json'))

    # create Text for each message
    for message in chat["msg_data"]:
        #decrypt text
        text = ef.aes_decrypt(key, b64decode(message["msg"]), b64decode(message["nonce"]))
        text = str(message["sent_by"]) + ": " + text

        #display operations
        lines = Text.get_lines(text)
        line_end = ((lines-1)*17 + 20 + line)
        if line_end > 310:
            Widgets.add(page,Button("v",x=550,y=350,wide=70,com=[page+1]))
            line = 50
            page += 1
            Widgets.add(page,Button("^",x=550,y=40,wide=70,com=[page-1]))
            if page > 129:
                print("Please expand message database")
                exit(-3)
        else:
            if start == 1:
                 start = 0
            else:
                line += 20

        Widgets.add(page,Text(text,10,line,wide=55,fs=12,highl=lines))
        line += (lines-1)*17


    Widgets.add(page,Button("v",x=550,y=350,wide=70,com=[page]))

    # chat interface generation
    name_string = "Chat with " + Data.c_other

    for j in range(110, page+1):
        Widgets.add(j,Button("Back",540,10,wide=40,fs=8,com=[88,91]))
        Widgets.add(j,Message(name_string, 210, 10, fs=20))
        Widgets.add(j,new_message)
        Widgets.add(j,Button("Send",460,350,wide=40,fs=8,com=[88,89]))

    # open chat on last page of text
    Widgets.seq([page])


   
