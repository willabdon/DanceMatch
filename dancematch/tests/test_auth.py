import pytest
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.mark.django_db
def test_obtain_token_success(api_client):
    # Setup: Create a test user
    user = User.objects.create_user(username='testuser', password='password123')

    # Send POST request to obtain token
    response = api_client.post('/api/token/', {
        'username': 'testuser',
        'password': 'password123'
    })

    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data


@pytest.mark.django_db
def test_obtain_token_invalid_credentials(api_client):
    # Send POST request with invalid credentials
    response = api_client.post('/api/token/', {
        'username': 'invaliduser',
        'password': 'wrongpassword'
    })

    assert response.status_code == 401
    assert 'access' not in response.data


@pytest.mark.django_db
def test_access_protected_endpoint_with_valid_token(api_client):
    # Setup: Create a test user and obtain a token
    user = User.objects.create_user(username='testuser', password='password123')
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    # Set token on API Client
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    # Send GET request to the protected endpoint
    response = api_client.get('/api/protected/')

    assert response.status_code == 200
    assert response.data['message'] == f"Hello, testuser, you are authenticated!"


@pytest.mark.django_db
def test_access_protected_endpoint_with_invalid_token(api_client):
    # Set token on API Client
    api_client.credentials(HTTP_AUTHORIZATION='Bearer invalidtoken')

    # Send GET request to the protected endpoint
    response = api_client.get('/api/protected/')

    assert response.status_code == 401
    assert response.data['detail'] == 'Given token not valid for any token type'


@pytest.mark.django_db
def test_access_protected_endpoint_without_token(api_client):
    # Send GET request to the protected endpoint
    response = api_client.get('/api/protected/')

    assert response.status_code == 401
    assert response.data['detail'] == 'Authentication credentials were not provided.'
