# 📌 Séance 1.2 : Configuration locale de l'environnement virtuel (.venv)
**Date :** 23 Juillet 2026

L'objectif de cette séance est d'ancrer l'environnement virtuel au sein même du dossier du projet. Cette configuration assure une intégration instantanée et transparente avec les IDE modernes (comme VSCode) et simplifie grandement l'automatisation locale.

---

### 1. 🎓 Nouveaux Concepts Introduits

*   **Isolation Hermétique en Projet (`in-project`) :** Technique de configuration de Poetry forçant la création de l'environnement virtuel dans un dossier local nommé `.venv` à la racine, plutôt que dans le dossier de cache global de l'utilisateur.
*   **Intégration IDE native :** Détection automatique de l'interprète de code Python par l'IDE (comme VSCode, PyCharm) sans nécessiter de pointage manuel fastidieux.
*   **Git Ignoring :** Déclaration de non-suivi de fichiers de dépendances. Étant donné que le dossier `.venv` contient des binaires et chemins absolus propres au système hôte (Linux, macOS, Windows), il ne doit jamais être commité sous peine de casser le projet chez les autres développeurs.

---

### 2. 🧠 Prises de Décisions & Choix Techniques

#### Dilemme A : Localisation physique de l'environnement virtuel
*   **Option A.1 : Dossier de cache global de l'utilisateur (`~/.cache/pypoetry/virtualenvs`)**
    *   *Inconvénient :* Difficile d'accès pour les scripts locaux et les outils d'IHM de tests. Les IDE peinent à l'associer automatiquement au projet sans configuration globale.
*   **Option A.2 : Dossier local à la racine (`.venv/`) (Retenue)**
    *   *Pourquoi ce choix ?* Offre un chemin d'accès prédictible (`.venv/bin/python`), simplifie la recherche de dépendances et assure la détection automatique de l'environnement de développement par VSCode dès l'ouverture du projet.

#### Dilemme B : Exclusion Git
*   **Option B.1 : Ajout de la commande de configuration globale de Poetry dans le README**
    *   *Pourquoi ce choix ?* Permet d'assurer que tout développeur clonant le projet configure son Poetry local de la même façon.
*   **Option B.2 : Fichier `.gitignore` rigoureux (Retenue)**
    *   *Pourquoi ce choix ?* Obligatoire pour éviter toute pollution accidentelle du dépôt avec des gigaoctets de binaires système.

---

### 3. 🛠️ Implémentation & Auto-Documentation

La configuration a été implémentée localement par :
1.  Le paramétrage de Poetry : `poetry config virtualenvs.in-project true`
2.  L'exclusion du répertoire `.venv/` dans le fichier `.gitignore`.

#### Configuration `.gitignore` :
```text
# Isolation de l'environnement virtuel Poetry local
.venv/
```

#### Commandes de validation à exécuter localement :
```bash
# Vérifier la présence physique du dossier .venv
ls -la .venv

# Vérifier si le dossier est bien ignoré par Git
git check-ignore .venv/
```
*Critère de succès :* La commande `git check-ignore` doit retourner `.venv/` (ce qui confirme que Git l'ignore correctement).

---

### 4. 📌 Bilan du Jour

1.  **Configuration locale de Poetry** pour forcer l'environnement virtuel dans la racine.
2.  **Création physique du répertoire `.venv/`** à la racine de `projets/AIPE_Framework/`.
3.  **Mise en place du fichier `.gitignore`** excluant le dossier `.venv` et les caches Python.
