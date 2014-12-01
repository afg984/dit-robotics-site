import string
import random

def gen_token(length):
    choices = string.ascii_letters + string.digits
    return ''.join(random.choice(choices) for k in range(length))
