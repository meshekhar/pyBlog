'''
Created on April 29, 2017

@author: ravishekhar
'''

import hashlib
import hmac
import random
import string

secret_key = "ravishekhar"

def make_salt(n):
    return ''.join(random.choice(string.letters) for x in xrange(n))


def make_pw_hash(name, pw, no_char_for_salt):
    salt = make_salt(no_char_for_salt)
    return "%s,%s" %(hashlib.sha256(name + pw + salt).hexdigest(), salt)


def hash_str(strg):
    return "%s | %s" %(strg, hmac.new(secret_key, strg).hexdigest())

