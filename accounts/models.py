from django.db import models
from django.db.models import Sum
from django.utils.datetime_safe import date


from transactions.models import Transaction


class Account(models.Model):
    name = models.CharField(max_length=50)
    opened_at = models.DateField(default=date.today, blank=True)

    @property
    def balance(self):
        credit_transactions_sum = Transaction.objects.filter(account_id=self.id, type='C').aggregate(Sum('amount'))
        debit_transactions_sum = Transaction.objects.filter(account_id=self.id, type='D').aggregate(Sum('amount'))

        credit_sum = 0
        debit_sum = 0

        if credit_transactions_sum['amount__sum'] is not None:
            credit_sum = credit_transactions_sum['amount__sum']
        elif debit_transactions_sum['amount__sum'] is not None:
            debit_sum = debit_transactions_sum['amount__sum']

        balance = credit_sum - debit_sum
        if balance < 0:
            return 0
        return balance

    def __str__(self):
        return f'({self.id}) Account: {self.name}'
