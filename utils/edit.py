from dbconfig import dbconfig
import cipher
import tkinter as tk
from tkinter import ttk
from tkinter import *
import generate_password

def edit_row(row_id, window, tv, password):
    edit_dialog = tk.Toplevel(window)
    edit_dialog.geometry("600x200")
    edit_dialog.title("Edit Entry")
    edit_dialog.resizable(False, False)

    sitename_label = tk.Label(edit_dialog, text="Site Name:")
    sitename_label.grid(row=0, column=0)
    sitename_entry = tk.Entry(edit_dialog, width=30)
    sitename_entry.grid(row=0, column=1)
    sitename_entry.insert(0, tv.item(row_id, 'values')[0])

    url_label = tk.Label(edit_dialog, text="URL:")
    url_label.grid(row=1, column=0)
    url_entry = tk.Entry(edit_dialog, width=30)
    url_entry.grid(row=1, column=1)
    url_entry.insert(0, tv.item(row_id, 'values')[1])

    email_label = tk.Label(edit_dialog, text="Email:")
    email_label.grid(row=2, column=0)
    email_entry = tk.Entry(edit_dialog, width=30)
    email_entry.grid(row=2, column=1)
    email_entry.insert(0, tv.item(row_id, 'values')[2])

    username_label = tk.Label(edit_dialog, text="Username:")
    username_label.grid(row=3, column=0)
    username_entry = tk.Entry(edit_dialog, width=30)
    username_entry.grid(row=3, column=1)
    username_entry.insert(0, tv.item(row_id, 'values')[3])

    password_label = tk.Label(edit_dialog, text="Password:")
    password_label.grid(row=4, column=0)
    password_entry = tk.Entry(edit_dialog, width=30, show='*')
    password_entry.grid(row=4, column=1)
    password_entry.insert(0, password)

    status_label = tk.Label(edit_dialog, text="", fg="green")
    status_label.place(relx=0.28, rely=0.9, anchor=CENTER)

    def generate_new_password():
        password = generate_password.generatePassword()
        password_entry.delete(0, "end")
        password_entry.insert(0, password)
        status_label.config(text="New secure password is generated.")

    def save_changes():
        new_sitename = sitename_entry.get()
        new_url = url_entry.get()
        new_email = email_entry.get()
        new_username = username_entry.get()
        new_password = password_entry.get()

        old_sitename = tv.item(row_id, 'values')[0]
        old_url = tv.item(row_id, 'values')[1]
        old_email = tv.item(row_id, 'values')[2]
        old_username = tv.item(row_id, 'values')[3]
        old_password = password

        tv.item(row_id, values=(new_sitename, new_url, new_email, new_username, new_password))
        edit_dialog.destroy()

        db = dbconfig()
        cursor = db.cursor()

        query = "SELECT * FROM passwordmanager.secrets"
        cursor.execute(query)
        row = cursor.fetchone()
        masterpassword = row[1]
        device_secret = row[2]

        masterkey = cipher.generateKey(masterpassword, device_secret)
        encrypted = cipher.encrypt(masterkey, new_password)
        encrypted = encrypted.decode()

        query = f"UPDATE passwordmanager.entries SET sitename = '{new_sitename}', url = '{new_url}', email = '{new_email}', username = '{new_username}', password = \"{encrypted}\" WHERE sitename = '{old_sitename}' AND url = '{old_url}' AND email = '{old_email}' AND username = '{old_username}'"
        cursor.execute(query)
        db.commit()
        
    generate_password_button = tk.Button(edit_dialog, text="Generate new secure password", command=generate_new_password)
    generate_password_button.grid(row=4, column=2, columnspan=2)

    save_button = tk.Button(edit_dialog, text="Save Changes", command=save_changes)
    save_button.grid(row=6, column=0, columnspan=2)

def delete_row(row_id, window, tv, frame):
    delete_dialog = tk.Toplevel(window)
    # delete_dialog.geometry("600x200")
    delete_dialog.title("Delete Entry")
    delete_dialog.resizable(False, False)

    delete_label = tk.Label(delete_dialog, text="Do you want to delete this entry from the password manager?\nIt cannot be recovered after deletion.", fg="red")
    delete_label.grid(row=1, column=0)

    def delete_yes():
        details = {'sitename':tv.item(row_id, 'values')[0], 'url':tv.item(row_id, 'values')[1], 'email':tv.item(row_id, 'values')[2], 'username':tv.item(row_id, 'values')[3]}

        db = dbconfig()
        cursor = db.cursor()

        query = "DELETE FROM passwordmanager.entries WHERE "
        for i in details:
            query += f"{i} = '{details[i]}' AND "
        query = query[:-5]
        cursor.execute(query)
        db.commit()

        delete_dialog.destroy()
        tv.delete(row_id)
        tv.configure(height=tv.cget("height")-1)

    def delete_no():
        delete_dialog.destroy()

    yes_button = tk.Button(delete_dialog, text="Yes", command=delete_yes)
    yes_button.grid(row=3, column=0, columnspan=2)

    no_button = tk.Button(delete_dialog, text="No", command=delete_no)
    no_button.grid(row=4, column=0, columnspan=3)
    