#!.venv/bin/python
"""
examples:
    certificate.py -u user -q -t user:password:db_name

required:
    psycopg
"""

import os
import argparse
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta


def generate_selfsigned_cert(hostname, ip_addresses=None, key=None):
    if key is None:
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, hostname)])
    now = datetime.now()
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(subject)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(now + timedelta(days=365))
        .add_extension(
            x509.BasicConstraints(ca=True, path_length=None),
            critical=True,
        )
        .add_extension(
            x509.SubjectAlternativeName(
                [x509.DNSName(hostname)] + [x509.DNSName(addr) for addr in ip_addresses if ip_addresses]
                if ip_addresses
                else [x509.DNSName(hostname)]
            ),
            critical=False,
        )
        .sign(key, hashes.SHA256())
    )

    return key, cert


def main():
    key, cert = generate_selfsigned_cert("localhost", ["127.0.0.1"])

    with open("tmp/server.key", "wb") as f:
        f.write(
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    with open("tmp/server.crt", "wb") as f:
        f.write(cert.public_bytes(encoding=serialization.Encoding.PEM))


def add_support_group(parser: argparse.ArgumentParser):
    args_group = parser.add_argument_group("support")

    args_group.add_argument(
        "-q",
        "--quite",
        action="store_true",
        help="... [default: False]",
    )
    return args_group


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    add_support_group(parser)

    parser.add_argument(
        "hostname",
        type=str,
        default="localhost",
        help="server hostname [default: localhost]",
    )

    parser.add_argument(
        "ip_addresses",
        type=str,
        nargs="*",
        default="127.0.0.1",
        help="server ip addresses [default: 127.0.0.1]",
    )

    args = parser.parse_args()

    # main()
    print("done")
