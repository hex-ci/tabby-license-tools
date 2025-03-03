#!/usr/bin/env python3
"""
Generate a custom license for Tabby using your own RSA key pair.
This script creates a JWT token signed with your private key.
"""

import argparse
import datetime
import json
import sys
import time

import jwt


def generate_license(
    email,
    license_type,
    seats,
    expiry_days,
    private_key_path
):
    # Read the private key
    try:
        with open(private_key_path, 'rb') as key_file:
            private_key = key_file.read()
    except Exception as e:
        print(f"Error reading private key: {e}")
        sys.exit(1)

    # Current time and expiry time
    now = int(time.time())
    expiry = now + (expiry_days * 24 * 60 * 60)

    # Create the payload
    payload = {
        "iss": "tabbyml.com",  # Issuer - keep as is for compatibility
        "sub": email,          # Subject - email of the licensee
        "iat": now,            # Issued at timestamp
        "exp": expiry,         # Expiry timestamp
        "typ": license_type.upper(),  # License type (TEAM, ENTERPRISE, etc.)
        "num": seats           # Number of seats
    }

    # Sign the token with the private key using RS512 algorithm
    try:
        token = jwt.encode(
            payload,
            private_key,
            algorithm="RS512"
        )
        return token
    except Exception as e:
        print(f"Error generating license: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Generate a custom Tabby license")
    parser.add_argument("--email", required=True, help="Email address of the licensee")
    parser.add_argument("--type", required=True, choices=["team", "enterprise"], 
                        help="License type (team or enterprise)")
    parser.add_argument("--seats", required=True, type=int, help="Number of seats")
    parser.add_argument("--days", required=True, type=int, 
                        help="Number of days until license expires")
    parser.add_argument("--key", required=True, help="Path to the private key file")
    parser.add_argument("--output", help="Output file (optional, defaults to stdout)")

    args = parser.parse_args()

    license_token = generate_license(
        args.email,
        args.type,
        args.seats,
        args.days,
        args.key
    )

    # Decode the token to show the payload (for verification)
    header = jwt.get_unverified_header(license_token)
    payload = jwt.decode(license_token, options={"verify_signature": False})
    
    # Format expiry date for display
    expiry_date = datetime.datetime.fromtimestamp(payload["exp"]).strftime('%Y-%m-%d %H:%M:%S')

    # Output the license information
    info = {
        "token": license_token,
        "header": header,
        "payload": {
            "issuer": payload["iss"],
            "subject": payload["sub"],
            "issued_at": datetime.datetime.fromtimestamp(payload["iat"]).strftime('%Y-%m-%d %H:%M:%S'),
            "expires_at": expiry_date,
            "type": payload["typ"],
            "seats": payload["num"]
        }
    }

    output_text = f"""
License Token:
{license_token}

License Information:
  Issued to: {payload['sub']}
  License type: {payload['typ']}
  Seats: {payload['num']}
  Expires: {expiry_date}
"""

    if args.output:
        with open(args.output, 'w') as f:
            f.write(license_token)
        print(f"License written to {args.output}")
        print(output_text)
    else:
        print(output_text)


if __name__ == "__main__":
    main()
