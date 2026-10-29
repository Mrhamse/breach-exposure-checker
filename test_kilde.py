import sys
from kilder import xposedornot

epost = sys.argv[1] if len(sys.argv) > 1 else "test@example.com"
print(f"[*] Sjekker {epost} mot {xposedornot.NAVN}...")

funn = xposedornot.sjekk(epost)
if not funn:
    print("[+] Ingen lekkasjer funnet.")
else:
    print(f"[!] Funnet i {len(funn)} lekkasjer:")
    for f in funn:
        print(f"    - {f['navn']}  ({f['kilde']})")
