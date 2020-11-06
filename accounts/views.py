from django_filters import rest_framework as filters
from rest_framework import viewsets
from accounts.models import Account
from accounts.serializers import AccountSerializer

from accounts.filters import AccountsFilter


class AccountsViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = AccountsFilter
