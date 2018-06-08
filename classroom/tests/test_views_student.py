from django.test import TestCase
from lms.tests.test_views import create_test_user
from django.urls import reverse


class TestViews(TestCase):

    def test_forbids_unauthorized_users(self):
        instructor = create_test_user('test-user', 'instructor')
        self.client.force_login(instructor)
        response = self.client.get(reverse('classroom:student_view', kwargs={'choice':'assignments'}))
        self.assertEqual(response.status_code, 403)


