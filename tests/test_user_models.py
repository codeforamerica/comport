# -*- coding: utf-8 -*-
"""Model unit tests."""
import datetime as dt

import pytest

from comport.user.models import User, Role
from comport.department.models import Extractor
from .factories import UserFactory, DepartmentFactory


@pytest.mark.usefixtures('db')
class TestUserInheritance:
    def test_extractors_are_users(self):
        department = DepartmentFactory()
        department.save()

        extractor = Extractor.create(username='foobarbaz', email='foo2@bar.com', department_id=department.id)
        
        assert extractor.department_id == department.id


@pytest.mark.usefixtures('db')
class TestUser:

    def test_get_by_id(self):
        user = User('foo', 'foo@bar.com')
        user.save()

        retrieved = User.get_by_id(user.id)
        assert retrieved == user

    def test_created_at_defaults_to_datetime(self):
        user = User(username='foo', email='foo@bar.com')
        user.save()
        assert bool(user.created_at)
        assert isinstance(user.created_at, dt.datetime)

    def test_password_is_nullable(self):
        user = User(username='foo', email='foo@bar.com')
        user.save()
        assert user.password is None

    def test_factory(self, db):
        user = UserFactory(password="myprecious")
        db.session.commit()
        assert bool(user.username)
        assert bool(user.email)
        assert bool(user.created_at)
        assert user.active is True
        assert user.check_password('myprecious')

    def test_check_password(self):
        user = User.create(username="foo", email="foo@bar.com",
                    password="foobarbaz123")
        assert user.check_password('foobarbaz123') is True
        assert user.check_password("barfoobaz") is False

    def test_full_name(self):
        user = UserFactory(first_name="Foo", last_name="Bar")
        assert user.full_name == "Foo Bar"

    def test_role(self):
        role = Role(name='admin')
        role.save()
        u = UserFactory()
        u.roles.append(role)
        u.save()
        assert role in u.roles

    def test__many_roles(self):
        admin_role = Role(name='admin')
        admin_role.save()
        other_role = Role(name='other')
        other_role.save()
        u = UserFactory()
        u.roles.append(admin_role)
        u.roles.append(other_role)
        u.save()
        assert admin_role in u.roles
        assert other_role in u.roles

    def test_many_users(self):
        admin_role = Role(name='admin')
        admin_role.save()

        u = UserFactory()
        u.roles.append(admin_role)
        u.save()

        admin_role_two = Role(name='admin')
        admin_role_two.save()

        u_two = UserFactory()
        u_two.roles.append(admin_role_two)
        u_two.save()

        assert admin_role in u.roles
        assert admin_role_two in u_two.roles

    def test_is_admin(self):
        admin_role = Role(name='admin')
        admin_role.save()

        u = UserFactory()
        u.roles.append(admin_role)
        u.save()

        assert u.is_admin()

    def test_is_not_admin(self):

        u = UserFactory()
        u.save()

        assert not u.is_admin()
