import optparse
import os
import sys

from django.core.management.base import LabelCommand
from django.contrib.gis.utils.layermapping import LayerMapping, LayerMapError
from django.template.defaultfilters import slugify

from countries.models import Country


class CountryLayerMapping(LayerMapping):
    """
    Custom layer mapping that sets a slug based on the country name
    and sets the contested flag based on the country type.
    """
    mapping = {
        'gdp': 'GDP_MD_EST',
        'name': 'SUBUNIT',
        'population': 'POP_EST',
        'shape': 'Geometry',
        'color': 'MAP_COLOR',
        'iso2': 'ISO_A2',
        'iso3': 'ISO_A3',
    }

    def __init__(self, shp_path, **kwargs):
        kwargs.update(model=Country, data=shp_path, mapping=self.mapping)
        super(CountryLayerMapping, self).__init__(**kwargs)

    def feature_kwargs(self, feature):
        kwargs = super(CountryLayerMapping, self).feature_kwargs(feature)

        # Raise LayerMapError to ignore feature
        if kwargs['iso2'] == '-99':
            raise LayerMapError('Bad ISO2 "%(iso2)s" for "%(name)s"' % kwargs)

        # Clean model fields
        kwargs['slug'] = slugify(kwargs['name'])
        if kwargs['gdp'] in (-99, 0):
            kwargs['gdp'] = None
        if kwargs['population'] in (-99, 0):
            kwargs['population'] = None

        return kwargs


class Command(LabelCommand):
    help = "Imports countries from the Natural Earth country shapefiles"
    label = 'shp_path'
    option_list = LabelCommand.option_list + (
        optparse.make_option('--purge', action='store_true', dest='purge'),
    )

    def handle_label(self, label, **options):
        if options.get('purge'):
            sys.stdout.write('deleting all countries...')
            Country.objects.all().delete()

        shp_path = os.path.abspath(label)
        mapping = CountryLayerMapping(shp_path, encoding='iso-8859-1')
        mapping.save(strict=False, silent=False)
