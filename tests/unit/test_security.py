import uuid
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)


def test_password_hashing():
    raw_password = "SecurePassword123!"
    hashed = get_password_hash(raw_password)
    assert hashed != raw_password
    assert verify_password(raw_password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_jwt_access_token():
    user_id = uuid.uuid4()
    org_id = uuid.uuid4()
    role = "ADMIN"

    token = create_access_token(subject=user_id, org_id=org_id, role=role)
    payload = decode_token(token, is_refresh=False)

    assert payload["sub"] == str(user_id)
    assert payload["org_id"] == str(org_id)
    assert payload["role"] == role
    assert payload["type"] == "access"


def test_jwt_refresh_token():
    user_id = uuid.uuid4()
    family_id = uuid.uuid4()

    token = create_refresh_token(subject=user_id, token_family_id=family_id)
    payload = decode_token(token, is_refresh=True)

    assert payload["sub"] == str(user_id)
    assert payload["family"] == str(family_id)
    assert payload["type"] == "refresh"
