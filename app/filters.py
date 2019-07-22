# Standard Library
import functools
import logging
import operator

# Third-Party Imports
from django.db.models import Q
from django_filters import rest_framework as filters

# App Imports
from .authentication.models import User

logger = logging.getLogger(__name__)

NULL_VALUE = "unspecified"


class BaseFilter(filters.FilterSet):
    def filter_contains_with_multiple_query_values(self, queryset, name, value):
        options = set(value.split(","))
        null_lookup = {}
        if NULL_VALUE in options:
            options.remove(NULL_VALUE)
            null_lookup = {"__".join([name, "isnull"]): True}
        if options:
            lookup = functools.reduce(
                operator.or_,
                {Q(**{"__".join([name, "icontains"]): item}) for item in options},
            )
        else:
            lookup = Q(**{})

        return queryset.filter(Q(lookup | Q(**null_lookup)))

    def filter_exact_with_multiple_query_values(self, queryset, name, value):
        options = set(value.split(","))
        null_lookup = {}
        if NULL_VALUE in options:
            options.remove(NULL_VALUE)
            null_lookup = {"__".join([name, "isnull"]): True}
        lookup = {"__".join([name, "in"]): options}
        return queryset.filter(Q(**lookup) | Q(**null_lookup))


class UserFilter(BaseFilter):
    phone_number = filters.CharFilter(
        field_name="phone_number",
        lookup_expr="iexact",
        method="filter_exact_with_multiple_query_values",
    )

    class Meta:
        model = User
        fields = ["phone_number"]
