import unittest
import time
from app import create_app, db
from app.models import User, AnonymousUser, Role, Permission


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

    def test_valid_reset_token(self):
        user = User(password='Test.123')
        db.session.add(user)
        db.session.commit()
        token = user.generate_reset_token()
        self.assertTrue(user.reset_password(token, '1new_Password'))
        self.assertTrue(user.verify_password('1new_Password'))

    def test_invalid_reset_token(self):
        user1 = User(password='Test.123')
        user2 = User(password='456-Test')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        token = user1.generate_reset_token()
        self.assertFalse(user2.reset_password(token, '1new_Password'))
        self.assertTrue(user2.verify_password('456-Test'))

    def test_valid_email_change_token(self):
        user = User(email='user@example.com', password='Test.123')
        db.session.add(user)
        db.session.commit()
        token = user.generate_email_change_token('new-email@example.org')
        self.assertTrue(user.change_email(token))
        self.assertTrue(user.email == 'new-email@example.org')

    def test_invalid_email_change_token(self):
        user1 = User(email='user1@example.com', password='Test.123')
        user2 = User(email='user2@example.org', password='456-Test')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        token = user1.generate_email_change_token('new-user1@example.net')
        self.assertFalse(user2.change_email(token))
        self.assertTrue(user2.email == 'user2@example.org')

    def test_duplicate_email_change_token(self):
        user1 = User(email='user1@example.com', password='Test.123')
        user2 = User(email='user2@example.org', password='456-Test')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        token = user2.generate_email_change_token('user1@example.com')
        self.assertFalse(user2.change_email(token))
        self.assertTrue(user2.email == 'user2@example.org')

    def test_roles_and_permissions(self):
        Role.insert_roles()
        user = User(email='user@example.com', password='Test.123')
        self.assertTrue(user.can(Permission.WRITE_CONTENT))
        self.assertFalse(user.can(Permission.MODERATE_COMMENTS))

    def test_anonymous_user(self):
        user = AnonymousUser()
        self.assertFalse(user.can(Permission.FOLLOW))

