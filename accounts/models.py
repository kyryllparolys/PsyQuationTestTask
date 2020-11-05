from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=50)
    opened_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'({self.id}) Account: {self.name}'