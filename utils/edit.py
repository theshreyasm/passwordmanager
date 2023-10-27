from utils.dbconfig import dbconfig
import utils.cipher as cipher
import tkinter as tk
from tkinter import ttk
from tkinter import *
import utils.generate_password as generate_password

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

# function to edit an entry in the database and gui
def edit_row(row_id, window, tv):

    # creating a new dialog box called edit_dialog
    edit_dialog = tk.Toplevel(window)
    edit_dialog.geometry("400x150")
    edit_dialog.title("Edit Entry")
    edit_dialog.resizable(False, False)

    # sitename entry in edit_dialog
    sitename_label = tk.Label(edit_dialog, text="Site Name:")
    sitename_label.grid(row=0, column=0)
    sitename_entry = tk.Entry(edit_dialog, width=30)
    sitename_entry.grid(row=0, column=1)
    sitename_entry.insert(0, tv.item(row_id, 'values')[0])

    # url entry in edit_dialog
    url_label = tk.Label(edit_dialog, text="URL:")
    url_label.grid(row=1, column=0)
    url_entry = tk.Entry(edit_dialog, width=30)
    url_entry.grid(row=1, column=1)
    url_entry.insert(0, tv.item(row_id, 'values')[1])

    # email entry in edit_dialog
    email_label = tk.Label(edit_dialog, text="Email:")
    email_label.grid(row=2, column=0)
    email_entry = tk.Entry(edit_dialog, width=30)
    email_entry.grid(row=2, column=1)
    email_entry.insert(0, tv.item(row_id, 'values')[2])

    # username entry in edit_dialog
    username_label = tk.Label(edit_dialog, text="Username:")
    username_label.grid(row=3, column=0)
    username_entry = tk.Entry(edit_dialog, width=30)
    username_entry.grid(row=3, column=1)
    username_entry.insert(0, tv.item(row_id, 'values')[3])

    # status label in edit_dialog. initially no text is displayed
    status_label = tk.Label(edit_dialog, text="", fg="green")
    status_label.grid(row=5, columnspan=2)

    # fucntion to save the updated changes in the database and gui
    def save_changes():

        # get the new sitename, url, email, username values from the respective entry boxes
        new_sitename = sitename_entry.get()
        new_url = url_entry.get()
        new_email = email_entry.get()
        new_username = username_entry.get()

        # get the old sitename, url, email and username values from the treeview
        old_sitename = tv.item(row_id, 'values')[0]
        old_url = tv.item(row_id, 'values')[1]
        old_email = tv.item(row_id, 'values')[2]
        old_username = tv.item(row_id, 'values')[3]

        # checking if new sitename is empty
        if(new_sitename == ''):
            status_label.config(text="Sitename cannot be empty.", fg="red")
        
        # checking if entry with new values already exists
        elif(checkEntry(new_sitename, new_url, new_email, new_username)):
            status_label.config(text="Entry with these details already exists.", fg="red")

        else:
            # connect to database
            db = dbconfig()
            cursor = db.cursor()

            # query to update values in database
            query = f"UPDATE passwordmanager.entries SET sitename = '{new_sitename}', url = '{new_url}', email = '{new_email}', username = '{new_username}' WHERE sitename = '{old_sitename}' AND url = '{old_url}' AND email = '{old_email}' AND username = '{old_username}'"
            cursor.execute(query)
            db.commit()

            # update values in gui and destroy edit_dialog
            tv.item(row_id, values=(new_sitename, new_url, new_email, new_username, '{hidden}', 'Edit Entry', 'Edit Password', 'Copy Password to Clipboard', 'Delete'))
            edit_dialog.destroy()

    # save changes button in edit_dialog
    save_button = tk.Button(edit_dialog, text="Save Changes", command=save_changes)
    save_button.grid(row=4, column=0, columnspan=2)


