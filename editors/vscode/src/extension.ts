/**
 * SkillScan Security — VS Code Extension
 *
 * Runs `skillscan` on MCP skill files (SKILL.md, CLAUDE.md, *.yaml) and
 * surfaces findings as VS Code diagnostics (squiggles + Problems panel).
 *
 * Design: thin shell wrapper — no bundled Python, no network calls.
 * The user must have `skillscan` installed (`pip install skillscan-security`).
 */

import * as vscode from "vscode";
import { execFile } from "child_process";
import * as path from "path";

// ---------------------------------------------------------------------------
// Types matching skillscan's --format sarif output
// ---------------------------------------------------------------------------

interface SarifResult {
  ruleId: string;
  level?: "error" | "warning" | "note" | "none";
  message: { text: string };
  locations?: Array<{
    physicalLocation?: {
      artifactLocation?: { uri: string };
      region?: { startLine?: number; startColumn?: number; endLine?: number; endColumn?: number };
    };
  }>;
}

interface SarifRun {
  results?: SarifResult[];
}

interface SarifLog {
  runs?: SarifRun[];
}

// ---------------------------------------------------------------------------
// Extension state
// ---------------------------------------------------------------------------

let diagnosticCollection: vscode.DiagnosticCollection;
let statusBarItem: vscode.StatusBarItem;
let outputChannel: vscode.OutputChannel;

// ---------------------------------------------------------------------------
// Activation
// ---------------------------------------------------------------------------

export function activate(context: vscode.ExtensionContext): void {
  diagnosticCollection = vscode.languages.createDiagnosticCollection("skillscan");
  outputChannel = vscode.window.createOutputChannel("SkillScan");

  statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
  statusBarItem.command = "skillscan.openResults";
  statusBarItem.text = "$(shield) SkillScan";
  statusBarItem.tooltip = "SkillScan Security — click to show results";
  statusBarItem.show();

  context.subscriptions.push(
    diagnosticCollection,
    statusBarItem,
    outputChannel,

    vscode.commands.registerCommand("skillscan.scanFile", () => {
      const editor = vscode.window.activeTextEditor;
      if (editor) {
        scanFile(editor.document.uri);
      }
    }),

    vscode.commands.registerCommand("skillscan.scanWorkspace", () => {
      scanWorkspace();
    }),

    vscode.commands.registerCommand("skillscan.openResults", () => {
      outputChannel.show();
    }),

    // Auto-scan on save if enabled
    vscode.workspace.onDidSaveTextDocument((doc) => {
      const cfg = vscode.workspace.getConfiguration("skillscan");
      if (cfg.get<boolean>("scanOnSave", true) && isSkillFile(doc.uri)) {
        scanFile(doc.uri);
      }
    }),

    // Clear diagnostics when file is closed
    vscode.workspace.onDidCloseTextDocument((doc) => {
      diagnosticCollection.delete(doc.uri);
    }),
  );

  // Scan already-open skill files on activation
  vscode.workspace.textDocuments.forEach((doc) => {
    if (isSkillFile(doc.uri)) {
      scanFile(doc.uri);
    }
  });
}

export function deactivate(): void {
  diagnosticCollection?.dispose();
}

// ---------------------------------------------------------------------------
// File detection
// ---------------------------------------------------------------------------

function isSkillFile(uri: vscode.Uri): boolean {
  const base = path.basename(uri.fsPath).toLowerCase();
  const ext = path.extname(uri.fsPath).toLowerCase();
  return (
    base === "skill.md" ||
    base === "claude.md" ||
    base === ".mcp.json" ||
    ext === ".md" ||
    ext === ".yaml" ||
    ext === ".yml"
  );
}

// ---------------------------------------------------------------------------
// Scanning
// ---------------------------------------------------------------------------

function getExecutable(): string {
  return vscode.workspace.getConfiguration("skillscan").get<string>("executablePath", "skillscan");
}

function getExtraArgs(): string[] {
  return vscode.workspace.getConfiguration("skillscan").get<string[]>("extraArgs", []);
}

function getFailOn(): string {
  return vscode.workspace.getConfiguration("skillscan").get<string>("failOn", "warn");
}

function getRulesPath(): string {
  return vscode.workspace.getConfiguration("skillscan").get<string>("rulesPath", "");
}

function buildArgs(target: string): string[] {
  const args = ["scan", target, "--format", "sarif"];
  const rulesPath = getRulesPath();
  if (rulesPath) {
    args.push("--rules", rulesPath);
  }
  args.push(...getExtraArgs());
  return args;
}

