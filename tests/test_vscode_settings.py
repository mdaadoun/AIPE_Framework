"""Tests de validation de la configuration IDE VSCode (.vscode/).

Ce module vérifie que les fichiers de configuration de l'environnement de
développement VSCode sont présents, syntaxiquement valides et contiennent
les paramètres essentiels pour aligner l'expérience de développement locale
avec les vérifications de la CI (pre-commit hooks + Makefile).

Fichiers validés :
    - .vscode/settings.json  : Formatage automatique à la sauvegarde via Ruff.
    - .vscode/extensions.json : Recommandations d'extensions pour l'équipe.
"""

import json
from pathlib import Path

# Chemin absolu vers la racine du projet AIPE_Framework
PROJECT_DIR = Path(__file__).resolve().parent.parent


# ==============================================================================
# SECTION 1 : Existence et validité syntaxique des fichiers
# ==============================================================================


def test_vscode_settings_file_exists() -> None:
    """Vérifie que le fichier .vscode/settings.json existe et n'est pas vide."""
    settings_file = PROJECT_DIR / ".vscode" / "settings.json"

    assert settings_file.exists(), (
        "Le fichier .vscode/settings.json est manquant. "
        "Ce fichier est indispensable pour le formatage automatique à la sauvegarde."
    )
    assert (
        settings_file.stat().st_size > 0
    ), "Le fichier .vscode/settings.json est vide."


def test_vscode_extensions_file_exists() -> None:
    """Vérifie que le fichier .vscode/extensions.json existe et n'est pas vide."""
    extensions_file = PROJECT_DIR / ".vscode" / "extensions.json"

    assert extensions_file.exists(), (
        "Le fichier .vscode/extensions.json est manquant. "
        "Ce fichier recommande automatiquement les extensions nécessaires."
    )
    assert (
        extensions_file.stat().st_size > 0
    ), "Le fichier .vscode/extensions.json est vide."


def test_vscode_settings_is_valid_json() -> None:
    """Vérifie que settings.json est un fichier JSON syntaxiquement valide.

    Note : VSCode accepte les commentaires dans le JSON (JSONC), mais la
    bibliothèque standard Python `json` ne les supporte pas. On nettoie donc
    les commentaires avant le parsing pour valider la structure sous-jacente.
    """
    settings_file = PROJECT_DIR / ".vscode" / "settings.json"
    content = settings_file.read_text(encoding="utf-8")

    # Suppression des commentaires de type // (JSONC → JSON standard)
    # On traite ligne par ligne pour ne pas casser les URLs contenant //
    cleaned_lines = []
    for line in content.splitlines():
        stripped = line.lstrip()
        # Ligne commençant par // = commentaire JSONC pur
        if stripped.startswith("//"):
            continue
        # Commentaire en fin de ligne : on cherche // précédé d'un espace
        # mais on évite les faux positifs dans les chaînes (ex: "http://")
        cleaned_lines.append(line)

    cleaned_content = "\n".join(cleaned_lines)

    # Suppression des commentaires inline restants (// après une valeur)
    import re

    # Supprime les // qui ne sont PAS à l'intérieur de guillemets
    # Approche simplifiée : supprime // suivi de texte non-guillemet en fin de ligne
    cleaned_content = re.sub(
        r'(?<=[,{}\[\]\d"])\s*//.*$', "", cleaned_content, flags=re.MULTILINE
    )

    try:
        data = json.loads(cleaned_content)
        assert isinstance(
            data, dict
        ), "Le fichier settings.json doit contenir un objet JSON racine."
    except json.JSONDecodeError as e:
        raise AssertionError(
            f"Le fichier .vscode/settings.json contient du JSON invalide : {e}"
        ) from e


def test_vscode_extensions_is_valid_json() -> None:
    """Vérifie que extensions.json est un fichier JSON syntaxiquement valide."""
    extensions_file = PROJECT_DIR / ".vscode" / "extensions.json"
    content = extensions_file.read_text(encoding="utf-8")

    # Nettoyage des commentaires JSONC
    cleaned_lines = [
        line for line in content.splitlines() if not line.lstrip().startswith("//")
    ]
    cleaned_content = "\n".join(cleaned_lines)

    try:
        data = json.loads(cleaned_content)
        assert isinstance(
            data, dict
        ), "Le fichier extensions.json doit contenir un objet JSON racine."
    except json.JSONDecodeError as e:
        raise AssertionError(
            f"Le fichier .vscode/extensions.json contient du JSON invalide : {e}"
        ) from e


# ==============================================================================
# SECTION 2 : Paramètres critiques du formatage (settings.json)
# ==============================================================================


def _load_settings() -> dict:
    """Charge et parse le fichier settings.json en nettoyant les commentaires JSONC.

    Retourne le dictionnaire JSON résultant pour les assertions des tests.
    """
    import re

    settings_file = PROJECT_DIR / ".vscode" / "settings.json"
    content = settings_file.read_text(encoding="utf-8")

    # Suppression des lignes de commentaire JSONC
    cleaned_lines = [
        line for line in content.splitlines() if not line.lstrip().startswith("//")
    ]
    cleaned_content = "\n".join(cleaned_lines)
    cleaned_content = re.sub(
        r'(?<=[,{}\[\]\d"])\s*//.*$', "", cleaned_content, flags=re.MULTILINE
    )

    return json.loads(cleaned_content)


