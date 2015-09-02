from functools import wraps
from flask_login import current_user
from flask import flash, redirect,request

def requires_roles(required_roles):
    '''
    Takes in a list of roles and checks whether the user
    has access to those role
    '''
    def check_roles(view_function):
        @wraps(view_function)
        def decorated_function(*args, **kwargs):
            def names(role):
                return role.name
            if not all(r in map(names, current_user.roles) for r in required_roles):
                flash('You do not have sufficent permissions to do that', 'alert alert-danger')
                return redirect(request.args.get('next') or '/')
            return view_function(*args, **kwargs)
        return decorated_function
    return check_roles
