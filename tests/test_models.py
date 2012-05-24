import unittest
import sqlalchemy.orm
from nose.tools import *
from application import create_app
from application.models import *


class TestCaseUsingDatabase(unittest.TestCase):
    def setUp(self):
        create_app("test")
        from application import app, db
        self.app = app

        with app.test_request_context():
            db.create_all()
            # Initialize database, if needed
            self.db_session = db.create_scoped_session()
            # IMPORTANT: Always use self.db_session.query(Klass) NOT Klass.query
            # as the latter will create a new session

    def tearDown(self):
        pass

    def count_in_db(self, _klass):
        return _klass.query.count()

    def exists_in_db(self, _klass, _name, _msg=None):
        ok_(_klass.query.filter(_klass.name == _name).count() == 1, _msg)

    def does_not_exist_in_db(self, _klass, _name, _msg=None):
        ok_(_klass.query.filter(_klass.name == _name).count() == 0, _msg)


class UserModelTestCase(TestCaseUsingDatabase):
    def test_user_can_be_added(self):
        with self.app.test_request_context():
            user = User('admin', 'admin@example.com')
            self.db_session.add(user)
            self.db_session.commit()

            found_user = User.query.one()
            ok_(found_user.name == 'admin')
            ok_(found_user.email == 'admin@example.com')
