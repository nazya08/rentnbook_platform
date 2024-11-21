import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

from review.models import Review
from user.models import Renter, LandLord

from tests.booking.booking_tests import accommodation, landlord_profile_fixture


@pytest.fixture
def renter_user():
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
def landlord_user():
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


# Fixtures
@pytest.mark.django_db
def test_create_review(client, renter_user, accommodation):
    """Test creating a review for an accommodation."""
    renter, renter_profile = renter_user
    client.login(email=renter.email, password="password123")

    data = {
        'rating': 5,
        'comment': 'Excellent accommodation!',
    }

    url = reverse('review_create', kwargs={'uuid': accommodation.uuid})

    response = client.post(url, data)

    assert response.status_code == 302
    assert Review.objects.count() == 1
    assert Review.objects.first().renter == renter_profile
    assert Review.objects.first().accommodation == accommodation


@pytest.mark.django_db
def test_create_review_multiple(client, renter_user, accommodation):
    """Test creating a review twice for the same accommodation."""
    renter, renter_profile = renter_user
    client.login(email=renter.email, password="password123")

    data = {
        'rating': 4,
        'comment': 'Good accommodation.',
    }
    url = reverse('review_create', kwargs={'uuid': accommodation.uuid})
    response = client.post(url, data)
    assert response.status_code == 302

    data = {
        'rating': 3,
        'comment': 'It was okay.',
    }
    response = client.post(url, data)

    assert response.status_code == 200
    assert 'rating' in response.context['form'].errors
    assert Review.objects.count() == 1


@pytest.mark.django_db
def test_create_review_invalid_rating(client, renter_user, accommodation):
    """Test creating a review with invalid rating (outside 1-5)."""
    renter, renter_profile = renter_user
    client.login(email=renter.email, password="password123")

    data = {
        'rating': 6,
        'comment': 'Too good to be true!',
    }

    url = reverse('review_create', kwargs={'uuid': accommodation.uuid})
    response = client.post(url, data)

    assert response.status_code == 200
    assert 'rating' in response.context['form'].errors
    assert Review.objects.count() == 0


@pytest.mark.django_db
def test_create_review_missing_comment(client, renter_user, accommodation):
    """Test creating a review without a comment."""
    renter, renter_profile = renter_user
    client.login(email=renter.email, password="password123")

    data = {
        'rating': 3,
        'comment': '',
    }

    url = reverse('review_create', kwargs={'uuid': accommodation.uuid})
    response = client.post(url, data)

    assert response.status_code == 302
    assert Review.objects.count() == 1
    assert Review.objects.first().comment == ''


@pytest.mark.django_db
def test_create_review_redirect_if_authenticated(client, renter_user, accommodation):
    """Test that authenticated users are redirected to the review page after submitting a valid review."""
    renter, renter_profile = renter_user
    client.login(email=renter.email, password="password123")

    data = {
        'rating': 4,
        'comment': 'Very nice place!',
    }

    url = reverse('review_create', kwargs={'uuid': accommodation.uuid})
    response = client.post(url, data)

    success_url = reverse('accommodation_detail', kwargs={'uuid': accommodation.uuid})

    assert response.status_code == 302
    assert response.url == success_url
