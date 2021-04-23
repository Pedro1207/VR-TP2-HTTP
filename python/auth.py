import requests

def check_login(user, token):
    x = requests.get('http://tp2-auth/checklogin?username={}&token={}'.format(user, token))
    if x.text == "True":
        return True
    else:
        return False

def check_admin(user):
    x = requests.get('http://tp2-auth/checkadmin?username={}'.format(user))
    if x.text == "(1,)":
        return True
    else:
        return False
