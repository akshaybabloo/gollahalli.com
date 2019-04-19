<#
.SYNOPSIS
    This script builds and deploys Hugo website to firebase.
.DESCRIPTION
    This script fist checks if the "public" folder exists or not, if so it deletes it.
    Then it builds the website with the correct environment variable (just build or deply it).
    If "Deploy" is set to "1", then this scrips calls the "firebase" CLI to deploy the public folder.
    Once that is done, it calls a Python script that publishes new index to Algolia, pings Google and Bing.
.NOTES
    Author
    File Name  : Build-Hugo.ps1
    Author     : Akshay Raj Gollahalli - akshay@gollahalli.com
.LINK
    https://github.com/akshaybabloo/gollahalli.com
.EXAMPLE
    Build-Hugo -Build production
    Builds Hugo website for production and does NOT deploy it.
.EXAMPLE
    Build-Hugo -Deploy 1
    Builds and deploys Hugo to firebase.
#>
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
        $Text,

        [bool]
        $NewLine
    )

    if ($NewLine) {
        Write-Host ("`e[1m" + $Text + "`e[0m") -ForegroundColor DarkGreen -NoNewline
    }
    else {
        Write-Host ("`e[1m" + $Text + "`e[0m") -ForegroundColor DarkGreen
    }
}
function BuildHugo {
    Log -Text "PS> Building Hugo for Producation..."
    $Env:HUGO_ENV = "production"

    $public_folder = Join-Path -Path $PSScriptRoot -ChildPath "public"
    $resources_folder = Join-Path -Path $PSScriptRoot -ChildPath "resources"

    if (Test-Path -Path "$public_folder" -ErrorAction SilentlyContinue) {
        Log -Text "PS> 'public and resources' folders found, deleting it..." -Newline 1
        Remove-Item -Path "$public_folder" -Recurse -Force
        Remove-Item -Path "$resources_folder" -Recurse -Force
        Log -Text "Done"
        Start-Sleep -Seconds 1
    }

    Log -Text "PS> Building website..." -Newline 1
    hugo -v --minify --gc --quiet
    Log -Text "Done"
    Log -Text "PS> Website built @ $public_folder"
}

function UpdateDependencies{

}

if ($Build -eq "production") {
    BuildHugo
}

if ($Deploy) {
    BuildHugo

    Log -Text "PS> Deploying website..."
    firebase --version
    firebase deploy

    Log -Text "PS> Running Pyton Script..."
    python ./utils.py
}

$Env:HUGO_ENV = "dev"
