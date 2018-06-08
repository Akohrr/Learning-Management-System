import unittest
from django.test import TestCase
from accounts.models import User
from django.urls import reverse
from lms.tests.test_views import create_test_user



class TestViews(TestCase):

    def test_forbids_unauthorized_users(self):
        instructor = create_test_user('test-user', 'instructor')
        self.client.force_login(instructor)
        response = self.client.get(reverse('classroom:lms_admin_view', kwargs={'choice':'assignments'}))
        self.assertEqual(response.status_code, 403)

    # def test_lms_admin_permissions(self):
    #     lms_admin = create_test_user('test-user', 'lms-admin')
    #     self.client.force_login(lms_admin)
    #     self.client.get()


