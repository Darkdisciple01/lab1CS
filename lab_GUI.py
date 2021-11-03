import tkinter as tk

"""
_________________________________________________________________

TKINTER VARIABLES
_________________________________________________________________
"""

backgroundColor = 'gray16'
defaultFontColor = 'gray84'

widgets = []
root = tk.Tk()

#dim = [root.winfo_screenwidth(),root.winfo_screenheight()]
dim = [600, 400]

halfx=dim[0]/2
halfy=dim[1]/2

root.geometry(str(dim[0])+"x"+str(dim[1]))
root.configure(background=backgroundColor)
root.wm_title("")

account = []



"""
_________________________________________________________________

TKINTER CLASSES
_________________________________________________________________
"""

"""
The Widget class is designed to more easily customize and initialize widgets from Tkinter. Widgets are placed at inputs x and y.
Each of its children correspond to a data type in the Tkinter library
"""

class Widget:
    global root,backgroundColor,defaultFontColor
    def __init__(self, widget, frame, x, y):
        self.data = [0,0]
        self.data=[widget,frame,x,y,0]

    def place(self):
        #print("trying to place message" if self.data[4]==0 else "trying to print button") 
        self.data[1].place(x=self.data[2],y=self.data[3])
        self.data[0].pack()

    def forget(self):
        self.data[0].pack_forget()
        self.data[1].place_forget()


class Message(Widget):
    def __init__(self, text, x, y, wide=200, high=40, fs=14, color="lightgray"):
        frame = tk.Frame(root,bg=backgroundColor,width=wide,height=high,highlightbackground=color)
        msg = tk.Message(frame, text=text, width=wide,bg=backgroundColor,fg=defaultFontColor)
        msg.configure(font=("Times "+str(fs)))
        super().__init__(msg, frame, x, y)


class Button(Widget):
    def __init__(self, text, x, y, msgload=0, com=0, wide=200, high=40, fs=14, color="lightgray"):
        frame = tk.Frame(root,bg=backgroundColor,width=wide,height=high,highlightbackground=color)
        if msgload == 0:
            btn = tk.Button(frame, text=text,bg="gray",fg=defaultFontColor,command= lambda: Widgets.seq(com))
        else:
            btn = tk.Button(frame, text=text,bg="gray",fg=defaultFontColor,command= lambda: chat_load(com, msgload-1))
        btn.configure(font=("Roboto "+str(fs)))
        super().__init__(btn, frame, x, y)

    def configure(self, wide, high):
        self.data[0].configure(width=wide, height=high)


class Input_Box(Widget):
    def __init__(self, x, y, hidden=0, entry_var="", wide=200, high=40, fs=14, color="lightgray"):
        frame = tk.Frame(root,bg=backgroundColor,width=wide,height=high,highlightbackground=color)
        entry_var=tk.StringVar()
        entry = tk.Entry(frame, textvariable=entry_var)
        entry.configure(font=("Times "+str(fs)))
        if(hidden):
            entry.configure(show="*")
        super().__init__(entry, frame, x, y)
        self.data.append(entry_var)

    def configure(self, wide):
        self.data[0].configure(width=wide)

    def get_val(self):
        return self.data[5].get()

    def clear(self):
        self.data[5].set("")


class Text(Widget):
    def __init__(self, text, x, y, wide=200, high=40, fs=14, color="lightgray", highl=2):
        frame = tk.Frame(root,bg=backgroundColor,width=wide,height=high,highlightbackground=color)
        txt = tk.Text(frame,width=wide, height=highl, bg=backgroundColor,fg=defaultFontColor,highlightthickness=0,borderwidth=0)
        txt.insert(tk.END, text)
        txt.configure(font=("Helvetica "+str(fs)))
        super().__init__(txt, frame, x, y)


"""
The Widgets class organizes and calls on "events" or different pages. The home page is denoted as page 0. The seq function accepts input of either a single number or an array of numbers, and runs those pages on the screen.
"""


