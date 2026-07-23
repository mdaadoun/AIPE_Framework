"""Application Flask principale pour le Dashboard interactif d'AIPE_Framework.

Permet de :
- Suivre la feuille de route du projet (Roadmap)
- Étudier le Glossaire Technique
- Consulter le Journal d'Apprentissage
- S'entraîner aux entretiens avec un simulateur interactif (FAQ)
- Exécuter la suite de tests unitaires locaux (QA Terminal)
- Rediriger vers la documentation Swagger du microservice FastAPI
"""

import os
import re
import html
import subprocess
import sys
from pathlib import Path
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Configuration des chemins
DASHBOARD_DIR = Path(__file__).resolve().parent
PROJECT_DIR = DASHBOARD_DIR.parent
DOCS_DIR = PROJECT_DIR / "docs"
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://127.0.0.1:8000")


def markdown_to_html(md_text: str) -> str:
    """Convertit un texte Markdown simple en HTML stylisé (headers, listes, code blocks, bold, inline code)."""
    if not md_text:
        return ""

    lines = md_text.split("\n")
    html_lines = []
    in_list = False
    in_quote = False
    in_code_block = False
    code_lines = []
    code_lang = ""

    for line in lines:
        line_raw = line
        line_str = line.strip()

        # Gestion des blocs de code ```
        if line_str.startswith("```"):
            if in_code_block:
                code_text = html.escape("\n".join(code_lines))
                lang_badge = f"<div style='font-size: 0.68rem; font-family: monospace; color: var(--secondary); background: rgba(139, 92, 246, 0.15); padding: 2px 10px; border-radius: 4px 4px 0 0; display: inline-block; font-weight: bold; border: 1px solid rgba(139, 92, 246, 0.2); border-bottom: none;'>{code_lang}</div>" if code_lang else ""
                border_radius = "0 6px 6px 6px" if code_lang else "6px"

                html_lines.append(
                    f"<div style='margin: 14px 0;'>"
                    f"{lang_badge}"
                    f"<pre style='background: rgba(10, 15, 30, 0.75); border: 1px solid rgba(255,255,255,0.1); padding: 12px 14px; border-radius: {border_radius}; overflow-x: auto; color: #d8b4fe; font-family: monospace; font-size: 0.8rem; margin: 0; line-height: 1.45;'><code>{code_text}</code></pre>"
                    f"</div>"
                )
                in_code_block = False
                code_lines = []
                code_lang = ""
            else:
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
                if in_quote:
                    html_lines.append("</blockquote>")
                    in_quote = False
                in_code_block = True
                code_lang = line_str[3:].strip()
                code_lines = []
            continue

        if in_code_block:
            code_lines.append(line_raw)
            continue

        # Ligne horizontale
        if line_str in ("---", "***", "___"):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if in_quote:
                html_lines.append("</blockquote>")
                in_quote = False
            html_lines.append("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.1); margin: 18px 0;'>")
            continue

        # Titres
        if line_str.startswith("### "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if in_quote:
                html_lines.append("</blockquote>")
                in_quote = False
            html_lines.append(f"<h3 style='color: var(--secondary); margin-top: 18px; margin-bottom: 8px; font-family: var(--font-outfit); font-size: 1.05rem;'>{html.escape(line_str[4:])}</h3>")
            continue
        elif line_str.startswith("## "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if in_quote:
                html_lines.append("</blockquote>")
                in_quote = False
            html_lines.append(f"<h2 style='color: var(--secondary); margin-top: 22px; margin-bottom: 10px; font-family: var(--font-outfit); font-size: 1.2rem; border-bottom: 1px solid rgba(139, 92, 246, 0.2); padding-bottom: 4px;'>{html.escape(line_str[3:])}</h2>")
            continue
        elif line_str.startswith("# "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if in_quote:
                html_lines.append("</blockquote>")
                in_quote = False
            html_lines.append(f"<h1 style='color: var(--secondary); margin-top: 24px; margin-bottom: 12px; font-family: var(--font-outfit); font-size: 1.4rem;'>{html.escape(line_str[2:])}</h1>")
            continue

        # Bloc de citation (Blockquote)
        if line_str.startswith("> "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if not in_quote:
                html_lines.append("<blockquote style='background: rgba(139, 92, 246, 0.08); border-left: 3px solid var(--secondary); padding: 10px 14px; margin: 10px 0; border-radius: 4px; font-size: 0.85rem;'>")
                in_quote = True
            quote_text = html.escape(line_str[2:])
            html_lines.append(f"<p style='margin: 4px 0; color: #e2e8f0;'>{quote_text}</p>")
            continue
        elif in_quote and not line_str.startswith("> "):
            html_lines.append("</blockquote>")
            in_quote = False

        # Puces de liste
        if line_str.startswith("* ") or line_str.startswith("- ") or (line_str[0:1].isdigit() and line_str[1:3] == ". "):
            if not in_list:
                html_lines.append("<ul style='padding-left: 20px; margin: 8px 0;'>")
                in_list = True
            content_start = 2 if line_str.startswith("* ") or line_str.startswith("- ") else 3
            html_lines.append(f"<li style='margin-bottom: 6px; color: #cbd5e1;'>{html.escape(line_str[content_start:])}</li>")
            continue
        elif in_list and not (line_str.startswith("* ") or line_str.startswith("- ") or (line_str[0:1].isdigit() and line_str[1:3] == ". ")):
            html_lines.append("</ul>")
            in_list = False

        # Paragraphes
        if line_str:
            html_lines.append(f"<p style='margin: 8px 0; line-height: 1.5; color: #f8fafc;'>{html.escape(line_str)}</p>")

    if in_code_block:
        code_text = html.escape("\n".join(code_lines))
        html_lines.append(f"<pre style='background: rgba(10, 15, 30, 0.75); padding: 12px; border-radius: 6px; color: #d8b4fe; font-family: monospace;'><code>{code_text}</code></pre>")
    if in_list:
        html_lines.append("</ul>")
    if in_quote:
        html_lines.append("</blockquote>")

    html_content = "\n".join(html_lines)
    # Remplacement du formatage inline (bold, italic, code inline)
    html_content = re.sub(r"\*\*(.*?)\*\*", r'<strong style="color: #ffffff;">\1</strong>', html_content)
    html_content = re.sub(r"\*(.*?)\*", r"<em>\1</em>", html_content)
    html_content = re.sub(r"`(.*?)`", r'<code style="background: rgba(0,0,0,0.4); padding: 2px 6px; border-radius: 4px; color: #d8b4fe; font-family: monospace;">\1</code>', html_content)

    return html_content


def parse_faq_questions():
    """Parcoure docs/faq_entretien.md et en extrait une liste de questions/réponses."""
    faq_file = DOCS_DIR / "faq_entretien.md"
    if not faq_file.exists():
        return []

    content = faq_file.read_text(encoding="utf-8")
    questions = []
    
    parts = re.split(r'### Q\d+\.\s*', content)
    for part in parts[1:]:
        lines = part.strip().split('\n')
        if not lines:
            continue
        title = lines[0].strip()
        body = '\n'.join(lines[1:]).strip()
        questions.append({
            "question": title,
            "answer_markdown": body,
            "answer_html": markdown_to_html(body)
        })
    return questions


@app.route("/")
def index():
    """Rend l'interface Single Page Application (SPA)."""
    return render_template("index.html")


@app.route("/api/presentation", methods=["GET"])
def get_presentation():
    """Renvoie le contenu HTML de la présentation vulgarisée."""
    presentation_file = DOCS_DIR / "presentation.md"
    if not presentation_file.exists():
        return jsonify({"status": "error", "message": "Fichier presentation.md introuvable"}), 404

    try:
        content = presentation_file.read_text(encoding="utf-8")
        html_content = markdown_to_html(content)
        return jsonify({"status": "success", "html": html_content}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/roadmap", methods=["GET"])
def get_roadmap():
    """Renvoie le contenu HTML de la feuille de route."""
    roadmap_file = DOCS_DIR / "roadmap_details.md"
    if not roadmap_file.exists():
        return jsonify({"status": "error", "message": "Fichier roadmap_details.md introuvable"}), 404
    
    try:
        content = roadmap_file.read_text(encoding="utf-8")
        # Remplacer les raccourcis d'affichage pour les icônes
        content = content.replace("✅", "<span style='color: #10b981; font-weight: bold;'>✅</span>")
        content = content.replace("🔲", "<span style='color: #6b7280; font-weight: bold;'>🔲</span>")
        html_content = markdown_to_html(content)
        return jsonify({"status": "success", "html": html_content}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/glossaire", methods=["GET"])
def get_glossaire():
    """Renvoie le contenu HTML du glossaire."""
    glossaire_file = DOCS_DIR / "glossaire.md"
    if not glossaire_file.exists():
        return jsonify({"status": "error", "message": "Fichier glossaire.md introuvable"}), 404

    try:
        content = glossaire_file.read_text(encoding="utf-8")
        html_content = markdown_to_html(content)
        return jsonify({"status": "success", "html": html_content}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/journal", methods=["GET"])
def get_journal():
    """Renvoie le contenu HTML du journal d'apprentissage."""
    journal_file = DOCS_DIR / "journal_apprentissage.md"
    if not journal_file.exists():
        return jsonify({"status": "error", "message": "Fichier journal_apprentissage.md introuvable"}), 404

    try:
        content = journal_file.read_text(encoding="utf-8")
        html_content = markdown_to_html(content)
        return jsonify({"status": "success", "html": html_content}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/entretien", methods=["GET"])
def get_entretien_questions():
    """Renvoie la liste des questions d'entretien disponibles pour le simulateur."""
    try:
        questions = parse_faq_questions()
        clean_questions = [
            {"id": idx, "question": q["question"]} for idx, q in enumerate(questions)
        ]
        return jsonify({"status": "success", "questions": clean_questions}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/entretien/<int:question_id>", methods=["GET"])
def get_entretien_answer(question_id: int):
    """Renvoie la réponse pour une question spécifique."""
    try:
        questions = parse_faq_questions()
        if question_id < 0 or question_id >= len(questions):
            return jsonify({"status": "error", "message": "Question introuvable"}), 404
        return jsonify({
            "status": "success", 
            "question": questions[question_id]["question"],
            "answer_html": questions[question_id]["answer_html"]
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/run-tests", methods=["POST"])
def run_tests():
    """Lancement de la suite de tests unitaires via subprocess (pytest)."""
    # Utilise le python de l'environnement virtuel local s'il est présent pour garantir
    # que les dépendances (fastapi, pydantic, etc.) sont bien chargées
    venv_python = PROJECT_DIR / ".venv" / "bin" / "python"
    if venv_python.exists():
        cmd = [str(venv_python), "-m", "pytest", "tests/"]
    else:
        cmd = [sys.executable, "-m", "pytest", "tests/"]
    
    tests_dir = PROJECT_DIR / "tests"
    if not tests_dir.exists():
        return jsonify({
            "status": "failed",
            "message": "Le dossier 'tests/' n'existe pas encore dans le framework AIPE.",
            "stdout": "",
            "stderr": "Erreur: Aucun test n'est défini. Créez d'abord le dossier 'tests/'."
        }), 200

    try:
        process = subprocess.run(
            cmd,
            cwd=str(PROJECT_DIR),
            capture_output=True,
            text=True,
            timeout=30
        )
        
        stdout = process.stdout
        stderr = process.stderr
        
        if process.returncode == 0:
            return jsonify({
                "status": "success",
                "message": "Tous les tests sont passés avec succès !",
                "stdout": stdout,
                "stderr": stderr,
                "exit_code": process.returncode
            }), 200
        else:
            return jsonify({
                "status": "failed",
                "message": f"Certains tests ont échoué (code de sortie: {process.returncode}).",
                "stdout": stdout,
                "stderr": stderr,
                "exit_code": process.returncode
            }), 200
            
    except subprocess.TimeoutExpired:
        return jsonify({
            "status": "error",
            "message": "L'exécution des tests a expiré après 30 secondes."
        }), 504
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erreur de lancement de la suite de tests : {str(e)}"
        }), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
