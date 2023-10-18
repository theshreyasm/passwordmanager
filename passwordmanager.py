from utils.dbconfig import dbconfig
import utils.add as add
import utils.retrieve as retrieve
import hashlib
import getpass


def authenticate():

    password = getpass.getpass("\nEnter master password for your password manager: ")
    
    db = dbconfig()
    cursor = db.cursor()
    query = 'SELECT * FROM passwordmanager.secrets'
    cursor.execute(query)
    res = cursor.fetchone()
    salt = res[0]
    hashed_masterpassword = res[1]
    cursor.close()
    db.close()
    
    hashedpass = hashlib.sha256((salt + password).encode()).hexdigest()

    if hashedpass == hashed_masterpassword:
        return [res[1], res[2]]
    else:
        print("Password is incorrect.")
        return None

def passwordmanager():

    auth = None

    while auth is None:
        auth = authenticate()
        
    masterpassword = auth[0]
    device_secret = auth[1]

    option = input("\n1. Add new entry\n2. Retrieve all entries\n3. Search entry\n4. Exit\nInput option number. ")

    while(option != '4'):

        while(option != '1' and option != '2' and option != '3' and option !='4'):
            print("Input either 1, 2, 3, or 4.")
            option = input("\n1. Add new entry\n2. Retrieve all entries\n3. Search entry\n4. Exit\nInput option number. ")
        
        if option == '4':
            return
        
        if option == '1':

            website = input("\nEnter site name: ")
            if website == "":
                while website == "":
                    print("Site name cannot be empty.")
                    website = input("Enter site name: ")
            
            url = input("Enter url: ")
            if url == "":
                while url == "":
                    print("url cannot be empty.")
                    url = input("Enter url: ")

            email = input("Enter email address: ")
            username = input("Enter username: ")

            add.addEntry(masterpassword, device_secret, website, url, email, username)
        
        if option == '2':

            details = {}
            retrieve.retrieve(masterpassword, device_secret, details)

        if option == '3':

            details = {}

            website = input("\nEnter site name: ")
            if website != "":
                details['website'] = website

            url = input("Enter url: ")
            if url != "":
                details['url'] = url

            username = input("Enter username: ")
            if username != "":
                details['username'] = username

            email = input("Enter email address: ")
            if email != "":
                details['email'] = email
            
            retrieve.retrieve(masterpassword, device_secret, details)

        option = input("\n1. Add new entry\n2. Retrieve all entries\n3. Search entry\n4. Exit\nInput option number. ")
    
    return


