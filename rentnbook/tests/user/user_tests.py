from django.urls import reverse
import pytest
from django.contrib.auth import get_user_model

from user.models import RolesChoices

User = get_user_model()


@pytest.mark.django_db
def test_profile_view(client):
    User.objects.create_user(
        email="user@example.com",
        password="password123",
        role=RolesChoices.RENTER,
    )
    client.login(email="user@example.com", password="password123")

    url = reverse('profile')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_profile_view(client):
    user = User.objects.create_user(
        email="user@example.com",
        password="password123",
        role=RolesChoices.RENTER,
    )
    client.login(email="user@example.com", password="password123")

    url = reverse('update_profile')
    response = client.post(url, {
        'first_name': 'Updated',
        'last_name': 'User',
        'middle_name': 'UpdatedMiddleName',
        'telegram_name': 'UpdatedTelegramName',
    })
    user.refresh_from_db()
    assert response.status_code == 302
    assert user.first_name == 'Updated'
    assert user.last_name == 'User'
    assert user.middle_name == 'UpdatedMiddleName'
    assert user.telegram_name == 'UpdatedTelegramName'
