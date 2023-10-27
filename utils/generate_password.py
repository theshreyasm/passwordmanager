import random
import string

# function to generate secure password
def generatePassword():

    # returns a random string of length 16 consisting of digits and letters
    return ''.join(random.choices(string.ascii_letters + string.digits, k = 16))