import django_filters
from django.db.models import Max, F
from django.db.models.functions import Now
from rest_framework.pagination import PageNumberPagination

from apps.booking.models import BookingContact, Deal

BOOKING_KIND_FILTER_CHOICES = (("upcoming", "Upcoming"), ("past", "Past"))


class DealPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "size"


KIND_CHOICES = (("international", "International"), ("domestic", "Domestic"))


class DealFilterSet(django_filters.FilterSet):
    kind = django_filters.ChoiceFilter(choices=KIND_CHOICES, method="filter_kind")
    airlines = django_filters.BaseCSVFilter(method="filter_airlines")

    class Meta:
        model = Deal
        fields = ["city_from", "airlines", "kind"]

    def filter_kind(self, qs, name, value):
        qs = qs.filter(country_from__isnull=False, country_to__isnull=False)
        if value == "international":
            qs = qs.exclude(country_from=F("country_to"))
        elif value == "domestic":
            qs = qs.filter(country_from=F("country_to"))
        return qs

    def filter_airlines(self, qs, name, value):
        return qs.filter(airlines__contained_by=value)


class BookingFilter(django_filters.FilterSet):
    kind = django_filters.ChoiceFilter(
        choices=BOOKING_KIND_FILTER_CHOICES, method="filter_kind"
    )

    class Meta:
        model = BookingContact
        fields = ["kind"]

    def filter_kind(self, queryset, name, value):
        qs = queryset.annotate(last_flight_date=Max("flights__arrival_time"))
        if value == "upcoming":
            return qs.filter(last_flight_date__gte=Now())
        elif value == "past":
            return qs.filter(last_flight_date__lt=Now())
