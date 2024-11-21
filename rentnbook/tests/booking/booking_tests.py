import pytest
from django.test import Client
from django.urls import reverse

from django.utils import timezone
from django.contrib.auth import get_user_model

from accommodation.models import Accommodation, RentalTypeChoices
from booking.models import Booking, BookingStatusChoices
from user.models import RolesChoices, LandLord, Renter


@pytest.fixture
def renter_user2():
    """Fixture to create a renter user."""
    User = get_user_model()

    user = User.objects.create_user(
        email="renter@example.com",
        password="password123",
        first_name="Renter",
        last_name="User"
    )
    renter_profile = Renter.objects.create(user=user)
    return user, renter_profile


@pytest.fixture
def landlord_user2():
    """Fixture to create a landlord user."""
    User = get_user_model()

    user = User.objects.create_user(
        email="landlord@example.com",
        password="password123",
        first_name="Landlord",
        last_name="User"
    )
    landlord_profile = LandLord.objects.create(user=user)
    return user, landlord_profile


@pytest.fixture
def landlord_profile_fixture():
    """Fixture для створення одендодавця."""
    return get_user_model().objects.create_user(
        email='landlord_profile@example.com', password='password', role=RolesChoices.LANDLORD, phone_number='67890'
    )


@pytest.fixture
def renter_profile_fixture():
    """Fixture для створення одендаря."""
    return get_user_model().objects.create_user(
        email='renter_profile@example.com', password='password', role=RolesChoices.RENTER, phone_number='12345'
    )


@pytest.fixture
def accommodation(landlord_profile_fixture):
    """Fixture для створення житла."""
    return Accommodation.objects.create(
        title="Test Accommodation",
        description="Test description",
        available_from=timezone.now().date(),
        available_to=timezone.now().date() + timezone.timedelta(days=30),
        rental_type=RentalTypeChoices.APARTMENT,
        price_per_night=100,
        location="Test Location",
        max_guests=5,
        owner=landlord_profile_fixture.landlord_profile
    )


@pytest.fixture
def booking(renter_profile_fixture, accommodation):
    """Fixture для створення бронювання."""
    return Booking.objects.create(
        renter=renter_profile_fixture.renter_profile,
        accommodation=accommodation,
        start_date=timezone.now().date() + timezone.timedelta(days=1),
        end_date=timezone.now().date() + timezone.timedelta(days=5),
        guests=2,
    )


@pytest.mark.django_db
def test_booking_creation(booking):
    """Тест перевірки створення бронювання."""
    assert booking.renter is not None
    assert booking.accommodation is not None
    assert booking.status == BookingStatusChoices.PENDING
    assert booking.guests == 2


@pytest.mark.django_db
def test_booking_unique_together(booking):
    """Тест перевірки унікальності бронювання для однакових дат і житла."""
    accommodation = booking.accommodation
    start_date = booking.start_date
    end_date = booking.end_date
    with pytest.raises(Exception):
        Booking.objects.create(
            renter=booking.renter,
            accommodation=accommodation,
            start_date=start_date,
            end_date=end_date,
            guests=3
        )


@pytest.mark.django_db
def test_create_booking(client, accommodation, renter_user2):
    """Тест для створення бронювання."""
    renter, renter_profile = renter_user2

    client.login(email=renter.email, password='password123')

    accommodation_uuid = accommodation.uuid

    data = {
        'start_date': '2024-12-01',
        'end_date': '2024-12-05',
        'guests': 2,
    }

    response = client.post(reverse('create_booking', args=[accommodation_uuid]), data)

    assert response.status_code == 302
    assert Booking.objects.count() == 1


@pytest.mark.django_db
def test_booking_create_invalid_guests(client, accommodation, renter_user2):
    """Тест для перевірки помилки при введенні кількості гостей, що перевищує ліміт."""
    renter, renter_profile = renter_user2

    client.login(email=renter.email, password='password123')

    data = {
        'start_date': '2024-12-01',
        'end_date': '2024-12-05',
        'guests': 6,
    }

    accommodation_uuid = accommodation.uuid

    response = client.post(reverse('create_booking', args=[accommodation_uuid]), data)
    assert response.status_code == 200
    assert 'guests' in response.context['form'].errors
