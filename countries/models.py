from django.conf import settings
from django.contrib.gis.db import models
from django_hstore import hstore
import pycountry


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

    @property
    def metadata(self):
        if not hasattr(self, '_metadata'):
            try:
                metadata = pycountry.countries.get(alpha2=self.iso2)
            except KeyError:
                metadata = None
            setattr(self, '_metadata', metadata)

        return self._metadata
