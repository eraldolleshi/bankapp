import pytest

@pytest.mark.django_db
def test_banker_manage_clients(banker_client):
    client, _ = banker_client

    # Create client
    res_create = client.post("/api/clients/", {
        "username": "clientx",
        "password": "testpass",
        "email": "clientx@example.com",
        "role": "CLIENT"
    }, content_type="application/json")
    assert res_create.status_code == 201
    client_id = res_create.data["id"]

    # Edit client
    res_edit = client.patch(f"/api/clients/{client_id}/", {
        "email": "updated@example.com"
    }, content_type="application/json")
    assert res_edit.status_code == 200
    assert res_edit.data["email"] == "updated@example.com"

    # Delete client
    res_delete = client.delete(f"/api/clients/{client_id}/")
    assert res_delete.status_code == 204
