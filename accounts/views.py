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

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AccountsFilter

    def paginate_queryset(self, queryset, view=None):
        if "no_page" in self.request.query_params:
            return None
        else:
            return self.paginator.paginate_queryset(queryset, self.request, view=self)

    @action(detail=False, methods=["GET",], filterset_class=None)
    def get_top(self, request):
        accounts = Account.objects.all()

        accounts_dict = {}
        for account in accounts:
            if account.balance != 0:
                accounts_dict[account] = account.balance

        top_len = len(accounts_dict) if len(accounts_dict) < 100 else 100
        top_accounts = heapq.nlargest(top_len, accounts_dict, key=accounts_dict.get)

        serializer = self.get_serializer(top_accounts, many=True)
        return Response(serializer.data)
