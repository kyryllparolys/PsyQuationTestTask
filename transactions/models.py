from django.db import models


class Transaction(models.Model):
    account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    amount = models.IntegerField()  # this potentially allows the balance to become less than 0

    TRANSACTOIN_TYPE_CHOICES = [
        ('D', 'Debit'),  # money taken from an account
        ('C', 'Credit')  # money added to an account
    ]
    type = models.CharField(max_length=1, choices=TRANSACTOIN_TYPE_CHOICES)

    def __str__(self):
        return f'({self.id}) {self.type} Transaction for {self.amount}$ Account: {self.account.name}'
