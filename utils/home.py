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

def query_database(tv, sitename, url, email, username):
    db = dbconfig()
    cursor = db.cursor()

    query = f"SELECT * FROM passwordmanager.entries WHERE sitename LIKE '{sitename}%' AND url LIKE '{url}%' AND email LIKE '{email}%' AND username LIKE '{username}%'"
    cursor.execute(query)
    rows = cursor.fetchall()

    tv.delete(*tv.get_children())
    tv.configure(height=cursor.rowcount)

    for row in rows:
        hidden_str = '{hidden}'
        edit_str = 'Edit'
        copy_str = 'Copy Password to Clipboard'
        delete_str = 'Delete'
        password = row[4]
        tv.insert('', 'end', values=row[:4] + (hidden_str, edit_str, copy_str, delete_str))

def display():
    
    window = Tk()

    search_frame = tk.Frame(window)
    search_frame.pack(pady=50)

    frame = Frame(window)
    frame.pack(pady=50)

    tv = ttk.Treeview(frame, columns=(1, 2, 3, 4, 5, 6, 7, 8), show="headings", height=0)
    tv.pack()

    def search():
        sitename = sitename_entry.get()
        url = url_entry.get()
        email = email_entry.get()
        username = username_entry.get()

        query_database(tv, sitename, url, email, username)

    def clear_search():

        sitename_entry.delete(0, 'end')
        url_entry.delete(0, 'end')
        email_entry.delete(0, 'end')
        username_entry.delete(0, 'end')
        query_database(tv, '', '', '', '')


    sitename_label = tk.Label(search_frame, text="Site Name:")
    sitename_label.pack(side=tk.LEFT)
    sitename_entry = tk.Entry(search_frame, width=30)
    sitename_entry.pack(side=tk.LEFT, padx=5)

    url_label = tk.Label(search_frame, text="       URL:")
    url_label.pack(side=tk.LEFT)
    url_entry = tk.Entry(search_frame, width=30)
    url_entry.pack(side=tk.LEFT, padx=5)

    email_label = tk.Label(search_frame, text="     Email:")
    email_label.pack(side=tk.LEFT)
    email_entry = tk.Entry(search_frame, width=30)
    email_entry.pack(side=tk.LEFT, padx=5)

    username_label = tk.Label(search_frame, text="      Username:")
    username_label.pack(side=tk.LEFT)
    username_entry = tk.Entry(search_frame, width=30)
    username_entry.pack(side=tk.LEFT, padx=5)

    spacer_label = tk.Label(search_frame, text="        ")
    spacer_label.pack(side=tk.LEFT)
    
    search_button = tk.Button(search_frame, text="Search", command=search)
    search_button.pack(side=tk.LEFT)

    spacer_label = tk.Label(search_frame, text="        ")
    spacer_label.pack(side=tk.LEFT)

    clear_search_button = tk.Button(search_frame, text="Clear searches", command=clear_search)
    clear_search_button.pack(side=tk.LEFT)

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

    query_database(tv, '', '', '', '')

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

    add_entry_button = tk.Button(frame, text="Add Entry", command=new_entry)
    add_entry_button.pack(pady=15)

    window.title("Password Manager")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{screen_width}x{screen_height}")
    window.resizable(True, True)
    return window

home = auth()
home.mainloop()
