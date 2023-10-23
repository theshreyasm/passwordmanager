import tkinter as tk
from tkinter import ttk
from tkinter import *
from dbconfig import dbconfig

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

home = display()
home.mainloop()
