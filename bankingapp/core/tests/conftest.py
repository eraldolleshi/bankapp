import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from core.models import BankAccount, Transaction, DebitCard

User = get_user_model()

@pytest.fixture
def user_client():
    user = User.objects.create_user(username='client1', password='pass123', role='CLIENT')
    client = APIClient()
    client.force_authenticate(user=user)
    return client, user

@pytest.fixture
def banker_client():
    user = User.objects.create_user(username='banker1', password='pass123', role='BANKER')
    client = APIClient()
    client.force_authenticate(user=user)
    return client, user

@pytest.fixture
def create_bank_account():
    def _create(user):
        return BankAccount.objects.create(
            owner=user,
            iban="DE000000000001",
            currency="EUR",
            balance=1000.0,
            is_approved=True
        )
    return _create


@pytest.fixture
def create_transaction():
    def _create(user):
        account = BankAccount.objects.create(
            owner=user,
            iban="DE000000000002",
            currency="EUR",
            balance=1000.0,
            is_approved=True
        )
        return Transaction.objects.create(
            bank_account=account,
            type="DEBIT",
            amount=200.0,
            currency="EUR"
        )
    return _create

@pytest.fixture
def create_two_accounts():
    def _create(user):
        acc1 = BankAccount.objects.create(
            owner=user,
            iban="DE000000000003",
            currency="EUR",
            balance=500.0,
            is_approved=True
        )
        acc2 = BankAccount.objects.create(
            owner=user,
            iban="DE000000000004",
            currency="EUR",
            balance=700.0,
            is_approved=True
        )
        return acc1, acc2
    return _create


@pytest.fixture
def create_approved_debit_card():
    def _create(account):
        return DebitCard.objects.create(
            account=account,
            salary = 700,
            is_approved=True
        )
    return _create



@pytest.fixture
def create_unapproved_debit_card(create_bank_account):
    def _create(user):
        account = create_bank_account(user)
        return DebitCard.objects.create(
            account=account,
            is_approved=False
        )
    return _create


@pytest.fixture
def create_unapproved_bank_account():
    def _create(user):
        return BankAccount.objects.create(
            owner=user,
            iban="DE999999999999",
            currency="EUR",
            balance=0.0,
            is_approved=False
        )
    return _create