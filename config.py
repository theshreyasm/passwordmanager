from utils.dbconfig import dbconfig
import getpass
import hashlib
import random
import string


def generateRandomString(length):

    return ''.join(random.choices(string.ascii_letters + string.digits, k = length))


def config():

    # creating a new database
    db = dbconfig()
    cursor = db.cursor()

    cursor.execute("CREATE DATABASE passwordmanager")

    # create table secrets to store hash of the masterpassword and the device secret
    query = "create table passwordmanager.secrets (salt TEXT NOT NULL, masterpassword_hash TEXT NOT NULL, device_secret TEXT NOT NULL)"
    cursor.execute(query)

    # create table entries to store all website info, usernames and passwords
    query = "create table passwordmanager.entries (website TEXT NOT NULL, url TEXT NOT NULL, email TEXT, username TEXT, password TEXT NOT NULL)"
    cursor.execute(query)

    # obtaining the user's master password
    masterpassword = ""

    while(True):
        masterpassword = getpass.getpass("Enter your Master Password: ")
        if masterpassword == "":
            print("Password cannot be empty.")
            continue
        confirmpassword = getpass.getpass("Confirm your Master Password: ")
        if masterpassword != confirmpassword:
            print("Passwords do not match.")
            continue
        print("Master password is set. Do not lose this password as it cannot be recovered and you cannot access your passwords without the master password.")
        break

    # generate the salt to be used to hash the master password
    salt = generateRandomString(length = 25)

    # hash the master password after adding the salt
    hashedpass = hashlib.sha256((salt + masterpassword).encode()).hexdigest()

    # generate device secret 
    device_secret = generateRandomString(length = 15)

    # insert salt, hashed password and device secret in the secrets table
    query = "INSERT INTO passwordmanager.secrets (salt, masterpassword_hash, device_secret) VALUES (%s, %s, %s)"
    val = (salt, hashedpass, device_secret)
    cursor.execute(query, val)
    db.commit()

    # close the cursor and database connection
    cursor.close()
    db.close()
    



        



