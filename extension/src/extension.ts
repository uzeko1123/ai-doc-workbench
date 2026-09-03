// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from "vscode";
import * as path from "path";

const workspacePath = vscode.workspace.workspaceFolders![0].uri.fsPath;
const pythonPath = path.join(
  workspacePath,
  "tools",
  ".venv",
  "Scripts",
  "python.exe",
);

function runPythonScript(scriptPath: string, args: string[]) {
  const command = [pythonPath, scriptPath, ...args]
    .map((arg) => `"${arg}"`)
    .join(" ");
  const terminalName = "ai-doc-workbench";
  const terminal =
    vscode.window.terminals.find((t) => t.name === terminalName) ??
    vscode.window.createTerminal(terminalName);
  terminal.show();
  terminal.sendText(command);
}

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {
  // Use the console to output diagnostic information (console.log) and errors (console.error)
  // This line of code will only be executed once when your extension is activated
  console.log(
    'Congratulations, your extension "ai-doc-workbench" is now active!',
  );

  // The command has been defined in the package.json file
  // Now provide the implementation of the command with registerCommand
  // The commandId parameter must match the command field in package.json
  const disposable_convert = vscode.commands.registerCommand(
    "ai-doc-workbench.convert",
    (uri: vscode.Uri) => {
      const scriptPath = path.join(workspacePath, "tools", "convert.py");
      const args = [uri.fsPath];
      runPythonScript(scriptPath, args);
    },
  );
  const disposable_export = vscode.commands.registerCommand(
    "ai-doc-workbench.export",
    (uri: vscode.Uri) => {
      const scriptPath = path.join(workspacePath, "tools", "export.py");
      const args = [uri.fsPath];
      runPythonScript(scriptPath, args);
    },
  );

  context.subscriptions.push(disposable_convert, disposable_export);
}

// This method is called when your extension is deactivated
export function deactivate() {}
