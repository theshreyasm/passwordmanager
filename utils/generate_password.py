import random
import string

def generatePassword():

    return ''.join(random.choices(string.ascii_letters + string.digits, k = 16))