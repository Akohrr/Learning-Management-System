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


    # def test_redirect_users_to_appropriate_home_page(self):
    #     instructor = create_test_user('instructor', 'Instructor')
    #     self.client.force_login(instructor)
    #     # self.assertEqual(response.url, reverse('home'))
    #     response = self.client.get(reverse('home'))
    #     self.assertEqual(response.url, reverse('classroom:instructor_view', kwargs={'choice':'assignments'}))

    # def test_redirect_users_to_appropriate_home_page(self):
    #     instructor = create_test_user('instructor', 'instructor')
    #     # self.client.login(username=instructor.username, password=instructor.password)
    #     self.client.force_login(instructor)
    #     response = self.client.get(reverse('classroom:instructor_view', kwargs={'choice':'assignments'}))
    #     self.assertEqual(response.status_code, 403)
    #     # self.assertEqual(response.url, reverse('classroom:instructor_view', kwargs={'choice':'assignments'}))

