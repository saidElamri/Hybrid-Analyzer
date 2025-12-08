"""
Tests for authentication endpoints.
"""
import pytest
from auth.utils import verify_password


def test_register_success(client):
    """Test successful user registration."""
    response = client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepassword123"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["username"] == "newuser"
    assert data["user"]["email"] == "newuser@example.com"


def test_register_duplicate_username(client, test_user):
    """Test registration with existing username."""
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "different@example.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_register_duplicate_email(client, test_user):
    """Test registration with existing email."""
    response = client.post(
        "/auth/register",
        json={
            "username": "differentuser",
            "email": "test@example.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_register_invalid_email(client):
    """Test registration with invalid email."""
    response = client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "email": "invalid-email",
            "password": "password123"
        }
    )
    
    assert response.status_code == 422  # Validation error


def test_register_short_password(client):
    """Test registration with short password."""
    response = client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "short"
        }
    )
    
    assert response.status_code == 422  # Validation error


def test_login_success(client, test_user):
    """Test successful login."""
    response = client.post(
        "/auth/login",
        json={
            "username": "testuser",
            "password": "testpassword123"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["username"] == "testuser"


def test_login_wrong_password(client, test_user):
    """Test login with incorrect password."""
    response = client.post(
        "/auth/login",
        json={
            "username": "testuser",
            "password": "wrongpassword"
        }
    )
    
    assert response.status_code == 401
    assert "incorrect" in response.json()["detail"].lower()


def test_login_nonexistent_user(client):
    """Test login with non-existent username."""
    response = client.post(
        "/auth/login",
        json={
            "username": "nonexistent",
            "password": "password123"
        }
    )
    
    assert response.status_code == 401


def test_password_hashing(db_session, test_user):
    """Test that passwords are properly hashed."""
    # Password should not be stored in plain text
    assert test_user.password_hash != "testpassword123"
    
    # Verify password works
    assert verify_password("testpassword123", test_user.password_hash)
    assert not verify_password("wrongpassword", test_user.password_hash)
