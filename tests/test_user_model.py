import unittests
from app.models import User

class UserModelTestCase(unittest.TestCase):
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
        user = User(password='Test.123')
        user2 = User(password='321.Test')
        self.assertTrue(user.password_hash != user2.password_hash)

