# -*- coding: utf-8 -*-

from django.test import TestCase
import pycountry

from countries.models import Country
from countries.utils import memoized_property


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


class TestUtils(TestCase):
    def test_memoized_property(self):
        class TestClass(object):
            def __init__(self):
                self._call_count = 0

            def call_count(self):
                self._call_count += 1
                return self._call_count

            @memoized_property
            def new_count(self):
                return self.call_count + 8

        c = TestClass()
        self.assertEqual(c.call_count(), 1)
        self.assertEqual(c.call_count(), 2)

        TestClass.call_count = memoized_property(TestClass.call_count)
        self.assertEqual(c.call_count, 2)
        self.assertEqual(c.call_count, 2)

        self.assertTrue(not hasattr(c, '_new_count'))
        self.assertEqual(c.new_count, 10)
        self.assertTrue(hasattr(c, '_new_count'))
