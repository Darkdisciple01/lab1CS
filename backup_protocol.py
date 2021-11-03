from encryption_functions import hash_file
import json
import tkinter as tk

"""
Adds a backup of the current data.json file (or specified) into the backups folder
backup is added into the file "backup1", and contents of "backup1" are pushed to "backup2"
Only 2 backup files and their hashes are stored
"""

def add_backup(filename = "data.json"):

    # file data
    backup_file = open(filename, "r")
    backup1_path = "backups/backup1.json"
    backup1 = open(backup1_path)
    backup2 = open("backups/backup2.json", "w")
    backuphashes_path = "backups/backuphashes.json"

    # add backup
    backup2.write(backup1.read())
    open(backup1_path, "w").write(backup_file.read())

    # adjust hashes
    hash1 = hash_file(filename)

    backuphashes = json.load(open(backuphashes_path, "r+"))
    backuphashes["hash2"] = backuphashes["hash1"]
    backuphashes["hash1"] = hash1

    backuphashes_file = open(backuphashes_path, "w")
    json.dump(backuphashes, backuphashes_file)

    backup_file.close()
    backup1.close()
    backup2.close()



"""
Checks for corruption or inconsistency in database since last backup
If it finds a corruption, reverts to last uncorrupted backup
If no uncorrupted backup, prompts user to wipe database
unfinished - write load backup 1 and load backup 2
"""
def check_corruption(filename = "data.json", index = "hash1", root = 0):

    flag = 0
    backuphashes_path = "backups/backuphashes.json"
    
    # get current hash, compare to last backup (closing of program)
    hash1 = hash_file(filename)
    backuphash = json.load(open(backuphashes_path, "r"))[index]

    if filename == "data.json" and not hash1 == backuphash:
        print("Data does not match last backup")
        print("This may be caused by program interruption or data corruption")
        print("Checking backup validity")
        
        if check_corruption("backups/backup1.json", "hash1", root) == 1:
            # continue with loading backup1
            f = open("data.json", "w")
            f.write(open("backups/backup1.json", "r+").read())
            f.close()
            print("\nBackup 1 valid, restoring data")
            print("Data restored, please restart the application")
            add_backup()
            add_backup()

        return 0

    if filename == "backups/backup1.json" and not hash1 == backuphash:
        print("\nBackup file 1 corrupted, checking file 2")
        if check_corruption("backups/backup2.json", "hash2", root) == 1:
            # continue with loading backup2
            f = open("data.json", "w")
            f.write(open("backups/backup2.json", "r+").read())
            f.close()
            print("\nBackup 2 valid, restoring data")
            print("Data restored, please restart application")
            add_backup()
            add_backup()
            return 0
    elif filename == "backups/backup1.json":
        return 1

    if filename == "backups/backup2.json" and not hash1 == backuphash:
        root.withdraw()
        print("\nBackup file 2 corrupted, requesting permission to wipe system data")
        input("Enter any key to continue...")
        input("Are you sure? This will delete all existing users and chats")
        f = open("data.json", "w")
        json.dump({"users":[],"messages":[]},f,indent=4)
        f.close()
        print("\nDatabase has been wiped, please restart the application")
        add_backup()
        add_backup()
        return 0
    elif filename == "backups/backup2.json":
        return 1







