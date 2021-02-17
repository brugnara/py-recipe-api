from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe
from recipe.serializers import RecipeSerializer


RECIPES_URL = reverse('recipe:recipe-list')

def sample_recipe(user, **params):
    """create and return a recipe"""
    defaults = {
        'title': 'sample recipe',
        'time_minutes': 10,
        'price': 5,
    }

    # replace or add keys in defaults using params
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeApiTests(TestCase):
    """test unauth recipe apis"""

    def setUp(self):
        self.client = APIClient()

    def test_required_auth(self):
        """test that auth is required"""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


def PrivateRecipeApiTests(TestCase):
    """Test auth"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'pippo@granc.aso',
            'password'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """test retrieving a list of recipes"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """dd"""
        user2 = get_user_model().objects.create_user(
            'pi412ppo@granc.aso',
            'passw31ord'
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
