import pytest
from sqlalchemy.orm import Session

from db.models import UserModel, UserGroupModel, UserGroupEnum, UserProfileModel
from db.security.passwords import verify_password

def test_user_profile_creation(db: Session, user: UserModel):
    profile = UserProfileModel(
        user_id=user.id,
        first_name="John",
        last_name="Doe",
        gender="man"
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)

    assert profile.user_id == user.id
    assert profile.first_name == "John"
    assert profile.gender == "man"
    assert profile.user.id == user.id

def test_user_password_setter_and_verify(user_group: UserGroupModel):
    user = UserModel.create(
        email="new@example.com",
        raw_password="AnotherStrongPass1!",
        group_id=user_group.id
    )
    assert user._hashed_password is not None
    assert user.verify_password("AnotherStrongPass1!")
    assert not user.verify_password("WrongPassword")


@pytest.fixture
def user_group(db: Session):
    group = UserGroupModel(name=UserGroupEnum.USER)
    db.add(group)
    db.commit()
    db.refresh(group)
    return group

@pytest.fixture
def user(db: Session, user_group: UserGroupModel):
    u = UserModel.create(
        email="test@example.com",
        raw_password="StrongPassw0rd!",
        group_id=user_group.id
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return u

def test_user_creation(user: UserModel):
    assert user.email == "test@example.com"
    assert user.is_active is False
    assert user.has_group("user") is True
    assert verify_password("StrongPassw0rd!", user._hashed_password)
