import re

def check_password_strength(password): # password criteria
    length = len(password)
    if length < 8:
        return 'Weak'
    
    uppercase= re.search(r'[A-Z]', password)
    lowercase = re.search(r'[a-z]', password)
    digit = re.search(r'\d', password)
    special_char = re.search(r'[!@#$%^&*(),.?\":{}|<>_]', password)
    
    if uppercase and lowercase and digit and special_char and length:
        return 'Strong'
    elif (uppercase or lowercase) and digit and (length >=10 or length <=8):
        return 'Fair'
    else:
        return 'Weak'