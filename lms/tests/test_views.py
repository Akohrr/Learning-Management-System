import unittest
from django.test import TestCase

class TestViews(TestCase):
    def test_redirect_to_login_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)