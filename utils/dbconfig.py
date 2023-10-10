import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
MYSQL_USERNAME = os.getenv('MYSQL_USERNAME')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')

# function to connect to mysql database
def dbconfig():
    db = mysql.connector.connect(
        host = 'localhost',
        user = MYSQL_USERNAME,
        password = MYSQL_PASSWORD
        )

    return db