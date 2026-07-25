"""Application Flask principale pour le Dashboard interactif d'AIPE_Framework.

Permet de :
- Suivre la feuille de route du projet (Roadmap)
- Étudier le Glossaire Technique
- Consulter le Journal d'Apprentissage
- S'entraîner aux entretiens avec un simulateur interactif (FAQ)
- Exécuter la suite de tests unitaires locaux (QA Terminal)
- Rediriger vers la documentation Swagger du microservice FastAPI
"""

import html
import os
import re
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
                lang_badge = (
                    f"<div style='font-size: 0.68rem; font-family: monospace; color: var(--secondary); background: rgba(139, 92, 246, 0.15); padding: 2px 10px; border-radius: 4px 4px 0 0; display: inline-block; font-weight: bold; border: 1px solid rgba(139, 92, 246, 0.2); border-bottom: none;'>{code_lang}</div>"
                    if code_lang
                    else ""
                )
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
            html_lines.append(
                "<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.1); margin: 18px 0;'>"
            )
            continue

        # Titres
        if line_str.startswith("#### "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if in_quote:
                html_lines.append("</blockquote>")
                in_quote = False
            html_lines.append(
                f"<h4 style='color: var(--secondary); margin-top: 14px; margin-bottom: 6px; font-family: var(--font-outfit); font-size: 0.95rem; font-weight: 600;'>{html.escape(line_str[5:])}</h4>"
            )
            continue
        elif line_str.startswith("### "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if in_quote:
                html_lines.append("</blockquote>")
                in_quote = False
            html_lines.append(
                f"<h3 style='color: var(--secondary); margin-top: 18px; margin-bottom: 8px; font-family: var(--font-outfit); font-size: 1.05rem;'>{html.escape(line_str[4:])}</h3>"
            )
            continue
        elif line_str.startswith("## "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if in_quote:
                html_lines.append("</blockquote>")
                in_quote = False
            html_lines.append(
                f"<h2 style='color: var(--secondary); margin-top: 22px; margin-bottom: 10px; font-family: var(--font-outfit); font-size: 1.2rem; border-bottom: 1px solid rgba(139, 92, 246, 0.2); padding-bottom: 4px;'>{html.escape(line_str[3:])}</h2>"
            )
            continue
        elif line_str.startswith("# "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if in_quote:
                html_lines.append("</blockquote>")
                in_quote = False
            html_lines.append(
                f"<h1 style='color: var(--secondary); margin-top: 24px; margin-bottom: 12px; font-family: var(--font-outfit); font-size: 1.4rem;'>{html.escape(line_str[2:])}</h1>"
            )
            continue

        # Bloc de citation (Blockquote)
        if line_str.startswith("> "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if not in_quote:
                html_lines.append(
                    "<blockquote style='background: rgba(139, 92, 246, 0.08); border-left: 3px solid var(--secondary); padding: 10px 14px; margin: 10px 0; border-radius: 4px; font-size: 0.85rem;'>"
                )
                in_quote = True
            quote_text = html.escape(line_str[2:])
            html_lines.append(
                f"<p style='margin: 4px 0; color: #e2e8f0;'>{quote_text}</p>"
            )
            continue
        elif in_quote and not line_str.startswith("> "):
            html_lines.append("</blockquote>")
            in_quote = False

        # Puces de liste
        if (
            line_str.startswith("* ")
            or line_str.startswith("- ")
            or (line_str[0:1].isdigit() and line_str[1:3] == ". ")
        ):
            if not in_list:
                html_lines.append("<ul style='padding-left: 20px; margin: 8px 0;'>")
                in_list = True
            content_start = (
                2 if line_str.startswith("* ") or line_str.startswith("- ") else 3
            )
            html_lines.append(
                f"<li style='margin-bottom: 6px; color: #cbd5e1;'>{html.escape(line_str[content_start:])}</li>"
            )
            continue
        elif in_list and not (
            line_str.startswith("* ")
            or line_str.startswith("- ")
            or (line_str[0:1].isdigit() and line_str[1:3] == ". ")
        ):
            html_lines.append("</ul>")
            in_list = False

        # Paragraphes
        if line_str:
            html_lines.append(
                f"<p style='margin: 8px 0; line-height: 1.5; color: #f8fafc;'>{html.escape(line_str)}</p>"
            )

    if in_code_block:
        code_text = html.escape("\n".join(code_lines))
        html_lines.append(
            f"<pre style='background: rgba(10, 15, 30, 0.75); padding: 12px; border-radius: 6px; color: #d8b4fe; font-family: monospace;'><code>{code_text}</code></pre>"
        )
    if in_list:
        html_lines.append("</ul>")
    if in_quote:
        html_lines.append("</blockquote>")

    html_content = "\n".join(html_lines)
    # Remplacement du formatage inline (bold, italic, code inline, liens)
    html_content = re.sub(
        r"\*\*(.*?)\*\*", r'<strong style="color: #ffffff;">\1</strong>', html_content
    )
    html_content = re.sub(r"\*(.*?)\*", r"<em>\1</em>", html_content)
    html_content = re.sub(
        r"`(.*?)`",
        r'<code style="background: rgba(0,0,0,0.4); padding: 2px 6px; border-radius: 4px; color: #d8b4fe; font-family: monospace;">\1</code>',
        html_content,
    )
    html_content = re.sub(
        r"\[(.*?)\]\((.*?)\)",
        r'<a href="\2" style="color: var(--secondary); text-decoration: none; border-bottom: 1px dashed var(--secondary);" target="_blank">\1</a>',
        html_content,
    )

    return html_content


def parse_faq_questions():
    """Parcoure docs/faq_entretien.md et en extrait une liste de questions/réponses."""
    faq_file = DOCS_DIR / "faq_entretien.md"
    if not faq_file.exists():
        return []

    content = faq_file.read_text(encoding="utf-8")
    questions = []

    parts = re.split(r"### Q\d+\.\s*", content)
    for part in parts[1:]:
        lines = part.strip().split("\n")
        if not lines:
            continue
        title = lines[0].strip()
        body = "\n".join(lines[1:]).strip()
        questions.append(
            {
                "question": title,
                "answer_markdown": body,
                "answer_html": markdown_to_html(body),
            }
        )
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
        return jsonify(
            {"status": "error", "message": "Fichier presentation.md introuvable"}
        ), 404

    try:
        content = presentation_file.read_text(encoding="utf-8")
        html_content = markdown_to_html(content)
        return jsonify({"status": "success", "html": html_content}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


def parse_roadmap_to_html() -> str:
    """Parse le fichier roadmap_details.md et le convertit en grille de cartes de phases et d'étapes."""
    roadmap_file = DOCS_DIR / "roadmap_details.md"
    if not roadmap_file.exists():
        return "<div style='color: var(--danger); padding: 20px;'>Fichier roadmap_details.md introuvable.</div>"

    try:
        content = roadmap_file.read_text(encoding="utf-8")
    except Exception as e:
        return f"<div style='color: var(--danger); padding: 20px;'>Erreur de lecture : {html.escape(str(e))}</div>"

    def clean_text(txt):
        txt = html.escape(txt.strip())
        txt = re.sub(
            r"\*\*(.*?)\*\*", r'<strong style="color: #ffffff;">\1</strong>', txt
        )
        txt = re.sub(
            r"`(.*?)`",
            r'<code style="background: rgba(0,0,0,0.4); padding: 2px 6px; border-radius: 4px; color: #d8b4fe; font-family: monospace;">\1</code>',
            txt,
        )
        txt = re.sub(
            r"\[(.*?)\]\((.*?)\)",
            r'<a href="\2" style="color: var(--secondary); text-decoration: none; border-bottom: 1px dashed var(--secondary);" target="_blank">\1</a>',
            txt,
        )
        return txt

    html_out = []
    html_out.append('<div class="roadmap-container">')
    html_out.append('  <div class="roadmap-header-section">')
    html_out.append(
        '    <h2 class="roadmap-main-title">🗺️ Feuille de Route & Suivi</h2>'
    )
    html_out.append(
        '    <p class="roadmap-main-subtitle">Suivi chronologique de la construction d\'AIPE_Framework (AI Product Engineering)</p>'
    )
    html_out.append("  </div>")

    lines = content.split("\n")

    in_steps_grid = False
    in_phase = False
    in_pre_block = False
    pre_lines = []

    current_step_lines = []

    def flush_step():
        if not current_step_lines:
            return ""

        step_header_line = current_step_lines[0]
        parts = step_header_line.split("—")
        title_part = parts[0].replace("###", "").strip()
        status_part = parts[1].strip() if len(parts) > 1 else "🔲 À venir"

        title_subparts = title_part.split(":")
        step_num = title_subparts[0].strip()
        step_title = (
            ":".join(title_subparts[1:]).strip()
            if len(title_subparts) > 1
            else title_part
        )

        status_class = "pending"
        badge_text = "À venir"
        badge_class = "badge-pending"

        if "✅" in status_part or "Validé" in status_part:
            status_class = "completed"
            badge_text = "Validé"
            badge_class = "badge-completed"
        elif "En cours" in status_part or "⏳" in status_part:
            status_class = "active"
            badge_text = "En cours"
            badge_class = "badge-active"

        step_html = []
        step_html.append(f'<div class="step-card {status_class}">')
        step_html.append('  <div class="step-header">')
        step_html.append(f'    <span class="step-number">{step_num}</span>')
        step_html.append(
            f'    <span class="step-badge {badge_class}">{badge_text}</span>'
        )
        step_html.append("  </div>")
        step_html.append(f'  <h4 class="step-title">{step_title}</h4>')
        step_html.append('  <div class="step-details">')

        for line in current_step_lines[1:]:
            line_str = line.strip()
            if not line_str:
                continue
            if line_str.startswith("* ") or line_str.startswith("- "):
                line_str = line_str[2:].strip()

            if line_str.startswith("**Description :**") or line_str.startswith(
                "**Description:**"
            ):
                desc_text = (
                    line_str.replace("**Description :**", "")
                    .replace("**Description:**", "")
                    .strip()
                )
                step_html.append(
                    f'    <div class="detail-item"><strong>Description :</strong> {clean_text(desc_text)}</div>'
                )
            elif (
                line_str.startswith("**Concept clé :**")
                or line_str.startswith("**Concept clé:**")
                or line_str.startswith("**Concept clef :**")
            ):
                concept_text = (
                    line_str.replace("**Concept clé :**", "")
                    .replace("**Concept clé:**", "")
                    .replace("**Concept clef :**", "")
                    .strip()
                )
                step_html.append(
                    f'    <div class="detail-item"><strong>Concept clé :</strong> {clean_text(concept_text)}</div>'
                )
            elif line_str.startswith(
                "**Critère de validation :**"
            ) or line_str.startswith("**Critère de validation:**"):
                validation_text = (
                    line_str.replace("**Critère de validation :**", "")
                    .replace("**Critère de validation:**", "")
                    .strip()
                )
                step_html.append(
                    f'    <div class="detail-item validation-item"><strong>Critère de validation :</strong> {clean_text(validation_text)}</div>'
                )
            else:
                step_html.append(
                    f'    <div class="detail-item">{clean_text(line_str)}</div>'
                )

        step_html.append("  </div>")
        step_html.append("</div>")
        return "\n".join(step_html)

    for line in lines:
        line_raw = line
        line_str = line.strip()

        # Handle code blocks
        if line_str.startswith("```"):
            if in_pre_block:
                in_pre_block = False
                code_text = html.escape("\n".join(pre_lines))
                html_out.append(
                    f"<pre style='background: rgba(10, 15, 30, 0.75); border: 1px solid rgba(255,255,255,0.1); padding: 12px 14px; border-radius: 6px; overflow-x: auto; color: #d8b4fe; font-family: monospace; font-size: 0.8rem; margin: 14px 0; line-height: 1.45;'><code>{code_text}</code></pre>"
                )
                pre_lines = []
            else:
                in_pre_block = True
                pre_lines = []
            continue

        if in_pre_block:
            pre_lines.append(line_raw)
            continue

        if line_str.startswith("## Phase"):
            if current_step_lines:
                html_out.append(flush_step())
                current_step_lines = []
            if in_steps_grid:
                html_out.append("    </div>")  # Close steps-grid
                in_steps_grid = False
            if in_phase:
                html_out.append("  </div>")  # Close phase-section

            in_phase = True

            parts = line_str.split("—")
            phase_part = parts[0].replace("##", "").strip()
            status_part = parts[1].strip() if len(parts) > 1 else "🔲 À venir"

            phase_subparts = phase_part.split(":")
            phase_idx = phase_subparts[0].strip()
            phase_title = (
                ":".join(phase_subparts[1:]).strip()
                if len(phase_subparts) > 1
                else phase_part
            )

            status_class = "pending"
            status_text = "À venir"
            if "✅" in status_part or "Validé" in status_part:
                status_class = "completed"
                status_text = "Validé"
            elif "En cours" in status_part or "⏳" in status_part:
                status_class = "active"
                status_text = "En cours"

            html_out.append(f'  <div class="phase-section {status_class}">')
            html_out.append(f'    <div class="phase-banner {status_class}">')
            html_out.append('      <div class="phase-banner-info">')
            html_out.append(f'        <span class="phase-index">{phase_idx}</span>')
            html_out.append(f'        <h3 class="phase-title">{phase_title}</h3>')
            html_out.append("      </div>")
            html_out.append(
                f'      <span class="phase-status-badge {status_class}">{status_text}</span>'
            )
            html_out.append("    </div>")

        elif line_str.startswith("*Objectif"):
            obj_text = line_str.replace("*", "").strip()
            html_out.append(f'    <p class="phase-objective"><em>{obj_text}</em></p>')
            html_out.append('    <div class="steps-grid">')
            in_steps_grid = True

        elif line_str.startswith("### Étape"):
            if current_step_lines:
                html_out.append(flush_step())
                current_step_lines = []
            current_step_lines.append(line_str)

        elif current_step_lines:
            current_step_lines.append(line)

        else:
            if not line_str:
                continue
            if line_str.startswith("# "):
                html_out.append(
                    f'<h1 style="color: #ffffff; font-size: 1.6rem; border-bottom: 1px solid var(--border); padding-bottom: 8px; margin-bottom: 16px; font-family: var(--font-outfit);">{clean_text(line_str[2:])}</h1>'
                )
            elif line_str.startswith("## "):
                html_out.append(
                    f'<h2 style="color: var(--secondary); font-size: 1.3rem; margin-top: 24px; border-bottom: 1px solid rgba(139, 92, 246, 0.15); padding-bottom: 6px; font-family: var(--font-outfit);">{clean_text(line_str[3:])}</h2>'
                )
            else:
                html_out.append(
                    f'<p style="margin: 10px 0; color: #e2e8f0; font-size: 0.95rem;">{clean_text(line_str)}</p>'
                )

    # Flush remaining
    if current_step_lines:
        html_out.append(flush_step())
    if in_steps_grid:
        html_out.append("    </div>")
    if in_phase:
        html_out.append("  </div>")

    html_out.append("</div>")
    return "\n".join(html_out)


@app.route("/api/roadmap", methods=["GET"])
def get_roadmap():
    """Renvoie le contenu HTML de la feuille de route."""
    try:
        html_content = parse_roadmap_to_html()
        return jsonify({"status": "success", "html": html_content}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


def parse_glossary_concepts():
    """Parse le fichier glossaire.md et extrait les concepts et leurs définitions."""
    glossaire_file = DOCS_DIR / "glossaire.md"
    if not glossaire_file.exists():
        return []

    content = glossaire_file.read_text(encoding="utf-8")
    concepts = []

    parts = re.split(r"### ", content)
    for part in parts[1:]:
        lines = part.strip().split("\n")
        if not lines:
            continue
        concept_name = lines[0].strip()
        definition = "\n".join(lines[1:]).strip()
        concepts.append(
            {
                "id": len(concepts),
                "concept": concept_name,
                "definition_markdown": definition,
                "definition_html": markdown_to_html(definition),
            }
        )
    return concepts


@app.route("/api/glossaire", methods=["GET"])
def get_glossaire():
    """Renvoie la liste des concepts du glossaire."""
    try:
        concepts = parse_glossary_concepts()
        clean_concepts = [{"id": c["id"], "concept": c["concept"]} for c in concepts]
        return jsonify({"status": "success", "concepts": clean_concepts}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/glossaire/<int:concept_id>", methods=["GET"])
def get_glossaire_concept(concept_id: int):
    """Renvoie la définition d'un concept spécifique."""
    try:
        concepts = parse_glossary_concepts()
        if concept_id < 0 or concept_id >= len(concepts):
            return jsonify({"status": "error", "message": "Concept introuvable"}), 404

        return jsonify(
            {
                "status": "success",
                "concept": concepts[concept_id]["concept"],
                "html": concepts[concept_id]["definition_html"],
            }
        ), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


def parse_journal_file_info(file_path, file_id):
    """Extrait le titre et la date d'un fichier journal Markdown pour les boutons d'indexation."""
    try:
        content = file_path.read_text(encoding="utf-8")
        title = "Sans titre"
        date = "Date inconnue"

        for line in content.splitlines():
            line_str = line.strip()
            if line_str.startswith("# "):
                title = line_str[2:].strip()
                # Nettoyer les emojis de début de titre pour l'affichage du bouton
                title = re.sub(r"^[^\w\s\d]+", "", title).strip()
            elif "Date :" in line_str:
                date_match = re.search(r"\*\*Date\s*:\s*\*\*(.*)", line_str)
                if date_match:
                    date = date_match.group(1).strip()
                else:
                    date = line_str.replace("Date :", "").replace("**", "").strip()

        return {"id": file_id, "title": title, "date": date}
    except Exception:
        return {
            "id": file_id,
            "title": file_path.stem.replace("_", " ").capitalize(),
            "date": "Date inconnue",
        }


@app.route("/api/journal", methods=["GET"])
def get_journal():
    """Renvoie la liste des articles de journal disponibles avec leurs métadonnées."""
    entries = []

    # 1. Ajouter l'introduction
    journal_file = DOCS_DIR / "journal_apprentissage.md"
    if journal_file.exists():
        entries.append(parse_journal_file_info(journal_file, "intro"))

    # 2. Ajouter les séances individuelles triées par nom de fichier
    journal_dir = DOCS_DIR / "journal"
    if journal_dir.exists() and journal_dir.is_dir():
        seances = sorted(
            [f for f in journal_dir.glob("*.md") if f.name != "journal_template.md"]
        )
        for seance in seances:
            entries.append(parse_journal_file_info(seance, seance.stem))

    return jsonify({"status": "success", "entries": entries}), 200


@app.route("/api/journal/<article_id>", methods=["GET"])
def get_journal_content(article_id: str):
    """Renvoie le contenu HTML rendu d'un article de journal spécifique."""
    if article_id == "intro":
        file_path = DOCS_DIR / "journal_apprentissage.md"
    else:
        # Assainir l'identifiant pour empêcher toute traversée de chemin (path traversal)
        clean_id = re.sub(r"[^a-zA-Z0-9_.-]", "", article_id)
        file_path = DOCS_DIR / "journal" / f"{clean_id}.md"

    if not file_path.exists():
        return jsonify(
            {"status": "error", "message": f"Article '{article_id}' introuvable"}
        ), 404

    try:
        content = file_path.read_text(encoding="utf-8")
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
        return jsonify(
            {
                "status": "success",
                "question": questions[question_id]["question"],
                "answer_html": questions[question_id]["answer_html"],
            }
        ), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/tests/list", methods=["GET"])
def list_tests():
    """Renvoie la liste détaillée et hiérarchique des tests unitaires découverts dynamiquement via AST."""
    tests_dir = PROJECT_DIR / "tests"
    if not tests_dir.exists() or not tests_dir.is_dir():
        return jsonify({"status": "success", "tests": []}), 200

    try:
        import ast

        test_list = [
            {
                "id": "all",
                "name": "🧪 Toute la suite (pytest)",
                "file": "all",
                "docstring": "Exécute l'ensemble des tests unitaires et d'intégration du framework AIPE.",
                "type": "suite",
            }
        ]

        # Recherche et parcours de tous les fichiers de test
        for file_path in sorted(tests_dir.glob("test_*.py")):
            rel_path = f"tests/{file_path.name}"

            # Parsing AST pour lire le docstring global et les fonctions du fichier
            try:
                tree = ast.parse(
                    file_path.read_text(encoding="utf-8"), filename=str(file_path)
                )
                file_doc = ast.get_docstring(tree) or ""
            except Exception:
                file_doc = ""

            test_list.append(
                {
                    "id": rel_path,
                    "name": f"📁 {file_path.name} (Tout le fichier)",
                    "file": rel_path,
                    "docstring": file_doc.strip()
                    or f"Exécute tous les tests du fichier {file_path.name}.",
                    "type": "file",
                }
            )

            # Extraction de chaque fonction commençant par "test_"
            try:
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and node.name.startswith(
                        "test_"
                    ):
                        docstring = ast.get_docstring(node) or ""
                        test_id = f"{rel_path}::{node.name}"
                        test_list.append(
                            {
                                "id": test_id,
                                "name": f"   └─ {node.name}",
                                "file": rel_path,
                                "docstring": docstring.strip()
                                or "Aucune description de test.",
                                "type": "function",
                            }
                        )
            except Exception:
                pass

        return jsonify({"status": "success", "tests": test_list}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/run-tests", methods=["POST"])
def run_tests():
    """Lancement de la suite de tests unitaires (pytest) globale ou ciblée à la fonction près."""
    test_name = "all"
    if request.is_json and request.json.get("test_name"):
        test_name = request.json.get("test_name")

    # Utilise le python de l'environnement virtuel local s'il est présent pour garantir
    # que les dépendances (fastapi, pydantic, etc.) sont bien chargées
    venv_python = PROJECT_DIR / ".venv" / "bin" / "python"
    python_exec = str(venv_python) if venv_python.exists() else sys.executable

    if test_name == "all":
        cmd = [python_exec, "-m", "pytest", "tests/"]
    else:
        # Sécurisation du nom : on autorise les deux-points pour la syntaxe pytest (::)
        clean_name = re.sub(r"[^a-zA-Z0-9_.-/:]", "", test_name)
        if not (clean_name.startswith("tests/test_") and ".py" in clean_name):
            return jsonify(
                {
                    "status": "error",
                    "message": "Nom de test ou de fonction de test invalide.",
                }
            ), 400

        # Vérification de l'existence du fichier physique correspondant
        file_part = clean_name.split("::")[0]
        file_path = PROJECT_DIR / file_part
        if not file_path.exists():
            return jsonify(
                {
                    "status": "error",
                    "message": f"Fichier de test '{file_part}' introuvable.",
                }
            ), 404

        cmd = [python_exec, "-m", "pytest", clean_name]

    tests_dir = PROJECT_DIR / "tests"
    if not tests_dir.exists():
        return jsonify(
            {
                "status": "failed",
                "message": "Le dossier 'tests/' n'existe pas encore dans le framework AIPE.",
                "stdout": "",
                "stderr": "Erreur: Aucun test n'est défini. Créez d'abord le dossier 'tests/'.",
            }
        ), 200

    try:
        process = subprocess.run(
            cmd, cwd=str(PROJECT_DIR), capture_output=True, text=True, timeout=30
        )

        stdout = process.stdout
        stderr = process.stderr

        if process.returncode == 0:
            return jsonify(
                {
                    "status": "success",
                    "message": f"Exécution réussie : {test_name}",
                    "stdout": stdout,
                    "stderr": stderr,
                    "exit_code": process.returncode,
                }
            ), 200
        else:
            return jsonify(
                {
                    "status": "failed",
                    "message": f"Certains tests ont échoué (code de sortie: {process.returncode}).",
                    "stdout": stdout,
                    "stderr": stderr,
                    "exit_code": process.returncode,
                }
            ), 200

    except subprocess.TimeoutExpired:
        return jsonify(
            {
                "status": "error",
                "message": "L'exécution des tests a expiré après 30 secondes.",
            }
        ), 504
    except Exception as e:
        return jsonify(
            {
                "status": "error",
                "message": f"Erreur de lancement de la suite de tests : {str(e)}",
            }
        ), 500


@app.route("/api/code/list", methods=["GET"])
def list_code_files():
    """Renvoie la liste des fichiers éligibles pour le navigateur de code."""
    allowed_roots = ["src", "tests", "scripts"]
    allowed_files = [
        "Makefile",
        "pyproject.toml",
        ".pre-commit-config.yaml",
        ".gitignore",
        "Dockerfile",
        ".dockerignore",
        ".vscode/settings.json",
        ".vscode/extensions.json",
    ]

    files = []
    try:
        # Ajout des fichiers autorisés à la racine
        for fname in allowed_files:
            fpath = PROJECT_DIR / fname
            if fpath.exists() and fpath.is_file():
                files.append({"name": fname, "path": fname})

        # Parcours récursif des dossiers sources
        for rdir in allowed_roots:
            target_dir = PROJECT_DIR / rdir
            if target_dir.exists() and target_dir.is_dir():
                for path in sorted(target_dir.rglob("*")):
                    if path.is_file():
                        # Ignorer les répertoires de cache système
                        if "__pycache__" in path.parts or ".pytest_cache" in path.parts:
                            continue
                        rel_path = str(path.relative_to(PROJECT_DIR))
                        files.append({"name": path.name, "path": rel_path})

        files.sort(key=lambda x: x["path"])
        return jsonify({"status": "success", "files": files}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/code/file", methods=["GET"])
def get_code_file():
    """Renvoie le contenu textuel d'un fichier de code sécurisé."""
    file_path = request.args.get("path", "")
    if not file_path:
        return jsonify(
            {"status": "error", "message": "Chemin du fichier manquant"}
        ), 400

    try:
        # Sécurisation contre la traversée de répertoires (directory traversal)
        resolved_path = (PROJECT_DIR / file_path).resolve()
        project_resolved = PROJECT_DIR.resolve()

        if not str(resolved_path).startswith(str(project_resolved)):
            return jsonify({"status": "error", "message": "Accès interdit"}), 403

        # Interdiction d'accès aux répertoires masqués et système (.venv, .git)
        if ".venv" in resolved_path.parts or ".git" in resolved_path.parts:
            return jsonify(
                {"status": "error", "message": "Accès aux dossiers système interdit"}
            ), 403

        if not resolved_path.exists() or not resolved_path.is_file():
            return jsonify({"status": "error", "message": "Fichier introuvable"}), 404

        content = resolved_path.read_text(encoding="utf-8")
        return jsonify({"status": "success", "content": content}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
