iban_hunter.py
#!/usr/bin/env python3
# Euro-IBAN-Leak-Hunter - Made in Sindh, Pakistan
# Author: bugbounty-sindh

import re

IBAN_REGEX = r'\b[A-Z]{2}[0-9]{2}[A-Z0-9]{11,30}\b'

def validate_iban(iban):
    iban = iban.replace(' ', '').upper()
    if len(iban) < 15 or len(iban) > 34:
        return False
    rearranged = iban[4:] + iban[:4]
    numeric = ''.join(str(ord(c)-55) if c.isalpha() else c for c in rearranged)
    return int(numeric) % 97 == 1

def hunt(file_path):
    print(f"[+] Hunting IBANs in {file_path}")
    with open(file_path, 'r', errors='ignore') as f:
        content = f.read()
        matches = re.findall(IBAN_REGEX, content)
        for m in set(matches):
            if validate_iban(m):
                print(f"[!] LEAK FOUND: {m}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 iban_hunter.py <file>")
    else:
        hunt(sys.argv[1])