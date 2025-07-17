import pytest

@pytest.mark.django_db
def test_create_bank_account(user_client):
    client, user = user_client

    data = {
        "iban": "DE1234567890",
        "currency": "EUR",
        "balance": 1000.0,
        "owner": user.id
    }

    response = client.post("/api/bankaccounts/", data)
    assert response.status_code == 201
    assert response.data["iban"] == data["iban"]
