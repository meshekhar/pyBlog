'''
Created on April 29, 2017

@author: ravishekhar
'''

import hashlib
import hmac
import random
import string

secret_key = "smaw@eix1y4ws1d5gtd#"

def make_salt(n):
    return ''.join(random.choice(string.letters) for x in xrange(n))


def make_pw_hash(name, pw, no_char_for_salt):
    salt = make_salt(no_char_for_salt)
    return "%s,%s" %(hashlib.sha256(name + pw + salt).hexdigest(), salt)


# creates secret string with combining secret key and user value
def hash_str(strg):
    return "%s|%s" % (strg, hmac.new(secret_key, strg).hexdigest())


# checks input string agains the secret key and input
def check_hash_strg(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == hash_str(val):
        return val
