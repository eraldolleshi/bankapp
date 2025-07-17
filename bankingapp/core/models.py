from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('BANKER', 'Banker'),
        ('CLIENT', 'Client'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"

class BankAccount(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    iban = models.CharField(max_length=34, unique=True)
    currency = models.CharField(max_length=3, default='EUR')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=900.00)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.iban} ({self.owner.username})"


class DebitCard(models.Model):
    account = models.OneToOneField(BankAccount, on_delete=models.CASCADE, related_name='debit_card')
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_approved = models.BooleanField(default=False)
    reject_reason = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"Debit Card for {self.account.iban}"

class Transaction(models.Model):
    DEBIT = 'DEBIT'
    CREDIT = 'CREDIT'
    TRANSACTION_TYPES = [
        (DEBIT, 'Debit'),
        (CREDIT, 'Credit'),
    ]

    bank_account = models.ForeignKey(BankAccount, related_name='transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='EUR')
    type = models.CharField(max_length=6, choices=TRANSACTION_TYPES)
   

