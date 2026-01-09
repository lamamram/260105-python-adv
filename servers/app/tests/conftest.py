"""
Configuration pytest partagée pour tous les tests
Fixtures globales et configuration
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.orm.database import get_db

# Ajouter le répertoire parent au PYTHONPATH pour les imports
# Permet d'importer app.main, app.orm.models, etc.
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


# ========== FIXTURES GLOBALES ==========

@pytest.fixture
def mock_db_session():
    """
    Fixture qui crée une session DB mockée
    Retourne un Mock de Session SQLAlchemy
    """
    mock_session = Mock(spec=Session)
    return mock_session


@pytest.fixture
def client(mock_db_session):
    """
    Fixture qui crée un client de test FastAPI
    avec une base de données mockée
    """
    # Override de la dépendance get_db avec notre mock
    def override_get_db():
        try:
            yield mock_db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Créer le client de test
    with TestClient(app) as test_client:
        yield test_client
    
    # Nettoyer après les tests
    app.dependency_overrides.clear()


# ========== CONFIGURATION PYTEST ==========

def pytest_configure(config):
    """Enregistrer les markers personnalisés"""
    config.addinivalue_line(
        "markers", 
        "integration: mark test as integration test (slow, uses real DB)"
    )
    config.addinivalue_line(
        "markers",
        "slow: mark test as slow running"
    )
