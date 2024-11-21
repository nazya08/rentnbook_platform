import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_home_view(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_signup_view_get(client):
    response = client.get(reverse('signup'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_view_get(client):
    response = client.get(reverse('login'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_view_post(client, django_user_model):
    django_user_model.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='testpassword123',
    )

    response = client.post(
        reverse('login'),
        data={'email': 'testuser@example.com', 'password': 'testpassword123'}
    )
    assert response.status_code == 302
    assert response.url == reverse('home')


@pytest.mark.django_db
def test_logout_view(client, django_user_model):
    django_user_model.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='testpassword123',
    )
    client.login(email='testuser@example.com', password='testpassword123')

    response = client.get(reverse('logout'))
    assert response.status_code == 302
    assert response.url == reverse('home')
