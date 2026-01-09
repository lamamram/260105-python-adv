"""
Tests pour les routes utilisateurs (user_router)
Utilise pytest avec mock de la base de données SQLite
"""
# pip install pytest pytest-cov httpx
# Lancer les tests
# cd servers/app
# pytest tests/test_users_router.py -v

import pytest
from unittest.mock import MagicMock

from app.orm.models import User as UserModel

# Note: Les fixtures mock_db_session et client sont dans conftest.py


# ========== FIXTURES SPÉCIFIQUES AUX TESTS USERS ==========

@pytest.fixture
def sample_user():
    """
    Fixture qui crée un utilisateur exemple pour les tests
    """
    user = UserModel(
        id=1,
        username="testuser",
        password="hashed_password"
    )
    return user


# ========== TESTS search_users ==========

def test_search_users_no_keyword(client, mock_db_session, sample_user):
    """
    Test: recherche sans mot-clé (retourne tous les users limités)
    Expected: status 200 avec liste d'utilisateurs
    """
    # Arrange
    user2 = UserModel(id=2, username="alice", password="hash")
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [sample_user, user2]
    mock_db_session.execute.return_value = mock_result
    
    # Act
    response = client.get("/users/search")
    
    # Assert
    assert response.status_code == 200
    # Note: la route actuelle a un bug - elle retourne un objet Result au lieu de users
    # Ce test va échouer jusqu'à correction


def test_search_users_with_keyword(client, mock_db_session, sample_user):
    """
    Test: recherche avec mot-clé
    Expected: status 200 avec utilisateurs filtrés
    """
    # Arrange
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [sample_user]
    mock_db_session.execute.return_value = mock_result
    
    # Act
    response = client.get("/users/search?keyword=test&max_results=10")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) == 1
    assert data["results"][0]["username"] == "testuser"


def test_search_users_keyword_too_short(client):
    """
    Test: recherche avec mot-clé trop court (< 3 caractères)
    Expected: status 422 (validation error)
    """
    # Act
    response = client.get("/users/search?keyword=ab")
    
    # Assert
    assert response.status_code == 422


# ========== TESTS home ==========

def test_home_route(client, mock_db_session, sample_user):
    """
    Test: route /users/home avec template
    Expected: status 200 et HTML
    """
    # Arrange
    user2 = UserModel(id=2, username="bob", password="hash")
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [sample_user, user2]
    mock_db_session.execute.return_value = mock_result
    
    # Act
    response = client.get("/users/home")
    
    # Assert
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    # Vérifier que le template contient le username
    assert "testuser" in response.text or "bob" in response.text
