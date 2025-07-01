# from django.test import TestCase
# from core import models

# class ModelTests(TestCase):
#   def test_create_url_successful(self):
#     url = 'url'
#     new_url = url_model.create_url(url=url)
#     self.assertEqual(new_url, url)

#   def test_new_url_empty(self):
#     with self.assertRaises(ValueError):
#       models.UrlManager.create_url(original_url='')

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Url

class UrlApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_url = "https://example.com"

    def test_shorten_url(self):
        """Test shortening a valid URL"""
        response = self.client.post('/api/shorten', {'original_url': self.test_url}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("shortened_url", response.data)

    def test_redirect_to_original_url(self):
        """Test redirecting from a shortened code"""
        url_obj = Url.objects.create(original_url=self.test_url, shortened_code="ABC123")
        response = self.client.get(f'/api/{url_obj.shortened_code}')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.data['original_url'], self.test_url)

    def test_url_stats(self):
        """Test retrieving stats for a shortened URL"""
        url_obj = Url.objects.create(original_url=self.test_url, shortened_code="XYZ789", clicks=5)
        response = self.client.get(f'/api/stats/{url_obj.shortened_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['original_url'], self.test_url)
        self.assertEqual(response.data['clicks'], 5)
