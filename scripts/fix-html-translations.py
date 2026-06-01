#!/usr/bin/env python3
"""
fix-html-translations.py — Fix stripped HTML in fr.json and en.json.

The original translate-pages.py used BeautifulSoup's get_text() which stripped
all HTML tags. But the i18n system (i18n.js) uses innerHTML swapping, so the
JSON values must contain the raw HTML markup.

This script:
1. Scans all HTML files for elements with data-i18n attributes
2. Extracts the actual innerHTML (preserving <strong>, <a>, <br/>, <sup>, etc.)
3. Updates fr.json page_* keys with correct innerHTML values
4. Updates en.json page_* keys with English translations that preserve HTML structure
"""

import json
import re
import os
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag

# ─── Configuration ───────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent
PAGES_DIR = ROOT / "pages"
INDEX_HTML = ROOT / "index.html"
FR_JSON = ROOT / "data" / "translations" / "fr.json"
EN_JSON = ROOT / "data" / "translations" / "en.json"

# ─── Brand names to preserve (never translate) ──────────────────────────────

BRAND_NAMES = {
    "Gouvernance et Structures",
    "Gouvernance & Structures",
    "G & S",
    "G&S",
    "G & S",  # nbsp variant
    "Guy Le Péchon",
    "Maison Effervescence",
    "Centrale-Supelec Executive Education",
    "Centrale-Supélec Executive Education",
    "Centrale Supelec Executive Education",
    "Centrale Supélec Executive Education",
    "Valérie Lejeune",
    "Institut Français des Administrateurs",
    "AdValorem",
    "L'Harmattan",
    "Pascal Picq",
    "Marie-Pierre Rixain",
    "Hi-Team",
    "INSEAD",
    "ETHIC",
}

# ─── Comprehensive FR→EN phrase translation map ─────────────────────────────
# Applied at text-node level, longest match first

