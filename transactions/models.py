from django.db import models


class Transaction(models.Model):
    account_id = models.ForeignKey('accounts.Account', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    amount = models.IntegerField()

    TRANSACTOIN_TYPE_CHOICES = [
        ('D', 'Debit'),  # money taken from an account
        ('C', 'Credit')  # money added to an account
    ]
    type = models.CharField(max_length=1, choices=TRANSACTOIN_TYPE_CHOICES)

    def __str__(self):
        return f'({self.id}) Transaction'
