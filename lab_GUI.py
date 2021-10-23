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

    def get_val(self):
        return self.data[5].get()

    def clear(self):
        return


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
        for widget in widgets:
            if widget[0] == n:
                widgets.remove(widget)


"""
_________________________________________________________________

TKINTER SETUP
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
Widgets(15,Message("username not in database, try again",x=220,y=250,fs=10,wide=200))
Widgets(16,Message("incorrect password, try again",x=220,y=250,fs=10,wide=200))




"""
Page 1
message board
"""

# title
Widgets(1,Message("Messages",halfx-50,10,color="darkgray",wide=200,high=40,fs=20))

# log out
Widgets(1,Button("Logout",530,10,wide=40,fs=8,com=[0,3]))


# create new chat


# display chats - buttons with names of recipients
# have to load chats, have a function with Widgets within range (300,inf)?


# error for if no messages



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
Pages 100-110
chat display
"""


def chat_load(data, mode, account=[]):

    # mode 2 is loading all the chats on Widgets seq 100-108, data = json["messages"]
    if mode == 2:
        user = account[0] 
        Widgets.rem_seq(100)

        Widgets(100,Button("^",x=550,y=40,wide=70,com=[1,100]))
        Widgets(100,Button("v",x=550,y=350,wide=70,com=[1,101]))

        for i in range(101,108):
            Widgets.rem_seq(i)
            Widgets(i,Button("^",x=550,y=40,wide=70,com=[1,i-1]))
            Widgets(i,Button("v",x=550,y=350,wide=70,com=[1,i+1]))

        Widgets.rem_seq(108)
    
        Widgets(108,Button("^",x=550,y=40,wide=70,com=[1,107]))
        Widgets(108,Button("v",x=550,y=350,wide=70,com=[1,108]))

        i = 0
        for chat in data:
            if user == chat["user1"] or user == chat["user2"]:
                name = chat["user1"] if not chat["user1"] == user else chat["user2"]
                new_button = Button(name,x=40,y=50+75*(int(i)%5),wide=200,msgload=2,com=[chat,account,name])
                new_button.configure(wide=35,high=1)
                Widgets(100+(int(i)/5),new_button)
                i+=1
                if i >= 45:
                    print("Please expand chat database")
                    exit(-3)
        if i == 0:
            Widgets(100,Widget("Sorry, you have no chats at this time","",halfx-150,10,wide=200,fs=18))

        Widgets.seq([100,1])

    # mode 1 is getting password, data = ["messages",account,name], seq 109
    elif mode == 1:
        # get the password
        passkeyBox = Input_Box(x=205,y=200,wide=100,hidden=1)
        Widgets(109,Message("Please enter the password for this chat",halfx-125,50,wide=250,fs=18))
        Widgets(109,passkeyBox)
        Widgets(109,Button("Continue",x=235,y=320,wide=100,msgload=1,com=[data, passkeyBox]))
        Widgets(109,Button("Back",530,10,wide=40,fs=8,com=[100,1]))

        Widgets.seq(109)

    # mode 0 loads all chats and begins display from end, seq 110-129, data=[["messages",account,name],passkeyBox]
    elif mode == 0:
        for i in range(110,130):
            Widgets.rem_seq(i)   #untested
        page = 110
        line = 50
        password = data[1].get_val()
        password = sha256_hash(password.encode())
        hashed_pass = sha256_hash(password)
        init_vec = b64decode(data[0][0]["init_vec"])

        if not hashed_pass == b64decode(data[0][0]["hashed_key"]):
            Widgets.seq([16,109])
        else:
            data[0][1][2] = data[0][0]

            for message in data[0][0]["msg_data"]:
                #decrypt text
                #hashed pass as key
                text = aes_decrypt(password, b64decode(message["msg"]), init_vec)
                text = str(message["sent_by"]) + ": " + text
                
                #display operations
                lines = len(text)/55 + 1
                line_end = (lines*20 + line)
                if line_end > 310:
                    line = 50
                    page += 1
                    if page > 129:
                        print("Please expand message database")
                        exit(-3)
                else:
                    line += 20*lines

                Widgets(page,Text(text,10,line,wide=55,fs=12,highl=lines))

            user = data[0][1][0]
            name = data[0][2]
    
            name_string = "Chat with " + name

            for j in range(110, page+1):
                Widgets(j,Button("Back",530,10,wide=40,fs=8,com=[100,1]))
                Widgets(j,Message(name_string, halfx-90, 10, fs=20))

            Widgets.seq([page])




"""

#will have to load chats, batch 100-110, 
#establish 5 at a time, then assign 5 to 200, 5 to 201, etc.
# - done in load
#
#messages will appear as buttons with the name of person to message

#on click to messages when logging in, runs load_chats - each chat with the dictionary of message data

#chat button: displays name of other user, on click runs load_messages unpacking dictionary
# - password prompt as key for the encryption
# - until signatures?
# - chats/messages have a next_true byte?


#implement update account
#Widgets(100,Text("User 1: This is my text box",10,50,wide=55,fs=12, highl=1))
#Widgets(100,Text("User 2: This is my text box",10,70,wide=55,fs=12))
#figure out how to do it backwards
#figure out how password is going to be manipulated, Hk?
#implement message bar to send messages

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






