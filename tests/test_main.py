from fastapi.testclient import TestClient

from src.main import app

# Initialisation du client de test FastAPI.
# Le TestClient simule des requêtes HTTP sur l'application FastAPI sans démarrer
# de serveur réseau réel, permettant des tests d'intégration rapides et isolés.
client = TestClient(app)


def test_health_check() -> None:
    """Vérifie le comportement de la route GET /health."""
    response = client.get("/health")

    # Validation du code de statut HTTP
    assert response.status_code == 200

    # Validation du schéma et du contenu de la réponse JSON
    data = response.json()
    assert data["status"] == "OK"
    assert data["environment"] == "production"
    assert data["version"] == "0.1.0"
