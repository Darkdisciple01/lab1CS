import tkinter as tk
import tkinter.font as tkFont
import main_loop

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
        main_loop.mainfunc(n)


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


