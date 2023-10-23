import tkinter as tk
from tkinter import ttk
from tkinter import *
from dbconfig import dbconfig
import hashlib

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
    frame.pack(side=tk.LEFT, padx=40)

    tv = ttk.Treeview(frame, columns=(1, 2, 3, 4, 5), show="headings", height=cursor.rowcount)
    tv.pack()

    tv.heading(1, text="Site Name")
    tv.heading(2, text="Url")
    tv.heading(3, text="Email Address")
    tv.heading(4, text="Username")
    tv.heading(5, text="Password")

    tv.column(1, width=200, anchor='center')
    tv.column(2, width=250, anchor='center')
    tv.column(3, width=300, anchor='center')
    tv.column(4, width=200, anchor='center')
    tv.column(5, width=250, anchor='center')

    for row in rows:
        hidden_str = '{hidden}'
        tv.insert('', 'end', values=row[:4] + (hidden_str,))

    window.title("Password Manager")
    window.geometry("1300x800")
    window.resizable(True, True)
    return window

home = auth()
home.mainloop()
