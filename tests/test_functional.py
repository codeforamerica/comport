# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""
import pytest
from flask import url_for


from comport.user.models import User, Role, Invite_Code
from comport.department.models import Department
from .factories import UserFactory


class TestLoggingIn:

    def test_can_log_in_returns_200(self, user, testapp):
        # Goes to homepage
        res = testapp.get("/")
        # Fills out login form in navbar
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'myprecious'
        # Submits
        res = form.submit().follow()
        assert res.status_code == 200

    def test_sees_alert_on_log_out(self, user, testapp):
        res = testapp.get("/")
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
        res = testapp.get("/")
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
        res = testapp.get("/")
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
        assert "This is the admin-only page" in res

    def test_deparment_access(self, user, testapp):
        department = Department.create(name="Busy Town Public Safety")
        user.department_id = department.id
        user.save()
        TestLoggingIn.test_can_log_in_returns_200(self, user=user, testapp=testapp)
        res = testapp.get("/department/6").follow()

        assert res.status_code == 200
        assert "You do not have sufficent permissions to do that" in res

        
class TestRegistering:

    def test_can_register(self, user, testapp):
        department = Department.create(name="dept")
        Invite_Code.create(department_id=department.id, code="code")

        old_count = len(User.query.all())
        # Goes to homepage
        res = testapp.get("/")
        # Clicks Create Account button
        res = res.click("Create account")
        # Fills out the form
        form = res.forms["registerForm"]
        form['username'] = 'foobar'
        form['email'] = 'foo@bar.com'
        form['password'] = 'secret'
        form['confirm'] = 'secret'
        form['invite_code'] = 'code'
        # Submits
        res = form.submit().follow()
        assert res.status_code == 200
        # A new user was created
        assert len(User.query.all()) == old_count + 1
        assert len(department.users) == 1
