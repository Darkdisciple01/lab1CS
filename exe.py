from messager import *


"""
Loading the GUI class and interface
"""
root = tk.Tk()
Widgets(root)
init_msgGUI()


"""
Checking for corruption, loading variables
"""
corruption = check_corruption(root = Widgets.root)
if corruption == 0:
    exit(0)

user_database, salt_database, pass_database = load_account_data()
account = []
message_data = load_message_data()


"""
Different operation modes
0,NULL for GUI, 1 for Testing
"""


import sys
x = (int)(sys.argv[1]) if (len(sys.argv)>1) else 0

if x == 0:
    print("Booting GUI")
    # initiation
    Widgets.seq([0, 3])
    root.mainloop()

if x == 1:
    root.withdraw()




add_backup()




