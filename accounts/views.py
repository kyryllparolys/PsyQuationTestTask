from django.shortcuts import render
from rest_framework import viewsets
from accounts.models import Account
from accounts.serializers import AccountSerializer

class AccountsViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