class Widgets:
    global widgets,root
    currentSeq =[0]
    def __init__(self, n, w):
        #input widget w and number n, the number n being of the sequence it is displayed in
        widgets.append((n,w))

    @staticmethod
    def seq(n):
        Widgets.clear()
        if(isinstance(n,int)):
            n = [n]
        Widgets.currentSeq = n
        for num in n:    
            for widget in widgets:
                if widget[0] == num:
                    widget[1].place()
                    #print("placing widget under: "+ str(num))
        mainfunc(n)


    @staticmethod
    def clear():
        for num in Widgets.currentSeq:
            for widget in widgets:
                if widget[0] == num:
                    #print("removing widget under: " + str(num))
                    widget[1].forget()

    @staticmethod
    def rem_seq(n):
        x = len(widgets)
        c = 0
        for i in range(x):
            if i-c < x-c and widgets[i-c][0] == n:
                widgets.pop(i-c)
                c += 1
        c = 0



"""
_________________________________________________________________

TKINTER SETUP


Page designation:

0           login page
1           message board helper widgets
2           create user
3           username and password input
4           re-enter password
5           enter username
6-14        *unused* designated for page operations
15-16       login errors
17-19       create user errors
20          cannot create chat with self error
21-29       *unused* designated for errors
30-87       *undesignated*
88          no widgets contained, used in mainloop as a general indicator
89          no widgets contained, indicates message needs to be sent
90          no widgets contained, indicates new chat
91          no widgets contained, indicated reload messages
92-99       *unused* designated for indicators
100-108     displays chats (<45)
109         enter password for chat
110-129     displays messages in chat


Generalized page designation:
_________________________________________________________________

0-14:       pages
15-29:      errors
30-87:      undesignated
88-99:      indicators
100-109:    chats
110-129:    messages
_________________________________________________________________
"""



"""
Page 0
login page
"""

# title
Widgets(0,Message("Message Center",halfx-95,10,color="darkgray",wide=200,high=40,fs=20))

# continue
Widgets(0,Button("Continue",x=235,y=270,wide=100,com=[1,88]))

# create new user
Widgets(0,Button("create new user",x=240,y=315,wide=50,fs=6,com=[2,3]))

# error
Widgets(15,Message("username not in database, try again",x=195,y=245,fs=10,wide=200))
Widgets(16,Message("incorrect password, try again",x=220,y=250,fs=10,wide=200))



"""
Page 1
message board
other Widgets implemented in Pages 100-129
"""

# title
Widgets(1,Message("Messages",halfx-75,10,color="darkgray",wide=200,high=40,fs=20))

# log out
Widgets(1,Button("Logout",530,10,wide=40,fs=8,com=[0,3]))

# create new chat
Widgets(1,Button("New Chat",5,10,wide=40,fs=8,com=[5]))

# send new message box
new_message = Input_Box(30,350)
new_message.configure(45)



"""
Page 2
create user
"""

# title
Widgets(2,Message("Create New User",halfx-70,10,wide=200,fs=18))

# continue
Widgets(2,Button("Continue",x=235,y=320,wide=100,com=[0,3,88]))

# confirm password
confirm_passBox = Input_Box(250,275,wide=100,hidden=1)
Widgets(2,confirm_passBox)
Widgets(2,Message("Confirm password:",x=100,y=265,wide=100,fs=15))

# error
Widgets(17,Message("passwords do not match",230,300,fs=10,wide=200))
Widgets(18,Message("please enter username and password",230,300,fs=10,wide=200))

# error for username already taken
Widgets(19,Message("username already taken",230,300,fs=10,wide=200))

# back
Widgets(2,Button("Back",530,10,wide=40,fs=8,com=[0,3]))



"""
Page 3
user input
"""

# user input
Widgets(3,Message("Username:",x=100,y=125,wide=100,fs=15))
Widgets(3,Message("Password:",x=100,y=200,wide=100,fs=15))

userBox = Input_Box(x=250,y=125,wide=100)
Widgets(3,userBox)
passBox = Input_Box(x=250,y=200,wide=100,hidden=1)
Widgets(3,passBox)



"""
Page 4
re enter password (until signatures)
"""

# user input
chat_password = Input_Box(x=205,y=200,wide=100,hidden=1)
Widgets(4,chat_password)

# title
Widgets(4,Message("Please enter the password for this chat",halfx-125,50,wide=250,fs=18))

