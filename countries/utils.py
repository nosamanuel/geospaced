from gettext import translation

from pycountry import LOCALES_DIR


def clean_language_name(name):
    cleaned_name = name.split('; ')[0].split(', ')[0]
    if cleaned_name.endswith(' languages'):
        cleaned_name = cleaned_name.replace(' languages', '')
    return cleaned_name


def get_translation(language, type):
    """Gets a translation from a pycountry language"""
    for attr in ('alpha2', 'bibliographic'):
        code = getattr(language, attr, None)
        if not code:
            continue
        try:
            return translation(type, LOCALES_DIR, languages=[code])
        except IOError:
            pass

    return None


def get_language_translation(language):
    return get_translation(language, 'iso639')


def get_country_translation(language):
    return get_translation(language, 'iso3166')


def memoized_property(func):
    attr = '_%s' % func.__name__

    @property
    def wrapped(self):
        if not hasattr(self, attr):
            setattr(self, attr, func(self))
        return getattr(self, attr)

    return wrapped