def test_settings_has_ruff_formatter() -> None:
    """Vérifie que Ruff est configuré comme formateur par défaut pour Python."""
    data = _load_settings()

    python_section = data.get("[python]", {})
    assert python_section.get("editor.defaultFormatter") == "charliermarsh.ruff", (
        "Le formateur par défaut pour Python doit être 'charliermarsh.ruff'. "
        "Sans ce réglage, VSCode utiliserait un formateur aléatoire ou aucun."
    )


def test_settings_has_format_on_save() -> None:
    """Vérifie que le formatage automatique à la sauvegarde est activé."""
    data = _load_settings()

    python_section = data.get("[python]", {})
    assert python_section.get("editor.formatOnSave") is True, (
        "Le paramètre 'editor.formatOnSave' doit être activé (true) pour Python. "
        "C'est le critère de validation principal de l'étape 6.1."
    )


def test_settings_has_code_actions_on_save() -> None:
    """Vérifie que les corrections automatiques (fixAll + organizeImports) sont actives."""
    data = _load_settings()

    python_section = data.get("[python]", {})
    code_actions = python_section.get("editor.codeActionsOnSave", {})

    assert "source.fixAll" in code_actions, (
        "L'action 'source.fixAll' doit être configurée pour corriger "
        "automatiquement les erreurs de style à la sauvegarde."
    )
    assert "source.organizeImports" in code_actions, (
        "L'action 'source.organizeImports' doit être configurée pour "
        "trier automatiquement les imports à la sauvegarde."
    )


def test_settings_has_correct_line_length() -> None:
    """Vérifie la cohérence de la longueur de ligne entre VSCode et pyproject.toml."""
    data = _load_settings()

    # Récupération de la valeur dans settings.json
    ruff_line_length = data.get("ruff.lineLength")

    # Récupération de la valeur dans pyproject.toml pour comparaison
    pyproject_file = PROJECT_DIR / "pyproject.toml"
    pyproject_content = pyproject_file.read_text(encoding="utf-8")

    # Extraction de la valeur line-length dans [tool.ruff]
    import re

    match = re.search(r"line-length\s*=\s*(\d+)", pyproject_content)
    assert (
        match is not None
    ), "Impossible de trouver 'line-length' dans pyproject.toml [tool.ruff]."
    pyproject_line_length = int(match.group(1))

    assert ruff_line_length == pyproject_line_length, (
        f"Désalignement de la longueur de ligne : "
        f"settings.json = {ruff_line_length}, pyproject.toml = {pyproject_line_length}. "
        f"Les deux fichiers doivent utiliser la même valeur."
    )


def test_settings_has_ruff_lint_enabled() -> None:
    """Vérifie que le linting Ruff en temps réel est activé dans l'éditeur."""
    data = _load_settings()

    assert data.get("ruff.lint.enable") is True, (
        "Le paramètre 'ruff.lint.enable' doit être activé (true) pour "
        "afficher les erreurs de style directement dans l'éditeur."
    )


# ==============================================================================
# SECTION 3 : Cohérence avec les hooks pre-commit
# ==============================================================================


def test_settings_final_newline_matches_precommit() -> None:
    """Vérifie que l'insertion de la ligne finale est cohérente avec end-of-file-fixer."""
    data = _load_settings()

    assert data.get("files.insertFinalNewline") is True, (
        "Le paramètre 'files.insertFinalNewline' doit être activé pour "
        "correspondre au hook pre-commit 'end-of-file-fixer'."
    )


def test_settings_trim_whitespace_matches_precommit() -> None:
    """Vérifie que la suppression des espaces de fin correspond à trailing-whitespace."""
    data = _load_settings()

    assert data.get("files.trimTrailingWhitespace") is True, (
        "Le paramètre 'files.trimTrailingWhitespace' doit être activé pour "
        "correspondre au hook pre-commit 'trailing-whitespace'."
    )


# ==============================================================================
# SECTION 4 : Extensions recommandées (extensions.json)
# ==============================================================================


def test_extensions_recommends_ruff() -> None:
    """Vérifie que l'extension Ruff est dans la liste des recommandations."""
    extensions_file = PROJECT_DIR / ".vscode" / "extensions.json"
    content = extensions_file.read_text(encoding="utf-8")

    # Nettoyage des commentaires JSONC
    cleaned_lines = [
        line for line in content.splitlines() if not line.lstrip().startswith("//")
    ]
    data = json.loads("\n".join(cleaned_lines))

    recommendations = data.get("recommendations", [])
    assert "charliermarsh.ruff" in recommendations, (
        "L'extension 'charliermarsh.ruff' doit être recommandée dans extensions.json. "
        "Sans cette extension, le formatage automatique ne fonctionne pas."
    )


def test_extensions_recommends_python() -> None:
    """Vérifie que l'extension Python Microsoft est dans la liste des recommandations."""
    extensions_file = PROJECT_DIR / ".vscode" / "extensions.json"
    content = extensions_file.read_text(encoding="utf-8")

    cleaned_lines = [
        line for line in content.splitlines() if not line.lstrip().startswith("//")
    ]
    data = json.loads("\n".join(cleaned_lines))

    recommendations = data.get("recommendations", [])
    assert "ms-python.python" in recommendations, (
        "L'extension 'ms-python.python' doit être recommandée dans extensions.json. "
        "Elle fournit l'auto-complétion, le débogage et l'intégration pytest."
    )
