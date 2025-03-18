from rest_framework.test import APITestCase

from authentication.models import User


class TestModel(APITestCase):
    def test_create_user(self):
        user=User.objects.create_user(username="test", email="test@gmail.com", password="password")
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, "test@gmail.com")
        self.assertFalse(user.is_staff, False)

