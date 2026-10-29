from aggregator import sjekk_alle
from kilder import xposedornot, leakcheck, hibp

# Lat som kildene finner lekkasjer (LinkedIn gaar igjen i begge)
xposedornot.sjekk = lambda e: [
    {"kilde": "XposedOrNot", "navn": "LinkedIn"},
    {"kilde": "XposedOrNot", "navn": "Adobe"},
]
leakcheck.sjekk = lambda e: [
    {"kilde": "LeakCheck", "navn": "LinkedIn"},
    {"kilde": "LeakCheck", "navn": "Dropbox"},
]
hibp.sjekk = lambda e: []  # ingen noekkel

funn = sjekk_alle("testbruker@eksempel.no")
print("[*] Tester at flere kilder slaas sammen riktig:\n")
for f in funn:
    kilder = ", ".join(f["kilder"])
    print(f"   • {f['navn']:12}  funnet av: {kilder}")
