# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""
from flask import url_for
from comport.user.models import User, Role, Invite_Code
from comport.department.models import Department


class TestLoggingIn:

    def test_can_log_in_returns_200(self, user, testapp):
        # Goes to homepage
        res = testapp.get("/login/")
        # Fills out login form in navbar
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'myprecious'
        # Submits
        res = form.submit().follow()
        assert res.status_code == 200

    def test_sees_alert_on_log_out(self, user, testapp):
        res = testapp.get("/login/")
        # Fills out login form in navbar
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'myprecious'
        # Submits
        res = form.submit().follow()
        res = testapp.get(url_for('public.logout')).follow()
        # sees alert
        assert 'You are logged out.' in res

    def test_sees_error_message_if_password_is_incorrect(self, user, testapp):
        # Goes to homepage
        res = testapp.get("/login/")
        # Fills out login form, password incorrect
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'wrong'
        # Submits
        res = form.submit()
        # sees error
        assert "Invalid password" in res

    def test_sees_error_message_if_username_doesnt_exist(self, user, testapp):
        # Goes to homepage
        res = testapp.get("/login/")
        # Fills out login form, password incorrect
        form = res.forms['loginForm']
        form['username'] = 'unknown'
        form['password'] = 'myprecious'
        # Submits
        res = form.submit()
        # sees error
        assert "Unknown user" in res


class TestUserRoles:

    def test_access(self, user, testapp):
        admin_role = Role.create(name="admin")
        user.roles.append(admin_role)
        user.save()
        TestLoggingIn.test_can_log_in_returns_200(self, user=user, testapp=testapp)
        res = testapp.get("/admin").follow()

        assert res.status_code == 200
        assert "Admin Dashboard" in res

    def test_department_access(self, user, testapp):
        department = Department.create(name="Busy Town Public Safety", short_name="BTPD", load_defaults=False)
        user.departments.append(department)
        user.save()
        TestLoggingIn.test_can_log_in_returns_200(self, user=user, testapp=testapp)
        res = testapp.get("/department/6").follow()

        assert res.status_code == 200
        assert "You do not have sufficent permissions to do that" in res


class TestRegistering:

    def test_can_register(self, user, testapp):
        ''' A new user can register.
        '''
        # The new user's credentials
        test_username = 'cato'
        test_email = 'cato@example.com'
        test_password = 'pistol_and_ball'
        test_invite_code = 'coffin_warehouses'

        # create a department and an invite code
        department = Department.create(name="Spleen Police Department", short_name="SPD", load_defaults=False)
        Invite_Code.create(department_id=department.id, code=test_invite_code)

        # establish that the user doesn't exist yet
        old_user_count = len(User.query.all())
        assert len(department.users) == 0
        assert User.query.filter_by(username=test_username).first() is None

        # Goes to register page
        response = testapp.get("/register/")
        # Fills out the form
        form = response.forms["registerForm"]
        form['username'] = test_username
        form['email'] = test_email
        form['password'] = test_password
        form['confirm'] = test_password
        form['invite_code'] = test_invite_code
        # Submits
        response = form.submit().follow()
        assert response.status_code == 200

        # The new user was created
        assert len(User.query.all()) == old_user_count + 1
        assert len(department.users) == 1
        check_user = User.query.filter_by(username=test_username).first()
        assert check_user is not None
        assert check_user.email == test_email
        assert check_user.check_password(test_password) is True
