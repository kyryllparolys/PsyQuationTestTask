from rest_framework import serializers
from accounts.models import Account
from transactions.serializers import TransactionSerializer


class AccountSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Account
        fields = (
            'id',
            'name',
            'opened_at',
            'transactions'
        )
