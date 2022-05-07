import unittest
from django.test import Client


class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_login(self):
        # Issue a GET request.
        response = self.client.post('/account/login', {'email': 'testuser1@example.com', 'password': 'testing12345'})
        self.assertEqual(response.status_code, 302)

    def test_backend_page(self):
        response = self.client.post('/account/login', {'email': 'testuser1@example.com', 'password': 'testing12345'})
        response = self.client.get('/backend')
        self.assertIn('Notification', str(response.content))
