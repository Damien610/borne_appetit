param(
    [string]$PythonCmd = "py"
)

$ErrorActionPreference = "Stop"

# Script PowerShell pour packager le code Lambda (Windows)
Set-Location -Path $PSScriptRoot

# Creer un repertoire temporaire
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
}
New-Item -ItemType Directory -Path "build" | Out-Null

# Copier le code source
Copy-Item -Recurse -Force "src\*" "build\"

# Installer les dependances Python
& $PythonCmd -m pip install -t "build\" PyJWT boto3 --quiet

# Creer le zip
if (Test-Path "lambda.zip") {
    Remove-Item -Force "lambda.zip"
}
Compress-Archive -Path "build\*" -DestinationPath "lambda.zip" -Force

# Nettoyer
Remove-Item -Recurse -Force "build"

Write-Host "Lambda package created: lambda.zip"
