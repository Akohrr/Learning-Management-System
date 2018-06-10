import unittest
from django.test import TestCase
from accounts.models import User
from django.urls import reverse


def create_test_user(username, user_role):
    user_type = {'Lms-Admin': 'LA', 'Instructor': 'IN',
                 'Student': 'ST'}[user_role.title()]
    user = User.objects.create(
        username=username, user_type=user_type)
    user.set_password=('makemigrations')
    user.save()

    return user


class TestViews(TestCase):
    def test_redirect_index_to_login_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_redirect_anonymous_user_to_login_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.url, reverse('accounts:login'))


    