from utils.dbconfig import dbconfig
import config
import utils.home as home

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

    try:
        root = config.config()
        root.mainloop()

    except:

        if checkConfig():
            root = home.auth()
            root.mainloop()
        else:
            root = config.config()
            root.mainloop()


main()

    
