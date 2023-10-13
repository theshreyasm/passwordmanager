from dbconfig import dbconfig
import cipher
from prettytable import PrettyTable
import pyperclip

def retrieve(masterpassword, device_secret, details):

    db = dbconfig()
    cursor = db.cursor()

    query = ''

    if len(details)==0:
        query = "SELECT * FROM passwordmanager.entries"
    else:
        query = "SELECT * FROM passwordmanager.entries WHERE "

        for i in details:
            query += f"{i} = '{details[i]}' AND "
        query = query[:-5]

    cursor.execute(query)
    results = cursor.fetchall()

    if len(results)==0:
        print("No such entry available.")
    else:
        table = PrettyTable(cursor.column_names)
        for row in results:
            table.add_row(row[0], row[1], row[2], row[3], "{hidden}")

        if len(results)==1:
            option = input("Do you want to retrieve the password for this entry? y or n? ")

            while(option != 'y' and option != 'n'):
                print("Answer either y or n.")
                option = input("Do you want to retrieve the password for this entry? y or n? ")

            if(option == 'y'):
                masterkey = cipher.generateKey(masterpassword, device_secret)
                password = cipher.decrypt(masterkey, row[4])
                pyperclip.copy(password)
                print("Password copied to clipboard")
    
    cursor.close()
    db.close()
    
    return