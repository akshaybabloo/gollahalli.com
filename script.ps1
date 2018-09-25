param(
    [string]$build,
    [bool]$deploy,
    [bool]$clean
)

Import-Module .\secrets.ps1

function log {
    param (
        [string]$text
    )

    Write-Host $text -ForegroundColor Magenta
}
function BuildHugo {
    log("Building Hugo for Producation...")
    $Env:HUGO_ENV = "production"

    $public_folder = Join-Path -Path $PSScriptRoot -ChildPath "public"

    if (Test-Path -Path "$public_folder" -ErrorAction SilentlyContinue) {
        log("'public' folder found, deleting it...")
        Remove-Item -Path "$public_folder" -Recurse
        log("'public' folder deleted...")
        Start-Sleep -Seconds 1
    }

    log("Building website...")
    hugo -v --minify --gc
    log("Website built @ $public_folder")
}

if ($build -eq "production") {
    BuildHugo
}

if ($deploy) {
    BuildHugo

    log("Deploying website...")
    firebase deploy

    log("Uploading search index to Algolia...")
    python .\algolia.py
    log("Done!")
}
