from utils.dbconfig import dbconfig
import utils.cipher as cipher
from utils.generate_password import generatePassword
import getpass
import tkinter as tk
from tkinter import ttk
from tkinter import *

# function to check if a given entry already exists in the database.
def checkEntry(sitename, url, email, username):
    
    #connect to the database
    db = dbconfig()
    cursor = db.cursor()

    # query to get all entries with given sitename, url, email and username
    query = f"SELECT * FROM passwordmanager.entries WHERE sitename = '{sitename}' AND url = '{url}' AND email = '{email}' AND username = '{username}'"
    cursor.execute(query)
    results = cursor.fetchall()

    # close the connection
    cursor.close()
    db.close()
    
    # returns true if such an entry already exists, otherwise returns false
    if len(results)!=0:
        return True
    return False


# function to add a new entry in the database and gui
def add_row(window, tv):
    
    # creating a new dialog box called add_dialog
    add_dialog = tk.Toplevel(window)
    add_dialog.geometry("400x300")
    add_dialog.title("Add New Entry")
    add_dialog.resizable(False, False)

    # sitename entry in add_dialog
    sitename_label = tk.Label(add_dialog, text="Site Name:")
    sitename_label.grid(row=0, column=0)
    sitename_entry = tk.Entry(add_dialog, width=30)
    sitename_entry.grid(row=0, column=1)

    # url entry in add_dialog
    url_label = tk.Label(add_dialog, text="URL:")
    url_label.grid(row=1, column=0)
    url_entry = tk.Entry(add_dialog, width=30)
    url_entry.grid(row=1, column=1)

    # email entry in add_dialog
    email_label = tk.Label(add_dialog, text="Email:")
    email_label.grid(row=2, column=0)
    email_entry = tk.Entry(add_dialog, width=30)
    email_entry.grid(row=2, column=1)

    # username entry in add_dialog
    username_label = tk.Label(add_dialog, text="Username:")
    username_label.grid(row=3, column=0)
    username_entry = tk.Entry(add_dialog, width=30)
    username_entry.grid(row=3, column=1)

    # password entry in add_dialog
    password_label = tk.Label(add_dialog, text="Enter password:")
    password_label.grid(row=4, column=0)
    password_entry = tk.Entry(add_dialog, width=30, show='*')
    password_entry.grid(row=4, column=1)

    # confirm password entry in add_dialog
    confirm_password_label = tk.Label(add_dialog, text="Confirm password:")
    confirm_password_label.grid(row=5, column=0)
    confirm_password_entry = tk.Entry(add_dialog, width=30, show='*')
    confirm_password_entry.grid(row=5, column=1)

    # status label in add_dialog. Initially does not display any text
    status_label = tk.Label(add_dialog, text="", fg="green")
    status_label.grid(row=7, column=0, columnspan=2)

    # function to add a new entry in the database and gui
    def add():

        # get all the values from the respective entry boxes in add_dialog 
        sitename = sitename_entry.get()
        url = url_entry.get()
        email = email_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        # checking if an entry with same details already exists
        if checkEntry(sitename, url, email, username):
            status_label.config(text="Entry with same details already exists.", fg='red')
    
        # checking if given sitename is empty
        elif sitename == '':
            status_label.config(text="Sitename cannot be empty.", fg="red")

        # checking if given password is empty
        elif password == '':
            status_label.config(text="Password cannot be empty.", fg="red")

        # checking if passwords do not match
        elif password != confirm_password:
            status_label.config(text="Passwords do not match.", fg="red")

        else:
            # connect to database
            db = dbconfig()
            cursor = db.cursor()

            # get the master password and device secret from secrets table
            query = "SELECT * FROM passwordmanager.secrets"
            cursor.execute(query)
            row = cursor.fetchone()
            masterpassword = row[1]
            device_secret = row[2]

            # generate masterkey and encrypt the password using masterkey
            masterkey = cipher.generateKey(masterpassword, device_secret)
            encrypted = cipher.encrypt(masterkey, password)

            # insert the new values into database
            query = "INSERT INTO passwordmanager.entries (sitename, url, email, username, password) values (%s, %s, %s, %s, %s)"
            val = (sitename, url, email, username, encrypted)
            cursor.execute(query, val)
            db.commit()

            # insert new row in gui and destry the add_dialog
            row_values = (sitename, url, email, username, '{hidden}', 'Edit Entry', 'Edit Password', 'Copy Password to Clipboard', 'Delete')
            add_dialog.destroy()
            tv.insert('', 'end', values=row_values)
            tv.configure(height=tv.cget("height")+1)

    # function to generate new password
    def generate_new_password():
        password = generatePassword()
        password_entry.delete(0, "end")
        password_entry.insert(0, password)
        confirm_password_entry.delete(0, "end")
        confirm_password_entry.insert(0, password)
        status_label.config(text="New secure password is generated.")
    
    # generate password button in add_dialog
    generate_password_button = tk.Button(add_dialog, text="Use a secure system-generated password", command=generate_new_password)
    generate_password_button.grid(row=6, column=0, columnspan=2)

    # add entry button in add_dialog
    save_button = tk.Button(add_dialog, text="Add Entry", command=add)
    save_button.grid(row=8, column=0, columnspan=2)

