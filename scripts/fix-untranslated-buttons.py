#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wire hardcoded French strings to the i18n system.

Adds data-i18n attributes to elements found by audit-translations.py and
creates the matching keys in fr.json / en.json (icons preserved in values).
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent

# rule = (FR text, key slug, EN text)
R_BACK = ("Retour à l'accueil", "retour_a_laccueil", "Back to home")
R_BACK_ARROW = ("← Retour à l'accueil", "retour_a_laccueil", "← Back to home")
R_CONTACT = ("Nous contacter", "nous_contacter_btn", "Contact us")

PAGE_RULES = {
    "mentions-legales.html": [R_BACK],
    "plan-du-site.html": [R_BACK],
    "pages/articles-presse.html": [R_BACK, R_CONTACT],
    "pages/conseils-numerique.html": [R_BACK, R_CONTACT],
    "pages/couverture-harmattan.html": [R_BACK, R_CONTACT],
    "pages/directive-europeenne.html": [R_BACK, R_CONTACT],
    "pages/entreprise-liberee.html": [R_BACK, R_CONTACT],
    "pages/generalites-corporate-governance.html": [R_BACK, R_CONTACT],
    "pages/ia-compliance.html": [R_BACK, R_CONTACT],
    "pages/information-administrateurs.html": [R_BACK, R_CONTACT],
    "pages/livre-gouvernance-ca.html": [R_BACK, R_CONTACT],
    "pages/missions-conseil.html": [R_BACK, R_CONTACT],
    "pages/monde-numerique.html": [R_BACK, R_CONTACT],
    "pages/observatoire-genres.html": [R_BACK, R_CONTACT],
    "pages/ouvrage-collectif-ca.html": [R_BACK, R_CONTACT],
    "pages/plateforme-formation.html": [R_BACK, R_CONTACT],
    "pages/recherche-administrateur.html": [R_BACK, R_CONTACT],
    "pages/soiree-lancement.html": [R_BACK, R_CONTACT],
    "pages/video-glp-vl.html": [R_BACK, R_CONTACT],
    "pages/webinaires-passes.html": [R_BACK, R_CONTACT],
    "pages/boards-et-comex.html": [R_BACK_ARROW],
    "pages/club-europeen.html": [R_BACK_ARROW],
    "pages/consultant-independant.html": [R_BACK_ARROW],
    "pages/ifa-et-numerique.html": [R_BACK_ARROW],
    "pages/loi-pacte.html": [R_BACK_ARROW],
    "pages/loi-zimmerman.html": [R_BACK_ARROW],
    "pages/questionnaire-rixain.html": [R_BACK_ARROW],
    "pages/loi-rixain-new.html": [
        R_BACK,
        ("Nous contacter pour un audit", "nous_contacter_pour_un_audit",
         "Contact us for an audit"),
    ],
    "pages/assises-parite-new.html": [
        R_BACK,
        ("8 mars 2024 - Journée internationale des droits des femmes",
         "event_date_8_mars_2024",
         "March 8, 2024 - International Women's Rights Day"),
        ("Directrice Générale, CAC 40", "directrice_generale_cac_40",
         "Chief Executive Officer, CAC 40"),
        ("Présidente du Cercle des Femmes Dirigeantes",
         "presidente_du_cercle_des_femmes_dirigeantes",
         "President of the Cercle des Femmes Dirigeantes"),
        ("Participer aux prochaines assises",
         "participer_aux_prochaines_assises",
         "Take part in the next conference"),
        ("Télécharger le rapport complet", "telecharger_le_rapport_complet",
         "Download the full report"),
    ],
    "pages/livre-eti-new.html": [
        R_BACK,
        ("Interview de Valérie Lejeune sur ETI Radio",
         "interview_de_valerie_lejeune_sur_eti_radio",
         "Interview with Valérie Lejeune on ETI Radio"),
        ("Vidéo de 20 minutes - Intervention de Guy Le Péchon au Jeudigital",
         "video_de_20_minutes_intervention_de_guy_le_pechon",
         "20-minute video - Talk by Guy Le Péchon at Jeudigital"),
    ],
    "pages/candidats-mandataires.html": [
        ("Expérience de mandataire social 1", "experience_de_mandataire_social_1",
         "Corporate officer experience 1"),
        ("Expérience de mandataire social 2", "experience_de_mandataire_social_2",
         "Corporate officer experience 2"),
        ("Expérience de mandataire social 3", "experience_de_mandataire_social_3",
         "Corporate officer experience 3"),
        ("Formation, indiquer le diplôme", "formation_indiquer_le_diplome",
         "Education, indicate the degree"),
        ("Envoyer", "envoyer", "Send"),
        ("Effacer", "effacer", "Clear"),
    ],
    "pages/monde-numerique-relation-client.html": [
        ("Publié le 24 septembre 2025", "publie_le_24_septembre_2025",
         "Published on September 24, 2025"),
        ("Généralités - Contributions", "generalites_contributions",
         "General - Contributions"),
    ],
    "pages/salarie-dirigeants-confiance.html": [
        ("Publié le 24 septembre 2025", "publie_le_24_septembre_2025",
         "Published on September 24, 2025"),
        ("Généralités - Contributions", "generalites_contributions",
         "General - Contributions"),
    ],
}

