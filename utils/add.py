from utils.dbconfig import dbconfig
import utils.cipher as cipher
from utils.generate_password import generatePassword
import getpass
import tkinter as tk
from tkinter import ttk
from tkinter import *

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

def add_row(window, tv):
    
    add_dialog = tk.Toplevel(window)
    add_dialog.geometry("400x300")
    add_dialog.title("Add New Entry")
    add_dialog.resizable(False, False)

    sitename_label = tk.Label(add_dialog, text="Site Name:")
    sitename_label.grid(row=0, column=0)
    sitename_entry = tk.Entry(add_dialog, width=30)
    sitename_entry.grid(row=0, column=1)

    url_label = tk.Label(add_dialog, text="URL:")
    url_label.grid(row=1, column=0)
    url_entry = tk.Entry(add_dialog, width=30)
    url_entry.grid(row=1, column=1)

    email_label = tk.Label(add_dialog, text="Email:")
    email_label.grid(row=2, column=0)
    email_entry = tk.Entry(add_dialog, width=30)
    email_entry.grid(row=2, column=1)

    username_label = tk.Label(add_dialog, text="Username:")
    username_label.grid(row=3, column=0)
    username_entry = tk.Entry(add_dialog, width=30)
    username_entry.grid(row=3, column=1)

    password_label = tk.Label(add_dialog, text="Enter password:")
    password_label.grid(row=4, column=0)
    password_entry = tk.Entry(add_dialog, width=30, show='*')
    password_entry.grid(row=4, column=1)

    confirm_password_label = tk.Label(add_dialog, text="Confirm password:")
    confirm_password_label.grid(row=5, column=0)
    confirm_password_entry = tk.Entry(add_dialog, width=30, show='*')
    confirm_password_entry.grid(row=5, column=1)

    status_label = tk.Label(add_dialog, text="", fg="green")
    status_label.grid(row=7, column=0, columnspan=2)

    def add():
        sitename = sitename_entry.get()
        url = url_entry.get()
        email = email_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if checkEntry(sitename, url, email, username):
            status_label.config(text="Entry with same details already exists.", fg='red')
    
        elif sitename == '':
            status_label.config(text="Sitename cannot be empty.", fg="red")

        elif password == '':
            status_label.config(text="Password cannot be empty.", fg="red")

        elif password != confirm_password:
            status_label.config(text="Passwords do not match.", fg="red")

        else:
            db = dbconfig()
            cursor = db.cursor()

            query = "SELECT * FROM passwordmanager.secrets"
            cursor.execute(query)
            row = cursor.fetchone()
            masterpassword = row[1]
            device_secret = row[2]

            masterkey = cipher.generateKey(masterpassword, device_secret)
            encrypted = cipher.encrypt(masterkey, password)

            query = "INSERT INTO passwordmanager.entries (sitename, url, email, username, password) values (%s, %s, %s, %s, %s)"
            val = (sitename, url, email, username, encrypted)
            cursor.execute(query, val)
            db.commit()

            row_values = (sitename, url, email, username, '{hidden}', 'Edit Entry', 'Edit Password', 'Copy Password to Clipboard', 'Delete')
            add_dialog.destroy()
            tv.insert('', 'end', values=row_values)
            tv.configure(height=tv.cget("height")+1)

    def generate_new_password():
        password = generatePassword()
        password_entry.delete(0, "end")
        password_entry.insert(0, password)
        confirm_password_entry.delete(0, "end")
        confirm_password_entry.insert(0, password)
        status_label.config(text="New secure password is generated.")
    
    generate_password_button = tk.Button(add_dialog, text="Use a secure system-generated password", command=generate_new_password)
    generate_password_button.grid(row=6, column=0, columnspan=2)

    save_button = tk.Button(add_dialog, text="Add Entry", command=add)
    save_button.grid(row=8, column=0, columnspan=2)

