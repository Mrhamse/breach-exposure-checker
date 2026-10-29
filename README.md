# Lekkasjesjekk

Et verktøy som sjekker om en e-post eller et passord har havnet på avveie i
kjente datalekkasjer. Det spør flere kilder samtidig og samler svaret ett sted.

Jeg bygde dette som starten på en idé jeg har: en enkel sikkerhetstjeneste for
frivillige lag og foreninger. Idrettslag og korps sitter på medlemslister med
barn og adresser, men styret er som regel foreldre uten datakompetanse. Den
vanligste måten de blir hacket på er gjenbrukte passord som allerede er lekket.
Dette verktøyet er motoren som fanger akkurat det.

## Hva den gjør
To ting:

1. **E-postsjekk** — slår opp en e-post mot flere lekkasjedatabaser og viser
   hvilke lekkasjer den er funnet i, og hvilke kilder som fant hver.
2. **Passordsjekk** — sjekker om et passord finnes i kjente lekkasjer, uten at
   passordet forlater maskinen.

## Eksempel

E-postsjekk:

    python agent.py navn@eksempel.no

    🔴 Funnet i 3 lekkasjer:
       • Adobe       (kilde: HaveIBeenPwned)
       • LinkedIn    (kilde: HaveIBeenPwned, XposedOrNot)
       • Dropbox     (kilde: LeakCheck)

Passordsjekk:

    python passord_sjekk.py
    🔴 Dette passordet er funnet 93 571 ganger i lekkasjer. Ikke bruk det!

## Hvordan det fungerer
E-postsjekken bygger på et adapter-mønster: hver datakilde er sin egen lille
modul i mappa `kilder/`, med samme grensesnitt. En aggregator spør alle
kildene, slår sammen svarene og fjerner duplikater. Vil jeg legge til en ny
kilde, skriver jeg én ny adapter — resten av koden rører jeg ikke.

Passordsjekken bruker k-anonymitet mot HIBP sitt Pwned Passwords-API: passordet
hashes lokalt, og bare de fem første tegnene av hashen sendes. Resten matches
mot svaret på maskinen. Dermed får ingen vite hvilket passord som ble sjekket.

## Kilder
- Have I Been Pwned (krever egen API-nøkkel for ekte e-poster; passordsjekken er gratis)
- XposedOrNot (gratis)
- LeakCheck (gratis, offentlig API)

Data fra Have I Been Pwned brukes under deres Creative Commons-lisens.
Kilde: https://haveibeenpwned.com

## Noen valg jeg tok
- **Flere kilder, ikke bare én.** Ingen database har alt. Ved å spørre flere
  samtidig fanger jeg mer enn én kilde ville klart alene.
- **Bare seriøse kilder.** Jeg bruker kun tjenester som sier *at* en e-post er
  lekket — aldri tjenester som selger passord i klartekst. Det siste er en
  juridisk og etisk grense jeg ikke vil krysse, særlig for et produkt tenkt mot
  lag med barnedata.
- **Personvern i passordsjekken.** K-anonymitet gjør at passordet aldri sendes.
- **Pen håndtering av manglende nøkkel.** Mangler HIBP-nøkkel, hopper verktøyet
  pent over den kilden i stedet for å krasje.

## Prosjektstruktur
| Fil | Ansvar |
|-----|--------|
| kilder/xposedornot.py | Adapter mot XposedOrNot |
| kilder/leakcheck.py | Adapter mot LeakCheck |
| kilder/hibp.py | Adapter mot Have I Been Pwned |
| aggregator.py | Spør alle kilder og slår sammen svaret |
| agent.py | E-postsjekk (kommandolinje) |
| passord_sjekk.py | Passordsjekk med k-anonymitet |

## Oppsett
    python3 -m venv .venv && source .venv/bin/activate
    pip install requests python-dotenv

For å bruke HIBP på ekte e-poster, legg en nøkkel i .env:

    HIBP_API_KEY=din-noekkel-her

## Begrensninger og videre arbeid
- HIBP krever betalt nøkkel for ekte e-poster. Testnøkkelen med bare nuller
  fungerer kun mot HIBP sine egne testadresser.
- Gratiskildene har rate-limits, så verktøyet er laget for enkeltoppslag, ikke
  masse-sjekk.
- Et naturlig neste steg er å koble dette til mockupen av «Lagvakt», slik at et
  styre kan sjekke alle styremedlemmer med samtykke og få et varsel.

## Juss og personvern
Verktøyet skal bare brukes på e-poster og passord man selv eier eller har fått
samtykke til å sjekke. Det sjekker kun *om* noe er lekket — det henter aldri
andres passord.

## Ansvarsfraskrivelse
Personlig læringsprosjekt.
