import pytest

@pytest.mark.django_db
def test_client_requests_debit_card(user_client, create_bank_account):
    client, user = user_client
    account = create_bank_account(user)

    data = {
        "salary" : 500.00,
        "account": account.id,
    }

    response = client.post("/api/debitcards/", data)

    assert response.status_code == 201
    assert response.data["account"] == account.id
    assert response.data["is_approved"] is False
