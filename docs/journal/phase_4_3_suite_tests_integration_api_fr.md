# 📌 Séance 4.3 : Suite de Tests d'Intégration de l'API & Couverture de Code
**Date :** 24 Juillet 2026

L'objectif de cette séance est d'implémenter et d'automatiser les tests d'intégration pour le point d'accès de santé de l'API FastAPI avec `TestClient` et d'assurer une configuration globale du projet pour atteindre et maintenir un taux de couverture de test de 100%.

---

### 1. 🎓 Nouveaux Concepts Introduits

*   **Test d'Intégration Automatisé :** Type de test logiciel vérifiant le comportement conjoint de plusieurs modules d'un système (ici, le routeur, la configuration et la sérialisation Pydantic de FastAPI), par opposition aux tests unitaires qui isolent un composant unique.
*   **Client de Test Synchrone (TestClient) :** Utilitaire fourni par Starlette permettant d'émettre de fausses requêtes HTTP sur l'application FastAPI en boucle locale sans allouer de port réseau ou démarrer de serveur physique.
*   **Couverture de Code (Code Coverage) :** Indicateur mesurant le pourcentage de lignes de code exécutées par la suite de tests. Une couverture de 100% garantit qu'aucune portion de code n'est laissée non testée.

---

### 2. 🧠 Prises de Décisions & Choix Techniques

#### Dilemme A : Configuration de la couverture via la ligne de commande ou pyproject.toml
*   **Option A.1 : Exécuter `pytest --cov=src` manuellement dans le Makefile**
    *   *Inconvénient :* Oblige à répéter les paramètres de couverture dans chaque script ou environnement de CI/CD.
*   **Option A.2 : Centraliser les options pytest et coverage dans le `pyproject.toml` (Retenue)**
    *   *Pourquoi ce choix ?* Simplicité et robustesse. En déclarant `addopts` et le seuil strict `fail_under = 100` dans le fichier de configuration centralisé, n'importe quelle exécution de `pytest` (via le Makefile, la ligne de commande ou le Dashboard) effectue automatiquement le calcul de couverture et fait échouer le build si une ligne de code de production n'est pas testée.

---

### 3. 🛠️ Implémentation & Auto-Documentation

#### Configuration Pytest & Coverage : [`pyproject.toml`](file:///home/michael/Code/job/projets/AIPE_Framework/pyproject.toml)
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
addopts = "--cov=src --cov-report=term-missing --cov-report=xml"

[tool.coverage.run]
source = ["src"]

[tool.coverage.report]
show_missing = true
fail_under = 100
```

#### Code de Test d'Intégration : [`tests/test_main.py`](file:///home/michael/Code/job/projets/AIPE_Framework/tests/test_main.py)
```python
from fastapi.testclient import TestClient
from src.main import app
from src.core.config import settings

client = TestClient(app)

def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == settings.HEALTH_STATUS
    assert data["environment"] == settings.ENVIRONMENT
    assert data["version"] == settings.VERSION
```

#### Commandes de validation à exécuter localement :
```bash
# Lancement de la suite de tests et calcul de la couverture
make test
```
*Le terminal affiche la table de couverture montrant 100% de réussite sur l'ensemble des fichiers de `src/`.*

---

### 4. 📌 Bilan du Jour

1.  **Mise en place de la suite de tests d'intégration** validant la route de santé de l'API.
2.  **Configuration automatisée de la couverture** de test dans `pyproject.toml`.
3.  **Validation d'un taux de couverture de 100%** sur l'ensemble du code source de production (`src/`).
