from django.test import TestCase

from countries.models import Country


class TestModels(TestCase):
    def test_flag_url(self):
        c = Country(iso2='US')
        self.assertEqual(c.flag_url, '/static/flags/us.svg')
