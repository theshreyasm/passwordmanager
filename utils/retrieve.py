from utils.dbconfig import dbconfig
import utils.cipher as cipher
from prettytable import PrettyTable
import pyperclip

# function to copy password of an entry to your clipboard
def copy_password(row_id, tv):

    # getting the sitename, url, email and username values of the entry from the treeview
    details = {'sitename':tv.item(row_id, 'values')[0], 'url':tv.item(row_id, 'values')[1], 'email':tv.item(row_id, 'values')[2], 'username':tv.item(row_id, 'values')[3]}

    # connect to the database
    db = dbconfig()
    cursor = db.cursor()

    # get the master password  and device secret from the secrets table
    query = "SELECT * FROM passwordmanager.secrets"
    cursor.execute(query)
    row = cursor.fetchone()
    masterpassword = row[1]
    device_secret = row[2]

    # query to get the row with the given sitename, url, email and username from the database
    query = "SELECT * FROM passwordmanager.entries WHERE "
    for i in details:
        query += f"{i} = '{details[i]}' AND "
    query = query[:-5]
    cursor.execute(query)
    result = cursor.fetchone()

    # generate masterkey and decrypt the password using the masterkey
    # result[4] is the encrypted password of the required entry
    masterkey = cipher.generateKey(masterpassword, device_secret)
    password = cipher.decrypt(masterkey, result[4])

    # copy password to clipboard
    pyperclip.copy(password)
