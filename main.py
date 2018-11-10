'''
Author: Eric Lai
Description: A simple password manager.
'''
import json
import getpass
import os.path
import io

def welcome():
    #prints welcome screen stating name, description and author of program

    name = "Name: Password Manager"
    desc = "Description: command line program for managing passwords"
    author = "Author: Eric Lai"
    length = 70

    print("#"*length)
    print("#" + " "*68 + "#")
    print("#" + " " + name + " "*(length - len(name) - 3) + "#")
    print("#" + " " + desc + " "*(length - len(desc) - 3) + "#")
    print("#" + " " + author + " "*(length - len(author) - 3) + "#")
    print("#" + " "*68 + "#")
    print("#"*length)


def checkFiles(data, profile, passwords):
    '''
    Checks if essential files exists. Takes 3 parameters. Returns true
    data
        string representing the relative path of the directory holding
        profile.json and passwords.json
    profile
        string representing the relative path of profile.json
    passwords
        string representing the relative path of passwords.json
    '''    
    # checks if data exists
    # creates the directory if it doesn't exist
    if not os.path.isdir(data):
        print("----------\nData directory not found. Creating data file in current directory.")
        os.mkdir(data)
        print("New directory 'Data' created in current directory")

    # checks for profile in data
    # if it doesn't exist, prompts user to set profile username and password
    if not os.path.isfile(profile):
        print("----------\nNo profile found. Please set a username and password.")
        user = input("Username: ")
        pw = input("Password: ")

        profile = {
            "mUsername": user,
            "mPassword": pw
        }

        newProfile = open("./data/profile.json", 'w')
        json.dump(profile, newProfile, indent=4)

    # checks for passwords in json
    # creates empty json it doesn't exist
    if not os.path.isfile(passwords):
        pwdict = {}
        with open(passwords, 'w') as pws:
            json.dump(pwdict, pws)

    return True


def viewAndEdit(profile, passwords):
    '''
    Authenticates if user can view and edit passwords.
    If user logs in, user can view and edit passwords
    function returns True when done. If user fails to
    log in, function returns False. Takes 2 parameters.
    profile
        string representing the relative path of profile.json
    passwords
        string representing the relative path of passwords.json
    '''

    with open(profile, 'r') as prof:
        values = json.load(prof)
        
        login = False

        for _ in range(3):
            usr = input("Enter your username: ")
            pw = getpass.getpass("Enter your password: ")

            if (usr == values["mUsername"] and pw == values["mPassword"]):
                print("----------\nSuccessfully logged in as " + values["mUsername"] + ".")
                login = True
                break
            else:
                print("Username or Password was incorrect. Try Again.")

        if (not login):
            print("----------\nToo many failed attempts.")
            return

    with open(passwords, 'r') as pwds:
        
        values = json.load(pwds)
        login_status = True

        print("enter -help for a list of commands")
        

        while(login_status):
            
            print()
            command = input("Password Manager>")

            if command == '-help':
                
                print('-'*10)
                help()

            elif command == '-entries':
                
                print('-'*10)

                if len(values) == 0:
                    print("There are no entries.")
                for name in sorted(values.keys()):
                    print(name)

            elif command == '-see':
                print('-'*10)

                entry = input("Enter entry name: ")

                if entry in values.keys():
                    print("printing current entry information")
                    print("###" + entry + "###")
                    for k, v in values[entry].items():
                        print(k + ":")
                        print("    " + v)
                else:
                    print("Entry does not exist")

            elif command == '-newEntry':

                print('-'*10)
                print("Preparing a new entry.\n")
                name = input("Enter entry name: ")
                if name in values.keys():
                    print(name + " is already an entry. Stopping entry.")
                else:
                    usrname = input("Enter username: ")
                    pw = input("Enter password: ")
                    details = input("Enter any details: ")
                    values[name] = {
                        "username":usrname,
                        "password":pw,
                        "details":details
                        }
                    print("Entered.")

            elif command == '-quit':

                login_status = False

            elif command == '-edit':

                print('-'*10)
                entry = input("Enter entry name: ")
                if entry in values.keys():
                    print("printing current entry information")
                    print("###" + entry + "###")
                    for k, v in values[entry].items():
                        print(k + ":")
                        print("    " + v)

                    if input("Enter q to leave entry unchanged, enter nothing to continue: ") != "q":
                        print('-'*10)
                        usrname = input("Enter username: ")
                        pw = input("Enter password: ")
                        details = input("Enter any details: ")
                        values[entry] = {
                            "username":usrname,
                            "password":pw,
                            "details":details
                            }
                        print("Entered.")
                    else:
                        print("Entry unchanged.")
                else:
                    print("This entry does not exist")
            
            elif command == '-delete':
                print('-'*10)
                entry = input("Enter entry name: ")
                if entry in values:
                    if input("Are you sure you want to delete '" + entry + "'? Enter q to leave entry unchanged, enter nothing to continue: ") != "q":
                        del values[entry]
                        print("password for '" + entry + "' has been deleted")
                    else:
                        print("Entry unchanged")
                else:
                    print("'" + entry + "' does not exist")
            
            else:
                print('-'*10)
                print(command + " is not a valid command, enter -help for a list of commands")
    
    
    with open(passwords, 'w') as pws:
        json.dump(values, pws, indent=4)

    print("----------\nAuto saved")


def help():
    # prints out the list of commands and their descriptions 

    commands = {
        "-help":"returns a list of commands with short descriptions",
        "-entries":"returns a list containing all password entry names",
        "-newEntry":"prompts user to create a new password entry",
        "-quit":"exits the program",
        "-edit":"edits an existing entry",
        "-see":"shows a specific password entry",
        "-delete":"deletes a specific password entry"
    }

    for k, v in sorted(commands.items()):
        print(k + ":")
        print("    " + v)


if __name__ == '__main__':
    
    # File Locations
    DATA = './data'
    PROFILE = DATA + '/profile.json'
    PWS = DATA + '/passwords.json'

    welcome()
    checkFiles(DATA, PROFILE, PWS)
    input("press ENTER to continue...")
    viewAndEdit(PROFILE, PWS)
    print("exiting...")
