import pytest
from rest_framework.test import APIClient
from wallet.models import Wallet


@pytest.mark.django_db
def test_wallet_balance():
    wallet = Wallet.objects.create(balance=1000.00)
    client = APIClient()

    response = client.get(f'/api/v1/wallets/{wallet.uuid}/')

    assert response.status_code == 200
    assert response.data['balance'] == "1000.00"


@pytest.mark.django_db
def test_wallet_operation():
    wallet = Wallet.objects.create(balance=1000.00)
    client = APIClient()

    response = client.post(f'/api/v1/wallets/{wallet.uuid}/operation/', {
        'operationType': 'DEPOSIT',
        'amount': 500
    }, format='json')

    assert response.status_code == 200
    wallet.refresh_from_db()
    assert wallet.balance == 1500.00
