# core/secrets.py

import keyring
import getpass

PREFIX = "keyring:"


def resolve_secret(value: str, fallback_key: str = "") -> str:
    if not value or not value.startswith(PREFIX):
        return value
    service_key = value[len(PREFIX):] or fallback_key
    return keyring.get_password("sonderbot", service_key) or ""


def set_secret(service_key: str, prompt: str = "Enter secret value: "):
    value = getpass.getpass(prompt)
    keyring.set_password("sonderbot", service_key, value)
    print(f"✔ Secret saved under key: {service_key}")


def delete_secret(service_key: str):
    keyring.delete_password("sonderbot", service_key)
    print(f"✘ Secret deleted: {service_key}")
