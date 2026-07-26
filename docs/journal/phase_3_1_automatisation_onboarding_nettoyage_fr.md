# 📌 Séance 3.1 : Automatisation de l'Onboarding et du Nettoyage (Makefile)
**Date :** 23 Juillet 2026

L'objectif de cette séance est d'implémenter les cibles `make install` et `make clean` du Makefile. Ces cibles automatisent la mise en place de l'environnement virtuel et l'installation des outils de qualité d'une part, et purgent l'ensemble des fichiers de cache d'autre part. Cela permet d'avoir un état de dépôt reproductible et propre.

---

### 1. 🎓 Nouveaux Concepts Introduits

*   **POSIX Make (Interface Abstraite) :** Outil historique permettant d'ordonner et d'automatiser des scripts via un fichier de configuration unique (`Makefile`). Il agit comme une couche d'abstraction masquant la complexité des outils sous-jacents.
*   **Zero-Setup Friction (Onboarding Développeur) :** Métrique mesurant le temps nécessaire à un nouveau développeur pour cloner le projet, installer l'intégralité des dépendances (virtualenv, linters, pre-commit hooks) et démarrer son travail. L'objectif industriel est de réduire ce temps sous la barre des 5 minutes.
*   **Nettoyage Récursif des Caches compilés :** Élimination programmatique des répertoires `__pycache__` et fichiers `*.pyc` générés par l'interpréteur Python lors de l'exécution, prévenant ainsi toute anomalie liée à des imports de fichiers obsolètes ou fantômes.

---

### 2. 🧠 Prises de Décisions & Choix Techniques

#### Dilemme A : Choix de la méthode d'onboarding
*   **Option A.1 : Guide markdown détaillé listant toutes les commandes (poetry install, pre-commit install, etc.)**
    *   *Inconvénient :* Risque d'erreur humaine élevée. Les versions de pre-commit ou les syntaxes peuvent varier selon l'OS du développeur, augmentant le support nécessaire lors de l'accueil.
*   **Option A.2 : Encapsuler les étapes dans une commande unique `make install` (Retenue)**
    *   *Pourquoi ce choix ?* Offre une expérience utilisateur unifiée. Le développeur n'a qu'à retenir `make install`. Make se charge d'installer les dépendances Poetry et d'injecter physiquement les hooks de commit locaux de manière déterministe.

#### Dilemme B : Outil de nettoyage (clean)
*   **Option B.1 : Script Python personnalisé (`clean.py`)**
    *   *Inconvénient :* Surcharge inutile. Lancer un interpréteur Python pour supprimer des dossiers de cache est plus lent que des commandes système natives.
*   **Option B.2 : Utilisation des commandes shell standard POSIX (find, rm) (Retenue)**
    *   *Pourquoi ce choix ?* Efficacité maximale. L'utilisation combinée de `rm -rf` et de `find . -type d -name "__pycache__" -exec rm -rf {} +` s'exécute de façon quasi-instantanée (en quelques millisecondes) sans aucune dépendance externe.

---

### 3. 🛠️ Implémentation & Auto-Documentation

La configuration a été implémentée dans le fichier [`Makefile`](file:///home/michael/Code/job/projets/AIPE_Framework/Makefile) :

#### Extrait du Makefile :
```makefile
install:
	poetry install
	poetry run pre-commit install

clean:
	@echo "Nettoyage des répertoires de cache..."
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
```

#### Commandes de validation exécutées :
```bash
# Simuler un nettoyage de tous les caches
make clean

# Réinstaller proprement
make install
```
*Critère de succès :* La commande `make clean` doit s'exécuter avec succès en renvoyant un statut vert, et aucun fichier de cache ne doit persister.

---

### 4. 📌 Bilan du Jour

1.  **Mise en place de la cible `install`** orchestrant Poetry et pre-commit.
2.  **Mise en place de la cible `clean`** nettoyant récursivement caches et artefacts de compilation.
3.  **Vérification de la conformité de l'onboarding** en testant la reconstruction de l'environnement de zéro.
