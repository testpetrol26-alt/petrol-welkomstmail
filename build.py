#!/usr/bin/env python3
"""
Merge-script welkomstmail — zelfde logica als straks de n8n Code-node.

Gebruik:  python3 build.py <taal> [--preview]

  template/welcome.html  +  content/<taal>.json  +  dynamische velden
  → verzendklare HTML

Met --preview worden de afbeeldingen als base64 ingebed en testwaarden
ingevuld, zodat het bestand los te bekijken is zonder hosting.
"""
import json, sys, base64, pathlib

ROOT = pathlib.Path(__file__).parent

# Dynamische velden: komen in productie uit de Zendesk-app via de webhook
DYNAMISCH = {
    "klantnummer": "DP12345",                       # voorbeeldwaarde
    "brandmovie_url": "https://www.petrolindustries.com/",  # nog aan te leveren
    "assets_base": "{{assets_base}}",               # wordt de GitHub raw-URL
}

def li(items):
    return "\n".join(f'            <li style="margin:0 0 4px 0;">{x}</li>' for x in items)

def build(taal, preview=False):
    tpl = (ROOT / "template" / "welcome.html").read_text()
    c = json.loads((ROOT / "content" / f"{taal}.json").read_text())

    # Lijsten → <li>-regels
    c["inloggen_stappen_html"] = li(c.pop("inloggen_stappen"))
    c["instellingen_bullets_html"] = li(c.pop("instellingen_bullets"))
    # Telefoonnummer als tel:-link (spaties eruit)
    c["support_tel_link"] = c["support_tel"].replace(" ", "")

    out = tpl
    for k, v in {**c, **DYNAMISCH}.items():
        out = out.replace("{{%s}}" % k, str(v))

    if preview:
        for naam, mime in [("logo.png", "image/png"), ("hero.jpg", "image/jpeg")]:
            data = base64.b64encode((ROOT / "assets" / naam).read_bytes()).decode()
            out = out.replace("{{assets_base}}/" + naam, f"data:{mime};base64,{data}")
        doel = ROOT / f"preview_{taal}.html"
    else:
        doel = ROOT / f"welcome_{taal}_gemerged.html"

    doel.write_text(out)
    rest = [r for r in out.split("{{") if "}}" in r.split("\n")[0]]
    print(f"OK → {doel.name}")
    if rest and not preview:
        print("Let op, nog open placeholders:", [r.split('}}')[0] for r in rest])

if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "nl", preview="--preview" in sys.argv)
