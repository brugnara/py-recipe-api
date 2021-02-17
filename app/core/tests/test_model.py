"""foo"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@test.com', password='password'):
    """creates a sample user"""
    return get_user_model().objects.create_user(email, password)


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

    def test_tag_str(self):
        """test tag string repr"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name="Raegan",
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredients_str(self):
        """str repr"""
        ingr = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber',
        )

        self.assertEqual(str(ingr), ingr.name)

    def test_convert_recipe_str(self):
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='name',
            time_minutes=10,
            price=8.01,
        )

        self.assertEqual(str(recipe), recipe.title)