PHRASE_MAP = {
    # === Certificat Centrale page ===
    "Certificat pour les membres de COMEX CODIR": "Certificate for COMEX CODIR Members",
    "en place ou potentiel(le)s": "Current or Potential",
    "Gouvernance 5.0": "Governance 5.0",
    "Les deux cabinets de conseils,": "The two consulting firms,",
    "ont depuis plus d'un an remarqué que, s'il existait pour les hommes et les femmes de nombreuses": "have for more than a year noted that, while there were numerous",
    "formations aux Conseils d'Administration": "Board of Directors training programmes",
    ", par contre tel n'était pas le cas pour les COMEX CODIR.": ", this was not the case for COMEX CODIR.",
    "par contre tel n'était pas le cas pour les COMEX CODIR": "this was not the case for COMEX CODIR",
    "Après une première tentative avec organisme universitaire, ils ont pu, aidés d'autres spécialistes élaborer avec": "After a first attempt with a university body, they were able, with the help of other specialists, to develop with",
    ", un programme approfondi pour la formation des membres des COMEX CODIR en place ou souhaitant le devenir.": ", an in-depth programme for the training of current or aspiring COMEX CODIR members.",
    "un programme approfondi pour la formation des membres des COMEX CODIR en place ou souhaitant le devenir": "an in-depth programme for the training of current or aspiring COMEX CODIR members",
    "L'esprit général du cours est de s'attacher à ce que les participants, fassent leurs les processus permettant à un organisme collectif opérationnel de réussir dans sa liaison entre les conseils d'administration et les opérationnels, en utilisant au mieux tous les outils et approches modernes aujourd'hui disponibles (": "The general spirit of the course is to ensure that participants internalise the processes enabling an operational collective body to succeed in its liaison between boards of directors and operational teams, making the best use of all modern tools and approaches available today (",
    "L'esprit général du cours est de s'attacher à ce que les participants, fassent leurs les processus permettant à un organisme collectif opérationnel de réussir dans sa liaison entre les conseils d'administration et les opérationnels, en utilisant au mieux tous les outils et approches modernes aujourd'hui disponibles": "The general spirit of the course is to ensure that participants internalise the processes enabling an operational collective body to succeed in its liaison between boards of directors and operational teams, making the best use of all modern tools and approaches available today",
    "Pour découvrir ce programme, il vous est possible de visionner :": "To discover this programme, you can view:",
    "Pour découvrir ce programme, il vous est possible de visionner": "To discover this programme, you can view",
    "ou bien": "or",
    "avec un directeur opérationnel expérimenté.": "with an experienced operational director.",
    "avec un directeur opérationnel expérimenté": "with an experienced operational director",
    "La brochure": "The brochure",
    "donne tous les détails.": "gives all the details.",
    "donne tous les détails": "gives all the details",
    "Une alliance a été conclue avec l'": "An alliance has been concluded with the ",
    "pour faire connaître ce nouveau certificat.": "to promote this new certificate.",
    "pour faire connaître ce nouveau certificat": "to promote this new certificate",
    "La": "The",
    "session": "session",
    "se déroulera à partir du": "will take place from",
    "23 avril 2026": "23 April 2026",
    ". Il reste encore quelques places.": ". A few places are still available.",
    "Il reste encore quelques places.": "A few places are still available.",
    "Il reste encore quelques places": "A few places are still available",

    # === Common phrases ===
    "Retour à l'accueil": "Back to Home",
    "Accueil": "Home",
    "Actualités futures": "Upcoming Events",
    "Actualités": "News",
    "Passé récent": "Recent Past",
    "Page en cours de construction": "Page Under Construction",
    "Page en cours de développement": "Page Under Development",
    "Cette page est actuellement en cours de construction.": "This page is currently under construction.",
    "Cette page est actuellement en cours de développement.": "This page is currently under development.",
    "Cette page est en cours de construction.": "This page is under construction.",
    "Le contenu sera disponible prochainement.": "Content will be available soon.",
    "Le contenu de cette page est en cours de préparation.": "The content of this page is being prepared.",
    "Pour plus d'informations": "For more information",
    "N'hésitez pas à nous contacter pour obtenir des informations sur ce sujet :": "Please do not hesitate to contact us for information on this topic:",
    "Pour toute question, n'hésitez pas à nous contacter :": "For any questions, please do not hesitate to contact us:",
    "Cliquer ici": "Click here",
    "En savoir plus": "Read more",
    "Télécharger": "Download",
    "Voir les détails": "View details",
    "Ouvrir": "Open",
    "En construction": "Under construction",
    "Email :": "Email:",
    "Contact :": "Contact:",
    "Nous contacter": "Contact Us",
    "Contenu à venir": "Content coming soon",
    "Page en construction": "Page under construction",
    "Cette page sera bientôt disponible.": "This page will be available soon.",

    # === Titles and headings ===
    "Administrateur indépendant un vaccin ?": "Independent Director - a Vaccine?",
    "Administrateur indépendant un vaccin": "Independent Director - a Vaccine",
    "Critères d'indépendance": "Independence Criteria",
    "L'actualité n'annihile pas les écrits passés importants": "Current events do not invalidate important past writings",
    "Articles de presse": "Press Articles",
    "Bibliographie \"Corporate Governance\"": "Corporate Governance Bibliography",
    "Notes et articles publiés par G & S": "Articles and papers published by G & S",
    "Rapports": "Reports",
    "Livres": "Books",
    "Diagnostics de Conseils d'Administration": "Board of Directors Assessments",
    "Diagnostic de Conseils d'Administration ou de Surveillance": "Board of Directors or Supervisory Board Assessment",
    "Candidats mandataires sociaux": "Corporate Officer Candidates",
    "Candidature comme mandataire": "Apply as a Board Member",
    "Féminisation des instances dirigeantes": "Gender Diversity in Corporate Leadership",
    "Observatoire des genres": "Gender Observatory",
    "Assises de la parité": "Gender Parity Conference",
    "Formations d'Administrateurs": "Board Member Training",
    "Formations INSTANCES DE DIRECTIONS": "LEADERSHIP BODIES TRAINING",
    "Des formations originales proposées par G & S": "Original training programmes offered by G & S",
    "Formations institutionnelles": "Institutional Training",
    "Formation au Comex Codir": "Comex Codir Training",
    "Formation au Comex/Codir": "Comex/Codir Training",
    "Formation au digital": "Digital Training",
    "Les missions": "Assignments",
    "Recherche de mandataires sociaux": "Search for Corporate Officers",
    "Travaux de l'IFA sur le digital": "IFA Digital Working Group Reports",
    "IFA et le Numérique": "IFA and Digital",
    "Documents pour l'administrateur": "Documents for directors",
    "Catalogue de documents pour l'administrateur": "Document catalogue for directors",
    "Sites intéressants": "Useful Links",
    "Gouvernance Advisors": "Governance Advisors",
    "Shadow Conseil d'Administration de jeunes": "Youth Shadow Board of Directors",
    "Shadow Conseil d'Administration": "Shadow Board of Directors",
    "Intelligence émotionnelle des administrateurs": "Emotional Intelligence of Directors",
    "Intelligence collective": "Collective Intelligence",
    "Le monde et la gouvernance des ETI": "The World and the Governance of Mid-Sized Companies",
    "Le Monde et la gouvernance des ETI": "The World and the Governance of Mid-Sized Companies",
    "Salariés et Dirigeants en Confiance": "Employees and Leaders in Trust",
    "Apports de l'Intelligence artificielle à la Compliance": "Contributions of Artificial Intelligence to Compliance",
    "Le monde numérique et la relation client": "The Digital World and Customer Relations",
    "Comment les DSI peuvent impliquer les Conseils d'Administration": "How CIOs Can Engage Boards of Directors",
    "Facilities Management, Les normes Européennes": "Facilities Management - European Standards",
    "Instances de gouvernance": "Governance Bodies",
    "Club Européen": "European Club",
    "Comparaison féminisation Boards et Comex": "Comparison of Board and Comex Gender Diversity",
    "Directive Européenne": "European Directive",
    "Loi Pacte": "Pacte Law",
    "Loi Rixain": "Rixain Law",
    "Loi Zimmerman": "Zimmerman Law",
    "Glossaire des Prestations de conseil": "Consulting Services Glossary",
    "Auto diagnostic Loi Rixain": "Rixain Law Self-Assessment",
    "Informatique": "IT / Digital",
    "Entreprise libérée": "Liberated Company",
    "Consultant indépendant": "Independent Consultant",
    "Ouvrage collectif": "Collective Work",
    "Webinaires passés": "Past Webinars",
    "Soirée de lancement": "Launch Evening",
    "Qui est G & S": "Who is G & S",
    "Présentation de G & S": "About G & S",
    "Historique": "History",
    "Communiqué de presse du 4 mai 2009": "Press Release of 4 May 2009",
    "Généralités": "General",
    "Généralités Corporate Governance": "Corporate Governance Overview",
    "Programme": "Programme",
    "Inscription": "Registration",
    "Modalités": "Terms",
    "Objectif du programme": "Programme Objective",
    "Public visé": "Target Audience",
    "Durée": "Duration",
    "Tarif": "Fee",
    "Lieu": "Location",
    "Intervenants": "Speakers",

    # === Long phrases found in various pages ===
    "Ni lien familial proche avec un mandataire social.": "No close family ties with a corporate officer.",
    "Ni administrateur de l'entreprise depuis plus de douze ans.": "Not a director of the company for more than twelve years.",
    "Inférieur à 10 % : indépendant si ne participe pas au contrôle.": "Below 10%: independent if does not participate in control.",
    "Actionnaires :": "Shareholders:",
    "Actionnaires": "Shareholders",

    # === AVANT-PROPOS / IA compliance ===
    "AVANT-PROPOS : RÉFLEXIONS D'UN BÉOTIEN DE L'IA ET DE LA COMPLIANCE": "FOREWORD: REFLECTIONS OF A LAYPERSON ON AI AND COMPLIANCE",
    "N'ayant pas de compétences particulières sur l'IA, j'ai simplement rédigé l'avant-propos qui suit.": "Not having any particular expertise in AI, I have simply written the following foreword.",

    # === Construction / info pages ===
    "Contenu à venir :": "Content coming soon:",
    "Informations détaillées, ressources et outils relatifs à ce sujet.": "Detailed information, resources and tools related to this topic.",

    # === Assises parite ===
    "Palais des Congrès, Paris": "Palais des Congres, Paris",
    "Un événement majeur pour l'égalité professionnelle": "A major event for professional equality",
    "Intervenants prestigieux": "Distinguished Speakers",
    "Objectifs de l'événement": "Event Objectives",
    "Résultats et impact": "Results and Impact",
    "Participants": "Participants",
    "Intervenants experts": "Expert Speakers",
    "de conférences": "Lectures",
    "Tables rondes": "Panel Discussions",
    "Retour d'expérience sur les initiatives réussies d'égalité professionnelle.": "Feedback on successful professional equality initiatives.",
    "Leadership féminin et performance": "Female Leadership and Performance",
    "Échanges et opportunités": "Exchanges and Opportunities",
    "Promouvoir l'égalité professionnelle": "Promote professional equality",
    "Échanger les bonnes pratiques": "Share best practices",
    "Sensibiliser aux enjeux de diversité": "Raise awareness of diversity issues",
    "Accompagner les transformations": "Support transformations",
    "Création d'un réseau de mentoring": "Creation of a mentoring network",
    "Lancement d'un observatoire de l'égalité": "Launch of an equality observatory",
    "Rendez-vous trimestriels programmés": "Quarterly meetings scheduled",
    "Indicateurs de suivi définis": "Monitoring indicators defined",
    "Prochaines assises prévues en 2025": "Next conference planned for 2025",
    "Engagements pris": "Commitments made",
    "Suivi des actions": "Action monitoring",
    "Obtenir le rapport complet": "Obtain the full report",
    "9h00 - Ouverture": "9:00 AM - Opening",
    "9h30 - Table ronde 1": "9:30 AM - Panel 1",
    "11h00 - Table ronde 2": "11:00 AM - Panel 2",
    "14h00 - Table ronde 3": "2:00 PM - Panel 3",
    "16h00 - Networking": "4:00 PM - Networking",

    # === Candidats mandataires sociaux ===
    "CANDIDAT(E)S MANDATAIRES — ADMINISTRATRICES/ADMINISTRATEURS": "BOARD MEMBER CANDIDATES - FEMALE AND MALE DIRECTORS",
    "Pour connaître leur nom et leurs coordonnées et les joindre, écrire à contact@g-et-s.com en indiquant la référence figurant.": "To learn their names and contact details and reach them, write to contact@g-et-s.com quoting the reference shown.",
    "Femmes candidates": "Female Candidates",
    "Hommes candidats": "Male Candidates",
    "Industrie pharmaceutique": "Pharmaceutical Industry",
    "Équipements et appareillages industriels (Énergie, Transports, Haute technologie)": "Industrial Equipment (Energy, Transport, High Technology)",
    "Aviation, Aéronautique, Spatial, Défense & Sécurité": "Aviation, Aeronautics, Space, Defence & Security",
    "Édition de logiciel": "Software Publishing",
    "Génie médical France et USA": "Medical Engineering France and USA",
    "Presse et Médias — Développement international": "Press and Media - International Development",
    "Administratrice indépendante grande société européenne": "Independent female director, large European company",

    # === Candidats mandataires form ===
    "POSTULER À DES POSTES D'ADMINISTRATEURS": "APPLY FOR DIRECTOR POSITIONS",
    "Postuler à des postes d'administrateurs": "Apply for director positions",
    "CANDIDATURE COMME MANDATAIRE": "APPLICATION AS BOARD MEMBER",
    "Candidature comme mandataire": "Application as Board Member",
    "Adresse électronique": "Email Address",
    "Adresse partie 1": "Address Line 1",
    "Adresse partie 2": "Address Line 2",
    "Adresse partie 3": "Address Line 3",
    "Code postal": "Postal Code",
    "Site internet": "Website",
    "Secteur d'activité 1": "Business Sector 1",
    "Secteur d'activité 2": "Business Sector 2",
    "Secteur d'activité 3": "Business Sector 3",
    "Langue maternelle 1": "Mother Tongue 1",
    "Langue maternelle 2": "Mother Tongue 2",
    "Langue courante 1": "Working Language 1",
    "Langue courante 2": "Working Language 2",
    "Langue courante 3": "Working Language 3",
    "Organisation": "Organisation",
    "Commentaires succincts éventuels": "Brief optional comments",
    "À ce stade un CV est inutile.": "At this stage a CV is not necessary.",
    "Les éléments figurant en bleu sont indispensables, les autres sont souhaitables.": "Items shown in blue are required, others are recommended.",
    "UTILISATION PAR G & S DES INFORMATIONS DU FORMULAIRE": "USE BY G & S OF FORM INFORMATION",
    "Indications pour le remplissage du formulaire": "Instructions for completing the form",
    "Un secteur d'activité correspond en général à un marché": "A business sector generally corresponds to a market",
    "Un pays d'activité est un pays où vous avez vécu au moins un an": "A country of activity is a country where you have lived at least one year",

    # === Catalogue documents ===
    "Documents disponibles en téléchargement": "Documents available for download",
    "Documents utiles pour l'administrateur": "Useful documents for the director",
    "Le contrat d'assurance de protection de l'administrateur": "The director's liability insurance contract",
    "La revue de presse hebdomadaire": "The weekly press review",
    "Catalogue de documents": "Document Catalogue",

    # === Formations administrateurs ===
    "International Directors Program": "International Directors Program",
    "Executive Education — Vision très internationale": "Executive Education - Highly international vision",
    "Divers programmes certifiants": "Various certification programmes",
    "Women Be European Board Ready": "Women Be European Board Ready",
    "Institute of Directors": "Institute of Directors",
    "FORMATIONS INSTITUTIONNELLES": "INSTITUTIONAL TRAINING",
    "DES FORMATIONS ORIGINALES PROPOSÉES PAR G & S": "ORIGINAL TRAINING PROGRAMMES OFFERED BY G & S",

    # === Historique ===
    "Site internet : http://www.g-et-s.com": "Website: http://www.g-et-s.com",
    "Contact : info@g-et-s.com": "Contact: info@g-et-s.com",
    "a rassemblé plus d'une soixantaine de participants": "brought together over sixty participants",
    "Voir les photos dans la colonne de gauche": "See photos in the left column",
    "Le thème a été introduit par Guy Le Péchon, Associé-gérant de": "The topic was introduced by Guy Le Péchon, Managing Partner of",

    # === Informatique ===
    "\"Cloud\" — Visite guidée d'un gros Data Center": "'Cloud' - Guided tour of a large Data Centre",
    "Internet des objets": "Internet of Things",
    "Gestion des documents pour Conseils": "Document Management for Boards",
    "Big Data et relation client": "Big Data and Customer Relations",
    "La cryptographie et les mots de passe": "Cryptography and Passwords",
    "Réalité virtuelle": "Virtual Reality",
    "Salle de gestion de crise": "Crisis Management Room",
    "Intelligence artificielle": "Artificial Intelligence",

    # === Loi Rixain ===
    "Article 14 de la Loi Rixain": "Article 14 of the Rixain Law",
    "Loi Rixain — Décembre 2021": "Rixain Law - December 2021",
    "Impact sur la gouvernance d'entreprise": "Impact on Corporate Governance",
    "Mesures clés de la Loi": "Key Measures of the Law",
    "Mesures clés de l'ensemble de la Loi": "Key Measures of the Entire Law",
    "Calendrier d'application": "Implementation Timeline",
    "Accompagnement G-ET-S": "G-ET-S Support",
    "Quota minimum de femmes dans les instances dirigeantes": "Minimum quota of women in governing bodies",
    "Obligations de reporting renforcées": "Strengthened reporting obligations",
    "Diversification des profils dirigeants": "Diversification of leadership profiles",
    "Amélioration de la prise de décision": "Improved decision-making",
    "Renforcement de la performance économique": "Strengthened economic performance",
    "Meilleure représentativité sociétale": "Better societal representation",
    "Transparence salariale": "Pay transparency",
    "Équilibre vie professionnelle": "Work-life balance",
    "Formation et sensibilisation": "Training and awareness",
    "Plan d'action personnalisé": "Customised action plan",
    "En mars 2029": "By March 2029",
    "Obligation d'atteindre 40% dans ces deux groupes de dirigeants.": "Obligation to reach 40% in these two groups of executives.",
    "Chiffres du ministère du travail": "Ministry of Labour figures",

    # === Shadow conseil ===
    "Pourquoi ? Est-ce possible ? Comment ?": "Why? Is it possible? How?",
    "Une approche innovante : le Conseil d'Administration de jeunes": "An innovative approach: The Youth Board of Directors",
    "Alors, comment procéder ?": "So, how to proceed?",
    "Plus de jeunes dans les Conseils d'Administration ?": "More young people on Boards of Directors?",
    "PLUS DE JEUNES DANS LES CONSEILS D'ADMINISTRATION ?": "MORE YOUNG PEOPLE ON BOARDS OF DIRECTORS?",

    # === Organisation GS ===
    "Diagnostics quant au fonctionnement ou de la composition des Conseils d'Administration ou de Surveillance, Comex ou Codir": "Diagnostics on the functioning or composition of Boards of Directors or Supervisory Boards, Comex or Codir",
    "Recrutement de dirigeants": "Executive Recruitment",
    "Gouvernance et Structures": "Gouvernance et Structures",  # brand name kept

    # === Glossaire ===
    "Le résultat est l'article rédigé par G & S": "The result is the article written by G & S",
    "Images générées par Intelligence artificielle": "Images generated by Artificial Intelligence",

    # === Livre ETI ===
    "Salon du livre des polytechniciens": "Polytechnicians' Book Fair",
    "Atelier ETHIC": "ETHIC Workshop",
    "Sceaux-Smart": "Sceaux-Smart",
    "Dédicaces et événements": "Book signings and events",
    "Éditeur : L'Harmattan, collection AdValorem": "Publisher: L'Harmattan, AdValorem collection",
    "Coordination : Guy Le Péchon (G&S) et Valérie Lejeune": "Coordination: Guy Le Péchon (G&S) and Valérie Lejeune",
    "Lieu : Mairie du 6ème arrondissement de Paris": "Venue: Town Hall of the 6th arrondissement of Paris",
    "Interview de Valérie Lejeune sur ETI Radio": "Interview with Valérie Lejeune on ETI Radio",
    "La soirée de lancement": "The launch evening",

    # === Questionnaire Rixain ===
    "À titre d'exemple, voici deux premières questions du questionnaire :": "As an example, here are the first two questions from the questionnaire:",
    "Pour obtenir le questionnaire complet": "To obtain the full questionnaire",
    "INSTANCE DIRIGEANTE": "GOVERNING BODY",
    "Instance dirigeante": "Governing body",
    "Il s'agit de vos instances dirigeantes hors du Conseil d'Administration ou du Conseil de Surveillance.": "This refers to your governing bodies other than the Board of Directors or Supervisory Board.",
    "Envisagez-vous une évolution du nombre de membres de cette instance dirigeante ?": "Do you anticipate a change in the number of members of this governing body?",
    "Réduction du nombre": "Reduction in number",
    "Augmentation du nombre": "Increase in number",

    # === Mentions legales ===
    "Cookies": "Cookies",
    "Loi Informatique, Fichiers et Libertés": "Data Protection and Civil Liberties Act",
    "Utilisation des données collectées": "Use of Collected Data",
    "Confidentialité des données": "Data Confidentiality",
    "Responsabilité de G & S": "G & S Liability",
    "Liens internet vers G & S et réciproquement": "Internet Links to G & S and Vice Versa",
    "Politique de G & S pour la gestion des données personnelles": "G & S Policy on Personal Data Management",

    # === Actualites ===
    "Simulation de réunions de Conseil d'Administration": "Board of Directors Meeting Simulation",
    "Première journée du nouveau Certificat de formation « Comex Codir, Gouvernance 5.0 »": "First day of the new 'Comex Codir, Governance 5.0' Training Certificate",
    "Consulter l'invitation": "View the invitation",
    "7 juillet 2026": "7 July 2026",

    # === Etude juin 2025 ===
    "Étude de juin 2025": "June 2025 Study",
    "Étude": "Study",

    # === Cours INSEEC ===
    "Intervention similaire possible en intra pour une entreprise.": "Similar in-company intervention possible for a business.",

    # === DSI ===
    "Comment les DSI peuvent impliquer les C.A.": "How CIOs Can Engage Boards",

    # === Facilities management ===
    "Facilities Management, les normes européennes": "Facilities Management - European Standards",

    # === Monde numérique ===
    "L'utilisation de l'Intelligence artificielle devrait faciliter la collecte et l'organisation de ces données « grises ».": "The use of Artificial Intelligence should facilitate the collection and organisation of this 'grey' data.",

    # === Intelligence collective ===
    "La vidéo de mon intervention (que je crois assez originale) est disponible à la page :": "The video of my presentation (which I believe is quite original) is available on the page:",
    "Atelier Intelligence Collective": "Collective Intelligence Workshop",

    # === Travaux IFA ===
    "De quelles informations l'administrateur a-t-il besoin ?": "What Information Does a Director Need?",

}

