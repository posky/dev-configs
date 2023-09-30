$ScriptPath = Join-Path -Path (Split-Path (Split-Path $MyInvocation.MyCommand.Path -Parent) -Parent) -ChildPath "vscode/windows/update.ps1"
. $ScriptPath