from django_filters import rest_framework as filters
from rest_framework import viewsets
from transactions.models import Transaction
from transactions.serializers import TransactionAccIdSerializer

from transactions.filters import TransactionsFilter


class TransactionsViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionAccIdSerializer

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TransactionsFilter

