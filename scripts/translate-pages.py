#!/usr/bin/env python3
"""
translate-pages.py — Extract French text from G&S HTML pages,
generate i18n keys, produce English translations, inject data-i18n
attributes, and update the JSON translation files.

Uses BeautifulSoup for robust HTML parsing.

Usage:
    python3 scripts/translate-pages.py
"""

import json
import os
import re
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag

# ─── Configuration ───────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent
PAGES_DIR = ROOT / "pages"
FR_JSON = ROOT / "data" / "translations" / "fr.json"
EN_JSON = ROOT / "data" / "translations" / "en.json"

# Tags whose direct text should be translated
CONTENT_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "td", "th",
                "figcaption", "caption", "blockquote", "dt", "dd", "summary",
                "label"}

# Tags to skip entirely (and their children)
SKIP_TAGS = {"script", "style", "link", "meta", "noscript", "code", "pre",
             "svg", "head"}

# Inline tags that are part of parent text (not standalone)
INLINE_TAGS = {"strong", "b", "em", "i", "span", "a", "small", "sub", "sup",
               "mark", "u", "abbr", "cite", "q"}

MIN_TEXT_LEN = 3


# ─── Translation dictionary ──────────────────────────────────────────────────

TRANSLATIONS = {
    # ── UI / Common ──
    "Actualités futures": "Upcoming Events",
    "Actualités": "News",
    "Passé récent": "Recent Past",
    "Page en cours de construction": "Page Under Construction",
    "Page en cours de développement": "Page Under Development",
    "Cette page est actuellement en cours de développement.": "This page is currently under development.",
    "Le contenu sera disponible prochainement.": "Content will be available soon.",
    "Pour plus d'informations": "For more information",
    "N'hésitez pas à nous contacter pour obtenir des informations sur ce sujet :": "Please do not hesitate to contact us for information on this topic:",
    "Retour à l'accueil": "Back to Home",
    "← Retour à l'accueil": "← Back to Home",
    "Cliquer ici": "Click here",
    "En savoir plus": "Read more",
    "Télécharger": "Download",
    "Voir les détails": "View details",
    "Ouvrir": "Open",
    "En construction": "Under construction",
    "Email :": "Email:",
    "Contact :": "Contact:",

    # ── Actualites ──
    "Simulation de réunions de Conseil d'Administration": "Board of Directors Meeting Simulation",
    "Guy Le Péchon sera l'un des deux animateurs de l'après-midi consacrée à des simulations avec jeux de rôles pour deux réunions de Conseil d'Administration.": "Guy Le Péchon will be one of the two facilitators for the afternoon devoted to role-playing simulations of two Board of Directors meetings.",
    "Cet après-midi se situe à la fin des cours se déroulant actuellement du Certificat de Centrale-Supélec Executive Education pour les membres en place ou potentiels de Comex et Codir.": "This afternoon session takes place at the end of the current courses of the Centrale-Supélec Executive Education Certificate for current or prospective Comex and Codir members.",
    "Ainsi, les participants amélioreront leur connaissance des relations attendues entre les Comex/ouCodir et les Conseils d'Administration.": "Participants will thus improve their understanding of the expected relationships between Comex/Codir and Boards of Directors.",
    "Première journée du nouveau Certificat de formation « Comex Codir, Gouvernance 5.0 »": "First day of the new 'Comex Codir, Governance 5.0' Training Certificate",
    "Première journée du nouveau Certificat de formation « Comex Codir, Gouvernance 5.0 » de Centrale-Supélec Executive Education.": "First day of the new 'Comex Codir, Governance 5.0' Training Certificate from Centrale-Supélec Executive Education.",
    "Voir les détails à la page « Formation au Comex Codir ».": "See details on the 'Comex Codir Training' page.",
    "G & S a participé à son élaboration et animera plusieurs cours.": "G & S participated in its development and will lead several courses.",
    "Séance inaugurale du Certificat de Centrale-Supélec Executive Education pour les membres en place ou à venir de Comex Codir": "Inaugural session of the Centrale-Supélec Executive Education Certificate for current or future Comex Codir members",
    "Salon du livre des polytechniciens": "Polytechnicians' Book Fair",
    "Présentation et dédicace de livres en particulier « Le Monde et la gouvernance des ETI ».": "Presentation and book signing, notably 'The World and the Governance of Mid-Sized Companies'.",
    "Voir l'article sur le monde et la gouvernance des ETI": "See the article on the world and the governance of mid-sized companies",
    "Soirée Hi-Team": "Hi-Team Evening",
    "Soirée : Mixité des instances (COMEX/CODIR) et cadres dirigeant(e)s": "Evening: Gender Diversity in Executive Bodies (COMEX/CODIR) and Senior Management",
    "Consulter l'invitation": "View the invitation",
    "Compte-rendu de la riche soirée": "Summary of the evening event",
    "Pour voir le contenu de la conférence et s'inscrire, cliquer ici": "Click here to see the lecture content and register",

    # ── Loi Zimmerman ──
    "La loi Zimmerman Janvier 2011 - Page en cours de construction": "The Zimmerman Law January 2011 — Page Under Construction",

    # ── Loi Rixain ──
    "Article 14 de la Loi Rixain": "Article 14 of the Rixain Law",
    "Loi Rixain — Décembre 2021": "Rixain Law — December 2021",
    "Loi Rixain": "Rixain Law",

    # ── Historique ──
    "Historique": "History",
    "Communiqué de presse du 4 mai 2009": "Press Release of 4 May 2009",

    # ── Organisation ──
    "Qui est G & S": "Who is G & S",
    "Présentation de G & S": "About G & S",

    # ── Formations ──
    "Formations d'Administrateurs": "Board Member Training",
    "Formations INSTANCES DE DIRECTIONS": "LEADERSHIP BODIES TRAINING",
    "Des formations originales proposées par G & S": "Original training programmes offered by G & S",
    "Formations institutionnelles": "Institutional Training",
    "Formation au Comex Codir": "Comex Codir Training",

    # ── Missions ──
    "Les missions": "Assignments",
    "Diagnostic de Conseils d'Administration ou de Surveillance": "Board of Directors or Supervisory Board Assessment",
    "Recherche de mandataires sociaux": "Search for Corporate Officers",

    # ── Bibliographie ──
    "Bibliographie \"Corporate Governance\"": "Corporate Governance Bibliography",
    "Notes et articles publiés par G & S": "Articles and papers published by G & S",
    "Rapports": "Reports",
    "Livres": "Books",

    # ── Diagnostics ──
    "Diagnostics de Conseils d'Administration": "Board of Directors Assessments",

    # ── Candidats ──
    "Candidats mandataires sociaux": "Corporate Officer Candidates",
    "Candidature comme mandataire": "Apply as a Board Member",

    # ── Études ──
    "Féminisation des instances dirigeantes": "Gender Diversity in Corporate Leadership",
    "Observatoire des genres": "Gender Observatory",
    "Assises de la parité": "Gender Parity Conference",

    # ── Digital / IFA ──
    "Travaux de l'IFA sur le digital": "IFA Digital Working Group Reports",
    "IFA et le Numérique": "IFA and Digital",
    "Documents pour l'administrateur": "Documents for directors",
    "Catalogue de documents pour l'administrateur": "Document catalogue for directors",

    # ── Sites ──
    "Sites intéressants": "Useful Links",

    # ── Advisors ──
    "Gouvernance Advisors": "Governance Advisors",

    # ── Shadow conseil ──
    "Shadow Conseil d'Administration de jeunes": "Youth Shadow Board of Directors",
    "Shadow Conseil d'Administration": "Shadow Board of Directors",

    # ── Intelligence ──
    "Intelligence émotionnelle des administrateurs": "Emotional Intelligence of Directors",
    "Intelligence collective": "Collective Intelligence",

    # ── Livre ETI ──
    "Le monde et la gouvernance des ETI": "The World and the Governance of Mid-Sized Companies",
    "Le Monde et la gouvernance des ETI": "The World and the Governance of Mid-Sized Companies",

    # ── Other articles ──
    "Administrateur indépendant un vaccin ?": "Independent Director — a Vaccine?",
    "Salariés et Dirigeants en Confiance": "Employees and Leaders in Trust",
    "Apports de l'Intelligence artificielle à la Compliance": "Contributions of Artificial Intelligence to Compliance",
    "Le monde numérique et la relation client": "The Digital World and Customer Relations",
    "Comment les DSI peuvent impliquer les Conseils d'Administration": "How CIOs Can Engage Boards of Directors",
    "Facilities Management, Les normes Européennes": "Facilities Management — European Standards",
    "Instances de gouvernance": "Governance Bodies",
    "Club Européen": "European Club",
    "Comparaison féminisation Boards et Comex": "Comparison of Board and Comex Gender Diversity",
    "Directive Européenne": "European Directive",
    "Loi Pacte": "Pacte Law",
    "Glossaire des Prestations de conseil": "Consulting Services Glossary",
    "Auto diagnostic Loi Rixain": "Rixain Law Self-Assessment",
    "Articles de presse": "Press Articles",
    "Formation au digital": "Digital Training",
    "Informatique": "IT / Digital",
    "Entreprise libérée": "Liberated Company",
    "Consultant indépendant": "Independent Consultant",
    "Ouvrage collectif": "Collective Work",
    "Webinaires passés": "Past Webinars",
    "Soirée de lancement": "Launch Evening",

    # ── Certificat Centrale page ──
    "Certificat « Comex Codir Gouvernance 5.0 »": "'Comex Codir Governance 5.0' Certificate",
    "Certificat Comex Codir Gouvernance 5.0": "Comex Codir Governance 5.0 Certificate",
    "Formation au Comex/Codir": "Comex/Codir Training",
    "Objectif du programme": "Programme Objective",
    "Public visé": "Target Audience",
    "Durée": "Duration",
    "Tarif": "Fee",
    "Lieu": "Location",
    "Intervenants": "Speakers",
    "Programme": "Programme",
    "Inscription": "Registration",
    "Modalités": "Terms",

    # ── Construction page common text ──
    "Cette page est en cours de construction.": "This page is under construction.",
    "Le contenu de cette page est en cours de préparation.": "The content of this page is being prepared.",
    "Pour toute question, n'hésitez pas à nous contacter :": "For any questions, please do not hesitate to contact us:",
    "Cette page sera bientôt disponible.": "This page will be available soon.",
    "Contenu à venir": "Content coming soon",
    "Page en construction": "Page under construction",
}


