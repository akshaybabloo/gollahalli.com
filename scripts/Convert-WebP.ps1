$webp_version = "1.4.0"
$user_bin = "$env:USERPROFILE\bin"

function Compare-WebPVersion {
    param (
        [string]$toInstall
    )
    # Invoke expression, get first line of output as 0.0.0 version and compare it to $toInstall
    Invoke-Expression "cwebp.exe -version" | Select-Object -First 1 | ForEach-Object {
        $installedVersion = $_ -replace '.*(\d+\.\d+\.\d+).*', '$1'
        if ($installedVersion -lt $toInstall) {
            return $false
        }
        return $true
    }
}

if ($env:CI -or !(Get-Command "cwebp" -ErrorAction SilentlyContinue) -or !(Compare-WebPVersion $webp_version)) {
    Write-Host "Installing cwebp and gif2webp (forced installation in CI environment)."

    if (!(Test-Path $user_bin)) {
        New-Item -Path $user_bin -ItemType Directory | Out-Null
    }

    $zipPath = "$env:TEMP\libwebp.zip"
    Invoke-WebRequest -Uri "https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-$webp_version-windows-x64.zip" -OutFile $zipPath
    Expand-Archive -Path $zipPath -DestinationPath $env:TEMP -Force
    Move-Item "$env:TEMP\libwebp-$webp_version-windows-x64\bin\*" $user_bin -Force

    Remove-Item -Recurse -Force "$env:TEMP\libwebp-$webp_version-windows-x64"
    Remove-Item -Force $zipPath

    $env:PATH += ";$user_bin"

    Write-Host "`ncwebp has been installed to $user_bin`n"
    $cwebp_path = "$user_bin\cwebp.exe"
    $gif2webp_path = "$user_bin\gif2webp.exe"
}
else {
    Write-Host "`ncwebp is already installed.`n"
    $cwebp_path = "cwebp.exe"
    $gif2webp_path = "gif2webp.exe"
}

Invoke-Expression "$cwebp_path -version"
Invoke-Expression "$gif2webp_path -version"

$scriptLocation = Split-Path $MyInvocation.MyCommand.Path
$parentDirectory = Split-Path $scriptLocation -Parent

$imageExtensions = @('*.jpg', '*.png', '*.gif')

$results = [System.Collections.Generic.List[PSCustomObject]]::new()

foreach ($extension in $imageExtensions) {
    Write-Progress -Activity "Converting images to .webp format in $parentDirectory" -Status "Processing $extension files"

    $imageFiles = Get-ChildItem -Path $parentDirectory -Filter $extension -File -Recurse

    $imageFiles | ForEach-Object -Parallel {
        $cwebp_path = $using:cwebp_path
        $gif2webp_path = $using:gif2webp_path
        $extension = $using:extension

        $newFileName = [IO.Path]::ChangeExtension($_.Name, ".webp")

        $originalSize = if ($_.Length -ge 1MB) { "{0:N2} MB" -f ($_.Length / 1MB) } else { "{0:N2} KB" -f ($_.Length / 1KB) }
        if ($extension -like '*.gif') {
            $command = "$gif2webp_path -mt -lossy -q 75 $($_.FullName) -o $(Join-Path $_.Directory.FullName $newFileName)"
        }
        else {
            $command = "$cwebp_path -mt -q 75 $($_.FullName) -o $(Join-Path $_.Directory.FullName $newFileName)"
        }

        $conversionError = $null
        $output = $null
        Invoke-Expression $command -ErrorVariable conversionError -ErrorAction SilentlyContinue -OutVariable output 2>&1

        if ($LASTEXITCODE -eq 0) {
            $newSize = (Get-Item (Join-Path $_.Directory.FullName $newFileName)).Length
            $newSize = if ($newSize -ge 1MB) { "{0:N2} MB" -f ($newSize / 1MB) } else { "{0:N2} KB" -f ($newSize / 1KB) }

            $originalFileName = if ($_.Name.Length -gt 30) { $_.Name.Substring(0, 27) + "..." } else { $_.Name }
            $newFileNameTruncated = if ($newFileName.Length -gt 30) { $newFileName.Substring(0, 27) + "..." } else { $newFileName }

            [PSCustomObject]@{
                'OriginalFile' = $originalFileName
                'NewFile'      = $newFileNameTruncated
                'OriginalSize' = $originalSize
                'NewSize'      = $newSize
                'Successful'   = [char]0x2705
            }
        }
        else {
            $conversionError = $output | ForEach-Object { $_.ToString() }
            Write-Output "Failed to convert $($_.Name) ($originalSize) to $newFileName. Error: $conversionError"
            [PSCustomObject]@{
                'OriginalFile' = $originalFileName
                'NewFile'      = $newFileNameTruncated
                'OriginalSize' = $originalSize
                'NewSize'      = $null
                'Successful'   = [char]0x274C
            }
        }
    } -ThrottleLimit 5 | ForEach-Object { $results.Add($_) }
}

$results | Format-Table
