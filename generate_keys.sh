#!/bin/bash
# Generate a new RSA key pair for license signing

# Generate private key
openssl genrsa -out license.key 4096

# Extract public key from private key
openssl rsa -in license.key -pubout -out license.key.pub

echo "RSA key pair generated:"
echo "Private key: license.key"
echo "Public key: license.key.pub"
