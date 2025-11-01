#!/usr/bin/env python3
"""
TRU Wallet Generator - Just Works™ Edition
Handles all the RIPEMD160 issues automatically
"""

import os
import sys

print("TRU Wallet - Checking requirements...")

# Auto-install required packages if missing
required = ['base58', 'ecdsa', 'pycryptodome']
for package in required:
    try:
        __import__(package.replace('pycryptodome', 'Crypto'))
    except ImportError:
        print(f"Installing {package}...")
        os.system(f"{sys.executable} -m pip install {package} --quiet")

# Now import everything
import json
import hashlib
import secrets
import base58
import ecdsa
from datetime import datetime
from Crypto.Hash import RIPEMD160


class TRUWallet:
    """Simple TRU Wallet that just works"""
    
    def __init__(self):
        print("✅ Wallet initialized")
    
    def generate_address(self):
        """Generate a TRU address - no fuss, no muss"""
        
        # 1. Generate private key (32 random bytes)
        private_key = secrets.token_bytes(32)
        private_key_hex = private_key.hex()
        
        # 2. Get public key (compressed)
        signing_key = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
        verifying_key = signing_key.get_verifying_key()
        
        # Get x,y coordinates
        x = verifying_key.pubkey.point.x()
        y = verifying_key.pubkey.point.y()
        
        # Compressed public key
        prefix = b'\x02' if y % 2 == 0 else b'\x03'
        public_key = prefix + x.to_bytes(32, 'big')
        public_key_hex = public_key.hex()
        
        # 3. Generate address
        # SHA256
        sha = hashlib.sha256(public_key).digest()
        
        # RIPEMD160 (using pycryptodome)
        ripe = RIPEMD160.new(sha).digest()
        
        # Add version byte
        versioned = b'\x00' + ripe
        
        # Checksum
        checksum = hashlib.sha256(hashlib.sha256(versioned).digest()).digest()[:4]
        
        # Final address
        address_bytes = versioned + checksum
        address = base58.b58encode(address_bytes).decode()
        
        return {
            'address': address,
            'private_key': private_key_hex,
            'public_key': public_key_hex
        }
    
    def save_to_file(self, data, filename="tru_wallet.json"):
        """Save wallet data to file"""
        wallet_data = {
            'address': data['address'],
            'public_key': data['public_key'],
            'private_key': data['private_key'],
            'created': datetime.now().isoformat(),
            'warning': 'KEEP YOUR PRIVATE KEY SECRET!'
        }
        
        with open(filename, 'w') as f:
            json.dump(wallet_data, f, indent=2)
        
        print(f"💾 Wallet saved to {filename}")


# SUPER SIMPLE USAGE
if __name__ == "__main__":
    print()
    print("=" * 50)
    print("     TRU BLOCKCHAIN WALLET GENERATOR")
    print("=" * 50)
    print()
    
    # Create wallet
    wallet = TRUWallet()
    
    # Generate address
    print("🔑 Generating TRU address...")
    result = wallet.generate_address()
    
    print()
    print("✅ SUCCESS!")
    print("-" * 50)
    print(f"YOUR TRU ADDRESS: {result['address']}")
    print("-" * 50)
    print()
    print("Share this address to receive TRU coins!")
    print()
    
    # Save to file
    wallet.save_to_file(result)
    
    print()
    print("⚠️  IMPORTANT:")
    print("• Never share your private key")
    print("• Backup tru_wallet.json safely")
    print("• This address works on the TRU blockchain")
    print()
