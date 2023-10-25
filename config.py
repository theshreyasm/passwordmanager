from utils.dbconfig import dbconfig
import getpass
import hashlib
import random
import string
import tkinter as tk
from tkinter import ttk
from tkinter import *


def generateRandomString(length):

    return ''.join(random.choices(string.ascii_letters + string.digits, k = length))


def config():

    db = dbconfig()
    cursor = db.cursor()

    cursor.execute("CREATE DATABASE passwordmanager")

    # create table secrets to store hash of the masterpassword and the device secret
    query = "create table passwordmanager.secrets (salt TEXT NOT NULL, masterpassword_hash TEXT NOT NULL, device_secret TEXT NOT NULL)"
    cursor.execute(query)

    # create table entries to store all website info, usernames and passwords
    query = "create table passwordmanager.entries (sitename TEXT NOT NULL, url TEXT, email TEXT, username TEXT, password TEXT NOT NULL)"
    cursor.execute(query)

    window = Tk()
    window.title("Configure Password Manager")
    window.geometry("700x300")
    window.resizable(False, False)

    password_frame = tk.Frame(window)
    password_frame.pack()

    text_label = tk.Label(password_frame, text="Create master password for your password manager.", fg="green")
    text_label.grid(row=0, columnspan=2, pady=20)
    
    password_label = tk.Label(password_frame, text="Enter Master Password:")
    password_label.grid(row=1, column=0)
    password_entry = tk.Entry(password_frame, width=30, show='*')
    password_entry.grid(row=1, column=1)

    confirm_password_label = tk.Label(password_frame, text="Confirm Master Password:")
    confirm_password_label.grid(row=2, column=0)
    confirm_password_entry = tk.Entry(password_frame, width=30, show='*')
    confirm_password_entry.grid(row=2, column=1)

    status_label = tk.Label(password_frame, text="", fg="red")
    status_label.grid(row=4, columnspan=2)


    def save(): 

        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if password == "":
            status_label.config(text="Password cannot be empty.")
        
        elif password != confirm_password:
            status_label.config(text="Passwords do not match.")

        else:
            
            salt = generateRandomString(length = 25)
            hashedpass = hashlib.sha256((salt + password).encode()).hexdigest()
            device_secret = generateRandomString(length = 15)

            query = "INSERT INTO passwordmanager.secrets (salt, masterpassword_hash, device_secret) VALUES (%s, %s, %s)"
            val = (salt, hashedpass, device_secret)
            cursor.execute(query, val)
            db.commit() 

            cursor.close()
            db.close()

            window.destroy()

            warning_window = Tk()
            warning_window.title("Warning")
            warning_window.resizable(False, False)

            warning_label = tk.Label(warning_window, text="Master password is set for your password manager.\nDo not lose this master password as you cannot access your password manager without it.\nReopen this application to access your password manager.", fg="red")
            warning_label.pack(padx=30, pady=30)

            return warning_window
    
    save_button = tk.Button(password_frame, text="Save Master Password", command=save)
    save_button.grid(row=3, columnspan=2, pady=20)
    return window



