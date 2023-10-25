from utils.dbconfig import dbconfig
import utils.cipher as cipher
from prettytable import PrettyTable
import pyperclip

def copy_password(row_id, tv):

    details = {'sitename':tv.item(row_id, 'values')[0], 'url':tv.item(row_id, 'values')[1], 'email':tv.item(row_id, 'values')[2], 'username':tv.item(row_id, 'values')[3]}

    db = dbconfig()
    cursor = db.cursor()

    query = "SELECT * FROM passwordmanager.secrets"
    cursor.execute(query)
    row = cursor.fetchone()
    masterpassword = row[1]
    device_secret = row[2]

    query = "SELECT * FROM passwordmanager.entries WHERE "
    for i in details:
        query += f"{i} = '{details[i]}' AND "
    query = query[:-5]
    cursor.execute(query)
    result = cursor.fetchone()

    masterkey = cipher.generateKey(masterpassword, device_secret)
    password = cipher.decrypt(masterkey, result[4])
    pyperclip.copy(password)
