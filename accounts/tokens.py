import string
import random

def gen_token(length):
    return ''.join(random.choice(string.ascii_letters) for k in range(length))
