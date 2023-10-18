from utils.dbconfig import dbconfig
from config import config
import passwordmanager as pm

def checkConfig():

    db = dbconfig()
    cursor = db.cursor()
    
    query = "SHOW DATABASES LIKE 'passwordmanager'"
    cursor.execute(query)
    res = cursor.fetchone()

    if res:

        query = "USE passwordmanager"
        cursor.execute(query)

        query = "SHOW TABLES LIKE 'secrets'"
        cursor.execute(query)
        res_secrets = cursor.fetchone()

        if res_secrets:

            query = "SELECT COUNT(*) FROM secrets"
            cursor.execute(query)
            count = cursor.fetchone()[0]

            if count == 1:
                query = "SHOW TABLES LIKE 'entries'"
                cursor.execute(query)
                res_entries = cursor.fetchone()  

                if res_entries:
                    return True
        
        query = "DROP DATABASE passwordmanager"
        cursor.execute(query)
    
    return False
        


def main():

    option = input("1. Configure your password manager.\n2. Access your password manager.\n3. Delete your password manager.\nInput option number. ")

    while(option != '1' and option != '2' and option != '3'):
        print("Input either 1, 2, or 3.")
        option = input("1. Configure your password manager.\n2. Access your password manager.\n3. Delete your password manager.\nInput option number. ")

    if option == 1:

        if not checkConfig():
            print("Provide master password to configure your password manager.")
            config()

        else:
            print("Password manager is already configured.")
        
    if option == 2:

        if checkConfig():
            pm.passwordmanager()
        
        else:
            print("Password manager not yet configured. Please configure the password manager to access it.")
    
    if option == 3:

        db = dbconfig()
        cursor = db.cursor()

        query = "SHOW DATABASES LIKE 'passwordmanager'"
        cursor.execute(query)
        res = cursor.fetchone()

        if res:
            query = "DROP DATABASE passwordmanager"
            cursor.execute(query)
        
            print("Password manager is deleted.")
        
        else:
            print("Password manager does not exist.")
    
    return

if __name__ == main:
    main()

    
