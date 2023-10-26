# Password Manager

A secure, user-friendly password manager written in Python and MySQL. It employs PBKDF2 to generate a 256-bit key from the master password and the device secret, which is then used with AES-256 for encryption/decryption. Additionally, SHA-256 is utilized to hash the master password.
The GUI was developed using Tkinter.

## Installation

Python and MySQL are required to run this password manager.

### Install Python requirements

```
pip install requirements.txt
```

### Create MySQL user and grant permissions

**Login to mysql as root**
- If you are using Linux:
```
sudo mysql -u root -p
```
- If you are using Windows:
```
mysql.exe -u root -p
```

**Create User**


Give any username and password of your choice.
```
CREATE USER 'user'@localhost IDENTIFIED BY 'password';
```

**Grant Permissions**
```
GRANT ALL PRIVILEGES ON *.* TO 'user'@localhost IDENTIFIED BY 'password';
```

### Creating .env file

**Clone this repository and change directory**

```
git clone https://github.com/theshreyasm/passwordmanager.git
cd passwordmanager
```

**Create .env file**

Create a new file called .env. Enter the contents in the below code block in the .env file.
```
MYSQL_USERNAME = user
MYSQL_PASSWORD = password
```

Replace user and password with the username ad password you gave to the MySQL User that you created above.

## Run 

Now you have completed all the requirements to run the password manager. Whenever you want to use the password manager, change directory to where you cloned the repository above and run the command below.
```
python main.py
```

## Usage

![config](https://github.com/theshreyasm/passwordmanager/assets/97665416/55ef9dca-bb0d-4b99-b0a9-a787faec6d95)


![auth](https://github.com/theshreyasm/passwordmanager/assets/97665416/7873c131-d557-4b4b-9a1e-a586100a8cac)


![home](https://github.com/theshreyasm/passwordmanager/assets/97665416/9663cb7f-5e20-4d23-85e7-52e4da149d24)


- When you run this for the first time, 'Configure Password Manager' window opens up. Enter a master password of your choice and keep it safe and secure. 
- Use steps given in [Run](#run) to use the password manager.
- First, the authorization window opens up. Enter your correct master password to access your password manager.
- Click on 'Add Entry' button to add any new entry.
- Click on 'Copy Password to Clipboard' cell to copy password of the respective entry to your clipboard.
- Click on the cells 'Edit Entry' or 'Edit Password' to edit the entry or password respectively.
- Click on 'Delete' to delete that particular entry.
- You can search for particular entries using the entry boxes and the 'Search' button on the top.
- Click on 'Clear Search' to clear the searches.
