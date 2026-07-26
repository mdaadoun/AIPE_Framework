# 📌 Séance 5.3 : Sonde de Surveillance Système (HEALTHCHECK)
**Date :** 24 Juillet 2026

L'objectif de cette séance est d'intégrer une sonde de surveillance de santé native Docker (`HEALTHCHECK`) dans le stage `runtime` du Dockerfile. Cette sonde interroge l'endpoint `/health` de notre API toutes les 15 secondes via `curl` afin de permettre aux orchestrateurs de conteneurs (Docker Swarm, Kubernetes, ECS, Cloud Run) de connaître l'état réel de santé du service et de réagir automatiquement en cas de défaillance.

---

### 1. 🎓 Nouveaux Concepts Introduits

*   **Sonde de santé native Docker (Directive `HEALTHCHECK`) :** Instruction du Dockerfile qui indique au moteur Docker comment tester si l'application s'exécutant dans le conteneur est toujours fonctionnelle. Contrairement à un simple processus en cours (PID 1 actif), la sonde vérifie que l'application répond réellement aux requêtes réseau.
*   **Statut de santé du conteneur (`starting`, `healthy`, `unhealthy`) :** Cycle de vie de l'état de santé géré par le démon Docker. Au démarrage, le conteneur est `starting`. Dès que la première sonde réussit, il passe à `healthy`. Après plusieurs échecs consécutifs, il bascule à `unhealthy`.
*   **Délai de grâce (`--start-period`) :** Période d'initialisation accordée au conteneur au démarrage. Les échecs de la sonde durant cette fenêtre sont ignorés, laissant au serveur Web (Uvicorn) le temps de charger ses dépendances et de commencer à écouter sur le port HTTP.
*   **Commande `curl -f` (Fail Fast HTTP) :** L'option `-f` (ou `--fail`) de `curl` force la commande à renvoyer un code de sortie d'erreur (non-zéro) lorsque le serveur HTTP répond avec un code d'erreur 4xx ou 5xx. Sans ce drapeau, `curl` renverrait un succès même si l'API retourne une erreur 500 Internal Server Error.

---

### 2. 🧠 Prises de Décisions & Choix Techniques

#### Dilemme A : Choix de l'outil d'interrogation pour la sonde (`curl` vs `python -c` vs `wget`)

*   **Option A.1 : Script Python `python -c "import urllib.request..."` (Écartée)**
    *   *Inconvénient :* Démarrer un interpréteur Python à chaque vérification de santé (toutes les 15 secondes) consomme une quantité significative de CPU et de mémoire RAM. Sur des centaines de conteneurs, ce surcoût est considérable.
*   **Option A.2 : Utilisation de `wget` (Écartée)**
    *   *Inconvénient :* Bien que `wget` soit présent dans certaines images Debian de base, il est absent de `python:3.10-slim` et présente une syntaxe moins flexible pour la gestion des codes de retour HTTP en ligne de commande.
*   **Option A.3 : Installation explicite de `curl` dans le stage `runtime` (Retenue)**
    *   *Pourquoi ce choix ?* `curl` est l'standard universel pour les requêtes HTTP dans Linux. Son empreinte mémoire est minime (~3 Mo installés via `apt-get --no-install-recommends`). Il est ultra-rapide, ne nécessite pas de démarrer Python, et l'option `-f` gère parfaitement les codes HTTP d'erreur.

#### Dilemme B : Placement de l'installation de `curl` par rapport à `USER appuser`

*   **Option B.1 : Installer `curl` après `USER appuser` (Écartée)**
    *   *Inconvénient :* `apt-get` nécessite impérativement les privilèges super-utilisateur (`root`). Si `apt-get install curl` est placé après `USER appuser`, la construction de l'image échouera avec une erreur de permission refusée.
*   **Option B.2 : Installer `curl` au début du stage `runtime` avant `USER appuser` (Retenue)**
    *   *Pourquoi ce choix ?* En installant `curl` tant que le stage est sous l'identité `root`, puis en nettoyant les listes APT (`rm -rf /var/lib/apt/lists/*`), on garantit une installation réussie sans résidus temporaires, tout en basculant ensuite en toute sécurité vers `USER appuser`.

#### Dilemme C : Configuration des paramètres de timing (`--interval`, `--timeout`, `--start-period`, `--retries`)

*   **Choix retenu :** `--interval=15s --timeout=5s --start-period=10s --retries=3`
    *   *Justification :*
        *   `--interval=15s` offre un bon compromis entre réactivité face aux pannes et économie de ressources CPU.
        *   `--timeout=5s` évite de bloquer la sonde si le serveur est ralenti.
        *   `--start-period=10s` laisse 10 secondes à Uvicorn pour démarrer proprement.
        *   `--retries=3` empêche les fausses alarmes causées par un pic temporaire de charge (il faut 3 échecs consécutifs pour passer `unhealthy`).

---

### 3. 🛠️ Implémentation & Auto-Documentation

#### Extraits du Dockerfile : [Dockerfile](file:///home/michael/Code/ai-engineering/projets/AIPE_Framework/Dockerfile)

```dockerfile
# Installation minimale de curl dans le stage runtime (en tant que root)
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# ... [création appuser, COPY --chown, USER appuser, EXPOSE 8000] ...

# Sonde de surveillance de santé native Docker
HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

#### Tests de validation du HEALTHCHECK : [test_dockerfile.py](file:///home/michael/Code/ai-engineering/projets/AIPE_Framework/tests/test_dockerfile.py)

```python
def test_dockerfile_has_healthcheck() -> None:
    """Vérifie la présence et la configuration de l'instruction HEALTHCHECK."""
    content = (PROJECT_DIR / "Dockerfile").read_text(encoding="utf-8")
    assert "HEALTHCHECK" in content
    assert "curl" in content and "/health" in content
    assert "--interval=15s" in content
    assert "--timeout=5s" in content
    assert "--start-period=10s" in content
    assert "--retries=3" in content

def test_dockerfile_runtime_has_curl() -> None:
    """Vérifie l'installation de curl dans le stage runtime."""
    runtime_content = content[content.find("AS runtime"):]
    assert "apt-get" in runtime_content and "curl" in runtime_content

def test_dockerfile_curl_before_user() -> None:
    """Vérifie que curl est installé avant le basculement vers appuser."""
    runtime_content = content[content.find("AS runtime"):]
    assert runtime_content.find("RUN apt-get update") < runtime_content.find("USER appuser\n")
```

---

### 4. 📌 Bilan du Jour

1.  **Directive `HEALTHCHECK` intégrée** dans le `Dockerfile` interrogeant l'API `/health` toutes les 15s via `curl -f http://localhost:8000/health || exit 1`.
2.  **Installation ultra-légère de `curl`** dans le stage `runtime` avec nettoyage du cache APT (`--no-install-recommends`, `rm -rf /var/lib/apt/lists/*`).
3.  **3 nouveaux tests de validation** ajoutés à `tests/test_dockerfile.py` (total de 15/15 tests au vert).
4.  **Conformité orchestration** validée : statut `(healthy)` automatiquement géré par le démon Docker.
