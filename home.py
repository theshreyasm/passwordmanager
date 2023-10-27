import tkinter as tk
from tkinter import ttk
from tkinter import *
from utils.dbconfig import dbconfig
import utils.edit as edit
import hashlib
import utils.retrieve as retrieve
import utils.add as add

# authentication window before you access password manager
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
    
    # when enter button is clicked, call function submit()
    def on_enter_click(event):
        if event.char == '\r':
            submit()

    
    def submit():
        
        # get the password from the entry box
        password = password_entry.get()

        # connect to database
        db = dbconfig()
        cursor = db.cursor()

        # get the salt and hashed master password from secrets table
        query = 'SELECT * FROM passwordmanager.secrets'
        cursor.execute(query)
        res = cursor.fetchone()
        salt = res[0]
        hashed_masterpassword = res[1]

        # close the cpnnection
        cursor.close()
        db.close()
    
        # hash the entered password with the salt
        hashedpass = hashlib.sha256((salt + password).encode()).hexdigest()

        # check if the hashed password and the hashed master password are different
        if(hashedpass != hashed_masterpassword):
            status_label.config(text="Incorrect password. Please try again.", fg="red")
        else:
            # if both hashes are same, destroy authentication window and open password manager
            window.destroy()
            display()

    # binding function to deal with key press
    window.bind("<Key>", on_enter_click)

    # submit button
    submit_button = tk.Button(window, text="Submit", command=submit)
    submit_button.place(relx=0.5, rely=0.64, anchor=CENTER)

    return window

# function to get all required entries from database
def query_database(tv, sitename, url, email, username):

    # connect to database
    db = dbconfig()
    cursor = db.cursor()

    # query to get the required entries
    query = f"SELECT * FROM passwordmanager.entries WHERE sitename LIKE '{sitename}%' AND url LIKE '{url}%' AND email LIKE '{email}%' AND username LIKE '{username}%'"
    cursor.execute(query)
    rows = cursor.fetchall()

    # remove all existing rows from treeview
    tv.delete(*tv.get_children())

    # configure the treeview height
    tv.configure(height=cursor.rowcount)

    # insert the fetched rows from query into treeview
    for row in rows:
        hidden_str = '{hidden}'
        edit_str = 'Edit Entry'
        editpass_str = 'Edit Password'
        copy_str = 'Copy Password to Clipboard'
        delete_str = 'Delete'
        tv.insert('', 'end', values=row[:4] + (hidden_str, edit_str, editpass_str, copy_str, delete_str))

# password manager
def display():
    
    window = Tk()

    # search frame contains the entry boxes and search and clear search button to search for particular entries
    search_frame = tk.Frame(window)
    search_frame.pack(pady=50)

    # frame contains the treeview that shows all entries and the add entry button
    frame = Frame(window)
    frame.pack(pady=50)

    # treevieew
    tv = ttk.Treeview(frame, columns=(1, 2, 3, 4, 5, 6, 7, 8, 9), show="headings", height=0)
    tv.pack()

    # search function
    def search():

        # get the sitename, url, email adn username from the entry boxes
        sitename = sitename_entry.get()
        url = url_entry.get()
        email = email_entry.get()
        username = username_entry.get()

        # call query database by passing the sitename, url, email and username as parameters
        query_database(tv, sitename, url, email, username)

    # clear search function
    def clear_search():

        # empty the entry boxes and display all entries
        sitename_entry.delete(0, 'end')
        url_entry.delete(0, 'end')
        email_entry.delete(0, 'end')
        username_entry.delete(0, 'end')
        query_database(tv, '', '', '', '')

    # entry boxes in the search frame
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
    
    # search button
    search_button = tk.Button(search_frame, text="Search", command=search)
    search_button.pack(side=tk.LEFT)

    spacer_label = tk.Label(search_frame, text="        ")
    spacer_label.pack(side=tk.LEFT)

    # clear search button
    clear_search_button = tk.Button(search_frame, text="Clear searches", command=clear_search)
    clear_search_button.pack(side=tk.LEFT)

    # headings for all columns
    tv.heading(1, text="Site Name")
    tv.heading(2, text="Url")
    tv.heading(3, text="Email Address")
    tv.heading(4, text="Username")
    tv.heading(5, text="Password")
    tv.heading(6, text="Click to edit entry")
    tv.heading(7, text="Click to edit password")
    tv.heading(8, text="Click to copy password")
    tv.heading(9, text="Click to delete entry")

    # setting width and centering all columns
    tv.column(1, width=200, anchor='center')
    tv.column(2, width=250, anchor='center')
    tv.column(3, width=300, anchor='center')
    tv.column(4, width=200, anchor='center')
    tv.column(5, width=100, anchor='center')
    tv.column(6, width=150, anchor='center')
    tv.column(7, width=200, anchor='center')
    tv.column(8, width=200, anchor='center')
    tv.column(9, width=200, anchor='center')

    # display all entries
    query_database(tv, '', '', '', '')

    # call add_row() from add.py whenever new entry has to be added
    def new_entry():
        add.add_row(window, tv)

    # define commands to be performed during a cell click
    def on_cell_click(event):
        item = tv.selection()[0]

        # if cell clicked is in column 6 (i.e edit entry), call edit_row() from edit.py
        if tv.identify_column(event.x) == "#6":
            edit.edit_row(item, window, tv)

        # if cell clicked is in column 7 (i.e edit password), call edit_password() from edit.py
        if tv.identify_column(event.x) == "#7":
            edit.edit_password(item, window, tv)
        
        # if cell clicked is in column 8 (i.e copy password to clipboard), call copy_password() from retrieve.py
        if tv.identify_column(event.x) == "#8":
            retrieve.copy_password(item, tv)

        # if cell clicked is in column 9 (i.e delete), call delete_row() from edit.py
        if tv.identify_column(event.x) == "#9":
            edit.delete_row(item, window, tv, frame)
    
    # binding functions to dell with cell click
    tv.bind('<ButtonRelease-1>', on_cell_click)

    # add entry button
    add_entry_button = tk.Button(frame, text="Add Entry", command=new_entry)
    add_entry_button.pack(pady=15)

    # geometry and title of password manager window
    window.title("Password Manager")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{screen_width}x{screen_height}")
    window.resizable(True, True)
    
    return window

