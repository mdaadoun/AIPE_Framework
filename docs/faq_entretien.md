# ❓ FAQ d'Entretien Technique : Ingénierie Produit IA (AIPE)

Cette foire aux questions présente les questions d'entretien classiques posées par les recruteurs techniques concernant les architectures et choix d'outils appliqués dans ce blueprint.

---

### Q1. Pourquoi préférez-vous Poetry à un fichier `requirements.txt` classique ?
*   **Réponse :** Le fichier `requirements.txt` traditionnel ne liste que les dépendances directes, ce qui peut conduire à des dérives de version lors de l'installation de dépendances transitives (sous-dépendances). De plus, il n'isole pas nativement l'environnement.
*   **Avantages de Poetry :**
    1.  **Résolution déterministe :** Il calcule l'arbre complet des dépendances et verrouille les versions exactes dans le fichier `poetry.lock`.
    2.  **Séparation des environnements :** Il distingue nativement les paquets nécessaires à la production (ex: FastAPI) de ceux du développement (ex: Ruff, Pytest), évitant d'alourdir le conteneur final.
    3.  **Gestion de projet unifiée :** Il s'occupe à la fois du packaging, des scripts et des dépendances dans un fichier unique `pyproject.toml`.

---

### Q2. Quel est l'avantage d'intégrer Ruff plutôt que la combinaison Black, Flake8, isort et autoflake ?
*   **Réponse :** Ruff regroupe toutes ces fonctionnalités en un seul outil ultra-rapide écrit en Rust.
*   **Avantages :**
    1.  **Vitesse :** Ruff est 10 à 100 fois plus rapide que les outils originaux. Il analyse et formate un projet entier en quelques millisecondes.
    2.  **Maintenance simplifiée :** Une seule dépendance à déclarer et une seule section de configuration dans le `pyproject.toml` au lieu de 4 ou 5 fichiers séparés.
    3.  **Remplacement transparent :** Ruff intègre son propre formateur compatible à 99% avec Black, ce qui simplifie le pipeline de validation.

---

### Q3. Pourquoi imposer Mypy en mode strict (`strict = true`) ?
*   **Réponse :** Le mode strict de Mypy impose un contrat rigoureux au code en Python. Il force l'annotation explicite de toutes les fonctions et interdit le type `Any` implicite.
*   **Intérêts :**
    1.  **Sécurité :** Il élimine la majorité des bugs de type en production (ex. variables valant parfois `None` provoquant des `AttributeError`).
    2.  **Documentation active :** Les types agissent comme une documentation vivante, validée en temps réel par le compilateur statique.
    3.  **Refactoring serein :** Modifier une structure de données complexe est sécurisé car Mypy pointe immédiatement toutes les lignes du projet impactées.

---

### Q4. Comment justifiez-vous la mise en place de `detect-secrets` en pre-commit plutôt que de simples vérifications dans la CI/CD globale ?
*   **Réponse :** Si une clé d'API (comme `sk-proj-...` d'OpenAI) est poussée sur GitHub, elle est compromise même si le commit est supprimé ou réécrit ultérieurement, car elle reste stockée dans l'historique Git et les plateformes de backup.
*   **Justification :** Le hook pre-commit s'exécute localement *avant* la création physique du commit. Si un secret est détecté, le commit est intercepté sur la machine du développeur, empêchant le secret d'entrer dans l'historique local et de fuiter sur le cloud.

---

### Q5. Pourquoi utiliser un Dockerfile multi-stage ? Est-ce indispensable ?
*   **Réponse :** Oui, c'est indispensable pour concilier sécurité et performance en production.
*   **Justification :**
    1.  **Réduction du poids :** L'image finale ne contient pas le gestionnaire Poetry ni les compilateurs système nécessaires au build de certains paquets Python (ex. `gcc`). L'image runtime passe ainsi de ~1 Go à moins de 250 Mo.
    2.  **Sécurité :** Moins d'outils et de bibliothèques installées signifie une surface d'attaque beaucoup plus restreinte (moins de vulnérabilités CVE dans les paquets système).

---

### Q6. À quoi sert le Makefile dans votre architecture ? Est-ce encore utile à l'ère des conteneurs ?
*   **Réponse :** Le Makefile offre une couche d'abstraction essentielle pour l'expérience développeur (DX).
*   **Justification :** Au lieu de demander à un développeur (ou à un pipeline de CI) de se souvenir des commandes exactes (`poetry run pytest`, `poetry run ruff check`, etc.), le Makefile unifie le cycle de vie sous forme de commandes universelles (`make install`, `make test`, `make lint`). C'est la promesse d'un temps de prise en main inférieur à 5 minutes pour tout nouveau collaborateur.

