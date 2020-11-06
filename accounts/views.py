from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.models import Account
from accounts.serializers import AccountSerializer

from accounts.filters import AccountsFilter
import heapq


class AccountsViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = AccountsFilter

    @action(detail=False, methods=['GET',], filterset_class=None)
    def get_top(self, request):
        accounts = Account.objects.all()

        accounts_dict = {}
        for account in accounts:
            accounts_dict[account] = account.balance

        top_accounts = heapq.nlargest(100, accounts_dict, key=accounts_dict.get)

        serializer = self.get_serializer(top_accounts, many=True)
        return Response(serializer.data)