# Short words that should only be replaced as whole words (with word boundaries)
WORD_LEVEL_MAP = {
    "et": "and",
    "ou": "or",
}


def get_inner_html(element):
    """Extract the innerHTML of a BeautifulSoup element (everything inside the tag)."""
    parts = []
    for child in element.children:
        parts.append(str(child))
    return ''.join(parts)


def normalize_whitespace(text):
    """Normalize whitespace for comparison but preserve structure."""
    return re.sub(r'\s+', ' ', text).strip()


def translate_text_node(text):
    """Translate a text node (plain text, no HTML) from FR to EN.
    Uses longest-match-first strategy from PHRASE_MAP.
    Only replaces phrases that are 4+ chars. Short words use word-boundary matching."""
    if not text or not text.strip():
        return text

    result = text

    # Sort phrases by length (longest first) to avoid partial matches
    sorted_phrases = sorted(PHRASE_MAP.keys(), key=len, reverse=True)

    for fr_phrase in sorted_phrases:
        en_phrase = PHRASE_MAP[fr_phrase]
        # Only do simple replacement for phrases >= 4 chars
        # (short strings risk matching inside words)
        if len(fr_phrase) >= 4 and fr_phrase in result:
            result = result.replace(fr_phrase, en_phrase)

    # For very short words, use word-boundary regex (only "et" and "ou")
    for fr_word, en_word in WORD_LEVEL_MAP.items():
        # Match whole word only, preserving surrounding whitespace
        pattern = r'(?<![a-zA-ZàâäéèêëîïôöùûüçœÀÂÄÉÈÊËÎÏÔÖÙÛÜÇŒ])' + re.escape(fr_word) + r'(?![a-zA-ZàâäéèêëîïôöùûüçœÀÂÄÉÈÊËÎÏÔÖÙÛÜÇŒ\'-])'
        result = re.sub(pattern, en_word, result)

    return result


