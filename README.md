# Petrol Welkomstmail — B2B nieuwe klanten

Template-repo voor de geautomatiseerde welkomstmail, verstuurd vanuit Zendesk via n8n.
**Deze repo is de enige bron voor de mailopmaak, teksten en beelden.** Niets in n8n of
Zendesk hoeft aangepast te worden bij een tekst- of beeldwijziging.

## Structuur

```
template/welcome.html    Layout (1x, gedeeld door alle talen). E-mailproof: tables + inline CSS.
content/<taal>.json      Alle vaste teksten per taal (nl, de, fr, en, es, it, ...).
assets/logo.png          Vast slot: logo in de header en footer.
assets/hero.jpg          Vast slot: bannerfoto (weergave 600x280, aanleveren 1200x560 / ratio 15:7).
build.py                 Merge-script voor lokale previews. Zelfde logica als de n8n Code-node.
```

## Hoe het werkt

1. n8n haalt `template/welcome.html` en `content/<taal>.json` op (raw URLs).
2. Eén Code-node vervangt de `{{placeholders}}` — pure tekstvervanging, geen AI.
3. Dynamische velden komen uit Zendesk via de webhook: `klantnummer`, taal, ontvanger.
4. De afbeeldingen in de mail wijzen naar de raw-URLs van `assets/` in deze repo.

Lokale preview maken: `python3 build.py nl --preview` → opent `preview_nl.html`.

## Spelregels

- **Assets**: bestandsnamen zijn vast (`logo.png`, `hero.jpg`). Vervangen = zelfde naam,
  zelfde plek. De marketing-aanleverflow (Drive + Sheet → n8n) schrijft hier
  automatisch naartoe en houdt het hero-formaat op 1200x560.
- **Teksten**: wijzig alleen `content/<taal>.json`. De waarde mag simpele HTML bevatten
  (`<em>`, `<a>`). De merknaam "Petrol Industries" nooit vertalen of afkorten.
- **Nieuwe taal**: kopieer `content/nl.json` naar bijv. `content/de.json` en vertaal de
  waarden. De keys blijven identiek. Daarna verschijnt de taal vanzelf in de
  Zendesk-dropdown zodra hij daar is toegevoegd.
- **Layout**: wijzigingen alleen in `template/welcome.html`; gelden direct voor alle talen.

## Waarom public

De afbeeldingen in een e-mail worden geladen door het mailprogramma van de ontvanger en
moeten dus publiek bereikbaar zijn. De inhoud van deze repo is exact wat elke nieuwe
klant per mail ontvangt — er staat niets gevoeligs in.

## Dynamische placeholders (gevuld door n8n per verzending)

| Placeholder         | Bron                                   |
|---------------------|----------------------------------------|
| `{{klantnummer}}`   | Veld op de organisatie in Zendesk      |
| `{{brandmovie_url}}`| Vast, in te stellen in n8n (van marketing) |
| `{{assets_base}}`   | Raw-URL van `assets/` in deze repo     |

Alle overige placeholders komen uit het taalbestand.
