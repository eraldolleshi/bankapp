import pytest

@pytest.mark.django_db
def test_view_transactions(user_client, create_transaction):
    client, user = user_client
    create_transaction(user)

    response = client.get("/api/transactions/")

    assert response.status_code == 200
    assert isinstance(response.data, list)
    assert len(response.data) > 0
