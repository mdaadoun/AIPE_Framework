# ==============================================================================
# AIPE Framework - Tests - API Healthcheck Integration Tests
# ==============================================================================
# Ce module automatise les tests d'intégration de la route GET /health.
# Il garantit que l'API renvoie le bon code HTTP et la structure JSON attendue.
# ==============================================================================

from fastapi.testclient import TestClient

from src.core.config import settings
from src.main import app

# Initialisation du client de test FastAPI.
#
# Pour un dev junior :
# Le 'TestClient' simule de véritables appels HTTP (GET, POST, etc.) sur notre
# application FastAPI sans avoir à lancer de serveur réseau réel (pas d'écoute sur le port 8000).
# Cela permet d'exécuter nos tests en quelques millisecondes et de les intégrer
# dans des boucles de validation automatique (CI/CD ou localement).
client = TestClient(app)


def test_health_check() -> None:
    """
    Vérifie le comportement et la conformité de la route GET /health.

    Pour un dev junior :
    Un test d'intégration s'assure du bon fonctionnement combiné de plusieurs composants :
    le routeur, les schémas de données Pydantic, et la configuration globale.
    """
    # 1. Émettre une requête HTTP GET sur le chemin d'API /health
    response = client.get("/health")

    # 2. Valider le code de statut HTTP (200 OK indique que le service fonctionne)
    assert response.status_code == 200

    # 3. Récupérer et valider le corps de la réponse au format JSON
    data = response.json()

    # 4. Effectuer des assertions robustes en comparant le JSON reçu avec nos
    #    valeurs de configuration issues de 'settings'. Ainsi, si les réglages changent,
    #    les tests restent valides et dynamiques.
    assert data["status"] == settings.HEALTH_STATUS
    assert data["environment"] == settings.ENVIRONMENT
    assert data["version"] == settings.VERSION
