import pytest
from dancematch.serializers import DancerSerializer, UserSerializer


@pytest.mark.django_db
def test_create_user_with_valid_data():
    # Valid data
    data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    }
    
    serializer = UserSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    
    user = serializer.save()
    
    assert user.username == data["username"]
    assert user.email == data["email"]
    assert user.check_password(data["password"])

    
@pytest.mark.django_db
def test_create_user_with_invalid_data():
    # Invalid data (missing username)
    data = {
        "email": "testuser@example.com",
        "password": "password123"
    }
    
    serializer = UserSerializer(data=data)
    assert not serializer.is_valid()
    assert "username" in serializer.errors
    

@pytest.mark.django_db
def test_create_dancer_with_valid_data():
    # Valid data to create a dancer
    data = {
        "user": {
            "username": "testdancer",
            "email": "testdancer@example.com",
            "password": "password123"
        },
        "location": "João Pessoa",
        "level": "beginner"
    }
    
    serializer = DancerSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    
    dancer = serializer.save()
    assert dancer.user.username == data["user"]["username"]
    assert dancer.user.email == data["user"]["email"]
    assert dancer.user.check_password(data["user"]["password"])
    assert dancer.location == data["location"]
    assert dancer.level == data["level"]

    
@pytest.mark.django_db
def test_create_dancer_with_invalid_user_data():
    # Invalid user data (missing username)
    data = {
        "user": {
            "email": "testdancer@example.com",
            "password": "securepassword123"
        },
        "location": "São Paulo",
        "level": "beginner"
    }

    serializer = DancerSerializer(data=data)
    assert not serializer.is_valid()
    assert "user" in serializer.errors
    assert "username" in serializer.errors["user"]


@pytest.mark.django_db
def test_create_dancer_with_invalid_dancer_data():
    # Invalid dancer data (missing location)
    data = {
        "user": {
            "username": "testdancer",
            "email": "testdancer@example.com",
            "password": "securepassword123"
        },
        "location": "",
        "level": "beginner"
    }

    serializer = DancerSerializer(data=data)
    assert not serializer.is_valid()
    assert "location" in serializer.errors
