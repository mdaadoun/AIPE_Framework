"""Unit tests for Dashboard API endpoints (Flask & Next.js backend logic)."""

import json
from pathlib import Path

from dashboard.app import (
    app as flask_app,
)
from dashboard.app import (
    get_doc_file,
    markdown_to_html,
    parse_faq_questions,
    parse_glossary_concepts,
)

PROJECT_DIR = Path(__file__).resolve().parent.parent


def test_markdown_to_html_formatting() -> None:
    """Verify markdown to HTML converter handles headers, lists, and bold text."""
    md = "# Title\n\n- Item 1\n- Item 2\n\n**Bold text**"
    html_out = markdown_to_html(md)

    assert "Title" in html_out
    assert "Item 1" in html_out
    assert "Bold text" in html_out


def test_get_doc_file_language_resolution() -> None:
    """Verify get_doc_file resolves language suffixes (_en.md and _fr.md)."""
    file_en = get_doc_file("presentation", "en")
    file_fr = get_doc_file("presentation", "fr")

    assert file_en.name == "presentation_en.md"
    assert file_fr.name == "presentation_fr.md"


def test_parse_faq_questions_structure() -> None:
    """Verify FAQ parser returns structured list of questions."""
    questions_en = parse_faq_questions("en")
    questions_fr = parse_faq_questions("fr")

    assert len(questions_en) > 0
    assert len(questions_fr) > 0
    assert "question" in questions_en[0]
    assert "answer_html" in questions_en[0]


def test_parse_glossary_concepts_structure() -> None:
    """Verify glossary parser extracts concepts and definitions."""
    concepts = parse_glossary_concepts("fr")

    assert len(concepts) > 0
    assert "concept" in concepts[0]
    assert "definition_html" in concepts[0]


def test_flask_presentation_endpoint() -> None:
    """Verify presentation markdown API returns rendered HTML."""
    client = flask_app.test_client()
    response = client.get("/api/presentation?lang=en")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert "html" in data


def test_flask_roadmap_endpoint() -> None:
    """Verify roadmap markdown API returns rendered HTML."""
    client = flask_app.test_client()
    response = client.get("/api/roadmap?lang=en")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert "html" in data


def test_flask_glossary_endpoints() -> None:
    """Verify glossary list and single concept detail API endpoints."""
    client = flask_app.test_client()

    list_res = client.get("/api/glossaire?lang=fr")
    assert list_res.status_code == 200
    list_data = json.loads(list_res.data)
    assert list_data["status"] == "success"

    detail_res = client.get("/api/glossaire/0?lang=fr")
    assert detail_res.status_code == 200
    detail_data = json.loads(detail_res.data)
    assert detail_data["status"] == "success"


def test_flask_journal_endpoints() -> None:
    """Verify journal list and article content endpoints."""
    client = flask_app.test_client()

    list_res = client.get("/api/journal?lang=fr")
    assert list_res.status_code == 200
    list_data = json.loads(list_res.data)
    assert list_data["status"] == "success"

    detail_res = client.get("/api/journal/intro?lang=fr")
    assert detail_res.status_code == 200
    detail_data = json.loads(detail_res.data)
    assert detail_data["status"] == "success"


def test_flask_entretien_endpoints() -> None:
    """Verify interview FAQ list and answer detail endpoints."""
    client = flask_app.test_client()

    list_res = client.get("/api/entretien?lang=fr")
    assert list_res.status_code == 200
    list_data = json.loads(list_res.data)
    assert list_data["status"] == "success"

    detail_res = client.get("/api/entretien/0?lang=fr")
    assert detail_res.status_code == 200
    detail_data = json.loads(detail_res.data)
    assert detail_data["status"] == "success"


def test_flask_tests_list_endpoint() -> None:
    """Verify tests scanner API returns pytest targets."""
    client = flask_app.test_client()
    response = client.get("/api/tests/list")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert len(data["tests"]) > 0


def test_flask_code_browser_endpoints() -> None:
    """Verify repository code file index and raw content API endpoints."""
    client = flask_app.test_client()

    list_res = client.get("/api/code/list")
    assert list_res.status_code == 200
    list_data = json.loads(list_res.data)
    assert list_data["status"] == "success"

    file_res = client.get("/api/code/file?path=pyproject.toml")
    assert file_res.status_code == 200
    file_data = json.loads(file_res.data)
    assert file_data["status"] == "success"
    assert "poetry" in file_data["content"]
