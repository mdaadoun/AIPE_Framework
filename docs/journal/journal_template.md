# 📌 Gabarit d'Article de Journal (Template)

> [!IMPORTANT]
> **Règle de nommage du fichier :** Le fichier de chaque séance de journal doit être nommé en minuscules, au format *snake_case* suivant :
> `phase_[numero_phase]_[numero_etape]_[description_courte].md`
> *Exemple : `phase_1_2_setup_cli.md` ou `phase_2_1_aplatissement.md`*

---

# 📌 Séance [Numéro] : [Titre descriptif de la séance]
**Date :** [Jour] [Mois] 2026

*Décrire ici en un paragraphe court (2 à 4 lignes) le but principal de la séance de développement, les problématiques abordées et le périmètre ciblé.*

---

### 1. 🎓 Nouveaux Concepts Introduits

*   **[Concept 1] :** [Définition claire et vulgarisée du concept technique ou méthodologique. Exemple : Poetry, linter Ruff, typage strict Mypy, pre-commit, detect-secrets, Docker multi-stage.]
*   **[Concept 2] :** [Définition du second concept.]
*   **[Concept 3] :** [Définition du troisième concept.]

---

### 2. 🧠 Prises de Décisions & Choix Techniques

*Cette section documente le processus de réflexion (Architecture Decision Records - ADR) ayant mené aux choix technologiques.*

#### [Dilemme A : Titre du dilemme (ex. Choix du linter de code)]
*   **Option A.1 : [Nom de l'option 1]**
    *   *Avantage/Inconvénient :* [Brève analyse critique de cette option.]
*   **Option A.2 : [Nom de l'option 2 (Retenue)]**
    *   *Pourquoi ce choix ?* [Expliquer précisément le raisonnement technique et métier de cette décision (gain de vitesse, sécurité, maintenabilité).]

#### [Dilemme B : Autre dilemme (ex. Configuration de pre-commit)]
*   **Option B.1 : [Option 1 (Retenue)]**
    *   *Pourquoi ce choix ?* [Justification.]
*   **Option B.2 : [Option 2 (Écartée)]**
    *   *Pourquoi ce choix ?* [Justification.]

---

### 3. 🛠️ Implémentation & Auto-Documentation

*Décrire ici les détails d'implémentation, la structure de code créée ou les scripts configurés. Toujours inclure les commandes système ou de validation correspondantes.*

#### Exemple de configuration ou de code :
```toml
# Bloc de code illustrant la séance (ex. pyproject.toml, Makefile, Dockerfile...)
[tool.poetry]
name = "exemple"
version = "0.1.0"
```

#### Commandes de validation à exécuter localement :
```bash
# Exemple de commande de test, lint ou démarrage
make lint
```
*Expliquer brièvement la sortie attendue de cette commande ou le critère de succès (ex. "La commande doit renvoyer un statut vert sans erreur en moins de 2 secondes").*

---

### 4. 📌 Bilan du Jour

*Synthétiser ici les livrables concrets validés à l'issue de la séance sous forme de liste à puces :*
1.  **[Livrable 1]** (ex. Initialisation de Poetry et isolation locale du `.venv`).
2.  **[Livrable 2]** (ex. Intégration du hook pre-commit `detect-secrets`).
3.  **[Livrable 3]** (ex. Automatisation des commandes via le `Makefile`).
