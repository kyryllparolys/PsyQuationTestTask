from rest_framework import viewsets
from transactions.models import Transaction
from transactions.serializers import TransactionAccIdSerializer

class TransactionsViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionAccIdSerializer

