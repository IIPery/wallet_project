from django.db import models

import uuid


class Wallet(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (f'Номер счета: {self.uuid} Баланс: {self.balance}')
