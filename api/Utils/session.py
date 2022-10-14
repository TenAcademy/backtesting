import hashlib

pwd = "5f4dcc3b5aa765d61d8327deb882cf99"
def log_in(user:dict):
    uname=user["name"]
    password=user["pass"]
    hpwd=hashlib.md5(password.encode()).hexdigest()
    if uname=="name" and hpwd==pwd:
        return True
    else:
        return False
