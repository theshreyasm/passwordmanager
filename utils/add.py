from utils.dbconfig import dbconfig
import utils.cipher as cipher
from utils.generate_password import generatePassword
import getpass

def checkEntry(sitename, url, email, username):
    
    db = dbconfig()
    cursor = db.cursor()
    query = f"SELECT * FROM passwordmanager.entries WHERE sitename = '{sitename}' AND url = '{url}' AND email = '{email}' AND username = '{username}'"
    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    db.close()
    
    if len(results)!=0:
        return True
    return False

def addEntry(masterpassword, device_secret, sitename, url, email, username):

    if(checkEntry(sitename, url, email, username)):
        print("Entry with these details already exists.")
        return
    
    option = input("Do you want to use a secure system generated password? y or n? ")

    while(option != 'y' and option != 'n'):
        print("Answer either y or n.")
        option = input("Do you want to use a secure system generated password? y or n? ")

    if(option == 'n'):
        password = getpass.getpass("Enter your password: ")
    else:
        password = generatePassword()
        print("Secure password is generated.")

    masterkey = cipher.generateKey(masterpassword, device_secret)
    encrypted = cipher.encrypt(masterkey, password)

    db = dbconfig()
    cursor = db.cursor()
    query = "INSERT INTO passwordmanager.entries (sitename, url, email, username, password) values (%s, %s, %s, %s, %s)"
    val = (sitename, url, email, username, encrypted)
    cursor.execute(query, val)
    db.commit()

    cursor.close()
    db.close()
    
    print("New entry is created.")
