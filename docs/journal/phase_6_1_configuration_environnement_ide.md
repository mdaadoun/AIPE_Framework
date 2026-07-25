# 📌 Séance 16 : Configuration de l'Environnement IDE (Phase 6 - Étape 6.1)
**Date :** 25 Juillet 2026

Première étape de la phase 6 « Intégration IDE & Validation Finale ». L'objectif est de configurer VSCode pour que chaque sauvegarde d'un fichier Python applique automatiquement le formatage Ruff, le tri des imports et les corrections de style — exactement comme le ferait la chaîne pre-commit ou `make lint`, mais en temps réel dans l'éditeur. Cela referme la boucle de feedback : le développeur voit instantanément les corrections sans attendre le commit.

---

### 1. 🎓 Nouveaux Concepts Introduits

*   **Format-on-Save (Formatage à la Sauvegarde) :** Fonctionnalité de l'éditeur de code qui déclenche automatiquement le formateur configuré (ici Ruff) à chaque `Ctrl+S`. Le fichier est réécrit sur le disque déjà proprement formaté, éliminant le décalage entre ce que le développeur écrit et ce que la CI exige.
*   **JSONC (JSON with Comments) :** Variante du format JSON standard qui autorise les commentaires `//` et `/* */`. C'est le format utilisé par VSCode pour ses fichiers de configuration (`.vscode/settings.json`, `.vscode/extensions.json`). Le JSON classique de la spécification RFC 8259 interdit les commentaires.
*   **Code Actions on Save :** Mécanisme avancé de VSCode qui permet d'exécuter des « actions de code » automatiquement au moment de la sauvegarde. Contrairement au simple formatage (qui n'ajuste que l'indentation et les sauts de ligne), les Code Actions peuvent corriger le code lui-même : supprimer les imports inutilisés, réorganiser les imports, appliquer des quick-fixes.
*   **Workspace Recommendations (extensions.json) :** Fichier `.vscode/extensions.json` versionné dans Git qui déclare les extensions indispensables au projet. Lorsqu'un développeur ouvre le dossier, VSCode affiche automatiquement une notification proposant d'installer les extensions manquantes. Cela garantit l'uniformité de l'outillage dans l'équipe.

---

### 2. 🧠 Prises de Décisions & Choix Techniques

#### Dilemme A : Faut-il versionner le dossier `.vscode/` dans Git ?

*   **Option A.1 : Ignorer `.vscode/` via `.gitignore` (Écartée)**
    *   *Inconvénient :* Chaque développeur devrait configurer manuellement son VSCode. Le risque de désalignement est élevé : un membre de l'équipe pourrait utiliser autopep8 au lieu de Ruff, produisant des commits avec un formatage différent. Cela génère du bruit dans les diffs Git et des conflits de merge inutiles.
*   **Option A.2 : Versionner `.vscode/settings.json` et `.vscode/extensions.json` (Retenue)**
    *   *Pourquoi ce choix ?* En versionnant ces fichiers, la configuration de l'éditeur est traitée comme du code d'infrastructure (Infrastructure as Code). Tout nouveau développeur qui clone le projet hérite automatiquement du bon formateur, des bons réglages et des bonnes recommandations d'extensions. C'est un pilier du « Zero-Setup Friction » ciblé par notre roadmap.

#### Dilemme B : Choix du formateur VSCode pour Python (Ruff vs Black vs autopep8)

*   **Option B.1 : Utiliser l'extension Black (Écartée)**
    *   *Inconvénient :* Cela obligerait à maintenir deux outils de formatage séparés — Black pour l'éditeur et Ruff pour le pre-commit — avec un risque de désynchronisation des résultats. De plus, Black est écrit en Python et est ~100x plus lent que Ruff.
*   **Option B.2 : Utiliser l'extension officielle Ruff `charliermarsh.ruff` (Retenue)**
    *   *Pourquoi ce choix ?* Le formateur intégré de Ruff est compatible à 99% avec le style Black et est déjà configuré dans notre `pyproject.toml`. Utiliser le même outil dans l'éditeur et dans les hooks pre-commit garantit un résultat identique, éliminant tout risque de « ping-pong de formatage » entre deux outils qui se corrigent mutuellement.