function severityToDiagnostic(level: string | undefined, failOn: string): vscode.DiagnosticSeverity {
  const order = ["error", "warning", "note", "none"];
  const failIdx = order.indexOf(failOn === "block" ? "error" : failOn === "warn" ? "warning" : "note");
  const levelIdx = order.indexOf(level ?? "warning");
  if (levelIdx <= failIdx) {
    return vscode.DiagnosticSeverity.Error;
  }
  if (level === "note" || level === "none") {
    return vscode.DiagnosticSeverity.Information;
  }
  return vscode.DiagnosticSeverity.Warning;
}

function scanFile(uri: vscode.Uri): void {
  const exe = getExecutable();
  const args = buildArgs(uri.fsPath);
  const failOn = getFailOn();

  statusBarItem.text = "$(sync~spin) SkillScan";

  execFile(exe, args, { cwd: vscode.workspace.workspaceFolders?.[0]?.uri.fsPath }, (err, stdout, stderr) => {
    statusBarItem.text = "$(shield) SkillScan";

    if (stderr) {
      outputChannel.appendLine(`[stderr] ${stderr}`);
    }

    // skillscan exits non-zero when findings are present — that's expected
    if (err && !stdout) {
      // Real error (e.g. executable not found)
      if ((err as NodeJS.ErrnoException).code === "ENOENT") {
        vscode.window.showErrorMessage(
          `SkillScan: executable '${exe}' not found. Run: pip install skillscan-security`,
          "Install docs",
        ).then((choice) => {
          if (choice === "Install docs") {
            vscode.env.openExternal(vscode.Uri.parse("https://skillscan.sh/docs#install"));
          }
        });
      }
      diagnosticCollection.set(uri, []);
      return;
    }

    try {
      const sarif: SarifLog = JSON.parse(stdout);
      const diagnostics: vscode.Diagnostic[] = [];

      for (const run of sarif.runs ?? []) {
        for (const result of run.results ?? []) {
          const loc = result.locations?.[0]?.physicalLocation;
          const region = loc?.region;

          const startLine = Math.max(0, (region?.startLine ?? 1) - 1);
          const startCol = Math.max(0, (region?.startColumn ?? 1) - 1);
          const endLine = Math.max(0, (region?.endLine ?? startLine + 1) - 1);
          const endCol = region?.endColumn ? region.endColumn - 1 : startCol + 80;

          const range = new vscode.Range(startLine, startCol, endLine, endCol);
          const severity = severityToDiagnostic(result.level, failOn);
          const message = `[${result.ruleId}] ${result.message.text}`;

          const diag = new vscode.Diagnostic(range, message, severity);
          diag.source = "skillscan";
          diag.code = {
            value: result.ruleId,
            target: vscode.Uri.parse(`https://skillscan.sh/rules/${result.ruleId.toLowerCase()}`),
          };
          diagnostics.push(diag);
        }
      }

      diagnosticCollection.set(uri, diagnostics);

      const count = diagnostics.length;
      if (count > 0) {
        const errors = diagnostics.filter((d) => d.severity === vscode.DiagnosticSeverity.Error).length;
        statusBarItem.text = `$(shield) SkillScan $(error)${errors > 0 ? errors : ""}`;
        outputChannel.appendLine(`[${path.basename(uri.fsPath)}] ${count} finding(s)`);
      } else {
        statusBarItem.text = "$(shield) SkillScan $(check)";
      }
    } catch {
      outputChannel.appendLine(`[parse error] Could not parse SARIF output from skillscan`);
      outputChannel.appendLine(stdout.slice(0, 500));
    }
  });
}

function scanWorkspace(): void {
  const folders = vscode.workspace.workspaceFolders;
  if (!folders) {
    vscode.window.showWarningMessage("SkillScan: No workspace folder open.");
    return;
  }

  diagnosticCollection.clear();

  vscode.workspace.findFiles("**/{SKILL,CLAUDE}.md", "**/node_modules/**").then((uris) => {
    if (uris.length === 0) {
      vscode.window.showInformationMessage("SkillScan: No SKILL.md or CLAUDE.md files found in workspace.");
      return;
    }
    outputChannel.appendLine(`[workspace scan] Found ${uris.length} skill file(s)`);
    uris.forEach((uri) => scanFile(uri));
  });
}
