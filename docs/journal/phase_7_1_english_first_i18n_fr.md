# 📌 Séance 7.1 : Internationalisation English First (i18n) & Bilinguisme

**Date :** 26 Juillet 2026

Cette séance documente l'évolution majeure du framework AIPE vers une approche **"English First"** tout en préservant le support bilingue (Français/Anglais). L'objectif est d'aligner le projet sur les standards industriels mondiaux de l'ingénierie logicielle et de l'IA (codebases, docstrings, commentaires et interfaces en anglais), tout en permettant à l'utilisateur du tableau de bord Flask de basculer instantanément entre le Français et l'Anglais pour lire la documentation, le glossaire, la FAQ d'entretien et le journal d'apprentissage.

---

### 1. 🎓 Nouveaux Concepts Introduits

*   **English-First Architecture :** Convention industrielle préconisant la rédaction native du code source (variables, fonctions, docstrings), des commentaires et des documentations techniques primaires en anglais, afin d'assurer l'interopérabilité au sein des équipes internationales et l'analyse optimale par les LLMs/agents IA.
*   **Bilingual Markdown Resolution :** Mécanisme dans le backend Flask capable d'inspecter les requêtes (paramètre HTTP `lang=fr|en` ou cookie/header) et de servir la version linguistique correspondante des fichiers de documentation (`.md` ou `_en.md`), avec repli (fallback) automatique vers le fichier principal si une version n'existe pas.
*   **Dynamic Language Switcher (SPA i18n) :** Composant UI dans l'application web Single Page Application (SPA) permettant d'intervertir en direct les intitulés de l'interface et de recharger les contenus d'API selon la langue sélectionnée par l'utilisateur.

---

### 2. 🧠 Prises de Décisions & Choix Techniques

#### Dilemme : Stratégie de gestion de la bilinguisation de la documentation
*   **Option 1 : Utiliser un outil lourd de traduction dynamique d'API (gettext/Babel) sur le serveur Flask**
    *   *Avantage/Inconvénient :* Très adapté pour de petites chaînes de texte fixes, mais lourd et complexe pour des documents Markdown volumineux de formation et d'architecture.
*   **Option 2 : Doubler les fichiers Markdown (`doc.md` et `doc_en.md`) avec sélecteur explicite au niveau du backend Flask (Retenue)**
    *   *Pourquoi ce choix ?* Permet de conserver une lisibilité Markdown parfaite dans Git, une vitesse de rendu optimale (pas de parsing lourd à la volée), tout en offrant un basculement fluide FR/EN dans le Dashboard Flask.

---

### 3. 🛠️ Implémentation & Auto-Documentation

#### Modification de `app.py` pour supporter le paramètre `lang` :
```python
def get_doc_path(base_name: str, lang: str = "en") -> Path:
    """Résout le chemin d'un fichier de documentation selon la langue demandée (en par défaut)."""
    if lang == "en":
        en_path = DOCS_DIR / f"{base_name}_en.md"
        if en_path.exists():
            return en_path
    return DOCS_DIR / f"{base_name}.md"
```

#### Commandes de validation à exécuter localement :
```bash
make test
```
*Toutes les suites de tests unitaires et d'intégration valident la présence des documents et l'exécution sans régression des endpoints Flask et FastAPI.*

---

### 4. 📌 Bilan du Jour

1.  **Codebase et docstrings bilingues/anglais** : Les commentaires et docstrings des modules Python (`app.py`, `src/`) ont été enrichis pour être compréhensibles à l'international.
2.  **Sélection de langue dans le Dashboard** : Ajout d'un sélecteur de langue (EN / FR) sur le header de l'application Flask permettant d'afficher instantanément le Glossaire, la Roadmap, le Journal, la FAQ et la Présentation dans la langue choisie.
3.  **Fichiers de documentation bilingues** : Ajout des versions anglaises des documents clés (`glossaire_en.md`, `faq_entretien_en.md`, `presentation_en.md`, `roadmap_details_en.md`, `journal_apprentissage_en.md`).
