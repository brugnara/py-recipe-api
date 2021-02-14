"""foo"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """bar"""

    def test_create_user_with_email_succesfull(self):
        """test creating a new user with an email"""
        email = 'test@london.com'
        password = 'Tassword.123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """test normalized"""
        email = 'test@LONDON.com'
        password = 'Pasda1.412'

        user = get_user_model().objects.create_user(
            email,
            password,
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """should fail"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, '123')

    def test_create_new_superuser(self):
        """superuser"""
        user = get_user_model().objects.create_superuser(
            'test@london.com',
            'passqower1!'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
