# 📌 Séance 10 : Modularisation de l'API & Structure Clean Architecture (Phase 4)
**Date :** 24 Juillet 2026

L'objectif de cette séance est de refondre l'initialisation de l'API FastAPI en passant d'un fichier monolithique unique à une structure modulaire et extensible adaptée à des projets industriels. Ce découpage facilite la compréhension par un développeur junior et pose les fondations pour ajouter de nouvelles routes d'IA (RAG, agents).

---

### 1. 🎓 Nouveaux Concepts Introduits

*   **Séparation des préoccupations (Separation of Concerns - SoC) :** Principe d'architecture consistant à diviser un programme en sections distinctes, chacune gérant une unique responsabilité (ex: routage, validation, configuration). Cela améliore grandement la maintenabilité du code.
*   **APIRouter FastAPI :** Composant permettant de définir des groupes de routes d'API de manière isolée dans des fichiers séparés. Ces routeurs sont ensuite inclus et fusionnés au sein de l'application globale dans le point d'entrée `main.py`.
*   **Pattern de Configuration Centralisée (Settings) :** Utilisation d'une classe dédiée à la configuration globale de l'application pour isoler les variables d'environnement et de déploiement (métadonnées d'API, version, environnement d'exécution) du code métier opérationnel.

---

### 2. 🧠 Prises de Décisions & Choix Techniques

#### Dilemme A : Architecture Monolithique (`main.py` unique) vs Architecture Modulaire
*   **Option A.1 : Garder tout le code dans `src/main.py`**
    *   *Avantage :* Simple pour un PoC très court et rapide à lire.
    *   *Inconvénient :* Devient rapidement un "code spaghetti" ingérable dès que l'on ajoute des modules d'IA (RAG, LLM chains, agents).
*   **Option A.2 : Adopter une structure en paquets (`core`, `schemas`, `api/routes`) (Retenue)**
    *   *Pourquoi ce choix ?* C'est le standard de l'industrie pour les projets de production. Cela montre de bonnes pratiques dès le premier jour, permet aux développeurs de travailler sur des fonctionnalités différentes sans provoquer de conflits de fusion (merge conflicts) majeurs sur Git, et guide clairement un développeur junior sur l'endroit où ajouter du code.

#### Dilemme B : Définition des valeurs de Healthcheck statiques vs issues de la Configuration
*   **Option B.1 : Hardcoder "healthy", "production" et "0.1.0" directement dans la route**
    *   *Inconvénient :* Si la version de l'application change (ex: lors d'une release CI/CD) ou si l'API tourne en développement, le healthcheck renverra des données fausses ou nécessitera une modification manuelle du code de la route.
*   **Option B.2 : Charger les données dynamiquement depuis l'objet `settings` (Retenue)**
    *   *Pourquoi ce choix ?* Dynamisme et fiabilité. Les valeurs proviennent du module de configuration `src/core/config.py` qui peut lui-même charger des variables d'environnement cloud réelles. De plus, les tests unitaires s'adaptent dynamiquement en important et assertant ces mêmes réglages.

---

### 3. 🛠️ Implémentation & Auto-Documentation

#### Nouvelle Structure de Paquets de `src/` :
```text
src/
├── __init__.py
├── main.py                    # Point d'entrée principal (initialisation & inclusion des routeurs)
├── core/
│   ├── __init__.py
│   └── config.py              # Configuration globale centralisée (Settings)
├── schemas/
│   ├── __init__.py
│   └── health.py              # Schémas de validation Pydantic (HealthCheckResponse)
└── api/
    ├── __init__.py
    └── routes/
        ├── __init__.py
        └── health.py          # Routeur de l'endpoint /health (APIRouter)
```

#### Extrait du Routeur : [`src/api/routes/health.py`](file:///home/michael/Code/job/projets/AIPE_Framework/src/api/routes/health.py)
```python
from fastapi import APIRouter
from src.core.config import settings
from src.schemas.health import HealthCheckResponse

router = APIRouter()

@router.get("/health", response_model=HealthCheckResponse)
async def health_check() -> HealthCheckResponse:
    return HealthCheckResponse(
        status=settings.HEALTH_STATUS,
        environment=settings.ENVIRONMENT,
        version=settings.VERSION,
    )
```

#### Commandes de validation à exécuter localement :
```bash
# Lancement de la suite de tests avec rapports de couverture
make test
```
*La commande doit s'exécuter avec un taux de réussite de 100% (15 tests passés) et zéro warning Pydantic.*

---

### 4. 📌 Bilan du Jour

1.  **Refactoring modulaire complet** du répertoire `src/` en sous-paquets (`core`, `schemas`, `api/routes`).
2.  **Mise à jour des tests d'intégration** dans `tests/test_main.py` pour valider de façon dynamique les réponses de santé via les réglages globaux du framework.
3.  **Résolution des warnings de dépréciation Pydantic V2** en remplaçant le mot-clé `example` par `examples` dans la définition des champs de schémas.
4.  **Exécution de Ruff** (`check --fix` et `format`) assurant une qualité et un formatage de code 100% conformes aux règles configurées dans `pyproject.toml`.
