import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_login():
    User.objects.create_user(username="testuser", password="testpass")
    
    from rest_framework.test import APIClient
    client = APIClient()
    
    res = client.post("/api/login/", {"username": "testuser", "password": "testpass"})
    assert res.status_code == 200
    assert "token" in res.data
