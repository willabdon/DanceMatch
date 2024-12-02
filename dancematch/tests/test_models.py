import pytest
from dancematch.models import Dancer, DanceStyle
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_create_dance_style():
    # Create a dance style
    style = DanceStyle.objects.create(name="Forró", description="Traditional Brazilian dance.")
    assert style.name == "Forró"
    assert style.description == "Traditional Brazilian dance."


@pytest.mark.django_db
def test_create_dancer():
    # Create a user
    user = User.objects.create_user(username="testuser", password="password123")
    
    # Create a dancer
    dancer = Dancer.objects.create(user=user, location="João Pessoa", level=Dancer.INTERMEDIATE)
    assert dancer.user.username == "testuser"
    assert dancer.location == "João Pessoa"
    assert dancer.level == Dancer.INTERMEDIATE


@pytest.mark.django_db
def test_dancer_dance_styles_relationship():
    # Create dance styles
    style1 = DanceStyle.objects.create(name="Forró")
    style2 = DanceStyle.objects.create(name="Samba de Gafieira")

    # Create a user and a dancer
    user = User.objects.create_user(username="testuser", password="password123")
    dancer = Dancer.objects.create(user=user, location="João Pessoa", level=Dancer.ADVANCED)

    # Associate dance styles with the dancer
    dancer.styles.add(style1, style2)

    # Assert the relationship
    assert dancer.styles.count() == 2
    assert style1 in dancer.styles.all()
    assert style2 in dancer.styles.all()
