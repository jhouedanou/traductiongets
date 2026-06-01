#!/usr/bin/env python3
"""
batch-translate.py — Translate all remaining French strings in en.json
that are identical to their French counterparts.

This script reads fr.json and en.json, finds all page_* entries where
EN == FR (untranslated), and provides translations.

Usage:
    python3 scripts/batch-translate.py
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FR_JSON = ROOT / "data" / "translations" / "fr.json"
EN_JSON = ROOT / "data" / "translations" / "en.json"

# ─── Comprehensive Translation Map ───────────────────────────────────────────
# Key French phrases/sentences → English translations
# Ordered longest-first for best matching

PHRASE_MAP = {
    # Dates
    "janvier": "January", "février": "February", "mars": "March",
    "avril": "April", "mai": "May", "juin": "June",
    "juillet": "July", "août": "August", "septembre": "September",
    "octobre": "October", "novembre": "November", "décembre": "December",

    # Common words/phrases
    "Accueil": "Home",
    "Retour à l'accueil": "Back to Home",
    "Cliquer ici": "Click here",
    "cliquer ici": "click here",
    "En savoir plus": "Read more",
    "Télécharger": "Download",
    "télécharger": "download",
    "Voir les détails": "View details",
    "Pour plus d'informations": "For more information",
    "N'hésitez pas à nous contacter": "Do not hesitate to contact us",
    "n'hésitez pas à envoyer un courriel": "do not hesitate to send an email",
    "envoyer un courriel": "send an email",
    "courriel": "email",
    "Pour toute question": "For any question",
    "En cours de construction": "Under construction",
    "en cours de construction": "under construction",
    "en cours de développement": "under development",
    "Le contenu sera disponible prochainement": "Content will be available soon",
    "Page en cours de construction": "Page under construction",
    "Email :": "Email:",
    "Contact :": "Contact:",
    "Tél :": "Phone:",
    "Tél.": "Phone",
    "Site internet": "Website",
    "Courrier": "Mail",
    "Lire": "Read",
    "Voir": "See",
    "Vidéo": "Video",
    "Photo": "Photo",
    "Puis,": "Then,",
    "puis": "then",
    "Avec": "With",
    "avec": "with",
    "pour": "for",
    "dans": "in",
    "des": "of the",

    # Corporate governance vocabulary
    "Conseil d'Administration": "Board of Directors",
    "conseil d'administration": "board of directors",
    "Conseil de Surveillance": "Supervisory Board",
    "administrateur indépendant": "independent director",
    "Administrateur indépendant": "Independent Director",
    "administrateurs indépendants": "independent directors",
    "administrateur": "director",
    "Administrateur": "Director",
    "administrateurs": "directors",
    "Administrateurs": "Directors",
    "administratrice": "female director",
    "administratrices": "female directors",
    "mandataire social": "corporate officer",
    "mandataires sociaux": "corporate officers",
    "mandataire": "officer",
    "Comité": "Committee",
    "comité": "committee",
    "Comex": "Comex",
    "Codir": "Codir",
    "Directoire": "Management Board",
    "directoire": "management board",
    "Directeur Général": "Chief Executive Officer",
    "directeur général": "chief executive officer",
    "Président": "Chairman",
    "président": "chairman",
    "PDG": "CEO",
    "Secrétaire Général": "Secretary General",
    "Secrétaire Générale": "Secretary General",
    "gouvernance d'entreprise": "corporate governance",
    "Gouvernance d'entreprise": "Corporate governance",
    "corporate governance": "corporate governance",
    "Corporate Governance": "Corporate Governance",
    "gouvernance": "governance",
    "Gouvernance": "Governance",
    "instance de direction": "governing body",
    "instances de direction": "governing bodies",
    "instances dirigeantes": "governing bodies",
    "Instances de Gouvernance": "Governance Bodies",

    # G&S specific
    "Gouvernance & Structures": "Gouvernance & Structures",
    "Gouvernance-Advisors": "Governance Advisors",
    "G & S": "G & S",
    "G&S": "G&S",
    "Guy Le Péchon": "Guy Le Péchon",

    # Law terms
    "loi Rixain": "Rixain Law",
    "Loi Rixain": "Rixain Law",
    "loi Zimmerman": "Zimmerman Law",
    "Loi Zimmerman": "Zimmerman Law",
    "Loi Copé-Zimmerman": "Copé-Zimmerman Law",
    "loi Copé Zimmerman": "Copé-Zimmerman Law",
    "Loi Pacte": "Pacte Law",
    "directive européenne": "European directive",
    "Directive Européenne": "European Directive",
    "Commission Européenne": "European Commission",
    "proposition de Directive": "proposed Directive",

    # Business terms
    "sociétés cotées": "listed companies",
    "sociétés françaises": "French companies",
    "société": "company",
    "sociétés": "companies",
    "entreprise": "company",
    "entreprises": "companies",
    "Entreprise": "Company",
    "bourse": "stock exchange",
    "cotée": "listed",
    "cotées": "listed",
    "non cotées": "unlisted",
    "filiale": "subsidiary",
    "filiales": "subsidiaries",
    "chiffre d'affaires": "turnover",
    "bilan": "balance sheet",
    "capital": "capital",
    "actionnaire": "shareholder",
    "actionnaires": "shareholders",
    "investisseur": "investor",
    "investisseurs": "investors",

    # Féminisation
    "féminisation": "feminisation",
    "Féminisation": "Feminisation",
    "femmes": "women",
    "hommes": "men",
    "parité": "parity",
    "Parité": "Parity",
    "mixité": "gender diversity",
    "Mixité": "Gender Diversity",
    "quotas": "quotas",

    # Documents
    "rapport annuel": "annual report",
    "Rapport Annuel": "Annual Report",
    "rapports annuels": "annual reports",
    "rapport": "report",
    "Rapport": "Report",
    "étude": "study",
    "Étude": "Study",
    "études": "studies",
    "enquête": "survey",
    "Enquête": "Survey",
    "enquêtes": "surveys",
    "base de données": "database",
    "synthèse": "summary",
    "Synthèse": "Summary",
    "transparents": "slides",
    "présentation": "presentation",
    "Présentation": "Presentation",
    "programme": "programme",
    "Programme": "Programme",
    "bibliographie": "bibliography",
    "Bibliographie": "Bibliography",
    "formation": "training",
    "Formation": "Training",
    "formations": "training courses",
    "Formations": "Training courses",
    "certificat": "certificate",
    "Certificat": "Certificate",
    "article": "article",
    "Article": "Article",
    "articles": "articles",
    "Articles": "Articles",
    "livre": "book",
    "Livre": "Book",
    "livres": "books",
    "note": "note",
    "notes": "notes",
    "document": "document",
    "documents": "documents",
    "Documents": "Documents",

    # Actions / verbs
    "recherche": "search",
    "Recherche": "Search",
    "diagnostic": "assessment",
    "Diagnostic": "Assessment",
    "évaluation": "evaluation",
    "Évaluation": "Evaluation",
    "mission": "assignment",
    "Mission": "Assignment",
    "missions": "assignments",
    "Missions": "Assignments",
    "prestation": "service",
    "Prestation": "Service",
    "prestations": "services",
    "Prestations": "Services",
    "conseil": "consulting",
    "Conseil": "Council",
    "nomination": "appointment",
    "cooptation": "co-optation",
    "recrutement": "recruitment",
    "candidat": "candidate",
    "Candidat": "Candidate",
    "candidats": "candidates",
    "Candidats": "Candidates",

    # Misc
    "actuellement": "currently",
    "prochainement": "soon",
    "également": "also",
    "notamment": "notably",
    "ainsi": "thus",
    "Ainsi": "Thus",
    "en effet": "indeed",
    "En effet": "Indeed",
    "en particulier": "in particular",
    "En particulier": "In particular",
    "par exemple": "for example",
    "c'est-à-dire": "that is to say",
    "c.-à-d.": "i.e.",
    "etc.": "etc.",
    "cf.": "cf.",

    # Institutions
    "Institut Français des Administrateurs": "French Institute of Directors",
    "IFA": "IFA",
    "INSEAD": "INSEAD",
    "Euronext": "Euronext",
    "CAC 40": "CAC 40",
    "Cercle des Administrateurs": "Directors' Circle",

    # Page-specific content
    "Mentions légales": "Legal Notice",
    "Confidentialité": "Privacy",
    "Plan du site": "Sitemap",
    "Politique de confidentialité": "Privacy Policy",
    "Conditions d'utilisation": "Terms of Use",
    "Loi informatique, fichiers et libertés": "Data Protection and Civil Liberties Act",
    "Utilisation des données collectées": "Use of Collected Data",
    "Confidentialité des données": "Data Confidentiality",
    "Responsabilité": "Liability",
    "Liens Internet": "Internet Links",
    "Cookies": "Cookies",
    "données personnelles": "personal data",
    "Données personnelles": "Personal Data",

    # Informatics page
    "informatique": "IT",
    "Informatique": "IT",
    "numérique": "digital",
    "Numérique": "Digital",
    "transformation numérique": "digital transformation",
    "intelligence artificielle": "artificial intelligence",
    "Intelligence artificielle": "Artificial Intelligence",
    "réseaux sociaux": "social media",
    "micro-ordinateurs": "personal computers",

    # Construction pages standard text
    "Cette page est actuellement en cours de développement.": "This page is currently under development.",
    "Le contenu sera disponible prochainement.": "Content will be available soon.",
    "Cette page est en cours de construction.": "This page is under construction.",
}


def translate_sentence(fr: str) -> str:
    """Translate a French sentence to English using phrase-level replacement
    plus word-level fallback for common patterns."""

    # Skip if already looks English
    if re.match(r'^[A-Z][a-z]+ [a-z]', fr) and all(c.isascii() for c in fr):
        return fr

    en = fr

    # Sort phrases by length (longest first) for best matching
    sorted_phrases = sorted(PHRASE_MAP.items(), key=lambda x: -len(x[0]))

    for fr_phrase, en_phrase in sorted_phrases:
        if fr_phrase in en:
            en = en.replace(fr_phrase, en_phrase)

    return en


def main():
    print("=" * 60)
    print("Batch Translation of Remaining Strings")
    print("=" * 60)

    with open(FR_JSON, 'r', encoding='utf-8') as f:
        fr_dict = json.load(f)
    with open(EN_JSON, 'r', encoding='utf-8') as f:
        en_dict = json.load(f)

    translated = 0
    still_untranslated = 0

    for ns_key in list(en_dict.keys()):
        if not ns_key.startswith("page_"):
            continue

        fr_ns = fr_dict.get(ns_key, {})
        en_ns = en_dict.get(ns_key, {})

        if not isinstance(fr_ns, dict) or not isinstance(en_ns, dict):
            continue

        for key in list(en_ns.keys()):
            fr_val = fr_ns.get(key, "")
            en_val = en_ns.get(key, "")

            # Only translate if EN == FR (untranslated)
            if en_val == fr_val and len(fr_val) > 3:
                new_en = translate_sentence(fr_val)

                # Check if we actually translated something
                if new_en != fr_val:
                    en_ns[key] = new_en
                    translated += 1
                else:
                    still_untranslated += 1

        en_dict[ns_key] = en_ns

    # Save
    with open(EN_JSON, 'w', encoding='utf-8') as f:
        json.dump(en_dict, f, ensure_ascii=False, indent=2)

    print(f"\n  Translated: {translated} strings")
    print(f"  Still untranslated: {still_untranslated} strings")
    print(f"  Updated: {EN_JSON.relative_to(ROOT)}")

    # Updated review file
    review = []
    for ns_key, ns_data in fr_dict.items():
        if not ns_key.startswith("page_"):
            continue
        en_ns = en_dict.get(ns_key, {})
        if isinstance(ns_data, dict):
            for k, v in ns_data.items():
                en_v = en_ns.get(k, "")
                if en_v == v and len(v) > 10:
                    review.append(f"{ns_key}.{k} = {v[:120]}")

    if review:
        rpath = ROOT / "scripts" / "translation-review.txt"
        with open(rpath, 'w', encoding='utf-8') as f:
            f.write(f"# Remaining untranslated strings ({len(review)} items)\n")
            f.write("# These need manual translation or adding to the phrase map\n\n")
            for item in review:
                f.write(item + "\n")
        print(f"  Review: {rpath.relative_to(ROOT)} ({len(review)} items)")

    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
