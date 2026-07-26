# 📌 Séance 5.1 : Dockerfile Multi-Stage avec Poetry
**Date :** 24 Juillet 2026

L'objectif de cette séance est de conteneuriser l'application de production AIPE_Framework dans une image Docker optimisée en utilisant le pattern multi-stage build. Le stage `builder` installe Poetry et compile les dépendances, tandis que le stage `runtime` ne conserve que l'environnement virtuel compilé et le code source, produisant une image finale inférieure à 250 Mo.

---

### 1. 🎓 Nouveaux Concepts Introduits

*   **Docker Multi-Stage Build :** Technique de construction Docker utilisant plusieurs instructions `FROM` successives dans un même Dockerfile. Le premier stage (`builder`) installe les outils lourds (Poetry, compilateurs) nécessaires à la préparation des dépendances, puis le second stage (`runtime`) repart d'une image vierge et ne copie que le résultat compilé. Tout le reste (Poetry, pip, caches) est abandonné, réduisant le poids de l'image de 80% et sa surface d'attaque.
*   **Contexte de build Docker :** Ensemble de fichiers envoyés au démon Docker lors de l'exécution de `docker build`. Le fichier `.dockerignore` filtre les fichiers inutiles (`.venv`, `.git`, `tests/`, `dashboard/`) pour accélérer le transfert et éviter les fuites d'informations sensibles dans l'image.
*   **Optimisation du cache de couches Docker :** Stratégie consistant à copier les fichiers de manifeste (`pyproject.toml`, `poetry.lock`) avant le code source. Si seul le code change, Docker réutilise la couche mise en cache de `poetry install` sans retélécharger les dépendances.
*   **Variables d'environnement de production Python :** `PYTHONDONTWRITEBYTECODE` (empêche la génération de fichiers `.pyc` inutiles en conteneur) et `PYTHONUNBUFFERED` (force l'écriture immédiate des logs pour les orchestrateurs).

---

### 2. 🧠 Prises de Décisions & Choix Techniques

#### Dilemme A : Installation de Poetry via pip ou via le script officiel

*   **Option A.1 : `pip install poetry` dans le conteneur**
    *   *Inconvénient :* Installe Poetry dans l'environnement Python global du conteneur, ce qui risque de créer des conflits de dépendances entre Poetry et les paquets du projet. De plus, pip laisse des caches volumineux difficiles à nettoyer proprement.
*   **Option A.2 : Script d'installation officiel `install.python-poetry.org` (Retenue)**
    *   *Pourquoi ce choix ?* Le script officiel installe Poetry dans un répertoire isolé (`/opt/poetry`), complètement séparé de l'environnement Python du projet. Cela garantit l'absence de conflits et permet de contrôler précisément la version via `POETRY_VERSION`. L'isolement est d'autant plus important dans un contexte multi-stage où l'on ne veut aucune pollution résiduelle.

#### Dilemme B : Image de base Alpine ou Debian Slim

*   **Option B.1 : `python:3.10-alpine` (ultra-légère, ~5 Mo)**
    *   *Inconvénient :* Alpine utilise `musl` au lieu de `glibc`, ce qui provoque des incompatibilités avec certaines bibliothèques Python compilées (notamment `uvloop`, le moteur d'Uvicorn). La compilation nécessite l'ajout manuel de paquets de développement (`gcc`, `musl-dev`), annulant une partie du gain de poids et ajoutant de la complexité.
*   **Option B.2 : `python:3.10-slim` (Debian allégée, ~40 Mo) (Retenue)**
    *   *Pourquoi ce choix ?* L'image slim offre un excellent compromis entre légèreté et compatibilité. Elle utilise la glibc standard, garantissant la compatibilité avec toutes les bibliothèques de l'écosystème Python. Le gain marginal d'Alpine (~35 Mo) ne justifie pas les risques de bugs d'exécution subtils en production.

#### Dilemme C : Copier le .venv ou utiliser pip freeze + pip install

*   **Option C.1 : Exporter un `requirements.txt` et faire `pip install` dans le runtime**
    *   *Inconvénient :* On perd le bénéfice du verrouillage déterministe de Poetry (`poetry.lock`). Les versions de sous-dépendances pourraient diverger entre le build et le runtime.
*   **Option C.2 : Copier directement le dossier `.venv` compilé (Retenue)**
    *   *Pourquoi ce choix ?* Copier le `.venv` tel quel depuis le stage builder garantit une correspondance bit-à-bit entre les dépendances compilées et le runtime. Aucune résolution de dépendances n'est refaite dans le stage final, ce qui est plus rapide et 100% déterministe.

---

### 3. 🛠️ Implémentation & Auto-Documentation

#### Structure du Dockerfile multi-stage : [`Dockerfile`](file:///home/michael/Code/ai-engineering/projets/AIPE_Framework/Dockerfile)

```dockerfile
# Stage 1 : Builder — Compilation des dépendances
FROM python:3.10-slim AS builder
ENV POETRY_VERSION=1.8.2
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1
# ... installation de Poetry, copie des manifestes, poetry install --only main

# Stage 2 : Runtime — Image finale minimale
FROM python:3.10-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Fichier d'exclusion du contexte de build : [`.dockerignore`](file:///home/michael/Code/ai-engineering/projets/AIPE_Framework/.dockerignore)
```text
.venv/
.git/
tests/
dashboard/
docs/
__pycache__/
.pytest_cache/
.mypy_cache/
```

#### Tests de validation structurelle : [`tests/test_dockerfile.py`](file:///home/michael/Code/ai-engineering/projets/AIPE_Framework/tests/test_dockerfile.py)
```python
def test_dockerfile_has_multi_stage_build() -> None:
    """Vérifie la présence des stages builder et runtime."""
    content = (PROJECT_DIR / "Dockerfile").read_text(encoding="utf-8")
    assert "AS builder" in content
    assert "AS runtime" in content
    assert "--from=builder" in content
```

#### Commandes de validation à exécuter localement :
```bash
# Lancement des tests de validation du Dockerfile
make test

# Construction de l'image Docker (validation du critère < 250 Mo)
docker build -t aipe-framework:latest .
docker images aipe-framework:latest --format "{{.Size}}"
```
*Les tests pytest doivent tous passer au vert. La commande `docker images` doit afficher une taille inférieure à 250 Mo.*

---

### 4. 📌 Bilan du Jour

1.  **Rédaction du Dockerfile multi-stage** séparant le stage builder (Poetry + compilation) du stage runtime (image finale minimale).
2.  **Création du fichier `.dockerignore`** excluant les artefacts de développement du contexte de build Docker.
3.  **Suite de tests de validation** (`tests/test_dockerfile.py`) vérifiant la structure du Dockerfile (deux stages, dépendances de production uniquement, variables d'environnement, port, commande de démarrage).
4.  **Documentation exhaustive** de chaque instruction Docker avec commentaires vulgarisés dans le Dockerfile.