---

### Q7. Pourquoi forcer la configuration de l'environnement virtuel localement (in-project) plutôt que d'utiliser l'emplacement de cache par défaut de Poetry ?
*   **Réponse :** Forcer la création du dossier `.venv` à la racine du projet présente trois avantages industriels clés :
    1.  **Intégration IDE native :** Les éditeurs comme VSCode ou PyCharm détectent automatiquement l'environnement Python dès l'ouverture du dossier, sans action manuelle du développeur.
    2.  **Automatisation prédictible :** Les scripts locaux et serveurs de test (comme notre tableau de bord de QA) peuvent appeler l'interpréteur Python directement via un chemin relatif standardisé (`.venv/bin/python`).
    3.  **Nettoyage simple :** Supprimer l'environnement virtuel pour le reconstruire sainement se résume à un simple `rm -rf .venv`, sans devoir chercher dans les répertoires cachés du système de l'utilisateur.

---

### Q8. Comment testez-vous automatiquement l'efficacité de vos barrières de qualité (gatekeeping hooks) ?
*   **Réponse :** Nous n'attendons pas qu'un développeur commette une erreur pour vérifier si les outils fonctionnent. Nous avons automatisé cette validation via une suite de tests unitaires dédiés (`tests/test_gatekeeping.py`).
*   **Justification :** Ces tests créent dynamiquement des fichiers Python temporaires volontairement erronés (contenant une clé API en clair, du code mal formaté ou des signatures non annotées), puis exécutent les validateurs (`detect-secrets`, `ruff`, `mypy`) en analysant leurs codes de retour et sorties. Cela permet de garantir qu'une dérive de configuration ne désactivera pas silencieusement nos mécanismes de sécurité.

---

### Q9. Pourquoi ignorez-vous la règle Ruff E501 (longueur de ligne) dans ce projet ?
*   **Réponse :** Bien que la longueur de ligne standard de 88 caractères ( PEP 8 / style Black) soit idéale pour la lisibilité générale du code Python, ce framework intègre un dashboard interactif local écrit avec des templates et des chaînes de caractères HTML volumineuses incorporées.
*   **Justification :** Limiter de manière rigide ces fichiers à 88 caractères par ligne obligerait à découper artificiellement les blocs HTML ou les requêtes SQL complexes, ce qui nuirait grandement à leur lisibilité et à leur maintenance. Nous avons donc choisi de désactiver la règle `E501` tout en maintenant le niveau maximal de rigueur sur le style (E), la correction logique (F), le tri des imports (I) et les bonnes pratiques (B).

---

### Q10. Qu'est-ce que la directive `.PHONY` dans un Makefile et pourquoi est-elle cruciale dans ce projet ?
*   **Réponse :** Par défaut, `make` cherche à faire correspondre chaque cible (comme `install` ou `test`) à un fichier physique sur le disque. Si un fichier ou dossier du même nom existe et est à jour, Make considère qu'il n'a rien à faire.
*   **Justification :** Dans notre projet, nous possédons un dossier physique nommé `tests/`. Sans la directive `.PHONY: test`, exécuter `make test` renverrait l'avertissement `make: 'test' is up to date` et n'exécuterait jamais nos tests unitaires. Utiliser `.PHONY` force Make à ignorer la présence de fichiers ou dossiers homonymes et à toujours exécuter la commande.

---

### Q11. Comment validez-vous la robustesse et la stabilité de votre interface de commande (Makefile) ?
*   **Réponse :** Nous traitons notre outillage d'infrastructure avec la même rigueur que le code de production. Nous avons écrit une suite de tests unitaires dédiée dans `tests/test_makefile.py` pour valider l'interface.
*   **Justification :** Ces tests automatisent l'exécution de `make help`, `make clean` et `make lint` via des sous-processus et s'assurent que :
    1. L'aide récapitulative affiche toutes les cibles attendues.
    2. La cible `clean` supprime physiquement les caches locaux et fichiers de compilation temporaires.
    3. Les linters (`lint`) s'exécutent correctement sans lever de régression de configuration.

---

### Q12. Pourquoi avoir choisi FastAPI plutôt que Flask ou Django pour l'API de ce projet ?
*   **Réponse :** FastAPI est particulièrement adapté pour les architectures de services d'IA modernes grâce à sa prise en charge native de l'asynchronisme (ASGI) et de Pydantic.
*   **Justification :** Contrairement à WSGI (Flask/Django), ASGI permet de maintenir efficacement des connexions persistantes, ce qui est nécessaire pour diffuser en continu (streaming) les réponses de modèles d'IA. De plus, la validation automatique des schémas de typage à l'exécution avec Pydantic et l'auto-génération de la documentation OpenAPI (/docs) facilitent l'intégration par les développeurs frontend.

