import pytest

from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_banker_approves_bank_account(banker_client, create_unapproved_bank_account):
    client, _ = banker_client
    user = User.objects.create_user(username='client2', password='pass', role='CLIENT')
    account = create_unapproved_bank_account(user)

    response = client.patch(f"/api/bankaccounts/{account.id}/", {
        "is_approved": True
    }, content_type="application/json")

    assert response.status_code == 200
    assert response.data["is_approved"] is True
