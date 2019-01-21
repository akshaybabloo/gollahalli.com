param(
    [string]$Build,
    [bool]$Deploy
)

Import-Module .\secrets.ps1

function Log {
    param (
        [string]$Text
    )

    Write-Host $Text -ForegroundColor Magenta
}
function BuildHugo {
    Log -Text "Building Hugo for Producation..."
    $Env:HUGO_ENV = "production"

    $public_folder = Join-Path -Path $PSScriptRoot -ChildPath "public"
    $resources_folder = Join-Path -Path $PSScriptRoot -ChildPath "resources"

    if (Test-Path -Path "$public_folder" -ErrorAction SilentlyContinue) {
        Log -Text "'public and resources' folders found, deleting it..."
        Remove-Item -Path "$public_folder" -Recurse -Force
        Remove-Item -Path "$resources_folder" -Recurse -Force
        Log -Text "'public and recources' folders deleted..."
        Start-Sleep -Seconds 1
    }

    Log -Text "Building website..."
    hugo -v --minify --gc
    Log -Text "Website built @ $public_folder"
}

if ($Build -eq "production") {
    BuildHugo
}

if ($Deploy) {
    BuildHugo

    Log -Text "Deploying website..."
    firebase deploy

    Log -Text "Uploading search index to Algolia..."
    python ./utils.py
}

$Env:HUGO_ENV = "dev"