---

### Q13. Comment fonctionne le `TestClient` de FastAPI et quel est son intérêt pour les tests ?
*   **Réponse :** Le `TestClient` simule de vraies requêtes HTTP en s'appuyant sur la bibliothèque `httpx` sans avoir besoin d'allouer de port réseau ou de démarrer un serveur Web complet.
*   **Justification :** Il s'interface directement avec l'application FastAPI en invoquant son gestionnaire ASGI en boucle locale. Cela permet d'exécuter des tests d'intégration complets des routes, des schémas et de la sérialisation de façon extrêmement rapide (en quelques millisecondes), garantissant une boucle de feedback QA continue et fluide.

---

### Q14. Pourquoi avoir modularisé la structure de l'API (core, schemas, api/routes) plutôt que de laisser le code de base dans un fichier `main.py` unique ?
*   **Réponse :** Bien qu'un fichier unique soit plus rapide à écrire pour un PoC rudimentaire, il pose de graves problèmes de scalabilité et de maintenance à mesure que le projet grandit.
*   **Justification :**
    1. **Séparation des préoccupations (SoC) :** Isoler la configuration (`core`), la validation des données (`schemas`) et la définition des endpoints (`api/routes`) permet de diviser la complexité. Chaque fichier a une responsabilité unique.
    2. **Parallélisation du travail :** Plusieurs développeurs peuvent travailler simultanément sur des routes ou des modèles de données différents sans provoquer de conflits Git majeurs.
    3. **Maintenance et onboarding :** Un développeur junior identifie immédiatement où placer un nouveau schéma ou une nouvelle route, et le point d'entrée `main.py` reste propre et lisible en ne faisant qu'orchestrer et brancher les modules.

---

### Q15. Comment gérez-vous la validation de champs et les dépréciations dans les modèles Pydantic entre les versions V1 et V2 (par exemple, le mot-clé `example`) ?
*   **Réponse :** Pydantic V2 a introduit des changements majeurs de structure pour améliorer les performances (moteur écrit en Rust) et clarifier la spécification OpenAPI. Le mot-clé `example` passé directement dans `Field` a été déprécié.
*   **Justification :** Pour être compatible avec Pydantic V2 et éviter les avertissements d'exécution (`PydanticDeprecatedSince20`), nous utilisons le paramètre `examples` (qui accepte une liste d'exemples) au lieu de `example`. Alternativement, on peut déclarer les exemples via la structure `json_schema_extra={"example": "..."}`. Cela garantit que la génération Swagger reste propre tout en assurant un typage à l'épreuve du temps (future-proof) pour les migrations vers Pydantic V3.

---

### Q16. Quelle est la différence entre une sonde de démarrage (Startup), de vie (Liveness) et de disponibilité (Readiness), et comment votre endpoint s'intègre-t-il dans cette logique ?
*   **Réponse :**
    1. **Startup Probe :** Vérifie si l'application a démarré (crucial pour les applications lentes à charger).
    2. **Liveness Probe :** Indique si le conteneur est vivant. Si la route répond en échec, l'orchestrateur redémarre le conteneur.
    3. **Readiness Probe :** Indique si l'application est prête à traiter du trafic. Si elle échoue, le trafic réseau est redirigé vers d'autres conteneurs sains, sans redémarrer le conteneur.
*   **Justification :** Notre endpoint `/health` fournit le socle pour ces trois types de sondes. Dans une architecture avancée, la readiness probe pourrait interroger des chemins dépendants pour s'assurer que la base de données est accessible, tandis que la liveness probe reste ultra-légère pour simplement attester que le serveur ASGI traite les requêtes sans bloquer.

---

### Q17. Pourquoi est-il important de valider la réponse d'un endpoint de Healthcheck via un schéma strict (ex: Pydantic) plutôt que de simplement renvoyer un dictionnaire Python standard ?
*   **Réponse :** Renvoyer un simple dictionnaire `dict` en Python n'offre aucune garantie de structure à l'exécution ni au moment de la compilation.
*   **Justification :**
    1. **Détection des régressions :** Si un développeur modifie la structure de données renvoyée par erreur, Pydantic bloque la réponse HTTP à l'exécution en levant une erreur de validation, empêchant la production de données invalides de casser les clients consommateurs.
    2. **Génération OpenAPI :** Pydantic exporte automatiquement les types exacts du schéma de réponse dans le fichier OpenAPI JSON. Cela permet aux outils de supervision de valider automatiquement les types sans codage manuel.
    3. **Sécurité opérationnelle :** Cela formalise un contrat d'interface inviolable avec le reste du système (monitoring, passerelles d'API).
