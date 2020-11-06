from datetime import timedelta

from django.db.models import Q
from django.utils.datetime_safe import datetime
from django_filters import rest_framework as filters

from accounts.models import Account


class AccountsFilter(filters.FilterSet):
    is_new = filters.BooleanFilter(method="filter_is_new")
    is_active = filters.BooleanFilter(method="filter_is_active")

    class Meta:
        model = Account
        fields = (
            "id",
            "name",
            "opened_at",
        )

    def filter_is_new(self, queryset, name, value):
        today = datetime.now()
        week_ago = today - timedelta(7)
        if value:  # if any value is provided, even non-true
            return queryset.filter(Q(opened_at__range=[week_ago, today]))
        return queryset.filter(Q(opened_at__lt=week_ago))  # false

    def filter_is_active(self, queryset, name, value):
        three_days_ago = datetime.now() - timedelta(3)
        if value:
            return queryset.filter(Q(transaction__time__gt=three_days_ago))
        return queryset.filter(Q(transaction__time__lt=three_days_ago))