# function to edit password of an entry
def edit_password(row_id, window, tv):

    # get the sitename, url, email and username values from the treeview
    sitename = tv.item(row_id, 'values')[0]
    url = tv.item(row_id, 'values')[1]
    email = tv.item(row_id, 'values')[2]
    username = tv.item(row_id, 'values')[3]

    # creating a new dialog box edit_dialog
    edit_dialog = tk.Toplevel(window)
    edit_dialog.geometry("400x150")
    edit_dialog.title("Edit Password")
    edit_dialog.resizable(False, False)

    # password entry in edit_dialog
    password_label = tk.Label(edit_dialog, text="Enter password:")
    password_label.grid(row=0, column=0)
    password_entry = tk.Entry(edit_dialog, width=30, show='*')
    password_entry.grid(row=0, column=1)

    # confirm password entry in edit_dialog
    confirm_password_label = tk.Label(edit_dialog, text="Confirm password:")
    confirm_password_label.grid(row=1, column=0)
    confirm_password_entry = tk.Entry(edit_dialog, width=30, show='*')
    confirm_password_entry.grid(row=1, column=1)

    # status label in edit_dialog. initially no text is displayed.
    status_label = tk.Label(edit_dialog, text="", fg="green")
    status_label.grid(row=3, column=0, columnspan=2)

    # function to save the updated password in the database
    def save():

        # get the password and confirm password from the edit_dialog
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        # checking if password is empty
        if password == '':
            status_label.config(text="Password cannot be empty.", fg="red")

        # checking if passwords do not match
        elif password != confirm_password:
            status_label.config(text="Passwords do not match.", fg="red")

        else:
            
            # connect to database
            db = dbconfig()
            cursor = db.cursor()

            # get the master password  and device secret from the secrets table
            query = "SELECT * FROM passwordmanager.secrets"
            cursor.execute(query)
            row = cursor.fetchone()
            masterpassword = row[1]
            device_secret = row[2]

            # generate the masterkey and encrypt the new password using the masterkey
            masterkey = cipher.generateKey(masterpassword, device_secret)
            encrypted = cipher.encrypt(masterkey, password)
            encrypted = encrypted.decode()

            # update the new password in the database
            query = f"UPDATE passwordmanager.entries SET password = \"{encrypted}\" WHERE sitename = '{sitename}' AND url = '{url}' AND email = '{email}' AND username = '{username}'"
            cursor.execute(query)
            db.commit()

            # destroy the edit_dialog
            edit_dialog.destroy()

    # function to generate new password
    def generate_new_password():
        password = generate_password.generatePassword()
        password_entry.delete(0, "end")
        password_entry.insert(0, password)
        confirm_password_entry.delete(0, "end")
        confirm_password_entry.insert(0, password)
        status_label.config(text="New secure password is generated.", fg="green")
    
    # generate password button in edit_dialog
    generate_password_button = tk.Button(edit_dialog, text="Use a secure system-generated password", command=generate_new_password)
    generate_password_button.grid(row=6, column=0, columnspan=2)

    # save password button in edit_dialog
    save_button = tk.Button(edit_dialog, text="Save Password", command=save)
    save_button.grid(row=8, column=0, columnspan=2)

# function to delete entry in database and gui
def delete_row(row_id, window, tv, frame):

    # new dialog box called delete_dialog
    delete_dialog = tk.Toplevel(window)
    delete_dialog.title("Delete Entry")
    delete_dialog.resizable(False, False)

    # confirm whether to delete entry
    delete_label = tk.Label(delete_dialog, text="Do you want to delete this entry from the password manager?\nIt cannot be recovered after deletion.", fg="red")
    delete_label.grid(row=1, column=0)

    # delete entry if yes button clicked
    def delete_yes():

        # get the details of entry to be deleted from treeview
        details = {'sitename':tv.item(row_id, 'values')[0], 'url':tv.item(row_id, 'values')[1], 'email':tv.item(row_id, 'values')[2], 'username':tv.item(row_id, 'values')[3]}

        # connect to database
        db = dbconfig()
        cursor = db.cursor()

        # delete entry form database
        query = "DELETE FROM passwordmanager.entries WHERE "
        for i in details:
            query += f"{i} = '{details[i]}' AND "
        query = query[:-5]
        cursor.execute(query)
        db.commit()

        # destro delete dialog
        delete_dialog.destroy()

        # delete entry from gui
        tv.delete(row_id)
        tv.configure(height=tv.cget("height")-1)

    # destroy delete dialog with no changes if no button is clicked
    def delete_no():
        delete_dialog.destroy()

    # yes button in delete_dialog
    yes_button = tk.Button(delete_dialog, text="Yes", command=delete_yes)
    yes_button.grid(row=3, column=0, columnspan=2)

    # no button in delete_dialog
    no_button = tk.Button(delete_dialog, text="No", command=delete_no)
    no_button.grid(row=4, column=0, columnspan=3)
    