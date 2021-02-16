from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer


INGR_URL = reverse('recipe:ingredient-list')


class PublicIngrApiTests(TestCase):
    """Test public apis"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """tests that login is required"""
        res = self.client.get(INGR_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngrApiTest(TestCase):
    """test logged in stuff"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'email@email.it',
            'password',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingr_list(self):
        """test retrieving a list of ingredients"""
        Ingredient.objects.create(
            user=self.user,
            name='caffe',
        )
        Ingredient.objects.create(
            user=self.user,
            name='farina',
        )

        res = self.client.get(INGR_URL)

        list = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(list, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredientrs_limited_to_user(self):
        """vla"""
        user2 = get_user_model().objects.create_user(
            'asd2@email.it',
            'password',
        )

        Ingredient.objects.create(
            user=user2,
            name='caffe',
        )
        ing = Ingredient.objects.create(
            user=self.user,
            name='farina',
        )

        res = self.client.get(INGR_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ing.name)

    def test_create_ingredient(self):
        """test create a new ingredient"""
        payload = {
            'name': 'flour',
        }
        self.client.post(INGR_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name'],
        ).exists()
        self.assertTrue(exists)

    def test_create_invalid_ingredient(self):
        payload = {'name': ''}
        res = self.client.post(INGR_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
