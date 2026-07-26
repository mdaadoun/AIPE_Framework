# 📌 Séance 5.2 : Sécurisation Non-root du Conteneur Docker
**Date :** 24 Juillet 2026

L'objectif de cette séance est de renforcer la sécurité de l'image Docker de production en appliquant le principe de moindre privilège. Concrètement, on crée un utilisateur système non-privilégié `appuser` (UID 1000) dans le stage `runtime` du Dockerfile et on bascule l'exécution de l'application sous son identité, de sorte que le serveur Uvicorn ne tourne jamais en tant que `root`.

---

### 1. 🎓 Nouveaux Concepts Introduits

*   **Principe de moindre privilège (Least Privilege) :** Principe fondamental de sécurité selon lequel chaque composant d'un système (processus, utilisateur, programme) ne doit disposer que des permissions strictement nécessaires à l'accomplissement de sa tâche. Dans Docker, cela signifie exécuter l'application sous un utilisateur non-root. C'est comme donner à un stagiaire les clés des salles dont il a besoin, pas le passe-partout de tout le bâtiment.
*   **Directive USER dans un Dockerfile :** Instruction Docker qui bascule définitivement l'identité sous laquelle s'exécutent toutes les commandes suivantes (`RUN`, `CMD`, `ENTRYPOINT`). Placée après la copie des fichiers, elle constitue le « verrou final » du hardening : le processus principal du conteneur (PID 1) démarre avec les privilèges limités de l'utilisateur spécifié.
*   **Ports privilégiés vs non-privilégiés :** Sur Linux, seul `root` peut ouvrir des ports inférieurs à 1024 (ports privilégiés comme 80 ou 443). Les ports supérieurs à 1024 (comme notre port 8000) sont dits « non-privilégiés » et accessibles à tout utilisateur. Le choix du port 8000 est donc un prérequis technique pour l'exécution en tant que `appuser`.
*   **COPY --chown (Transfert de propriété Docker) :** Option de l'instruction `COPY` qui transfère la propriété des fichiers copiés à un utilisateur et un groupe spécifiques en une seule opération atomique. Cela évite de recourir à un `RUN chown -R` séparé, économisant une couche Docker et le temps de parcours récursif de l'arborescence.

---

### 2. 🧠 Prises de Décisions & Choix Techniques

#### Dilemme A : Création de l'utilisateur via `adduser --system` ou `useradd`

*   **Option A.1 : `useradd` (outil bas niveau) (Écartée)**
    *   *Inconvénient :* `useradd` est l'outil bas niveau de gestion des utilisateurs. Il nécessite davantage de drapeaux explicites (`--system`, `--no-create-home`, `--shell /usr/sbin/nologin`, `--gid`) pour obtenir un résultat sécurisé. Un oubli de drapeau peut créer un répertoire home inutile ou attribuer un shell de connexion exploitable par un attaquant.
*   **Option A.2 : `adduser --system` (outil haut niveau Debian) (Retenue)**
    *   *Pourquoi ce choix ?* `adduser` est le wrapper haut niveau fourni par Debian/Ubuntu avec des défauts sécurisés : pas de shell de connexion, pas de mot de passe, pas de répertoire home (avec `--no-create-home`). La syntaxe est plus lisible et la configuration par défaut est adaptée aux services système. C'est l'outil recommandé par les bonnes pratiques Docker officielles pour les images basées sur Debian.

#### Dilemme B : Transfert de propriété via `--chown` ou via `RUN chown -R`

*   **Option B.1 : `RUN chown -R appuser:appgroup /app` après COPY (Écartée)**
    *   *Inconvénient :* Cette approche crée une couche Docker supplémentaire contenant une copie complète de tous les fichiers modifiés (le changement de métadonnées de propriété invalide la couche précédente). Pour un `.venv` de 150 Mo, cela double la taille de la couche dans l'image. De plus, le parcours récursif (`chown -R`) ajoute du temps de build.
*   **Option B.2 : `COPY --chown=appuser:appgroup` directement sur l'instruction COPY (Retenue)**
    *   *Pourquoi ce choix ?* L'option `--chown` intégrée à `COPY` effectue le transfert de propriété pendant la phase de copie elle-même, en une seule opération atomique. Aucune couche supplémentaire n'est créée, pas de doublon de fichiers, et pas de parcours récursif additionnel. C'est l'approche la plus efficiente en termes de taille d'image et de vitesse de build.

#### Dilemme C : UID fixe (1000) ou UID dynamique attribué par le système

