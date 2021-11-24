import tkinter as tk
import tkinter.font as tkFont
import messager
from Data_class import *
import file_operations as fop
import encryption_functions as ef
import cert_auth.certificate_authority as CA

"""
The Widgets class organizes and calls on "events" or different pages. The home page is denoted as page 0. 
The seq function accepts input of either a single number or an array of numbers, and runs those pages on the screen.
"""

class Widgets:
    
    currentSeq =[0]
    widgets = []
    backgroundColor = 'gray16'
    defaultFontColor = 'gray84'
    root = None

    def __init__(self, rootg):
        dim = [600, 400]
        rootg.geometry(str(dim[0])+"x"+str(dim[1]))
        rootg.configure(background=Widgets.backgroundColor)
        rootg.wm_title("")
        root = rootg

    @staticmethod
    def add(n,w):
        #input widget w and number n, the number n being of the sequence it is displayed in
        Widgets.widgets.append((n,w))

    @staticmethod
    def seq(n):
        Widgets.clear()
        if(isinstance(n,int)):
            n = [n]
        Widgets.currentSeq = n
        for num in n:    
            for widget in Widgets.widgets:
                if widget[0] == num:
                    widget[1].place()
                    #print("placing widget under: "+ str(num))
        messager.mainfunc(n)


    @staticmethod
    def clear():
        for num in Widgets.currentSeq:
            for widget in Widgets.widgets:
                if widget[0] == num:
                    #print("removing widget under: " + str(num))
                    widget[1].forget()

    @staticmethod
    def rem_seq(n):
        x = len(Widgets.widgets)
        c = 0
        for i in range(x):
            if i-c < x-c and Widgets.widgets[i-c][0] == n:
                Widgets.widgets.pop(i-c)
                c += 1
        c = 0

    @staticmethod
    def get_data():
        return Widgets.root, Widgets.backgroundColor, Widgets.defaultFontColor



"""
The Widget class is designed to more easily customize and initialize widgets from Tkinter. Widgets are placed at inputs x and y.
Each of its children correspond to a data type in the Tkinter library
"""

class Widget:
    root,backgroundColor,defaultFontColor = Widgets.get_data()

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
        frame = tk.Frame(Widget.root,bg=Widget.backgroundColor,width=wide,height=high,highlightbackground=color)
        msg = tk.Message(frame, text=text, width=wide,bg=Widget.backgroundColor,fg=Widget.defaultFontColor)
        msg.configure(font=("Times "+str(fs)))
        super().__init__(msg, frame, x, y)


class Button(Widget):
    def __init__(self, text, x, y, msgload=0, com=0, wide=200, high=40, fs=14, color="lightgray"):
        frame = tk.Frame(Widget.root,bg=Widget.backgroundColor,width=wide,height=high,highlightbackground=color)
        if msgload == 0:
            btn = tk.Button(frame, text=text,bg="gray",fg=Widget.defaultFontColor,command= lambda: Widgets.seq(com))
        else:
            btn = tk.Button(frame, text=text,bg="gray",fg=Widget.defaultFontColor,command= com)
        btn.configure(font=("Roboto "+str(fs)))
        super().__init__(btn, frame, x, y)

    def configure(self, wide, high):
        self.data[0].configure(width=wide, height=high)


class Input_Box(Widget):
    def __init__(self, x, y, hidden=0, entry_var="", wide=200, high=40, fs=14, color="lightgray"):
        frame = tk.Frame(Widget.root,bg=Widget.backgroundColor,width=wide,height=high,highlightbackground=color)
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
        frame = tk.Frame(Widget.root,bg=Widget.backgroundColor,width=wide,height=high,highlightbackground=color)
        txt = tk.Text(frame,width=wide, height=highl, bg=Widget.backgroundColor,fg=Widget.defaultFontColor,highlightthickness=0,borderwidth=0)
        txt.insert(tk.END, text)
        txt.configure(font=("Helvetica "+str(fs)))
        super().__init__(txt, frame, x, y)
    
    @staticmethod
    def get_lines(text):
        helv12 = tkFont.Font(family='Helvetica',
        size=12)
        pixels = helv12.measure(text)
        return int(pixels/495) + 1




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

    if i == 0:
        Widgets.add(100,Message("Sorry, you have no chats at this time",190,175,wide=200,fs=18))

    Widgets.seq([100,1])






"""
Reloads messages in the range: pages 110-129
Assumes access has already been granted
Assumes account already points to current chat (hence reload)
"""
def msg_load(chat):
    new_message = Data.get_boxes2()
    Data.load_chat_data(chat)

    # calc key with Diffie Hellman
    a = int(CA.pem_to_hex(Data.t_priv, 128), 0)
    Y_other = fop.get_Y(Data.c_other)
    shared_key = ef.generate_Y(a, Y_other)

    #How to turn shared_key (int) into shared bytes
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
    js = fop.json.load(open('data.json'))

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


