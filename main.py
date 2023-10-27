from utils.dbconfig import dbconfig
import config
import home as home

# function to check if password manager is already configured
def checkConfig():

    # connect to database
    db = dbconfig()
    cursor = db.cursor()
    
    # check if database password manager exists
    query = "SHOW DATABASES LIKE 'passwordmanager'"
    cursor.execute(query)
    res = cursor.fetchone()

    # if database passwordmanager exists
    if res:

        query = "USE passwordmanager"
        cursor.execute(query)

        # check if table secrets exists
        query = "SHOW TABLES LIKE 'secrets'"
        cursor.execute(query)
        res_secrets = cursor.fetchone()

        # if table secrets exists
        if res_secrets:
            
            # count number of rows in secrets table
            query = "SELECT COUNT(*) FROM secrets"
            cursor.execute(query)
            count = cursor.fetchone()[0]

            # if secrets table has only one row 
            if count == 1:

                # check if table entries exists
                query = "SHOW TABLES LIKE 'entries'"
                cursor.execute(query)
                res_entries = cursor.fetchone()  

                # return true if table entries exists
                if res_entries:
                    return True
        
        # if even one condition fails, delete the passwordmanager database. it will be reconfigured again correctly
        query = "DROP DATABASE passwordmanager"
        cursor.execute(query)
    
    # return false if even any one of the above conditions fail
    return False

# main function
def main():

    # try configure password manager window
    try:
        root = config.config()
        root.mainloop()

    # if any exception, it might be that passwordmanager database already exists. 
    except:
        
        # if password manager is configured properly, run authenticate password manager
        if checkConfig():
            root = home.auth()
            root.mainloop()

        # else if checkConfig() return false, then database passwordmanager is deleted. Reconfigure the password manager.
        else:
            root = config.config()
            root.mainloop()


# run the main function
main()

    
