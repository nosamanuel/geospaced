# -*- coding: utf-8 -*-

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

    def test_missing_metdata_is_none(self):
        c = Country(iso2='SS')
        self.assertEqual(c.metadata, None)

    def test_languages_dictionary(self):
        c = Country(language_speakers={'spa': 112})
        self.assertEqual(c.language_speakers['spa'], 112)

    def test_languages(self):
        c = Country(iso2='MX', language_speakers={'spa': 112, 'nah': 1.38})
        self.assertEqual(c.languages[0].name, 'Spanish')
        self.assertEqual(c.languages[0].endonym.encode('utf8'), 'Español')
        self.assertEqual(c.languages[0].speakers, '112M')
        self.assertEqual(c.languages[1].name, 'Nahuatl')
        self.assertEqual(c.languages[1].endonym, None)
        self.assertEqual(c.languages[1].speakers, '1.38M')

    def test_endonyms(self):
        c = Country(iso2='MX', language_speakers={'spa': 112, 'nah': 1.38})
        self.assertEqual(c.endonyms[0].language.name, 'Spanish')
        self.assertEqual(c.endonyms[0].name.encode('utf8'), 'México')
