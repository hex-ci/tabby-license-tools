#!/bin/bash
# Install the generated public key into the Tabby project

# Check if the public key exists
if [ ! -f "license.key.pub" ]; then
    echo "Error: license.key.pub not found. Generate keys first."
    exit 1
fi

# Backup the original public key
BACKUP_DIR="backups/$(date +%Y%m%d%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp ../ee/tabby-webserver/keys/license.key.pub "$BACKUP_DIR/"
echo "Original public key backed up to $BACKUP_DIR/"

# Copy the new public key to the project
cp license.key.pub ../ee/tabby-webserver/keys/
echo "New public key installed successfully!"

echo "Remember to restart the Tabby server for changes to take effect."
