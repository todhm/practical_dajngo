from django.test import TestCase
from django.urls import reverse
# Create your tests here.
homepage = reverse("home")
about_us_page = reverse("about_us")

class TestPage(TestCase):

    def test_home_page_works(self):
        response = self.client.get(homepage)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response,'BookTime')


    def test_about_us_page_works(self):
        response = self.client.get(about_us_page)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'about_us.html')
        self.assertContains(response,'BookTime')