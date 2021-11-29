from main_loop import *
import backups.backup_protocol as bp


"""
Loading the GUI class and interface
"""
root = tk.Tk()
Widgets(root)
Data.root = root
init_msgGUI() # setup_GUI.py


"""
Checking for corruption
"""
corruption = bp.check_corruption()
if corruption == 0:
    exit(0)


"""
Loading account variables into Data class
"""
fop.load_account_data()


"""
Starting GUI with pages 0,3: login
"""
Widgets.seq([0, 3])
root.mainloop()


"""
Backing up database (after window close)
"""
bp.add_backup()