*   **Option C.1 : Laisser le système choisir l'UID (Écartée)**
    *   *Inconvénient :* Un UID dynamique peut varier selon l'image de base et les utilisateurs système déjà créés. En production, les orchestrateurs comme Kubernetes imposent des contraintes de sécurité (`PodSecurityPolicy`, `SecurityContext`) qui exigent souvent un UID ≥ 1000. Un UID dynamique pourrait se retrouver dans la plage des comptes système (< 1000), entraînant un rejet au déploiement.
*   **Option C.2 : Fixer l'UID à 1000 (Retenue)**
    *   *Pourquoi ce choix ?* L'UID 1000 est la convention standard pour le premier utilisateur non-root dans les conteneurs Docker. Fixer cet UID garantit la compatibilité avec les politiques de sécurité d'entreprise, assure la reproductibilité entre les environnements (dev, staging, production), et facilite le débogage (on sait toujours quel UID correspond à `appuser`).

---

### 3. 🛠️ Implémentation & Auto-Documentation

#### Modifications du Dockerfile (stage runtime) : [Dockerfile](file:///home/michael/Code/ai-engineering/projets/AIPE_Framework/Dockerfile)

```dockerfile
# Création du groupe et de l'utilisateur non-privilégié
RUN addgroup --system appgroup \
    && adduser --system --uid 1000 --ingroup appgroup --no-create-home appuser

# Copie avec transfert de propriété (--chown)
COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv
COPY --from=builder --chown=appuser:appgroup /app/src /app/src

# Basculement vers l'utilisateur non-privilégié
USER appuser

EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Tests de validation structurelle : [test_dockerfile.py](file:///home/michael/Code/ai-engineering/projets/AIPE_Framework/tests/test_dockerfile.py)

```python
def test_dockerfile_creates_non_root_user() -> None:
    """Vérifie la création de l'utilisateur et du groupe système."""
    content = (PROJECT_DIR / "Dockerfile").read_text(encoding="utf-8")
    assert "addgroup" in content and "appgroup" in content
    assert "adduser" in content and "appuser" in content
    assert "1000" in content

def test_dockerfile_uses_user_directive() -> None:
    """Vérifie la présence de la directive USER appuser."""
    content = (PROJECT_DIR / "Dockerfile").read_text(encoding="utf-8")
    assert "USER appuser" in content

def test_dockerfile_uses_chown_on_copy() -> None:
    """Vérifie l'utilisation de --chown sur les instructions COPY."""
    content = (PROJECT_DIR / "Dockerfile").read_text(encoding="utf-8")
    assert "--chown=appuser:appgroup" in content

def test_dockerfile_user_after_copy() -> None:
    """Vérifie que USER est placé APRÈS les COPY (ordre critique)."""
    content = (PROJECT_DIR / "Dockerfile").read_text(encoding="utf-8")
    assert content.find("USER appuser") > content.rfind("COPY --from=builder")
```

#### Commandes de validation à exécuter localement :

```bash
# Lancement des tests de validation du Dockerfile (hardening inclus)
poetry run pytest tests/test_dockerfile.py -v --no-cov

# Construction de l'image Docker sécurisée
docker build -t aipe-framework:latest .

# Vérification que le conteneur tourne bien en tant que appuser (et non root)
docker run --rm aipe-framework:latest whoami
# Sortie attendue : appuser

# Inspection de l'UID du processus principal
docker run --rm aipe-framework:latest id
# Sortie attendue : uid=1000(appuser) gid=999(appgroup) groups=999(appgroup)
```
*Les 12 tests pytest doivent tous passer au vert. La commande `whoami` dans le conteneur doit afficher `appuser` et non `root`.*

---

### 4. 📌 Bilan du Jour

1.  **Hardening non-root du Dockerfile** avec création de l'utilisateur système `appuser` (UID 1000) et du groupe `appgroup` via `adduser --system` / `addgroup --system`.
2.  **Transfert de propriété des fichiers** via le flag `--chown=appuser:appgroup` sur les instructions `COPY --from=builder`, évitant une couche Docker supplémentaire.
3.  **Basculement d'identité** avec la directive `USER appuser` placée après les copies et avant `EXPOSE` / `CMD`, garantissant que le processus principal (uvicorn) s'exécute en tant qu'utilisateur non-privilégié.
4.  **Suite de 4 tests de validation** ajoutée à `tests/test_dockerfile.py` vérifiant la création de l'utilisateur, la directive USER, le flag `--chown`, et le bon ordonnancement des instructions.
5.  **Documentation exhaustive** avec commentaires vulgarisés dans le Dockerfile expliquant chaque décision de sécurité.
