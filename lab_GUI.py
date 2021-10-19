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
    def __init__(self,message="",button="",x=0,y=0,color="lightgray",wide=200,high=40,fs=14,com=0,hidden=0,entry_var=""):
        
        self.data = [0,0]
        
        if(message!=""):
            frame = tk.Frame(root,bg=backgroundColor,width=wide,height=high,highlightbackground=color)
            msg = tk.Message(frame, text=message, width=wide,bg=backgroundColor,fg=defaultFontColor)
            msg.configure(font=("Times "+str(fs)))
            self.data=[msg,frame,x,y,0]

        elif(button!=""):
            frame = tk.Frame(root,bg=backgroundColor,width=wide,height=high,highlightbackground=color)
            btn = tk.Button(frame, text=button,bg="gray",fg=defaultFontColor,command= lambda: Widgets.seq(com))
            btn.configure(font=("Roboto "+str(fs)))
            self.data=[btn,frame,x,y,1]
        
        else:
            #input box
            frame = tk.Frame(root,bg=backgroundColor,width=wide,height=high,highlightbackground=color)
            entry_var=tk.StringVar()
            entry = tk.Entry(frame, textvariable=entry_var)
            entry.configure(font=("Times "+str(fs)))
            if(hidden):
                entry.configure(show="*")
            self.data=[entry,frame,x,y,1,entry_var]
    
    def place(self):
        #print("trying to place message" if self.data[4]==0 else "trying to print button") 
        if self.data[1] != -1:
            self.data[1].place(x=self.data[2],y=self.data[3])
            self.data[0].pack()
        else:
            self.data[0].place(x=self.data[2],y=self.data[3])
        

    def forget(self):
        if self.data[1] != -1:
            self.data[0].pack_forget()
            self.data[1].place_forget()
        else:
            self.data[0].place_forget()

    def get_val(self):
        return self.data[5].get()


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
Widgets(0,Widget("Message Center","",halfx-95,10,"darkgray",wide=200,high=40,fs=20))

# user input
Widgets(3,Widget("Username:","",x=100,y=125,wide=100,fs=15))
Widgets(3,Widget("Password:","",x=100,y=200,wide=100,fs=15))

userBox = Widget("","",x=250,y=125,wide=100)
Widgets(3,userBox)
passBox = Widget("","",x=250,y=200,wide=100,hidden=1)
Widgets(3,passBox)

# continue
Widgets(0,Widget("","Continue",x=235,y=270,wide=100,com=[1,88]))

# create new user
Widgets(0,Widget("","create new user",x=240,y=315,wide=50,fs=6,com=[2,3]))

# error
Widgets(15,Widget("usernamenot in database, try again","",x=220,y=250,fs=10,wide=200))
Widgets(16,Widget("incorrect password, try again","",x=220,y=250,fs=10,wide=200))




"""
Page 1
message board
"""

# title
Widgets(1,Widget("Messages","",halfx-50,10,"darkgray",wide=200,high=40,fs=20))

# log out
Widgets(1,Widget("","Logout",530,10,wide=40,fs=8,com=[0,3]))


# send new message

# error for if no messages



"""
Page 2
create user
"""

# title
Widgets(2,Widget("Create New User","",halfx-70,10,wide=200,fs=18))

# continue
Widgets(2,Widget("","Continue",x=235,y=320,wide=100,com=[0,3,88]))

# confirm password
confirm_passBox = Widget("","",250,275,wide=100,hidden=1)
Widgets(2,confirm_passBox)
Widgets(2,Widget("Confirm password:","",x=100,y=265,wide=100,fs=15))

# error
Widgets(17,Widget("passwords do not match","",230,300,fs=10,wide=200))
Widgets(18,Widget("please enter username and password","",230,300,fs=10,wide=200))

# error for username already taken