def translate_html_content(html_content):
    """Translate an HTML string from FR to EN, preserving all HTML tags.
    Only translates text nodes, not tag attributes or tag names."""

    if not html_content or not html_content.strip():
        return html_content

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Walk through all text nodes and translate them
    for text_node in soup.find_all(string=True):
        # Skip if inside a script or style tag
        parent = text_node.parent
        if parent and parent.name in ('script', 'style'):
            continue

        original = str(text_node)
        if not original.strip():
            continue

        # Check if this text is a brand name - skip if so
        stripped = original.strip()
        is_brand = False
        for brand in BRAND_NAMES:
            if stripped == brand:
                is_brand = True
                break
        if is_brand:
            continue

        translated = translate_text_node(original)
        if translated != original:
            text_node.replace_with(NavigableString(translated))

    return str(soup)


def extract_data_i18n_elements(filepath):
    """Parse an HTML file and extract all data-i18n elements with their innerHTML."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    results = {}

    for el in soup.find_all(attrs={'data-i18n': True}):
        key = el['data-i18n']
        # Only process page_* namespace keys
        if not key.startswith('page_'):
            continue

        inner_html = get_inner_html(el)

        # Clean up the innerHTML: normalize leading/trailing whitespace
        # but preserve internal whitespace and HTML structure
        inner_html = inner_html.strip()

        if inner_html:
            results[key] = inner_html

    return results


def main():
    print("=" * 60)
    print("Fix HTML Translations")
    print("=" * 60)

    # Load existing translations
    with open(FR_JSON, 'r', encoding='utf-8') as f:
        fr_dict = json.load(f)
    with open(EN_JSON, 'r', encoding='utf-8') as f:
        en_dict = json.load(f)

    # Collect all data-i18n elements from HTML files
    all_elements = {}

    # Process index.html
    if INDEX_HTML.exists():
        print(f"  Scanning {INDEX_HTML.name}...")
        elements = extract_data_i18n_elements(INDEX_HTML)
        all_elements.update(elements)
        print(f"    Found {len(elements)} page_* elements")

    # Process pages/*.html
    skip_files = {"0-template.html", "article-template.html",
                  "construction-template.html", "template-bootstrap.html"}

    for page in sorted(PAGES_DIR.glob("*.html")):
        if page.name in skip_files:
            continue
        if page.name.endswith('.bak'):
            continue
        print(f"  Scanning {page.name}...")
        elements = extract_data_i18n_elements(page)
        all_elements.update(elements)
        print(f"    Found {len(elements)} page_* elements")

    # Also scan root-level HTML files that might have page_* keys
    for root_html in ['actualites.html', 'mentions-legales.html', 'plan-du-site.html']:
        filepath = ROOT / root_html
        if filepath.exists():
            print(f"  Scanning {root_html}...")
            elements = extract_data_i18n_elements(filepath)
            all_elements.update(elements)
            print(f"    Found {len(elements)} page_* elements")

    print(f"\n  Total page_* elements found in HTML: {len(all_elements)}")

    # Update fr.json and en.json
    fr_updated = 0
    en_updated = 0

    for full_key, inner_html in all_elements.items():
        parts = full_key.split('.', 1)
        if len(parts) != 2:
            continue
        namespace, sub_key = parts

        # Ensure namespace exists in both dicts
        if namespace not in fr_dict:
            fr_dict[namespace] = {}
        if namespace not in en_dict:
            en_dict[namespace] = {}

        # Update FR with actual innerHTML
        old_fr = fr_dict[namespace].get(sub_key, '')
        if old_fr != inner_html:
            fr_dict[namespace][sub_key] = inner_html
            fr_updated += 1

        # Generate EN translation preserving HTML
        en_translation = translate_html_content(inner_html)
        old_en = en_dict[namespace].get(sub_key, '')
        if old_en != en_translation:
            en_dict[namespace][sub_key] = en_translation
            en_updated += 1

    # Save updated translations
    with open(FR_JSON, 'w', encoding='utf-8') as f:
        json.dump(fr_dict, f, ensure_ascii=False, indent=2)

    with open(EN_JSON, 'w', encoding='utf-8') as f:
        json.dump(en_dict, f, ensure_ascii=False, indent=2)

    print(f"\n  FR keys updated: {fr_updated}")
    print(f"  EN keys updated: {en_updated}")
    print(f"  Updated: {FR_JSON.relative_to(ROOT)}")
    print(f"  Updated: {EN_JSON.relative_to(ROOT)}")

    # Show certificat-centrale results for verification
    print(f"\n{'=' * 60}")
    print("Verification: page_certificat_centrale")
    print(f"{'=' * 60}")

    cc_fr = fr_dict.get('page_certificat_centrale', {})
    cc_en = en_dict.get('page_certificat_centrale', {})

    for key in sorted(cc_fr.keys()):
        fr_val = cc_fr[key]
        en_val = cc_en.get(key, '???')
        has_html = '<' in fr_val
        marker = " [HTML]" if has_html else ""
        print(f"\n  --- {key}{marker} ---")
        print(f"  FR: {fr_val[:120]}{'...' if len(fr_val) > 120 else ''}")
        print(f"  EN: {en_val[:120]}{'...' if len(en_val) > 120 else ''}")

    print(f"\n{'=' * 60}")
    print("Done!")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