# continue
Widgets(4,Button("Continue",x=235,y=320,wide=100,com=[88,89]))

# back
Widgets(4,Button("Back",530,10,wide=40,fs=8,com=[110]))



"""
Page 5
enter username
"""

# user input
chat_username = Input_Box(x=205,y=125,wide=100)
Widgets(5,chat_username)
chat_pass = Input_Box(x=205,y=200,wide=100)
Widgets(5,chat_pass)

# title
Widgets(5,Message("Please enter the username of who you'd like to chat with and the password for the chat",100,25,wide=400,fs=18))

# continue
Widgets(5,Button("Continue",x=235,y=320,wide=100,com=[88,90]))

# back
Widgets(5,Button("Back",530,10,wide=40,fs=8,com=[1,100]))

# error for starting chat with self
Widgets(20,Message("cannot start chat with self",x=200,y=250,fs=10,wide=200))

# error for chat already exists
Widgets(21,Message("chat already exists",x=200,y=250,fs=10,wide=200))



"""
Loads chats and displays them on the screen
Upon selecting a chat, prompts for a password
If password is correct, displays all messages corresponding to the chat

no returns
after login, chat_load(data.json["messages"], 2, [user, pass, {}]) is called
after correct password is entered function updates account to: 
                                [user, pass, data.json["messages"][i]["msg_chat"]
"""

def chat_load(data, mode, account=[]):
    global new_message
    # mode 2 is loading all the chats on Widgets seq 100-108, data = json["messages"]
    if mode == 2:
        user = account[0] 
        for i in range(100,109):
            Widgets.rem_seq(i)

        page = 100
        Widgets(100,Button("^",x=550,y=40,wide=70,com=[1,100]))

        new_button = ""
        i = 0
        for chat in data:
            if user == chat["user1"] or user == chat["user2"]:
                name = chat["user1"] if not chat["user1"] == user else chat["user2"]
                new_button = Button(name,x=40,y=75+65*(int(i)%5),wide=200,msgload=2,com=[chat,account,name])
                new_button.configure(wide=35,high=1)
                Widgets(int(100+i/5),new_button)
                i+=1
                if not page == int(100+i/5):
                    page += 1
                    Widgets.rem_seq(page)
                    Widgets(page-1,Button("v",x=550,y=350,wide=70,com=[1,page]))
                    Widgets(page,Button("^",x=550,y=40,wide=70,com=[1,page-1]))

                if i >= 45:
                    print("Please expand chat database")
                    exit(-3)

        Widgets(page,Button("v",x=550,y=350,wide=70,com=[1,page]))

        if i == 0:
            Widgets(100,Message("Sorry, you have no chats at this time",halfx-110,175,wide=200,fs=18))

        Widgets.seq([100,1])

    # mode 1 is getting password, data = [chat,account,name], seq 109
    elif mode == 1:
        # get the password
        passkeyBox = Input_Box(x=205,y=200,wide=100,hidden=1)
        Widgets(109,Message("Please enter the password for this chat",halfx-125,50,wide=250,fs=18))
        Widgets(109,passkeyBox)
        Widgets(109,Button("Continue",x=235,y=320,wide=100,msgload=1,com=[data, passkeyBox]))
        Widgets(109,Button("Back",530,10,wide=40,fs=8,com=[100,1]))

        Widgets.seq(109)

    # mode 0 loads all chats and begins display from end, seq 110-129, data=[[chat,account,name],passkeyBox]
    elif mode == 0:
        for i in range(110,130):
            Widgets.rem_seq(i)
        page = 110
        line = 50
        start = 1
        password = data[1].get_val()
        password = sha256_hash(password.encode())
        hashed_pass = sha256_hash(password)

        if not hashed_pass == b64decode(data[0][0]["hashed_key"]):
            Widgets.seq([16,109])
        else:
            data[0][1][2] = data[0][0]

            Widgets(110,Button("^",x=550,y=40,wide=70,com=[110]))

            for message in data[0][0]["msg_data"]:
                #decrypt text
                #hashed pass as key
                text = aes_decrypt(password, b64decode(message["msg"]), b64decode(message["nonce"]))
                text = str(message["sent_by"]) + ": " + text
                
                #display operations
                lines = int(len(text)/55 + 1)
                line_end = (lines*20 + line)
                if line_end > 310:
                    Widgets(page,Button("v",x=550,y=350,wide=70,com=[page+1]))
                    line = 50
                    page += 1
                    Widgets(page,Button("^",x=550,y=40,wide=70,com=[page-1]))
                    if page > 129:
                        print("Please expand message database")
                        exit(-3)
                else:
                    if start == 1:
                        start = 0
                    else:
                        line += 20

                Widgets(page,Text(text,10,line,wide=55,fs=12,highl=lines))
                line += (lines-1)*20

            Widgets(page,Button("v",x=550,y=350,wide=70,com=[page]))

            name = data[0][2]    
            name_string = "Chat with " + name

            for j in range(110, page+1):
                Widgets(j,Button("Back",540,10,wide=40,fs=8,com=[88,91]))
                Widgets(j,Message(name_string, halfx-90, 10, fs=20))
                Widgets(j,new_message)
                Widgets(j,Button("Send",460,350,wide=40,fs=8,com=[88,89]))

            Widgets.seq([page])


