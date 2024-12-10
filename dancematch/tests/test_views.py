import pytest
from django.contrib.auth.models import User
from rest_framework import status


@pytest.mark.django_db
def test_create_profile_valid_data(api_client):
        
    # Register a user profile
    response = api_client.post('/api/profiles/', {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123",
        "location": "João Pessoa",
        "level": "intermediate"
    })
    
    # Assertions
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["username"] == "testuser"
    assert response.data["location"] == "João Pessoa"
    assert response.data["level"] == "intermediate"
    assert "password" not in response.data
    assert User.objects.filter(id=response.data["id"]).exists()
    

@pytest.mark.django_db
def test_create_profile_missing_required_fields(api_client):
    
    # Attempt to register a user profile with missing fields
    response = api_client.post('/api/profiles/', {
        "username": "",
        "email": "",
        "password": ""
    })
    
    # Assertions
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "username" in response.data
    assert "email" in response.data
    assert "password" in response.data


@pytest.mark.django_db
def test_update_profile(api_client):
    
    # Setup: create user and authenticate
    user = User.objects.create_user(username="testuser", password="password123")
    api_client.force_authenticate(user=user)
    
    # Update the user's profile
    response = api_client.put(f'/api/profiles/{user.id}/', {
        "username": "updateduser",
        "email": "updated@example.com",
        "location": "Rio de Janeiro",
        "level": "advanced"
    })
    
    # Assertions
    assert response.status_code == status.HTTP_200_OK
    assert response.data['username'] == "updateduser"
    assert response.data['email'] == "updated@example.com"
    assert response.data['location'] == "Rio de Janeiro"
    assert response.data['level'] == "advanced"
    

@pytest.mark.django_db
def test_delete_profile(api_client):
    
    # Setup: create user and authenticate
    user = User.objects.create_user(username="testuser", password="password123")
    api_client.force_authenticate(user=user)
    
    # Delete the user's profile
    response = api_client.delete(f'/api/profiles/{user.id}/')
    
    # Assertions
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not User.objects.filter(id=user.id).exists()