# ─── Helpers ──────────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    """Convert text to a slug for i18n keys."""
    t = text.lower().strip()[:60]
    t = re.sub(r'[àâä]', 'a', t)
    t = re.sub(r'[éèêë]', 'e', t)
    t = re.sub(r'[îï]', 'i', t)
    t = re.sub(r'[ôö]', 'o', t)
    t = re.sub(r'[ùûü]', 'u', t)
    t = re.sub(r'[ç]', 'c', t)
    t = re.sub(r'[œ]', 'oe', t)
    t = re.sub(r'[«»""\'\'\u2019\u2018\u201c\u201d\u2039\u203a]', '', t)
    t = re.sub(r'[^a-z0-9]+', '_', t)
    return t.strip('_')[:45]


def page_key(filename: str) -> str:
    return "page_" + Path(filename).stem.replace("-", "_")


def clean_text(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


def translate_text(fr_text: str) -> str:
    """Translate FR→EN. Exact match first, then partial."""
    txt = fr_text.strip()

    # Exact match
    if txt in TRANSLATIONS:
        return TRANSLATIONS[txt]

    # Without trailing punctuation
    stripped = txt.rstrip('.,:;!? ')
    if stripped in TRANSLATIONS:
        return TRANSLATIONS[stripped] + txt[len(stripped):]

    # Best partial match for longer texts
    best_key = None
    best_len = 0
    for fr_key in TRANSLATIONS:
        if fr_key in txt and len(fr_key) > best_len and len(fr_key) > 15:
            best_key = fr_key
            best_len = len(fr_key)
    if best_key:
        return txt.replace(best_key, TRANSLATIONS[best_key])

    # Return original text (flagged for manual review)
    return txt


def should_translate(el: Tag) -> bool:
    """Check if an element should be translated."""
    # Skip if already has data-i18n
    if el.get('data-i18n'):
        return False
    # Skip hidden/style/script children
    if el.find_parent(SKIP_TAGS):
        return False
    return True


def get_direct_text(el: Tag) -> str:
    """Get the full visible text of an element (including inline children)."""
    return clean_text(el.get_text(strip=True))


def is_translatable(text: str) -> bool:
    """Check if text is worth translating."""
    if len(text) < MIN_TEXT_LEN:
        return False
    if text.isdigit():
        return False
    if re.match(r'^[\d\s\W]+$', text):
        return False
    if re.match(r'^https?://', text):
        return False
    if re.match(r'^[\w.+-]+@[\w-]+\.', text):
        return False
    # Skip Font Awesome class-only content
    if re.match(r'^fa[srlbd]?\s+fa-', text):
        return False
    return True


# ─── Main processing ─────────────────────────────────────────────────────────

def process_page(filepath: Path, fr_dict: dict, en_dict: dict) -> int:
    """Process one HTML page. Returns count of new keys."""
    rel = filepath.relative_to(ROOT)
    is_subpage = filepath.parent != ROOT
    ns = page_key(filepath.name)

    print(f"  {rel}")

    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Find all content elements
    page_fr = {}
    page_en = {}
    seen_slugs = set()
    count = 0

    for tag_name in CONTENT_TAGS:
        for el in soup.find_all(tag_name):
            if not should_translate(el):
                continue

            text = get_direct_text(el)
            if not is_translatable(text):
                continue

            # Generate unique key
            slug = slugify(text)
            if not slug:
                continue

            if slug in seen_slugs:
                # Add counter for duplicates
                i = 2
                while f"{slug}_{i}" in seen_slugs:
                    i += 1
                slug = f"{slug}_{i}"
            seen_slugs.add(slug)

            full_key = f"{ns}.{slug}"

            # Store translations
            page_fr[slug] = text
            page_en[slug] = translate_text(text)

            # Inject data-i18n attribute
            el['data-i18n'] = full_key
            count += 1

    if count == 0:
        print(f"    (no translatable text)")
        return 0

    # Ensure i18n.js is loaded
    head = soup.find('head')
    if head:
        # Check if i18n.js is already included
        existing = soup.find('script', src=re.compile(r'i18n\.js'))
        if not existing:
            prefix = "../" if is_subpage else ""
            # Find includes.js to insert before it
            includes_script = soup.find('script', src=re.compile(r'includes\.js'))
            if includes_script:
                new_script = soup.new_tag('script', src=f'{prefix}js/i18n.js')
                includes_script.insert_before(new_script)
                includes_script.insert_before('\n    ')

    # Write modified HTML
    output = str(soup)

    # Fix common BeautifulSoup formatting issues
    # Restore DOCTYPE if missing
    if '<!DOCTYPE' not in output[:50] and '<!DOCTYPE' in html[:50]:
        output = html[:html.index('>')+1] + '\n' + output[output.index('<html'):]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(output)

    # Store in dicts
    fr_dict[ns] = page_fr
    en_dict[ns] = page_en

    print(f"    +{count} keys")
    return count


def main():
    print("=" * 60)
    print("G&S i18n Page Translator (BeautifulSoup)")
    print("=" * 60)

    # Load existing translations
    with open(FR_JSON, 'r', encoding='utf-8') as f:
        fr_dict = json.load(f)
    with open(EN_JSON, 'r', encoding='utf-8') as f:
        en_dict = json.load(f)

    total = 0

    # Process actualites.html
    f = ROOT / "actualites.html"
    if f.exists():
        total += process_page(f, fr_dict, en_dict)

    # Process mentions-legales.html
    f = ROOT / "mentions-legales.html"
    if f.exists():
        total += process_page(f, fr_dict, en_dict)

    # Process plan-du-site.html
    f = ROOT / "plan-du-site.html"
    if f.exists():
        total += process_page(f, fr_dict, en_dict)

    # Process all pages/*.html
    skip = {"0-template.html", "article-template.html",
            "construction-template.html", "template-bootstrap.html"}

    for page in sorted(PAGES_DIR.glob("*.html")):
        if page.name in skip:
            continue
        total += process_page(page, fr_dict, en_dict)

    # Save updated translations
    with open(FR_JSON, 'w', encoding='utf-8') as f:
        json.dump(fr_dict, f, ensure_ascii=False, indent=2)

    with open(EN_JSON, 'w', encoding='utf-8') as f:
        json.dump(en_dict, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 60}")
    print(f"Total keys added: {total}")
    print(f"Updated: {FR_JSON.relative_to(ROOT)}")
    print(f"Updated: {EN_JSON.relative_to(ROOT)}")

    # Review report: strings where EN == FR (not translated)
    review = []
    for ns_key, ns_data in fr_dict.items():
        if not ns_key.startswith("page_"):
            continue
        en_ns = en_dict.get(ns_key, {})
        if isinstance(ns_data, dict):
            for k, v in ns_data.items():
                en_v = en_ns.get(k, "")
                if en_v == v and len(v) > 10:
                    review.append(f"{ns_key}.{k} = {v[:100]}")

    if review:
        rpath = ROOT / "scripts" / "translation-review.txt"
        with open(rpath, 'w', encoding='utf-8') as f:
            f.write(f"# Strings needing manual English translation ({len(review)} items)\n\n")
            for item in review:
                f.write(item + "\n")
        print(f"\n  {len(review)} strings need manual translation")
        print(f"  Review: scripts/translation-review.txt")

    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
