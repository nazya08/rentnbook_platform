import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from accommodation.models import Accommodation, RentalTypeChoices
from user.models import RolesChoices


@pytest.mark.django_db
def test_accommodation_create(client):
    """Тестуємо створення нового житла."""
    get_user_model().objects.create_user(email='testuser@gmail.com', password='password123', role=RolesChoices.LANDLORD)
    client.login(email='testuser@gmail.com', password='password123')

    data = {
        'title': 'Test Accommodation',
        'description': 'A great place to stay!',
        'rental_type': RentalTypeChoices.APARTMENT,
        'price_per_night': 100.0,
        'location': 'Test Location',
        'max_guests': 4,
        'available_from': '2024-12-01',
        'available_to': '2024-12-15',
    }

    response = client.post(reverse('accommodation_create'), data)

    assert response.status_code == 302
    assert Accommodation.objects.count() == 1
    accommodation = Accommodation.objects.first()
    assert accommodation.title == 'Test Accommodation'


@pytest.mark.django_db
def test_accommodation_update(client):
    """Тестуємо оновлення житла."""
    user = get_user_model().objects.create_user(email='testuser@gmail.com', password='password123', role=RolesChoices.LANDLORD)
    client.login(email='testuser@gmail.com', password='password123')

    accommodation = Accommodation.objects.create(
        owner=user.landlord_profile,
        title='Old Title',
        description='Old description',
        rental_type=RentalTypeChoices.HOUSE,
        price_per_night=100.0,
        location='Old Location',
        max_guests=4,
        available_from='2024-12-01',
        available_to='2024-12-15',
    )

    data = {
        'title': 'Updated Title',
        'description': 'Updated description',
        'rental_type': RentalTypeChoices.ROOM,
        'price_per_night': 120.0,
        'location': 'Updated Location',
        'max_guests': 6,
        'available_from': '2024-12-10',
        'available_to': '2024-12-20',
    }

    response = client.post(reverse('accommodation_update', kwargs={'uuid': accommodation.uuid}), data)

    assert response.status_code == 302
    accommodation.refresh_from_db()
    assert accommodation.title == 'Updated Title'
    assert accommodation.description == 'Updated description'


@pytest.mark.django_db
def test_accommodation_search(client):
    """Тестуємо пошук житла."""
    user = get_user_model().objects.create_user(email='testuser@gmail.com', password='password123', role=RolesChoices.LANDLORD)
    client.login(email='testuser@gmail.com', password='password123')

    accommodation_1 = Accommodation.objects.create(
        owner=user.landlord_profile,
        title='Accommodation 1',
        description='Description 1',
        rental_type=RentalTypeChoices.APARTMENT,
        price_per_night=100.0,
        location='Location 1',
        max_guests=4,
        available_from='2024-12-01',
        available_to='2024-12-15',
    )

    accommodation_2 = Accommodation.objects.create(
        owner=user.landlord_profile,
        title='Accommodation 2',
        description='Description 2',
        rental_type=RentalTypeChoices.HOUSE,
        price_per_night=150.0,
        location='Location 2',
        max_guests=2,
        available_from='2024-12-01',
        available_to='2024-12-15',
    )

    # Пошук за місцезнаходженням
    search_data = {'location': 'Location 1'}
    response = client.get(reverse('accommodation_search'), search_data)

    assert response.status_code == 200
    assert len(response.context['accommodations']) == 1
    assert response.context['accommodations'][0] == accommodation_1


@pytest.mark.django_db
def test_accommodation_detail(client):
    """Тестуємо перегляд детальної інформації про житло."""
    user = get_user_model().objects.create_user(email='testuser@gmail.com', password='password123', role=RolesChoices.LANDLORD)
    client.login(email='testuser@gmail.com', password='password123')

    accommodation = Accommodation.objects.create(
        owner=user.landlord_profile,
        title='Test Accommodation',
        description='A great place to stay!',
        rental_type=RentalTypeChoices.APARTMENT,
        price_per_night=100.0,
        location='Test Location',
        max_guests=4,
        available_from='2024-12-01',
        available_to='2024-12-15',
    )

    response = client.get(reverse('accommodation_detail', kwargs={'uuid': accommodation.uuid}))

    assert response.status_code == 200
    assert response.context['accommodation'] == accommodation


@pytest.mark.django_db
def test_accommodation_filter(client):
    """Тестуємо фільтрацію житла."""
    user = get_user_model().objects.create_user(email='testuser@gmail.com', password='password123', role=RolesChoices.LANDLORD)
    client.login(email='testuser@gmail.com', password='password123')

    accommodation_1 = Accommodation.objects.create(
        owner=user.landlord_profile,
        title='Accommodation 1',
        description='Description 1',
        rental_type=RentalTypeChoices.APARTMENT,
        price_per_night=100.0,
        location='Location 1',
        max_guests=4,
        available_from='2024-12-01',
        available_to='2024-12-15',
    )

    accommodation_2 = Accommodation.objects.create(
        owner=user.landlord_profile,
        title='Accommodation 2',
        description='Description 2',
        rental_type=RentalTypeChoices.HOUSE,
        price_per_night=150.0,
        location='Location 2',
        max_guests=2,
        available_from='2024-12-01',
        available_to='2024-12-15',
    )

    # Тестуємо фільтрацію за активним статусом
    response = client.get(reverse('my_accommodations'), {'is_active': 'on'})

    assert response.status_code == 200
    assert len(response.context['accommodations']) == 2
    assert accommodation_1 in response.context['accommodations']
    assert accommodation_2 in response.context['accommodations']
