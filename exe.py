from main_loop import *
import backups.backup_protocol as bp

"""
Loading the GUI class and interface
"""
print("Loading the GUI class and interface")

root = tk.Tk()
Widgets(root)
Data.root = root
init_msgGUI()


"""
Checking for corruption, loading variables into data class
"""
print("Checking for corruption, loading variables into data class")

corruption = bp.check_corruption()
if corruption == 0:
    exit(0)

fop.load_account_data()
message_data = fop.load_message_data()


"""
Different operation modes
0,NULL for GUI, 1 for Testing
"""
print("Starting GUI")

import sys
x = (int)(sys.argv[1]) if (len(sys.argv)>1) else 0

if x == 0:
    # initiation
    Widgets.seq([0, 3])
    root.mainloop()

if x == 1:
    # testing
    root.withdraw()


bp.add_backup()




