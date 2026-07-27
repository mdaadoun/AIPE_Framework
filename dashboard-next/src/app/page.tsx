"use client";

import React, { useState, useEffect } from "react";
import {
  FileText,
  Map,
  BookOpen,
  BookText,
  HelpCircle,
  Play,
  Code,
  Globe,
  CheckCircle,
  XCircle,
  Loader2,
  Terminal,
} from "lucide-react";

type TabType =
  | "presentation"
  | "roadmap"
  | "glossary"
  | "journal"
  | "entretien"
  | "tests"
  | "code";

interface QuestionItem {
  id: number;
  question: string;
}

interface ConceptItem {
  id: number;
  concept: string;
}

interface JournalItem {
  id: string;
  title: string;
  date: string;
}

interface TestItem {
  id: string;
  name: string;
  file: string;
  docstring: string;
  type: string;
}

interface CodeFileItem {
  name: string;
  path: string;
}

export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState<TabType>("roadmap");
  const [lang, setLang] = useState<"en" | "fr">("en");

  // Content states
  const [presentationHtml, setPresentationHtml] = useState("");
  const [roadmapHtml, setRoadmapHtml] = useState("");

  // Interview state
  const [questions, setQuestions] = useState<QuestionItem[]>([]);
  const [selectedQuestionId, setSelectedQuestionId] = useState<number | null>(null);
  const [answerHtml, setAnswerHtml] = useState("");
  const [loadingAnswer, setLoadingAnswer] = useState(false);

  // Glossary state
  const [concepts, setConcepts] = useState<ConceptItem[]>([]);
  const [selectedConceptId, setSelectedConceptId] = useState<number | null>(null);
  const [conceptHtml, setConceptHtml] = useState("");
  const [conceptSearch, setConceptSearch] = useState("");

  // Journal state
  const [journalEntries, setJournalEntries] = useState<JournalItem[]>([]);
  const [selectedJournalId, setSelectedJournalId] = useState<string>("intro");
  const [journalHtml, setJournalHtml] = useState("");

  // Test Runner state
  const [testList, setTestList] = useState<TestItem[]>([]);
  const [selectedTestId, setSelectedTestId] = useState<string>("all");
  const [runningTest, setRunningTest] = useState(false);
  const [testResult, setTestResult] = useState<{
    status: string;
    message: string;
    stdout: string;
    stderr: string;
    exit_code?: number;
  } | null>(null);

  // Code Browser state
  const [codeFiles, setCodeFiles] = useState<CodeFileItem[]>([]);
  const [selectedFilePath, setSelectedFilePath] = useState<string>("Makefile");
  const [codeContent, setCodeContent] = useState("");

  // Fetch Presentation
  useEffect(() => {
    if (activeTab === "presentation") {
      fetch(`/api/presentation?lang=${lang}`)
        .then((res) => res.json())
        .then((data) => setPresentationHtml(data.html || ""));
    }
  }, [activeTab, lang]);

  // Fetch Roadmap
  useEffect(() => {
    if (activeTab === "roadmap") {
      fetch(`/api/roadmap?lang=${lang}`)
        .then((res) => res.json())
        .then((data) => setRoadmapHtml(data.html || ""));
    }
  }, [activeTab, lang]);

  // Fetch Interview Questions
  useEffect(() => {
    if (activeTab === "entretien") {
      fetch(`/api/entretien?lang=${lang}`)
        .then((res) => res.json())
        .then((data) => {
          setQuestions(data.questions || []);
          if (data.questions && data.questions.length > 0) {
            setSelectedQuestionId(0);
          }
        });
    }
  }, [activeTab, lang]);

  // Fetch Interview Answer
  useEffect(() => {
    if (selectedQuestionId !== null && activeTab === "entretien") {
      setLoadingAnswer(true);
      fetch(`/api/entretien/${selectedQuestionId}?lang=${lang}`)
        .then((res) => res.json())
        .then((data) => {
          setAnswerHtml(data.answer_html || "");
          setLoadingAnswer(false);
        });
    }
  }, [selectedQuestionId, lang, activeTab]);

  // Fetch Glossary Concepts
  useEffect(() => {
    if (activeTab === "glossary") {
      fetch(`/api/glossaire?lang=${lang}`)
        .then((res) => res.json())
        .then((data) => {
          setConcepts(data.concepts || []);
          if (data.concepts && data.concepts.length > 0) {
            setSelectedConceptId(0);
          }
        });
    }
  }, [activeTab, lang]);

  // Fetch Glossary Concept Detail
  useEffect(() => {
    if (selectedConceptId !== null && activeTab === "glossary") {
      fetch(`/api/glossaire/${selectedConceptId}?lang=${lang}`)
        .then((res) => res.json())
        .then((data) => setConceptHtml(data.html || ""));
    }
  }, [selectedConceptId, lang, activeTab]);

  // Fetch Journal List
  useEffect(() => {
    if (activeTab === "journal") {
      fetch(`/api/journal?lang=${lang}`)
        .then((res) => res.json())
        .then((data) => {
          setJournalEntries(data.entries || []);
        });
    }
  }, [activeTab, lang]);

  // Fetch Journal Content
  useEffect(() => {
    if (activeTab === "journal" && selectedJournalId) {
      fetch(`/api/journal/${selectedJournalId}?lang=${lang}`)
        .then((res) => res.json())
        .then((data) => setJournalHtml(data.html || ""));
    }
  }, [selectedJournalId, lang, activeTab]);

  // Fetch Test List
  useEffect(() => {
    if (activeTab === "tests") {
      fetch(`/api/tests/list`)
        .then((res) => res.json())
        .then((data) => setTestList(data.tests || []));
    }
  }, [activeTab]);

  // Fetch Code File List
  useEffect(() => {
    if (activeTab === "code") {
      fetch(`/api/code/list`)
        .then((res) => res.json())
        .then((data) => setCodeFiles(data.files || []));
    }
  }, [activeTab]);

  // Fetch Code File Content
  useEffect(() => {
    if (activeTab === "code" && selectedFilePath) {
      fetch(`/api/code/file?path=${encodeURIComponent(selectedFilePath)}`)
        .then((res) => res.json())
        .then((data) => setCodeContent(data.content || ""));
    }
  }, [selectedFilePath, activeTab]);

  // Run Test Action
  const handleRunTest = async () => {
    setRunningTest(true);
    setTestResult(null);
    try {
      const res = await fetch("/api/run-tests", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ test_name: selectedTestId }),
      });
      const data = await res.json();
      setTestResult(data);
    } catch (e: any) {
      setTestResult({
        status: "error",
        message: e.message,
        stdout: "",
        stderr: e.message,
      });
    } finally {
      setRunningTest(false);
    }
  };

  const filteredConcepts = concepts.filter((c) =>
    c.concept.toLowerCase().includes(conceptSearch.toLowerCase())
  );

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header>
        <div className="header-container">
          <div className="logo">
            <span>🚀 AIPE_Framework</span>
            <span className="text-xs px-2 py-1 rounded bg-purple-900/50 text-purple-300 font-mono">
              Next.js TypeScript
            </span>
          </div>

          <div className="flex items-center gap-4">
            {/* Nav Tabs */}
            <nav className="nav-tabs">
              <button
                onClick={() => setActiveTab("roadmap")}
                className={`tab-btn ${activeTab === "roadmap" ? "active" : ""}`}
              >
                <Map size={15} />
                <span>Roadmap</span>
              </button>
              <button
                onClick={() => setActiveTab("presentation")}
                className={`tab-btn ${activeTab === "presentation" ? "active" : ""}`}
              >
                <FileText size={15} />
                <span>Presentation</span>
              </button>
              <button
                onClick={() => setActiveTab("glossary")}
                className={`tab-btn ${activeTab === "glossary" ? "active" : ""}`}
              >
                <BookOpen size={15} />
                <span>Glossary</span>
              </button>
              <button
                onClick={() => setActiveTab("journal")}
                className={`tab-btn ${activeTab === "journal" ? "active" : ""}`}
              >
                <BookText size={15} />
                <span>Journal</span>
              </button>
              <button
                onClick={() => setActiveTab("entretien")}
                className={`tab-btn ${activeTab === "entretien" ? "active" : ""}`}
              >
                <HelpCircle size={15} />
                <span>FAQ Interview</span>
              </button>
              <button
                onClick={() => setActiveTab("tests")}
                className={`tab-btn ${activeTab === "tests" ? "active" : ""}`}
              >
                <Play size={15} />
                <span>Test Runner</span>
              </button>
              <button
                onClick={() => setActiveTab("code")}
                className={`tab-btn ${activeTab === "code" ? "active" : ""}`}
              >
                <Code size={15} />
                <span>Code Browser</span>
              </button>
            </nav>

            {/* Language Switcher */}
            <div className="lang-switch">
              <button
                onClick={() => setLang("en")}
                className={`lang-btn ${lang === "en" ? "active" : ""}`}
              >
                EN
              </button>
              <button
                onClick={() => setLang("fr")}
                className={`lang-btn ${lang === "fr" ? "active" : ""}`}
              >
                FR
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main>
        <div className="content-card">
          {/* TAB: ROADMAP */}
          {activeTab === "roadmap" && (
            <div
              className="markdown-body"
              dangerouslySetInnerHTML={{ __html: roadmapHtml }}
            />
          )}

          {/* TAB: PRESENTATION */}
          {activeTab === "presentation" && (
            <div
              className="markdown-body"
              dangerouslySetInnerHTML={{ __html: presentationHtml }}
            />
          )}

          {/* TAB: GLOSSARY */}
          {activeTab === "glossary" && (
            <div className="interview-grid">
              <div className="question-list-panel">
                <input
                  type="text"
                  placeholder="Search concepts..."
                  value={conceptSearch}
                  onChange={(e) => setConceptSearch(e.target.value)}
                  style={{
                    padding: "8px 12px",
                    borderRadius: "6px",
                    border: "1px solid var(--border)",
                    background: "rgba(255,255,255,0.03)",
                    color: "var(--text-main)",
                    fontFamily: "var(--font-outfit)",
                    marginBottom: "8px",
                  }}
                />
                {filteredConcepts.map((item) => (
                  <button
                    key={item.id}
                    onClick={() => setSelectedConceptId(item.id)}
                    className={`question-item ${selectedConceptId === item.id ? "active" : ""}`}
                  >
                    {item.concept}
                  </button>
                ))}
              </div>
              <div
                className="answer-panel markdown-body"
                dangerouslySetInnerHTML={{ __html: conceptHtml }}
              />
            </div>
          )}

          {/* TAB: JOURNAL */}
          {activeTab === "journal" && (
            <div className="interview-grid">
              <div className="question-list-panel">
                {journalEntries.map((item) => (
                  <button
                    key={item.id}
                    onClick={() => setSelectedJournalId(item.id)}
                    className={`question-item ${selectedJournalId === item.id ? "active" : ""}`}
                  >
                    <div style={{ fontWeight: 600 }}>{item.title}</div>
                    <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", marginTop: "4px" }}>
                      📅 {item.date}
                    </div>
                  </button>
                ))}
              </div>
              <div
                className="answer-panel markdown-body"
                dangerouslySetInnerHTML={{ __html: journalHtml }}
              />
            </div>
          )}

          {/* TAB: FAQ INTERVIEW */}
          {activeTab === "entretien" && (
            <div className="interview-grid">
              <div className="question-list-panel">
                {questions.map((q) => (
                  <button
                    key={q.id}
                    onClick={() => setSelectedQuestionId(q.id)}
                    className={`question-item ${selectedQuestionId === q.id ? "active" : ""}`}
                  >
                    Q{q.id + 1}. {q.question}
                  </button>
                ))}
              </div>
              <div className="answer-panel">
                {loadingAnswer ? (
                  <div className="flex items-center gap-2 text-purple-400">
                    <Loader2 className="animate-spin" size={18} />
                    <span>Loading response...</span>
                  </div>
                ) : (
                  <div
                    className="markdown-body"
                    dangerouslySetInnerHTML={{ __html: answerHtml }}
                  />
                )}
              </div>
            </div>
          )}

          {/* TAB: TEST RUNNER */}
          {activeTab === "tests" && (
            <div className="grid-two-col">
              <div className="file-list-sidebar">
                <h4 style={{ fontFamily: "var(--font-outfit)", marginBottom: "8px", color: "var(--secondary)" }}>
                  Dynamic Test Suite
                </h4>
                {testList.map((item) => (
                  <button
                    key={item.id}
                    onClick={() => setSelectedTestId(item.id)}
                    className={`file-item ${selectedTestId === item.id ? "active" : ""}`}
                  >
                    {item.name}
                  </button>
                ))}
              </div>

              <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <div>
                    <h3 style={{ fontFamily: "var(--font-outfit)", fontSize: "1.1rem" }}>
                      Target: <span style={{ color: "var(--secondary)" }}>{selectedTestId}</span>
                    </h3>
                  </div>

                  <button
                    onClick={handleRunTest}
                    disabled={runningTest}
                    className="btn-run"
                  >
                    {runningTest ? (
                      <>
                        <Loader2 className="animate-spin" size={16} />
                        <span>Running pytest...</span>
                      </>
                    ) : (
                      <>
                        <Play size={16} />
                        <span>Run Selected Test</span>
                      </>
                    )}
                  </button>
                </div>

                {/* Execution Result Output */}
                {testResult && (
                  <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                    <div className={`badge ${testResult.status === "success" ? "badge-completed" : "badge-pending"}`}>
                      {testResult.status === "success" ? (
                        <span className="flex items-center gap-1">
                          <CheckCircle size={14} /> Passed (Exit 0)
                        </span>
                      ) : (
                        <span className="flex items-center gap-1" style={{ color: "var(--danger)" }}>
                          <XCircle size={14} /> Failed (Exit {testResult.exit_code || 1})
                        </span>
                      )}
                    </div>

                    <div className="code-viewer-container">
                      <pre className="code-block">
                        {testResult.stdout || testResult.stderr || testResult.message}
                      </pre>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* TAB: CODE BROWSER */}
          {activeTab === "code" && (
            <div className="grid-two-col">
              <div className="file-list-sidebar">
                <h4 style={{ fontFamily: "var(--font-outfit)", marginBottom: "8px", color: "var(--secondary)" }}>
                  Project Repository Files
                </h4>
                {codeFiles.map((file) => (
                  <button
                    key={file.path}
                    onClick={() => setSelectedFilePath(file.path)}
                    className={`file-item ${selectedFilePath === file.path ? "active" : ""}`}
                  >
                    📄 {file.path}
                  </button>
                ))}
              </div>

              <div className="code-viewer-container">
                <div style={{ paddingBottom: "8px", borderBottom: "1px solid var(--border)", marginBottom: "12px", fontFamily: "var(--font-fira)", fontSize: "0.8rem", color: "var(--secondary)" }}>
                  {selectedFilePath}
                </div>
                <pre className="code-block">{codeContent}</pre>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer style={{ marginTop: "auto", padding: "20px 40px", borderTop: "1px solid var(--border)", textAlign: "center", fontSize: "0.75rem", color: "var(--text-muted)" }}>
        AIPE_Framework Next.js TypeScript Industrial Dashboard — Antigravity Pair Programming
      </footer>
    </div>
  );
}
