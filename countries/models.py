from collections import namedtuple
from operator import itemgetter

from django.conf import settings
from django.contrib.gis.db import models
from django_hstore import hstore
import pycountry

from countries.utils import clean_language_name
from countries.utils import get_country_translation
from countries.utils import get_language_translation
from countries.utils import memoized_property


class Language(object):
    def __init__(self, iso3, speakers):
        self.iso3 = iso3
        self.speakers = '%sM' % speakers

        self._language = pycountry.languages.get(bibliographic=self.iso3)
        self._language_translation = get_language_translation(self._language)
        self._country_translation = get_country_translation(self._language)

    @property
    def name(self):
        return clean_language_name(self._language.name)

    @property
    def endonym(self):
        if self._language_translation:
            name = self._language_translation.ugettext(self._language.name)
            return clean_language_name(name)
        else:
            return None

    @property
    def country_translation(self):
        return self._country_translation


Translation = namedtuple('Translation', ['language', 'name'])


class Country(models.Model):
    objects = models.GeoManager()

    # Facts
    gdp = models.IntegerField(null=True)
    language_speakers = hstore.DictionaryField(null=True)
    name = models.CharField(max_length=256, unique=True)
    population = models.IntegerField(null=True)
    shape = models.MultiPolygonField()

    # Metadata
    color = models.IntegerField()
    contested = models.BooleanField(default=False)
    iso2 = models.CharField(max_length=2, unique=True)
    iso3 = models.CharField(max_length=3, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        db_table = 'country'
        verbose_name_plural = 'countries'

    def __unicode__(self):
        return self.name

    @property
    def flag_url(self):
        return '%sflags/%s.svg' % (settings.STATIC_URL, self.iso2.lower())

    @memoized_property
    def metadata(self):
        try:
            return pycountry.countries.get(alpha2=self.iso2)
        except KeyError:
            return None

    @memoized_property
    def languages(self):
        if not self.language_speakers:
            return None
        language_speakers = sorted(self.language_speakers.iteritems(),
                                   key=itemgetter(1), reverse=True)
        return [Language(*ls) for ls in language_speakers]

    @memoized_property
    def endonyms(self):
        country_translations = []
        for language in self.languages:
            if not language.country_translation:
                continue
            name = language.country_translation.ugettext(self.metadata.name)
            translation = Translation(language, name)
            country_translations.append(translation)
        return country_translations
