# 📌 Séance 2.1 : Configuration de Pre-commit & detect-secrets
**Date :** 23 Juillet 2026

L'objectif de cette séance est d'installer des barrières de sécurité et d'automatisation de formatage de code au plus près du développeur (git hooks). Nous mettons en œuvre `detect-secrets` de Yelp pour empêcher de manière proactive toute fuite de clés d'API (comme OpenAI, Gemini, ou AWS) dans l'historique Git.

---

### 1. 🎓 Nouveaux Concepts Introduits

*   **Hook Pre-commit :** Script s'exécutant automatiquement lors de la commande `git commit`. Si un hook échoue (comme la détection d'une clé API en clair), le commit est bloqué localement, obligeant le développeur à corriger le problème avant d'enregistrer le code.
*   **Security Baseline (`.secrets.baseline`) :** Fichier JSON généré contenant l'empreinte cryptographique des secrets existants ou des faux secrets autorisés (mocks) du projet, permettant à `detect-secrets` de ne signaler que les nouveaux secrets réels introduits par mégarde.
*   **Nettoyage de fin de ligne (trailing-whitespace / end-of-file-fixer) :** Outils de formatage passifs assurant la propreté du dépôt en retirant les espaces inutiles en fin de lignes et en s'assurant que chaque fichier se termine par un retour à la ligne unique.

---

### 2. 🧠 Prises de Décisions & Choix Techniques

#### Dilemme A : Choix de la phase de détection des secrets
*   **Option A.1 : Validation uniquement dans le pipeline CI/CD (GitHub Actions / GitLab CI)**
    *   *Inconvénient :* Trop tard. Si le secret est poussé sur le dépôt distant, il est compromis et visible dans l'historique Git, obligeant à révoquer la clé immédiatement et à purger l'historique Git (ce qui est lourd).
*   **Option A.2 : Validation locale pre-commit (Retenue)**
    *   *Pourquoi ce choix ?* Intercepte l'erreur sur la machine du développeur *avant* la création physique du commit. La clé ne rentre jamais dans l'historique Git local.

#### Dilemme B : Gestion des faux positifs (Mocks et fausses clés de test)
*   **Option B.1 : Désactiver le hook de détection de secrets**
    *   *Inconvénient :* Risque critique de sécurité.
*   **Option B.2 : Utilisation d'un fichier Baseline (`.secrets.baseline`) (Retenue)**
    *   *Pourquoi ce choix ?* Permet de scanner le projet une première fois et de figer les chaînes de caractères existantes (comme des clés de test bidon). Toute nouvelle clé API réelle sera interceptée, mais les mocks de tests déclarés ne bloqueront pas le travail.

---

### 3. 🛠️ Implémentation & Auto-Documentation

La configuration a été implémentée par :
1.  La création du fichier [`.pre-commit-config.yaml`](file:///home/michael/Code/job/projets/AIPE_Framework/.pre-commit-config.yaml) déclarant les hooks.
2.  La génération de la baseline initiale.
3.  L'installation du hook dans les hooks Git de travail locaux.

#### Extrait de configuration `.pre-commit-config.yaml` :
```yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks:
      - id: detect-secrets
        name: Détection passive des secrets et clés d'API
        args: ['--baseline', '.secrets.baseline']
```

#### Commandes de validation exécutées :
```bash
# Générer la baseline de secrets
poetry run detect-secrets scan > .secrets.baseline

# Installer le hook dans git
poetry run pre-commit install

# Lancer la validation sur tous les fichiers manuellement
poetry run pre-commit run --all-files
```
*Critère de succès :* Le lancement de la commande pre-commit doit retourner un statut global vert `Passed` sur l'ensemble des fichiers analysés.

---

### 4. 📌 Bilan du Jour

1.  **Création du fichier de configuration pre-commit** à la racine.
2.  **Génération de la baseline de sécurité** `.secrets.baseline`.
3.  **Installation physique du hook Git local** dans `.git/hooks/pre-commit`.
4.  **Ajout de la suite de tests de validation pre-commit** dans l'outil QA du dashboard.