"""
Returns the contents of the send bar
Only called after send is pressed
Clears the content of the send bar
"""
def get_message():
    global new_message
    temp = new_message.get_val()
    new_message.clear()
    return temp

"""
Returns the contents of chat_password
 - password entry box found in page 4
Clears the content of chat_password
"""
def get_password():
    global chat_password
    temp = chat_password.get_val()
    chat_password.clear()
    return temp

"""
Returns the contents of chat_username
 - username entry box found in page 5
Clears the content of chat_username
"""
def get_username():
    global chat_username, chat_pass
    temp1 = chat_username.get_val()
    temp2 = chat_pass.get_val()
    chat_username.clear()
    chat_pass.clear()
    return temp1, temp2


"""
Loads messages in the range: pages 110-129
Assumes access has already been granted
Assumes account already points to current chat (hence reload)
"""
def reload_messages(account, password):
    global new_message
    for i in range(110,130):
        Widgets.rem_seq(i)
    page = 110
    line = 50
    start = 1

    Widgets(110,Button("^",x=550,y=40,wide=70,com=[110]))

    js = json.load(open('data.json'))
 
    index = -1

    for i in range(len(js["messages"])):
        if js["messages"][i]["user1"] == account[2]["user1"] and js["messages"][i]["user2"] == account[2]["user2"]:
            index = i

    if index == -1:
        print("MAJOR LOGICAL ERROR IN RELOAD MESSAGES/ACCOUNT")
        exit(-5)
    
    msg_data = js["messages"][index]["msg_data"]

    for message in msg_data:
        #decrypt text
        text = aes_decrypt(password, b64decode(message["msg"]), b64decode(message["nonce"]))
        text = str(message["sent_by"]) + ": " + text

        #display operations
        lines = int(len(text)/55 + 1)
        line_end = (lines*20 + line)
        if line_end > 310:
            Widgets(page,Button("v",x=550,y=350,wide=70,com=[page+1]))
            line = 50
            page += 1
            Widgets(page,Button("^",x=550,y=40,wide=70,com=[page-1]))
            if page > 129:
                print("Please expand message database")
                exit(-3)
        else:
            if start == 1:
                 start = 0
            else:
                line += 20

        Widgets(page,Text(text,10,line,wide=55,fs=12,highl=lines))
        line += (lines-1)*20


    Widgets(page,Button("v",x=550,y=350,wide=70,com=[page]))

    user = account[0]
    name = js["messages"][index]["user1"] if not js["messages"][index]["user1"] == user else js["messages"][index]["user2"]

    name_string = "Chat with " + name

    for j in range(110, page+1):
        Widgets(j,Button("Back",540,10,wide=40,fs=8,com=[88,91]))
        Widgets(j,Message(name_string, halfx-90, 10, fs=20))
        Widgets(j,new_message)
        Widgets(j,Button("Send",460,350,wide=40,fs=8,com=[88,89]))

    Widgets.seq([page])

















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






