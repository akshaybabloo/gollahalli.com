param(
    [Parameter(Mandatory = $true)][string]$build,
    [bool]$deploy,
    [bool]$clean
)

function BuildHugo {
    Write-Host "Building Hugo for Producation..." -ForegroundColor Magenta
    $Env:HUGO_ENV = "production"
    
    $public_folder = Join-Path -Path $PSScriptRoot -ChildPath "public"
    
    if (Test-Path -Path "$public_folder" -ErrorAction SilentlyContinue) {
        Write-Host "'public' folder found, deleting it..." -ForegroundColor Magenta
        Remove-Item -Path "$public_folder" -Recurse 
        Write-Host "'public' folder deleted..." -ForegroundColor Magenta
        Start-Sleep -Seconds 1
    }
    
    Write-Host "Building website..." -ForegroundColor Magenta
    hugo -v --minify --gc
    Write-Host "Website built @ $public_folder" -ForegroundColor Magenta
}

if ($build -eq "production") {
    BuildHugo
}

if ($build -eq "production" -and $deploy ) {
    BuildHugo

    Write-Host "Deploying website..." -ForegroundColor Magenta
    firebase deploy
}
