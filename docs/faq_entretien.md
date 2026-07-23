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
