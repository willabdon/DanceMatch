import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.mark.django_db
def test_obtain_token_success():
    # Setup: Create a test user
    user = User.objects.create_user(username='testuser', password='password123')

    # Initialize API client
    client = APIClient()

    # Send POST request to obtain token
    response = client.post('/api/token/', {
        'username': 'testuser',
        'password': 'password123'
    })

    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data


@pytest.mark.django_db
def test_obtain_token_invalid_credentials():
    # Initialize API client
    client = APIClient()

    # Send POST request with invalid credentials
    response = client.post('/api/token/', {
        'username': 'invaliduser',
        'password': 'wrongpassword'
    })

    assert response.status_code == 401
    assert 'access' not in response.data


@pytest.mark.django_db
def test_access_protected_endpoint_with_valid_token():
    # Setup: Create a test user and obtain a token
    user = User.objects.create_user(username='testuser', password='password123')
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    # Initialize API client with token
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    # Send GET request to the protected endpoint
    response = client.get('/api/protected/')

    assert response.status_code == 200
    assert response.data['message'] == f"Hello, testuser, you are authenticated!"


@pytest.mark.django_db
def test_access_protected_endpoint_with_invalid_token():
    # Initialize API client with an invalid token
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer invalidtoken')

    # Send GET request to the protected endpoint
    response = client.get('/api/protected/')

    assert response.status_code == 401
    assert response.data['detail'] == 'Given token not valid for any token type'


@pytest.mark.django_db
def test_access_protected_endpoint_without_token():
    # Initialize API client without token
    client = APIClient()

    # Send GET request to the protected endpoint
    response = client.get('/api/protected/')

    assert response.status_code == 401
    assert response.data['detail'] == 'Authentication credentials were not provided.'
