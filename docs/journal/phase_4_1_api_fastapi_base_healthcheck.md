# 📌 Séance 9 : API FastAPI Base & Healthcheck (Phase 4)
**Date :** 23 Juillet 2026

L'objectif de cette séance est d'implémenter l'API de production de base du framework avec FastAPI, de créer la route de santé `/health` et d'automatiser sa validation à l'aide d'une suite de tests unitaires d'intégration HTTP.

---

### 1. 🎓 Nouveaux Concepts Introduits

*   **FastAPI & ASGI (Asynchronous Server Gateway Interface) :** Framework de conception d'API moderne de production. Par opposition à WSGI (utilisé par Flask), ASGI prend en charge l'asynchronisme natif, ce qui permet à l'API de gérer de manière concurrente des milliers de requêtes de longue durée (très utile pour la diffusion en continu d'agents d'IA ou la télémétrie asynchrone).
*   **Validation Pydantic de Données :** Déclaration de schémas de typage à l'aide de classes Pydantic. À l'exécution, Pydantic valide que le type des données reçues ou renvoyées est conforme à 100% au schéma défini, éliminant les erreurs d'exécution de données mal formées.
*   **TestClient FastAPI & httpx :** Outil de test d'intégration HTTP simulant des requêtes réelles. Le client Starlette s'appuie sur la bibliothèque `httpx` pour adresser des requêtes asynchrones en boucle locale fermée sur l'application.

---

### 2. 🧠 Prises de Décisions & Choix Techniques

#### Dilemme A : Choix du Framework Web
*   **Option A.1 : Utiliser Flask (utilisé pour notre dashboard local)**
    *   *Inconvénient :* Manque de support natif de l'asynchronisme. Pas de validation automatique de schéma ni de génération OpenAPI native.
*   **Option A.2 : Utiliser FastAPI (Retenue)**
    *   *Pourquoi ce choix ?* FastAPI est le standard de l'industrie pour les microservices d'IA en production. Sa vitesse et sa documentation interactive OpenAPI native (/docs) accélèrent considérablement l'intégration par les équipes frontend ou les orchestrateurs cloud.

#### Dilemme B : Ajout d'httpx comme dépendance de dev
*   **Option B.1 : Utiliser la bibliothèque `requests` classique**
    *   *Inconvénient :* Depuis les versions récentes de Starlette/FastAPI, `TestClient` requiert explicitement le paquet `httpx` pour s'exécuter sous peine de lever une exception `RuntimeError`.
*   **Option B.2 : Ajouter `httpx` aux dépendances de dev Poetry (Retenue)**
    *   *Pourquoi ce choix ?* Garantit la stabilité opérationnelle de nos tests. `httpx` a été ajouté via `poetry add -G dev httpx`, ce qui a mis à jour le verrou de dépendance `poetry.lock`.

---

### 3. 🛠️ Implémentation & Auto-Documentation

#### Extrait du Code Source : [`src/main.py`](file:///home/michael/Code/job/projets/AIPE_Framework/src/main.py)
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="AIPE_Framework API",
    description="Microservice d'API de production minimal pour le Blueprint AIPE.",
    version="0.1.0",
)

class HealthCheckResponse(BaseModel):
    status: str
    environment: str
    version: str

@app.get("/health", response_model=HealthCheckResponse)
async def health_check() -> HealthCheckResponse:
    return HealthCheckResponse(status="OK", environment="production", version="0.1.0")
```

#### Extrait des Tests : [`tests/test_main.py`](file:///home/michael/Code/job/projets/AIPE_Framework/tests/test_main.py)
```python
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "OK"
    assert data["environment"] == "production"
    assert data["version"] == "0.1.0"
```

---

### 4. 📌 Bilan du Jour

1.  **Création du point d'entrée de production** avec FastAPI et implémentation du Healthcheck conforme.
2.  **Ajout d'httpx** dans l'environnement virtuel pour satisfaire les requis du TestClient.
3.  **Écriture de `tests/test_main.py`** et validation à 100% de la suite de tests (15 réussites au total).
