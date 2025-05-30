#!/bin/bash

webp_version="1.5.0"

if [ -n "$CI" ] || ! command -v cwebp &>/dev/null; then
    echo "Installing cwebp and gif2webp (forced installation in CI environment)."

    user_bin="$HOME/bin"
    mkdir -p "$user_bin"
    curl -L https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-${webp_version}-linux-x86-64.tar.gz -o /tmp/libwebp.tar.gz
    tar -xzf /tmp/libwebp.tar.gz -C /tmp
    mv /tmp/libwebp-${webp_version}-linux-x86-64/bin/* "$user_bin"

    chmod +x "$user_bin"/*

    rm -rf /tmp/libwebp-${webp_version}-linux-x86-64 /tmp/libwebp.tar.gz

    if ! grep -q "$user_bin" "$HOME/.bashrc"; then
        echo "export PATH=\"$user_bin:\$PATH\"" >>"$HOME/.bashrc"
        source "$HOME/.bashrc"
    fi

    echo -e "cwebp has been installed to $user_bin\n"
    cwebp_path="$user_bin/cwebp"
    gif2webp_path="$user_bin/gif2webp"
else
    echo -e "cwebp is already installed.\n"
    cwebp_path="cwebp"
    gif2webp_path="gif2webp"
fi

echo -e "cwebp version: $($cwebp_path -version)\n"
echo -e "gif2webp version: $($gif2webp_path -version)\n"

scriptLocation="$(dirname "$(readlink -f "$0")")"
parentDirectory="$(dirname "$scriptLocation")"

echo "Converting images to .webp format in $parentDirectory"

convert_image() {
    imageFile="$1"
    newFileName="${imageFile%.*}.webp"

    # Skip if the webp version of the file already exists
    if [[ -z "$CI" && -e "$newFileName" ]]; then
        echo "Skipped conversion for $(basename "$imageFile"): .webp file already exists."
        return
    fi

    originalSizeBytes=$(stat -c%s "$imageFile")
    originalSize=""

    if [[ $originalSizeBytes -ge 1048576 ]]; then
        originalSize=$(awk -v bytes="$originalSizeBytes" 'BEGIN {printf "%.2f MB", bytes/1048576}')
    else
        originalSize=$(awk -v bytes="$originalSizeBytes" 'BEGIN {printf "%.2f KB", bytes/1024}')
    fi

    conversionError=""
    if [[ "${imageFile##*.}" == "gif" ]]; then
        # Convert the GIF image to .webp format with quality 75 and capture the error message if any
        conversionError=$("$gif2webp_path" -mt -lossy -q 75 "$imageFile" -o "$newFileName" 2>&1)
    else
        # Convert the image to .webp format with quality 75 and capture the error message if any
        conversionError=$("$cwebp_path" -mt -q 75 "$imageFile" -o "$newFileName" 2>&1)
    fi

    # Check if the command succeeded
    if [[ $? -eq 0 ]]; then
        newSizeBytes=$(stat -c%s "$newFileName")
        newSize=""

        if [[ $newSizeBytes -ge 1048576 ]]; then
            newSize=$(awk -v bytes="$newSizeBytes" 'BEGIN {printf "%.2f MB", bytes/1048576}')
        else
            newSize=$(awk -v bytes="$newSizeBytes" 'BEGIN {printf "%.2f KB", bytes/1024}')
        fi

        echo "Converted $(basename "$imageFile") ($originalSize) to $(basename "$newFileName") ($newSize) - ✅"
    else
        echo "Failed to convert $(basename "$imageFile") ($originalSize) to $(basename "$newFileName") - ❌"
        echo "Error: $conversionError"
    fi
}

export -f convert_image
export gif2webp_path
export cwebp_path

# Clean all files with extension .webp including the ones in subdirectories
# find "$parentDirectory" -type f -name "*.webp" -delete

find "$parentDirectory" -type f \( -name "*.jpg" -o -name "*.png" -o -name "*.gif" \) -print0 | xargs -0 -I {} -P 4 bash -c 'convert_image "$@"' _ {}
