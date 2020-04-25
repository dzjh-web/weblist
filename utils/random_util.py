import random
import string
import hashlib
import datetime
import django.utils.timezone as timezone;

def randomMulti(length):
    return ''.join(random.sample(string.ascii_letters + string.digits, length));

def randomStr(length):
    return ''.join(random.sample(string.ascii_letters, length));

def randomNum(length):
    return ''.join(random.sample(string.digits, length));

def randomToken(length = 32):
    randCode = randomMulti(length); # length长度的随机码
    return hashlib.md5("|".join([timezone.localtime(timezone.now()).strftime('%Y-%m-%d-%H-%M-%S'), randCode]).encode("utf-8")).hexdigest();