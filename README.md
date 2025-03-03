# Tabby License Tools

This directory contains tools to generate and install your own license for Tabby.

## Prerequisites

- OpenSSL (for key generation)
- Python 3 with PyJWT library (`pip install pyjwt`)

## Steps to Generate and Install Your Own License

### 1. Generate RSA Key Pair

```bash
# Make scripts executable
chmod +x generate_keys.sh install_key.sh

# Generate RSA key pair
./generate_keys.sh
```

This will create two files:
- `license.key` - Private key (keep this secure!)
- `license.key.pub` - Public key

### 2. Install the Public Key

```bash
# Install the public key into the Tabby project
./install_key.sh
```

This will backup the original public key and replace it with your new one.

### 3. Generate a License

```bash
# Install required Python package
pip install pyjwt

# Generate a license
python generate_license.py --email "your@email.com" --type "enterprise" --seats 100 --days 365 --key license.key --output license.txt
```

Parameters:
- `--email`: Email address of the licensee
- `--type`: License type (team or enterprise)
- `--seats`: Number of seats
- `--days`: Number of days until license expires
- `--key`: Path to the private key file
- `--output`: Output file (optional)

### 4. Apply the License

Use the Tabby API or UI to apply the generated license.

## Important Notes

- This does not modify the original license verification logic
- The license will be verified using your public key
- Keep your private key secure
- You need to restart the Tabby server after installing the new public key
