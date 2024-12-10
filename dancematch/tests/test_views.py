import pytest
from django.contrib.auth.models import User
from rest_framework import status

from dancematch.models import Dancer


@pytest.mark.django_db
def test_create_dancer_valid_data(api_client):
        
    # Register a dancer
    response = api_client.post('/api/dancers/', {
        "user": {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123",
        },
        "location": "João Pessoa",
        "level": "intermediate"
    }, format="json")
    
    # Assertions
    assert response.status_code == status.HTTP_201_CREATED, response.data
    assert response.data["user"]["username"] == "testuser"
    assert response.data["location"] == "João Pessoa"
    assert response.data["level"] == "intermediate"
    assert "password" not in response.data
    assert "password" not in response.data["user"]
    assert User.objects.filter(id=response.data["user"]["id"]).exists()
    assert Dancer.objects.filter(id=response.data["id"]).exists()
    

@pytest.mark.django_db
def test_create_dancer_missing_required_fields(api_client):
    
    # Attempt to register a user dancer with missing fields
    response = api_client.post('/api/dancers/', {
        "user": {
            "username": "",
            "password": ""
        },
        "level": "",
        "location": ""
    }, format="json")
    
    # Assertions
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "username" in response.data["user"]
    assert "password" in response.data["user"]
    assert "level" in response.data
    assert "location" in response.data


@pytest.mark.django_db
def test_update_dancer(api_client):
    
    # Setup: create user and authenticate
    user = User.objects.create_user(username="testuser", password="password123")
    dancer = Dancer.objects.create(user=user, location="João Pessoa", level=Dancer.BEGINNER)
    api_client.force_authenticate(user=user)
    
    # Update the dancer profile
    response = api_client.put(f'/api/dancers/{dancer.id}/', {
        "location": "Rio de Janeiro",
        "level": "advanced"
    })
    
    # Assertions
    assert response.status_code == status.HTTP_200_OK, response.data
    assert response.data['location'] == "Rio de Janeiro"
    assert response.data['level'] == "advanced"
    

@pytest.mark.django_db
def test_delete_dancer(api_client):
    
    # Setup: create user and authenticate
    user = User.objects.create_user(username="testuser", password="password123")
    dancer = Dancer.objects.create(user=user, location="João Pessoa", level=Dancer.BEGINNER)
    api_client.force_authenticate(user=user)
    
    # Delete the user's dancer
    response = api_client.delete(f'/api/dancers/{dancer.id}/')
    
    # Assertions
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not User.objects.filter(id=user.id).exists()
    assert not Dancer.objects.filter(id=dancer.id).exists()
