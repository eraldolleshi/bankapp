import pytest

@pytest.mark.django_db
def test_transfer_between_two_accounts(user_client, create_two_accounts, create_approved_debit_card):
    client, user = user_client
    acc1, acc2 = create_two_accounts(user)
    dc1 = create_approved_debit_card(acc1)

    response = client.post("/api/transfer/", {
    
        "amount": 10.0,
        "from_iban": acc1.iban,
        "to_iban": acc2.iban 
    }, content_type="application/json")
    assert response.status_code == 201
    assert response.json() == {"detail": "Transfer successful."}
 
