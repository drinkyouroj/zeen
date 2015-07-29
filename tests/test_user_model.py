import unittest
import time
from app import create_app, db
from app.models import User


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        user = User(password='Test.123')
        self.assertTrue(user.password_hash is not None)

    def test_no_password_getter(self):
        user = User(password='Test.123')
        with self.assertRaises(AttributeError):
            user.password

    def test_password_verification(self):
        user = User(password='Test.123')
        self.assertTrue(user.verify_password('Test.123'))
        self.assertFalse(user.verify_password('Wrong_password'))

    def test_password_salts_are_random(self):
        user1 = User(password='password')
        user2 = User(password='password')
        self.assertTrue(user1.password_hash != user2.password_hash)

    def test_valid_confirmation_token(self):
        user = User(password='Test.123')
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        self.assertTrue(user.confirm(token))

    def test_invalid_confirmation_token(self):
        user1 = User(password='Test.123')
        user2 = User(password='456-Test')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        token = user1.generate_confirmation_token()
        self.assertFalse(user2.confirm(token))

    def test_expired_confirmation_token(self):
        user = User(password='Test.123')
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token(1)
        time.sleep(2)
        self.assertFalse(user.confirm(token))

