import sys
from aggregator import sjekk_alle

if len(sys.argv) < 2:
    print("Bruk: python agent.py <e-post>")
    sys.exit(1)

epost = sys.argv[1]
print(f"[*] Sjekker {epost} mot alle kilder...\n")

funn = sjekk_alle(epost)

if not funn:
    print("🟢 Ingen lekkasjer funnet. Ser trygt ut!")
else:
    print(f"🔴 Funnet i {len(funn)} lekkasjer:\n")
    for f in funn:
        kilder = ", ".join(f["kilder"])
        print(f"   • {f['navn']}   (kilde: {kilder})")
    print("\nAnbefaling: bytt passord på disse tjenestene og skru på to-faktor.")
