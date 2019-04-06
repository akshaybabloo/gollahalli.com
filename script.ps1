param(
    [string]
    $Build,

    [bool]
    $Deploy
)

Import-Module .\secrets.ps1

function Log {

    param (
        [string]
        $Text
    )

    Write-Host $Text -ForegroundColor DarkGreen
}
function BuildHugo {
    Log -Text "PS> Building Hugo for Producation..."
    $Env:HUGO_ENV = "production"

    $public_folder = Join-Path -Path $PSScriptRoot -ChildPath "public"
    $resources_folder = Join-Path -Path $PSScriptRoot -ChildPath "resources"

    if (Test-Path -Path "$public_folder" -ErrorAction SilentlyContinue) {
        Log -Text "PS> 'public and resources' folders found, deleting it..."
        Remove-Item -Path "$public_folder" -Recurse -Force
        Remove-Item -Path "$resources_folder" -Recurse -Force
        Log -Text "PS> 'public and recources' folders deleted..."
        Start-Sleep -Seconds 1
    }

    Log -Text "PS> Building website..."
    hugo -v --minify --gc
    Log -Text "PS> Website built @ $public_folder"
}

if ($Build -eq "production") {
    BuildHugo
}

if ($Deploy) {
    BuildHugo

    Log -Text "PS> Deploying website..."
    firebase --version
    firebase deploy

    Log -Text "PS> Uploading search index to Algolia..."
    python ./utils.py
}

$Env:HUGO_ENV = "dev"
