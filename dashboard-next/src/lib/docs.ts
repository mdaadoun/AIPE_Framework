import fs from "fs";
import path from "path";
import { markdownToHtml } from "./markdown";

// Resolve project root (parent of dashboard-next)
export const PROJECT_DIR = path.resolve(process.cwd(), "..");
export const DOCS_DIR = path.join(PROJECT_DIR, "docs");

const ALIASES: Record<string, string> = {
  roadmap_details: "roadmap",
  faq_entretien: "questions",
  glossaire: "glossary",
  journal_apprentissage: "journal",
  cahier_charges: "specifications",
};

export function getDocFile(baseName: string, lang: string = "en"): string {
  const resolvedName = ALIASES[baseName] || baseName;
  const suffix = lang === "en" ? "_en" : "_fr";
  const targetPath = path.join(DOCS_DIR, `${resolvedName}${suffix}.md`);
  if (fs.existsSync(targetPath)) {
    return targetPath;
  }

  const fallbackSuffix = lang === "en" ? "_fr" : "_en";
  const fallbackPath = path.join(DOCS_DIR, `${resolvedName}${fallbackSuffix}.md`);
  if (fs.existsSync(fallbackPath)) {
    return fallbackPath;
  }

  return path.join(DOCS_DIR, `${resolvedName}.md`);
}

export interface FaqQuestion {
  question: string;
  answer_markdown: string;
  answer_html: string;
}

export function parseFaqQuestions(lang: string = "en"): FaqQuestion[] {
  const faqFile = getDocFile("questions", lang);
  if (!fs.existsSync(faqFile)) return [];

  const content = fs.readFileSync(faqFile, "utf-8");
  const questions: FaqQuestion[] = [];

  const parts = content.split(/### Q\d+\.\s*/);
  for (let i = 1; i < parts.length; i++) {
    const lines = parts[i].trim().split("\n");
    if (lines.length === 0) continue;
    const title = lines[0].trim();
    const body = lines.slice(1).join("\n").trim();
    questions.push({
      question: title,
      answer_markdown: body,
      answer_html: markdownToHtml(body),
    });
  }
  return questions;
}

export interface GlossaryConcept {
  id: number;
  concept: string;
  definition_markdown: string;
  definition_html: string;
}

export function parseGlossaryConcepts(lang: string = "en"): GlossaryConcept[] {
  const glossaireFile = getDocFile("glossary", lang);
  if (!fs.existsSync(glossaireFile)) return [];

  const content = fs.readFileSync(glossaireFile, "utf-8");
  const concepts: GlossaryConcept[] = [];

  const parts = content.split(/### /);
  for (let i = 1; i < parts.length; i++) {
    const lines = parts[i].trim().split("\n");
    if (lines.length === 0) continue;
    const conceptName = lines[0].trim();
    const definition = lines.slice(1).join("\n").trim();
    concepts.push({
      id: concepts.length,
      concept: conceptName,
      definition_markdown: definition,
      definition_html: markdownToHtml(definition),
    });
  }
  return concepts;
}

export interface JournalEntryInfo {
  id: string;
  title: string;
  date: string;
}

export function parseJournalFileInfo(filePath: string, fileId: string): JournalEntryInfo {
  try {
    const content = fs.readFileSync(filePath, "utf-8");
    let title: string | null = null;
    let date = "Unknown date";

    for (const line of content.split("\n")) {
      const lineStr = line.trim();
      if (lineStr.startsWith("# ") && title === null) {
        let rawTitle = lineStr.slice(2).trim();
        if (rawTitle.startsWith("📌")) {
          rawTitle = rawTitle.slice(1).trim();
        }
        title = rawTitle;
      } else if (lineStr.includes("Date") && (lineStr.includes(":") || lineStr.includes("**"))) {
        const dateMatch = lineStr.match(/\*\*Date\s*:?\s*\*\*:?\s*(.*)/i);
        if (dateMatch && dateMatch[1].trim()) {
          date = dateMatch[1].trim();
        } else {
          date = lineStr
            .replace("Date :", "")
            .replace("Date:", "")
            .replace(/\*\*/g, "")
            .trim();
        }
      }
    }

    if (!title) {
      title = path.basename(filePath, ".md").replace(/_/g, " ");
      title = title.charAt(0).toUpperCase() + title.slice(1);
    }

    return { id: fileId, title, date };
  } catch {
    return {
      id: fileId,
      title: path.basename(filePath, ".md").replace(/_/g, " "),
      date: "Unknown date",
    };
  }
}

export function parseRoadmapToHtml(lang: string = "en"): string {
  const roadmapFile = getDocFile("roadmap", lang);
  if (!fs.existsSync(roadmapFile)) {
    return "<div style='color: var(--danger); padding: 20px;'>Roadmap file not found.</div>";
  }

  try {
    const content = fs.readFileSync(roadmapFile, "utf-8");
    return markdownToHtml(content);
  } catch (e: any) {
    return `<div style='color: var(--danger); padding: 20px;'>Read error: ${e.message}</div>`;
  }
}
