from functools import wraps
from flask_login import current_user
from flask import flash, redirect,request, abort
from comport.department.models import Extractor, Department

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

def admin_or_department_required():
    '''
    Reads department from current_user and checks whether the user
    has access to that department or is an admin
    '''
    def check_department(view_function):
        @wraps(view_function)
        def decorated_function(*args, **kwargs):
            if current_user.department_id == kwargs["department_id"] or current_user.is_admin():
                return view_function(*args, **kwargs)
            flash('You do not have sufficent permissions to do that', 'alert alert-danger')
            return redirect(request.args.get('next') or '/')
        return decorated_function
    return check_department

def extractor_auth_required():
    '''
    Ensures that current_user is an extractor with access to the correct department
    '''
    def check_extractor(view_function):
        @wraps(view_function)
        def decorated_function(*args, **kwargs):
            username = request.authorization.username
            password = request.authorization.password

            found_extractor = Extractor.query.filter_by(username=username).first()

            if not found_extractor or not found_extractor.check_password(password):
                return ("Extractor authorization failed.", 401)

            return view_function(*args, **kwargs)
        return decorated_function
    return check_extractor