with open(ROOT / "data/translations/fr.json", encoding="utf-8") as f:
    FR = json.load(f)
with open(ROOT / "data/translations/en.json", encoding="utf-8") as f:
    EN = json.load(f)


def section_for(html):
    """Most common data-i18n prefix in the page."""
    prefixes = [k.split(".")[0] for k in re.findall(r'data-i18n="([^"]+)"', html)
                if "." in k]
    if not prefixes:
        return None
    return Counter(prefixes).most_common(1)[0][0]


ICON = r'<i\s[^>]*></i>'
total = 0

for rel, rules in sorted(PAGE_RULES.items()):
    path = ROOT / rel
    html = path.read_text(encoding="utf-8")
    section = section_for(html)
    if not section:
        print(f"SKIP {rel}: no section prefix found")
        continue
    changed = False
    for fr_text, slug, en_text in rules:
        key = f"{section}.{slug}"
        pattern = re.compile(
            r'<(a|button|div|span|strong)\b([^>]*)>'
            r'((?:\s|' + ICON + r')*' + re.escape(fr_text) +
            r'(?:\s|' + ICON + r')*)'
            r'</\1>')
        found = False
        pos = 0
        while True:
            m = pattern.search(html, pos)
            if m is None:
                break
            if "data-i18n" in m.group(2):
                pos = m.end()
                continue
            tag, attrs, inner = m.group(1), m.group(2), m.group(3)
            new_open = f'<{tag} data-i18n="{key}"{attrs}>'
            replacement = new_open + inner + f'</{tag}>'
            html = html[:m.start()] + replacement + html[m.end():]
            pos = m.start() + len(replacement)
            found = True
            changed = True
            total += 1
            # JSON values: FR = original inner, EN = inner with text swapped
            fr_inner = re.sub(r"\s+", " ", inner).strip()
            en_inner = fr_inner.replace(fr_text, en_text)
            FR.setdefault(section, {})[slug] = fr_inner
            EN.setdefault(section, {})[slug] = en_inner
        if not found:
            print(f"NO MATCH {rel}: {fr_text!r}")
    if changed:
        path.write_text(html, encoding="utf-8")
        print(f"OK {rel} (section {section})")

with open(ROOT / "data/translations/fr.json", "w", encoding="utf-8") as f:
    json.dump(FR, f, ensure_ascii=False, indent=2)
    f.write("\n")
with open(ROOT / "data/translations/en.json", "w", encoding="utf-8") as f:
    json.dump(EN, f, ensure_ascii=False, indent=2)
    f.write("\n")

print(f"\n{total} elements wired.")
