from django.views.generic.detail import DetailView

from .models import Country


class CountryDetailView(DetailView):
    model = Country
