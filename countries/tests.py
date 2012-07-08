from django.test import TestCase
import pycountry

from countries.models import Country


class TestModels(TestCase):
    def test_flag_url(self):
        c = Country(iso2='US')
        self.assertEqual(c.flag_url, '/static/flags/us.svg')

    def test_metadata_provided_by_pycountry(self):
        c = Country(iso2='MX')
        metadata = pycountry.countries.get(alpha2=c.iso2)
        self.assertEqual(c.metadata, metadata)