#### Dilemme C : Valeur de `editor.codeActionsOnSave` — `"explicit"` vs `"always"` vs `true`

*   **Option C.1 : Utiliser `"always"` ou `true` (Écartée)**
    *   *Inconvénient :* Le mode `"always"` déclenche les actions y compris lors des sauvegardes automatiques (auto-save, fenêtre perdant le focus), ce qui peut provoquer des modifications inattendues dans des fichiers que le développeur n'a pas intentionnellement sauvegardés.
*   **Option C.2 : Utiliser `"explicit"` (Retenue)**
    *   *Pourquoi ce choix ?* Le mode `"explicit"` n'exécute les Code Actions que lors d'une sauvegarde manuelle délibérée (`Ctrl+S`). Le développeur garde le contrôle total sur le moment où les corrections automatiques sont appliquées, évitant les surprises dans un workflow avec auto-save activé.

---

### 3. 🛠️ Implémentation & Auto-Documentation

#### Fichier de configuration principal : [.vscode/settings.json](file:///home/michael/Code/ai-engineering/projets/AIPE_Framework/.vscode/settings.json)

```json
{
    // Interpréteur Python local (environnement virtuel Poetry)
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",

    // Ruff comme formateur exclusif pour Python + formatage à la sauvegarde
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.fixAll": "explicit",
            "source.organizeImports": "explicit"
        }
    },

    // Alignement de la longueur de ligne avec pyproject.toml
    "ruff.lineLength": 88,
    "ruff.lint.enable": true,

    // Désactivation des linters concurrents
    "python.linting.enabled": false,

    // Cohérence avec les hooks pre-commit
    "files.insertFinalNewline": true,
    "files.trimTrailingWhitespace": true
}
```

#### Fichier de recommandations d'extensions : [.vscode/extensions.json](file:///home/michael/Code/ai-engineering/projets/AIPE_Framework/.vscode/extensions.json)

```json
{
    "recommendations": [
        "charliermarsh.ruff",
        "ms-python.python"
    ]
}
```

#### Suite de tests de validation : [tests/test_vscode_settings.py](file:///home/michael/Code/ai-engineering/projets/AIPE_Framework/tests/test_vscode_settings.py)

```python
# 13 tests organisés en 4 sections :
# Section 1 : Existence et validité syntaxique (4 tests)
# Section 2 : Paramètres critiques du formatage (5 tests)
# Section 3 : Cohérence avec les hooks pre-commit (2 tests)
# Section 4 : Extensions recommandées (2 tests)

def test_settings_has_correct_line_length() -> None:
    """Vérifie la cohérence de la longueur de ligne entre VSCode et pyproject.toml."""
    # Ce test croise les valeurs de settings.json et pyproject.toml
    # pour détecter tout désalignement de configuration.
```

#### Commandes de validation à exécuter localement :
```bash
# Exécuter uniquement les 13 tests de la configuration IDE
make test -- tests/test_vscode_settings.py --no-cov

# Ou directement via le venv :
.venv/bin/python -m pytest tests/test_vscode_settings.py -v --no-cov
```
*La commande doit renvoyer `13 passed` sans aucun échec.*

---

### 4. 📌 Bilan du Jour

1.  **Fichier `.vscode/settings.json` créé** avec formatage automatique à la sauvegarde via Ruff, Code Actions (fixAll + organizeImports), et cohérence avec les hooks pre-commit.
2.  **Fichier `.vscode/extensions.json` créé** recommandant automatiquement les extensions Ruff et Python Microsoft à tout développeur ouvrant le projet.
3.  **13 nouveaux tests de validation** ajoutés dans `tests/test_vscode_settings.py` (existence, syntaxe JSON, paramètres critiques, cohérence pyproject.toml/settings.json, extensions recommandées).
4.  **Boucle de feedback complète** fermée : le développeur voit les corrections de Ruff en temps réel dans l'éditeur, sans attendre le commit Git.
