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

    def paginate_queryset(self, queryset, view=None):
        if 'no_page' in self.request.query_params:
            return None
        else:
            return self.paginator.paginate_queryset(queryset, self.request, view=self)
