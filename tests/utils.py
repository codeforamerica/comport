
from comport.user.models import User, Role

def create_and_log_in_user(testapp=None, department=None, rolename=None, username="user"):
    # set up a user
    user = User.create(username=username, email="{}@example.com".format(username), password="password")

    # associate a department if a department is passed
    if department:
        user.departments.append(department)

    user.active = True
    user.save()

    # associate a role if a name is passed
    if rolename:
        user_role = Role(name=rolename)
        user_role.save()
        user.roles.append(user_role)

    # login
    response = testapp.get("/login/")
    form = response.forms['loginForm']
    form['username'] = user.username
    form['password'] = 'password'
    response = form.submit().follow()
    return user
