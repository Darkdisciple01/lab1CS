from GUI_class import *
from Data_class import *


"""
_________________________________________________________________

TKINTER SETUP


Page designation:

0           login page
1           message board helper widgets
2           create user
3           username and password input
4           account
5           enter username (create chat)
6           enter username (delete chat)
7           are you sure? (deleting account)
8-14        *unused* designated for page operations
15-16       login errors
17-19       create user errors
20          cannot create chat with self error
21          chat already exists
22          verification error
23          chat does not exist
24          error deleting account
25-29       *unused* designated for errors
30-87       *undesignated*
88          no widgets contained, used in mainloop as a general indicator
89          no widgets contained, indicates message needs to be sent
90          no widgets contained, indicates new chat
91          no widgets contained, indicates reload messages
92          no widgets contained, indicates logout
93          no widgets contained, indicates deleting chat
94          no widgets contained, indicates deleting user
95-99       *unused* designated for indicators
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


def init_msgGUI():

    """
    Page 0
    login page
    """

    # title
    Widgets.add(0,Message("Message Center",205,10,color="darkgray",wide=200,high=40,fs=20))

    # continue
    Widgets.add(0,Button("Continue",x=235,y=270,wide=100,com=[1,88]))

    # create new user
    Widgets.add(0,Button("create new user",x=240,y=315,wide=50,fs=6,com=[2,3]))

    # error
    Widgets.add(15,Message("username not in database, try again",x=195,y=245,fs=10,wide=200))
    Widgets.add(16,Message("incorrect password, try again",x=220,y=250,fs=10,wide=200))
    Widgets.add(22,Message("account could not be verified, please contact admin",x=180,y=230,fs=10,wide=200))



    """
    Page 1
    message board
    other Widgets implemented in Pages 100-129
    """

    # title
    Widgets.add(1,Message("Messages",225,10,color="darkgray",wide=200,high=40,fs=20))

    # log out
    Widgets.add(1,Button("Account",525,10,wide=40,fs=8,com=[4]))

    # create new chat
    Widgets.add(1,Button("New Chat",5,10,wide=40,fs=8,com=[5]))

    # send new message box
    new_message = Input_Box(30,350)
    new_message.configure(45)



    """
    Page 2
    create user
    """

    # title
    Widgets.add(2,Message("Create New User",200,10,wide=200,fs=20))

    # continue
    Widgets.add(2,Button("Continue",x=235,y=320,wide=100,com=[0,3,88]))

    # confirm password
    confirm_passBox = Input_Box(250,275,wide=100,hidden=1)
    Widgets.add(2,confirm_passBox)
    Widgets.add(2,Message("Confirm password:",x=100,y=265,wide=100,fs=15))

    # back
    Widgets.add(2,Button("Back",530,10,wide=40,fs=8,com=[0,3]))

    # error
    Widgets.add(17,Message("passwords do not match",230,300,fs=10,wide=200))
    Widgets.add(18,Message("please enter username and password",230,300,fs=10,wide=200))

    # error for username already taken
    Widgets.add(19,Message("username already taken",230,300,fs=10,wide=200))



    """
    Page 3
    user input
    """

    # box titles
    Widgets.add(3,Message("Username:",x=100,y=125,wide=100,fs=15))
    Widgets.add(3,Message("Password:",x=100,y=200,wide=100,fs=15))

    # input boxes
    userBox = Input_Box(x=250,y=125,wide=100)
    Widgets.add(3,userBox)
    passBox = Input_Box(x=250,y=200,wide=100,hidden=1)
    Widgets.add(3,passBox)



    """
    Page 4
    account
    """
   
    # title
    Widgets.add(4,Message("Account Operations",180,20,wide=300,fs=20))

    # log out
    bl = Button("Logout",140,115,wide=40,fs=8,com=[88,92])
    bl.configure(40,2)
    Widgets.add(4,bl)

    # delete chat
    bdc = Button("Delete a chat",140,195,wide=40,fs=8,com=[6])
    bdc.configure(40,2)
    Widgets.add(4,bdc)

    # delete user
    bdu = Button("Delete account",140,275,wide=40,fs=8,com=[7])
    bdu.configure(40,2)
    Widgets.add(4,bdu)

    # back
    Widgets.add(4,Button("Back",530,10,wide=40,fs=8,com=[88,91]))

    # error for account deletion failure
    Widgets.add(24,Message("error deleting account, please log out and try again",x=140,y=330,fs=10,wide=400))



    """
    Page 5
    enter username (create chat)
    """

    # user input
    chat_username = Input_Box(x=205,y=200,wide=100)
    Widgets.add(5,chat_username)

    # title
    Widgets.add(5,Message("Please enter the username of who you'd like to chat with",100,25,wide=400,fs=18))

    # continue
    Widgets.add(5,Button("Continue",x=235,y=320,wide=100,com=[88,90]))

    # back
    Widgets.add(5,Button("Back",530,10,wide=40,fs=8,com=[1,100]))

    # error for starting chat with self
    Widgets.add(20,Message("cannot start chat with self",x=200,y=250,fs=10,wide=200))

    # error for chat already exists
    Widgets.add(21,Message("chat already exists",x=200,y=250,fs=10,wide=200))



    """
    Page 6
    enter username (delete chat)
    """
    
    # user input
    Widgets.add(6,chat_username)

    # title
    Widgets.add(6,Message("Please enter the username of whose chat you'd like to delete",100,25,wide=400,fs=18))

    # continue
    Widgets.add(6,Button("Continue",x=235,y=320,wide=100,com=[88,93]))

    # back
    Widgets.add(6,Button("Back",530,10,wide=40,fs=8,com=[4]))

    # error for incorrect username
    Widgets.add(23,Message("chat does not exist",x=230,y=250,fs=10,wide=200))

    
    
    """
    Page 7
    are you sure? (delete account)
    """
    
    # title
    Widgets.add(7,Message("Are you sure you want to delete your account? This will also delete all of your existing chats.",100,25,wide=400,fs=18))
    
    # yes
    yes = Button("Yes",140,155,wide=40,fs=8,com=[88,94])
    yes.configure(40,2)
    Widgets.add(7,yes)

    # no
    no = Button("No",140,250,wide=40,fs=8,com=[4])
    no.configure(40,2)
    Widgets.add(7,no)



    """
    sending boxes to Data class
    """
    Data.set_boxes(userBox, passBox, confirm_passBox, new_message, chat_username)



"""
Returns the contents of the message send bar
Only called after send is pressed
Clears the content of the send bar
"""
def get_message():
    new_message = Data.get_boxes2()
    temp = new_message.get_val()
    new_message.clear()
    return temp


"""
Returns the contents of chat_username
 - username entry box found in page 5
Clears the content of chat_username
"""
def get_username():
    chat_username = Data.get_boxes3()
    temp = chat_username.get_val()
    chat_username.clear()
    return temp




