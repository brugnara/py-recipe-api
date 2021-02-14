"""aa"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    """Admin site tests"""

    def setUp(self):
        """setup"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@email.it',
            password='password134',
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@longocom',
            password='asdasdda',
            name='test user u',
        )

    def test_users_listed(self):
        """user should be listed"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """user asdad"""
        url = reverse('admin:core_user_change',
          args=[self.user.id],
        )
        # /admin/core/user
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """create user page"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
