# -*- coding: utf-8 -*-
from comport.public.forms import LoginForm
from comport.user.forms import RegisterForm
from comport.department.models import Department
from comport.user.models import Invite_Code


class TestRegisterForm:

    def test_validate_user_already_registered(self, user):
        # Enters username that is already registered
        form = RegisterForm(username=user.username, email='foo@bar.com', password='example', confirm='example', invite_code="bad")
        assert form.validate() is False
        assert 'Username already registered' in form.username.errors

    def test_validate_email_already_registered(self, user):
        # enters email that is already registered
        form = RegisterForm(username='unique', email=user.email, password='example', confirm='example', invite_code="bad")
        assert form.validate() is False
        assert 'Email already registered' in form.email.errors

    def test_validate_invite_code_valid(self, user):
        form = RegisterForm(username='newusername', email='new2@test.test', password='example', confirm='example', invite_code="bad")
        assert form.validate() is False
        assert 'Invite Code not recognized.' in form.invite_code.errors

    def test_validate_invite_code_used_already(self, user):
        department = Department.create(name="dept", short_name="DPD", load_defaults=False)
        Invite_Code.create(department_id=department.id, code="code1", used=True)

        form = RegisterForm(username='newusername', email='new2@test.test', password='example', confirm='example', invite_code="code1")
        assert form.validate() is False
        assert 'Invite Code has already been used.' in form.invite_code.errors

    def test_validate_success(self, db):
        department = Department.create(name="dept", short_name="DPD", load_defaults=False)
        Invite_Code.create(department_id=department.id, code="code")
        form = RegisterForm(username='newusername', email='new@test.test', password='example', confirm='example', invite_code="code")
        assert form.validate() is True


class TestLoginForm:

    def test_validate_success(self, user):
        user.set_password('example')
        user.save()
        form = LoginForm(username=user.username, password='example')
        assert form.validate() is True
        assert form.user == user

    def test_validate_unknown_username(self, db):
        form = LoginForm(username='unknown', password='example')
        assert form.validate() is False
        assert 'Unknown username' in form.username.errors
        assert form.user is None

    def test_validate_invalid_password(self, user):
        user.set_password('example')
        user.save()
        form = LoginForm(username=user.username, password='wrongpassword')
        assert form.validate() is False
        assert 'Invalid password' in form.password.errors

    def test_validate_inactive_user(self, user):
        user.active = False
        user.set_password('example')
        user.save()
        # Correct username and password, but user is not activated
        form = LoginForm(username=user.username, password='example')
        assert form.validate() is False
        assert 'User not activated' in form.username.errors
