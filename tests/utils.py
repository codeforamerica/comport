
from comport.user.models import User

def log_in_user(testapp, department):
    # set up a user
    user = User.create(username="user", email="user@example.com", password="password")
    user.departments.append(department)
    user.active = True
    user.save()
    # login
    response = testapp.get("/login/")
    form = response.forms['loginForm']
    form['username'] = user.username
    form['password'] = 'password'
    response = form.submit().follow()
    return user
