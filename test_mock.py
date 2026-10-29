from kilder import xposedornot

# Lag et falskt API-svar som om e-posten er funnet i tre lekkasjer
class FalsktSvar:
    status_code = 200
    def json(self):
        return {"breaches": [["Adobe", "LinkedIn", "Canva"]]}

# Bytt ut nettverkskallet med det falske svaret
xposedornot.requests.get = lambda *a, **k: FalsktSvar()

funn = xposedornot.sjekk("testbruker@eksempel.no")
print(f"[*] Tester at adapteren tolker et 'funnet'-svar riktig:\n")
if funn:
    print(f"[!] Funnet i {len(funn)} lekkasjer:")
    for f in funn:
        print(f"    - {f['navn']}  ({f['kilde']})")
else:
    print("[X] Noe er feil - burde funnet 3 lekkasjer.")
