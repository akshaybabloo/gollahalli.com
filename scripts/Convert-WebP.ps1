$scriptLocation = Split-Path $MyInvocation.MyCommand.Path
$parentDirectory = Split-Path $scriptLocation -Parent

$imageExtensions = @('*.jpg', '*.png', '*.gif')

$results = [System.Collections.Generic.List[PSCustomObject]]::new()

foreach ($extension in $imageExtensions) {
    Write-Progress -Activity "Converting images to .webp format in $parentDirectory" -PercentComplete 0

    $imageFiles = Get-ChildItem -Path $parentDirectory -Filter $extension -File -Recurse

    $imageFiles | ForEach-Object -Parallel {
        $newFileName = [IO.Path]::ChangeExtension($_.Name, ".webp")

        $originalSize = if ($_.Length -ge 1MB) { "{0:N2} MB" -f ($_.Length / 1MB) } else { "{0:N2} KB" -f ($_.Length / 1KB) }

        $conversionError = $null
        if ($extension -eq '*.gif') {
            $conversionError = & 'gif2webp' -mt -lossy -q 75 $_.FullName -o (Join-Path $_.Directory.FullName $newFileName) 2>&1
        }
        else {
            $conversionError = & 'cwebp' -mt -q 75 $_.FullName -o (Join-Path $_.Directory.FullName $newFileName) 2>&1
        }

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
