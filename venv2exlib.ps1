param(
    [string]$BlenderPython = $env:BLENDER_PYTHON,
    [string]$OutputSubdir,
    [switch]$SkipFreeze
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# PowerShell 7+: native command failures obey ErrorActionPreference
if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $true
}

function Invoke-UvOrThrow {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Args
    )

    & uv @Args
    if ($LASTEXITCODE -ne 0) {
        throw "uv command failed: uv $($Args -join ' ')"
    }
}

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    throw "uv command not found. Install uv first."
}

if (-not $SkipFreeze) {
    Write-Host "Updating requirements.txt..."
    uv pip freeze | Out-File -FilePath "requirements.txt" -Encoding utf8
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to update requirements.txt."
    }
}
else {
    Write-Host "Skipping requirements.txt update."
}

if ([string]::IsNullOrWhiteSpace($BlenderPython)) {
    throw "Blender Python path is required. Use -BlenderPython or BLENDER_PYTHON env var."
}

if (-not (Test-Path -LiteralPath $BlenderPython)) {
    throw "Blender Python not found: $BlenderPython"
}

if ([string]::IsNullOrWhiteSpace($OutputSubdir)) {
    $OutputSubdir = (& $BlenderPython -c "import sys; print(f'py{sys.version_info.major}{sys.version_info.minor}')").Trim()
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($OutputSubdir)) {
        throw "Failed to detect Python version tag from Blender Python."
    }
}

$targetRoot = Join-Path "ex-library" $OutputSubdir
if (Test-Path -LiteralPath $targetRoot) {
    Write-Host "Removing existing target: $targetRoot"
    Remove-Item -LiteralPath $targetRoot -Recurse -Force
}
New-Item -ItemType Directory -Path $targetRoot -Force | Out-Null

Write-Host "Installing dependencies into $targetRoot ..."
Invoke-UvOrThrow -Args @(
    "pip", "install",
    "-r", "requirements.txt",
    "--python", $BlenderPython,
    "--link-mode", "copy",
    "--target", $targetRoot
)

Write-Host "Done: $targetRoot updated."
# Optional zip:
# Compress-Archive -Path ".\ex-library\*" -DestinationPath ".\ex-library.zip" -Force
