import ssl
import socket
from pathlib import Path
import certifi

CERT_DIR = Path("data/certs")
CERT_DIR.mkdir(parents=True, exist_ok=True)

def fetch_server_cert(hostname: str, port: int) -> str:
    cert_path = CERT_DIR / f"{hostname}.pem"

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    with socket.create_connection((hostname, port)) as conn:
        with context.wrap_socket(conn, server_hostname=hostname) as sock:
            der_cert = sock.getpeercert(binary_form=True)
            pem_cert = ssl.DER_cert_to_PEM_cert(der_cert)

            with open(cert_path, "w") as f:
                f.write(pem_cert)

    return str(cert_path)

def make_ssl_context_with_local_cert(cert_path: str) -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    ctx.load_verify_locations(cafile=certifi.where())  # Load system certs first
    ctx.load_verify_locations(cafile=cert_path)        # Add local cert
    return ctx