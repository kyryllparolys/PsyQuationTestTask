from django_filters import rest_framework as filters
from transactions.models import Transaction


class TransactionsFilter(filters.FilterSet):
    class Meta:
        model = Transaction
        fields = ("account", "amount", "type")
