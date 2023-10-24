import tkinter as tk
from tkinter import ttk
from tkinter import *
from dbconfig import dbconfig
import edit
import hashlib
import retrieve
import add

def auth():
    window = Tk()
    window.title("Password Manager")
    window.geometry("700x300")
    window.resizable(False, False)

    password_label = tk.Label(window, text="Enter Master Password:  ")
    password_label.place(relx=0.37, rely=0.5, anchor=CENTER)
    password_entry = tk.Entry(window, show='*')
    password_entry.place(relx=0.63, rely=0.5, anchor=CENTER)

    status_label = tk.Label(window, text="", fg="green")
    status_label.place(relx = 0.5, rely = 0.75, anchor=CENTER)
    
    def on_enter_click(event):
        if event.char == '\r':
            submit()

    def submit():
        
        password = password_entry.get()
        db = dbconfig()
        cursor = db.cursor()
        query = 'SELECT * FROM passwordmanager.secrets'
        cursor.execute(query)
        res = cursor.fetchone()
        salt = res[0]
        hashed_masterpassword = res[1]
        cursor.close()
        db.close()
    
        hashedpass = hashlib.sha256((salt + password).encode()).hexdigest()

        if(hashedpass != hashed_masterpassword):
            status_label.config(text="Incorrect password. Please try again.", fg="red")
        else:
            window.destroy()
            display()

    window.bind("<Key>", on_enter_click)

    submit_button = tk.Button(window, text="Submit", command=submit)
    submit_button.place(relx=0.5, rely=0.64, anchor=CENTER)

    return window


def display():
    db = dbconfig()
    cursor = db.cursor()

    query = "SELECT * FROM passwordmanager.entries"
    cursor.execute(query)
    rows = cursor.fetchall()

    window = Tk()

    frame = Frame(window)
    frame.pack(side=tk.TOP, pady=150)

    tv = ttk.Treeview(frame, columns=(1, 2, 3, 4, 5, 6, 7, 8), show="headings", height=cursor.rowcount)
    tv.pack()

    tv.heading(1, text="Site Name")
    tv.heading(2, text="Url")
    tv.heading(3, text="Email Address")
    tv.heading(4, text="Username")
    tv.heading(5, text="Password")
    tv.heading(6, text="Click to edit entry")
    tv.heading(7, text="Click to copy password")
    tv.heading(8, text="Click to delete entry")

    tv.column(1, width=200, anchor='center')
    tv.column(2, width=250, anchor='center')
    tv.column(3, width=300, anchor='center')
    tv.column(4, width=200, anchor='center')
    tv.column(5, width=100, anchor='center')
    tv.column(6, width=150, anchor='center')
    tv.column(7, width=200, anchor='center')
    tv.column(8, width=200, anchor='center')

    for row in rows:
        hidden_str = '{hidden}'
        edit_str = 'Edit'
        copy_str = 'Copy Password to Clipboard'
        delete_str = 'Delete'
        password = row[4]
        tv.insert('', 'end', values=row[:4] + (hidden_str, edit_str, copy_str, delete_str))

    def new_entry():
        add.add_row(window, tv)

    def on_cell_click(event):
        item = tv.selection()[0]
        if tv.identify_column(event.x) == "#6":
            edit.edit_row(item, window, tv, password)
        
        if tv.identify_column(event.x) == "#7":
            retrieve.copy_password(item, tv)

        if tv.identify_column(event.x) == "#8":
            edit.delete_row(item, window, tv, frame)
    
    tv.bind('<ButtonRelease-1>', on_cell_click)

    add_entry_button = tk.Button(window, text="Add Entry", command=new_entry)
    add_entry_button.pack()

    window.title("Password Manager")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{screen_width}x{screen_height}")
    window.resizable(True, True)
    return window

home = auth()
home.mainloop()
