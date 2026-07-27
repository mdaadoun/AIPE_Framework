import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";
import { PROJECT_DIR } from "@/lib/docs";

export async function GET() {
  const testsDir = path.join(PROJECT_DIR, "tests");
  if (!fs.existsSync(testsDir) || !fs.statSync(testsDir).isDirectory()) {
    return NextResponse.json({ status: "success", tests: [] });
  }

  try {
    const testList: any[] = [
      {
        id: "all",
        name: "🧪 Full Test Suite (pytest)",
        file: "all",
        docstring: "Executes full unit and integration test suite.",
        type: "suite",
      },
    ];

    const files = fs.readdirSync(testsDir);
    const testFiles = files.filter((f) => f.startsWith("test_") && f.endsWith(".py")).sort();

    for (const fileName of testFiles) {
      const relPath = `tests/${fileName}`;
      const fullPath = path.join(testsDir, fileName);
      const fileContent = fs.readFileSync(fullPath, "utf-8");

      let fileDoc = "";
      const docMatch = fileContent.match(/^(?:'''|""")([\s\S]*?)(?:'''|""")/);
      if (docMatch) {
        fileDoc = docMatch[1].trim();
      }

      testList.push({
        id: relPath,
        name: `📁 ${fileName} (Full File)`,
        file: relPath,
        docstring: fileDoc || `Executes all tests in ${fileName}.`,
        type: "file",
      });

      const funcRegex = /def\s+(test_[a-zA-Z0-9_]+)\s*\([^)]*\)\s*:/g;
      let match: RegExpExecArray | null;
      while ((match = funcRegex.exec(fileContent)) !== null) {
        const funcName = match[1];
        const testId = `${relPath}::${funcName}`;

        testList.push({
          id: testId,
          name: `   └─ ${funcName}`,
          file: relPath,
          docstring: "Unit test function.",
          type: "function",
        });
      }
    }

    return NextResponse.json({ status: "success", tests: testList });
  } catch (error: any) {
    return NextResponse.json(
      { status: "error", message: error.message },
      { status: 500 }
    );
  }
}
