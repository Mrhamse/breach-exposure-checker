import hashlib
import getpass
import requests

URL = "https://api.pwnedpasswords.com/range/{prefix}"

def sjekk_passord(passord: str) -> int:
    """Returnerer hvor mange ganger passordet er sett i lekkasjer (0 = aldri)."""
    # Lag SHA-1-hash av passordet
    sha1 = hashlib.sha1(passord.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]

    # Send KUN de 5 foerste tegnene av hashen - passordet forlater aldri maskinen
    svar = requests.get(
        URL.format(prefix=prefix),
        headers={"Add-Padding": "true"},
        timeout=15,
    )
    svar.raise_for_status()

    # Se om vaar hash-suffix er blant svarene
    for linje in svar.text.splitlines():
        hash_suffix, _, antall = linje.partition(":")
        if hash_suffix == suffix:
            return int(antall)
    return 0

if __name__ == "__main__":
    passord = getpass.getpass("Skriv inn passordet som skal sjekkes (vises ikke): ")
    antall = sjekk_passord(passord)
    if antall == 0:
        print("🟢 Dette passordet er ikke funnet i noen kjent lekkasje.")
    else:
        print(f"🔴 Dette passordet er funnet {antall:,} ganger i lekkasjer. Ikke bruk det!")
