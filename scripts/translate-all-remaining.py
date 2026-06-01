#!/usr/bin/env python3
"""
Translate all remaining French strings in en.json to English.
Uses BeautifulSoup to preserve HTML tags, and a comprehensive
phrase/word-level dictionary for translation.

Strategy:
1. Parse HTML with BeautifulSoup, isolate text nodes
2. For each text node, apply phrase-level replacements (longest first)
3. Apply careful word-level replacements with strict boundaries
4. Reassemble HTML
"""

import json
import re
import sys
import os
from bs4 import BeautifulSoup, NavigableString, Comment

# Path configuration
EN_JSON = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "data", "translations", "en.json")
UNTRANSLATED_FILE = os.path.expanduser(
    "~/.claude/projects/-Users-houedanou-Downloads/"
    "8dd8f53f-3de8-4b4e-acd8-6cdf7c2b422d/tool-results/bzpoxcnri.txt"
)

# ============================================================
# PHRASE DICTIONARY - ordered longest first automatically
# ============================================================

PHRASES = {
    # Multi-word governance phrases
    "conseils d'administration and de surveillance des sociétés": "boards of directors and supervisory boards of companies",
    "conseils d'administration and de surveillance": "boards of directors and supervisory boards",
    "Conseils d'Administration and de Surveillance": "Boards of Directors and Supervisory Boards",
    "Conseil d'Administration and de Surveillance": "Board of Directors and Supervisory Board",
    "Conseil d'Administration or de Surveillance": "Board of Directors or Supervisory Board",
    "Conseil d'Administration": "Board of Directors",
    "Conseils d'Administration": "Boards of Directors",
    "conseil d'administration": "board of directors",
    "conseils d'administration": "boards of directors",
    "Conseil d'administration": "Board of Directors",
    "Conseils d'administration": "Boards of Directors",
    "Conseil de Surveillance": "Supervisory Board",
    "Conseil de Perfectionnement": "Advisory Board",
    "conseil de surveillance": "supervisory board",
    "conseils de surveillance": "supervisory boards",

    # Titles and roles
    "administrateur indépendant": "independent director",
    "Administrateur indépendant": "Independent director",
    "Administrateur Indépendant": "Independent Director",
    "administratrice indépendante": "independent director",
    "Administratrice indépendante": "Independent director",
    "administrateurs indépendants": "independent directors",
    "administratrices indépendantes": "independent directors",
    "Administrateur(E) au féminin": "Women on Boards",
    "administrateur qualifié": "qualified director",
    "administrateurs qualifiés": "qualified directors",
    "administratrices qualifiées": "qualified directors",
    "Administrateur de Sociétés": "Company Director",
    "administrateur de sociétés": "company director",
    "Administrateur de société": "Company Director",
    "administrateur de société": "company director",
    "Administrateur de sociétés": "Company Director",
    "femmes administrateurs": "women directors",
    "femmes administratrices": "women directors",
    "Femmes administratrices": "Women directors",
    "administrateur \"croisé\"": "cross-director",
    "mandataire social": "corporate officer",
    "mandataires sociaux": "corporate officers",
    "Mandataire social": "Corporate officer",
    "Mandataires sociaux": "Corporate officers",
    "Président du Conseil de Surveillance": "Chairman of the Supervisory Board",
    "Président du Conseil": "Chairman of the Board",
    "Président directeur général": "Chairman and CEO",
    "Président Directeur Général": "Chairman and CEO",
    "Présidente du Directoire": "Chairwoman of the Executive Board",
    "Directeur Général Adjoint": "Deputy CEO",
    "Directeur général Adjoint": "Deputy CEO",
    "Directeur Général": "CEO",
    "Directeur général": "CEO",
    "Direction Générale": "Senior Management",
    "direction générale": "senior management",
    "Direction générale": "Senior Management",
    "Directrice Déléguée à la Direction Générale": "Deputy Managing Director",
    "Directeur de Business Unit": "Business Unit Director",
    "Directeur du marketing International": "International Marketing Director",
    "Directeur International": "International Director",
    "Directeur de filiale": "Subsidiary Director",
    "Directeur Gérant": "Managing Director",
    "Directeur Adjoint": "Deputy Director",
    "Directrice juridique": "Legal Director",
    "Directeur Juridique": "Legal Director",
    "Direction Financière": "Finance Department",
    "direction financière": "finance department",
    "Directeur Financier": "CFO",
    "Directrice Financière": "CFO",
    "directeur financier": "CFO",
    "Comité d'audit": "Audit Committee",
    "Comité d'Audit": "Audit Committee",
    "comité d'audit": "audit committee",
    "Comité Scientifique": "Scientific Committee",
    "Comités Carrières": "Career Committees",
    "Comités de Direction": "Executive Committees",
    "comités de direction": "executive committees",
    "Comité de Direction": "Executive Committee",
    "comité de direction": "executive committee",
    "Comité exécutif": "Executive Committee",
    "Comités Exécutifs": "Executive Committees",
    "comité stratégique": "strategic committee",
    "Comité de Rémunérations": "Compensation Committee",
    "Comité de Rémunération": "Compensation Committee",
    "Comité d'audit or de Rémunérations": "Audit or Compensation Committee",
    "Secrétaire Générale": "Secretary General",
    "Secrétaire Général": "Secretary General",
    "Secrétaire général": "Secretary General",
    "secrétariat général": "general secretariat",
    "Secrétaire du Conseil": "Board Secretary",
    "Associé gérant": "Managing Partner",
    "associé gérant": "managing partner",
    "Fondé de pouvoir": "Authorized representative",
    "consultante indépendante": "independent consultant",
    "Consultante indépendante": "Independent consultant",
    "consultant indépendant": "independent consultant",
    "Consultant indépendant": "Independent consultant",
    "conseil indépendant": "independent advisor",
    "Commissaire aux comptes": "Statutory Auditor",
    "Commissaires aux comptes": "Statutory Auditors",
    "Expert-comptable": "Chartered Accountant",
    "expert-comptable": "chartered accountant",
    "Expert comptable": "Chartered Accountant",
    "expertise-comptable": "accounting firm",
    "auditeur interne": "internal auditor",
    "ingénieur commercial": "business graduate",

    # Corporate terms
    "sociétés cotées": "listed companies",
    "Sociétés cotées": "Listed companies",
    "sociétés françaises cotées": "French listed companies",
    "société cotée": "listed company",
    "sociétés du CAC 40": "CAC 40 companies",
    "sociétés du CAC40": "CAC 40 companies",
    "sociétés non cotées": "unlisted companies",
    "entreprises cotées": "listed companies",
    "fusions/acquisitions": "mergers and acquisitions",
    "fusions – acquisitions": "mergers and acquisitions",
    "fusions and acquisitions": "mergers and acquisitions",
    "Fusions &amp; Acquisitions": "Mergers & Acquisitions",
    "fusion/acquisition": "merger and acquisition",
    "fusion acquisition": "merger and acquisition",
    "fusion-acquisition": "merger and acquisition",
    "opérations de haut de bilan": "balance sheet operations",
    "haut de bilan": "balance sheet",
    "croissance externe": "external growth",
    "croissance interne": "organic growth",
    "procédures collectives": "insolvency proceedings",
    "restructurations de participations": "restructuring of investments",
    "centre de service partagé": "shared service center",
    "centres de profit": "profit centers",
    "centre de profit": "profit center",
    "gestion des risques": "risk management",
    "gestion d'actifs": "asset management",
    "gestion patrimoniale": "wealth management",
    "gestion de participations": "portfolio management",
    "gestion privée": "private banking",
    "levées de fonds": "fundraising",
    "levée de fond": "fundraising",
    "levée de fonds": "fundraising",
    "introduction en bourse": "IPO",
    "introduction sur à la bourse": "listing on the stock exchange",
    "Assemblées Générales": "General Meetings",
    "assemblées générales": "general meetings",
    "Assemblée Nationale": "National Assembly",
    "assemblées parlementaires": "parliamentary assemblies",
    "retournements de situation": "turnarounds",
    "retournement de situation": "turnaround",
    "affaires en redressement": "distressed businesses",
    "conflits d'intérêts": "conflicts of interest",
    "conflit d'intérêts": "conflict of interest",
    "abus de position dominante": "abuse of dominant position",
    "droit pénal des affaires": "white-collar criminal law",
    "droit des affaires": "business law",
    "Barreau de Paris": "Paris Bar",
    "droits de douanes": "customs duties",
    "valeur ajoutée": "added value",
    "parties prenantes": "stakeholders",
    "plafond de verre": "glass ceiling",
    "bonnes pratiques": "best practices",
    "bonne pratique": "best practice",
    "gouvernance des entreprises": "corporate governance",
    "Gouvernance des entreprises": "Corporate governance",
    "entreprise familiale": "family business",
    "entreprises familiales": "family businesses",
    "familles entrepreneuriales": "entrepreneurial families",
    "création d'entreprise": "business creation",
    "créateur d'entreprise": "business founder",
    "créateurs d'entreprise": "business founders",
    "chiffres d'affaires": "revenues",
    "chiffre d'affaires": "revenue",
    "produits de grande consommation": "consumer products",
    "grande consommation": "consumer goods",
    "développement durable": "sustainable development",
    "Développement durable": "Sustainable development",
    "intelligence artificielle": "artificial intelligence",
    "transformation numérique": "digital transformation",
    "système d'information": "information system",
    "systèmes d'information": "information systems",
    "haute technologie": "high technology",
    "hautes technologies": "high technologies",
    "Haute Technologie": "High Technology",
    "Commerce International": "International Trade",
    "commerce international": "international trade",
    "commerce électronique": "e-commerce",
    "distribution pharmaceutique": "pharmaceutical distribution",
    "Génie Médical": "Medical Engineering",
    "génie civil": "civil engineering",
    "génie industriel": "industrial engineering",
    "matériaux composites": "composite materials",
    "peintures aéronautiques": "aerospace coatings",
    "emballage plastique": "plastic packaging",
    "transformation du bois": "wood processing",
    "biens d'équipement": "capital goods",
    "objets d'arts": "art objects",
    "édition &amp; multimedia": "publishing & multimedia",
    "restauration &amp; séminaires": "catering & seminars",
    "arômes and parfums": "flavours and fragrances",
    "matières premières": "commodities",
    "santé animale": "animal health",
    "Santé animale": "Animal health",
    "pharmacie humaine": "human pharmacy",
    "Pharmacie humaine": "Human pharmacy",
    "secteur tertiaire": "service sector",
    "Direction de R & D": "R&D Management",
    "Direction de R &amp; D": "R&D Management",

    # Gender / Feminisation
    "féminisation des conseils": "board gender diversity",
    "Féminiser son board": "Improving board gender diversity",
    "féminiser leur conseil d'administration": "improve gender diversity on their board",
    "féminiser l'encadrement": "improve gender diversity in management",
    "féminisé leurs conseils": "improved gender diversity on their boards",
    "Féminisation": "Feminisation",
    "féminisation": "feminisation",
    "féminiser": "feminise",
    "Forum de la Mixité": "Forum de la Mixité",
    "mixité": "gender diversity",
    "Mixité": "Gender diversity",
    "parité femmes/hommes": "gender parity",
    "parité hommes/femmes": "gender parity",
    "Observatoire de la Parité": "Gender Parity Observatory",
    "l'égalité hommes-femmes": "gender equality",
    "représentation équilibrée des femmes and des hommes": "balanced representation of women and men",
    "quotas de femmes": "quotas for women directors",
    "Quotas de femmes": "Quotas for women directors",

    # Law terms
    "la Loi du 27 janvier 2011": "the Law of 27 January 2011",
    "la Loi du 27 Janvier 2011": "the Law of 27 January 2011",
    "la loi sur la parité": "the gender parity law",
    "proposition de Loi": "bill",
    "proposition de loi": "bill",
    "rapports annuels": "annual reports",
    "rapport annuel": "annual report",
    "rapport d'activité": "activity report",
    "Rapport d'activité": "Activity report",
    "études de cas": "case studies",
    "Direction du Trésor": "Treasury Department",
    "Ministère de l'Industrie": "Ministry of Industry",
    "ministère de la défense": "Ministry of Defence",
    "Direction Générale de l'Armement": "Directorate General of Armaments",
    "Commission Européenne": "European Commission",
    "Banque Mondiale": "World Bank",
    "pensée de groupe": "groupthink",

    # Education / Qualification terms
    "Ecole des Mines": "Ecole des Mines",
    "Ecole Supérieure de Commerce": "Business School",
    "grandes écoles": "top universities",
    "Maîtrise de Sciences Economiques": "Master's in Economics",
    "Sciences Economiques": "Economics",
    "Sciences Eco": "Economics",
    "langues orientales": "Oriental Languages",
    "Enseignement Supérieur": "Higher Education",
    "certificat d'administrateur de société": "director certification",
    "certificat d'administrateur": "director certificate",
    "Administrateur Certifié": "Certified Director",
    "Administratrice Certifiée": "Certified Director",
    "certifiée administratrice": "certified as director",
    "Certifié comme Administrateur de Sociétés": "Certified as Company Director",
    "Certifié comme Administrateur": "Certified as Director",
    "double nationalité": "dual nationality",
    "Trilingue français/anglais/allemand": "Trilingual French/English/German",
    "bilingue français/anglais": "bilingual French/English",
    "bilingue français anglais": "bilingual French/English",
    "Anglais courant": "Fluent English",
    "anglais courant": "fluent English",
    "pratique plusieurs langues": "speaks several languages",
    "Connaissance de la langue russe": "Knowledge of Russian",

    # Navigation / Action phrases
    "en cliquant ici": "by clicking here",
    "cliquant ici": "clicking here",
    "cliquer ici": "click here",
    "vous pouvez le télécharger": "you can download it",
    "peut être déchargée en": "can be downloaded by",
    "peut être déchargé en": "can be downloaded by",
    "Pour tout renseignement": "For any information",
    "envoyer un courriel à": "send an email to",
    "il vous suffit d'envoyer un courriel avec vos coordonnées à": "simply send an email with your contact details to",
    "il vous suffit d'envoyer": "simply send",
    "les transparents de sa présentation": "the slides of his presentation",
    "dossier de presse": "press kit",
    "Relations presse": "Press relations",
    "disponible en ligne": "available online",
    "voir dépliant": "see leaflet",
    "Voir Courbes": "See Charts",
    "vos coordonnées": "your contact details",

    # Connectors and prepositions (phrase level)
    "au cours de la": "during the",
    "Au cours de la": "During the",
    "au cours de": "during",
    "Au cours de": "During",
    "Au cours des": "Over the",
    "au cours des": "over the",
    "au sein de": "within",
    "Au sein de": "Within",
    "au sein d'": "within ",
    "Au sein d'": "Within ",
    "au sein du": "within the",
    "au sein des": "within the",
    "au travers de": "through",
    "Au travers de": "Through",
    "au travers des": "through the",
    "à l'occasion de": "during",
    "A l'occasion de": "During",
    "en tant que": "as",
    "En tant que": "As",
    "en particulier": "in particular",
    "En particulier": "In particular",
    "en ce qui concerne": "regarding",
    "en conséquence": "consequently",
    "en profondeur": "in depth",
    "en parallèle": "in parallel",
    "En parallèle": "In parallel",
    "en avant première": "as a preview",
    "en avant-première": "as a preview",
    "en qualité de": "in the capacity of",
    "pour le compte de": "on behalf of",
    "entre autres": "among other things",
    "entres autres": "among other things",
    "c'est-à-dire": "that is to say",
    "par exemple": "for example",
    "d'une part": "on the one hand",
    "d'autre part": "on the other hand",
    "à la fois": "both",
    "grâce à": "thanks to",
    "Grâce à": "Thanks to",
    "afin de": "in order to",
    "ainsi que": "as well as",
    "tels que": "such as",
    "par analogie": "by analogy",
    "à travers": "through",
    "à ce titre": "in this capacity",
    "A ce titre": "In this capacity",
    "de fait": "in fact",
    "De fait": "In fact",
    "de plus": "moreover",
    "De plus": "Moreover",
    "par ailleurs": "furthermore",
    "Par ailleurs": "Furthermore",
    "d'où": "hence",
    "à terme": "ultimately",
    "à ce jour": "to date",
    "dès que": "as soon as",
    "dès aujourd'hui": "as of today",
    "dès réception": "upon receipt",
    "y compris": "including",
    "Y compris": "Including",
    "il a une riche expérience": "he has extensive experience",
    "depuis plus d'une année": "for over a year",
    "depuis plus de": "for over",
    "Depuis plus de": "For over",
    "depuis plusieurs années": "for several years",
    "En remontant dans le temps": "Looking back in time",
    "Après un début de carrière": "After starting his career",
    "après un début de carrière": "after starting a career",
    "Après avoir été": "After serving as",
    "après avoir été": "after serving as",
    "Après avoir occupé": "After holding",
    "après avoir occupé": "after holding",
    "Après avoir": "After having",
    "après avoir": "after having",
    "Forte de": "Building on",
    "Fort de": "Building on",
    "forte de": "building on",
    "fort de": "building on",
    "Doté d'une triple formation": "With a triple educational background",
    "Doté d'une": "Equipped with",
    "Dotée d'une": "Equipped with",
    "à son actif": "to her/his credit",
    "a à son actif": "has to her/his credit",
    "Il a été administrateur": "He has served as director",
    "il a été administrateur": "he has served as director",
    "elle a été administrateur": "she has served as director",
    "elle a été administratrice": "she has served as director",
    "Elle a été administratrice": "She has served as director",
    "Il a été": "He served as",
    "il a été": "he served as",
    "Elle a été": "She served as",
    "elle a été": "she served as",
    "Il est depuis": "He has been for",
    "elle a créé": "she created",
    "Elle a créé": "She created",
    "il a créé": "he created",
    "Il connait": "He is thoroughly familiar with",
    "il connait": "he is thoroughly familiar with",
    "il connaît": "he is thoroughly familiar with",
    "elle connaît": "she is thoroughly familiar with",
    "est un des rares": "is one of the few",
    "peut faire bénéficier": "can bring the benefit of",
    "faire bénéficier": "provide the benefit of",
    "faire profiter": "provide the benefit of",
    "se ferait un plaisir": "would be happy",
    "construire des ponts": "build bridges",
    "met au service": "puts at the service",
    "mis au service": "put at the service",
    "large expérience": "extensive experience",
    "longue expérience": "long experience",
    "vaste expérience": "vast experience",
    "riche expérience": "rich experience",
    "grande expérience": "extensive experience",
    "longue and large expérience": "long and extensive experience",
    "Large expérience": "Extensive experience",
    "Longue expérience": "Long experience",
    "Longue and large expérience": "Long and extensive experience",
    "Grande expérience": "Extensive experience",
    "l'une des causes": "one of the causes",
    "de très hautes responsabilités": "very senior positions",
    "hautes responsabilités": "senior positions",
    "haute responsabilité": "senior position",
    "postes de direction de haut niveau": "senior management positions",
    "postes de direction": "management positions",
    "postes de responsabilité": "positions of responsibility",
    "postes de très hautes responsabilités opérationnelles": "very senior operational positions",
    "postes de hautes responsabilités": "senior positions",
    "poste d'administrateur indépendant": "independent director position",
    "poste d'administratrice indépendante": "independent director position",
    "poste d'administrateur": "director position",
    "poste d'administratrice": "director position",
    "postes d'administrateurs": "director positions",
    "postes d'administrateur": "director positions",
    "Candidat à un poste d'administrateur indépendant": "Candidate for an independent director position",
    "candidat à un poste d'administrateur indépendant": "candidate for an independent director position",
    "Candidate à un poste d'administratrice indépendante": "Candidate for an independent director position",
    "candidate à un poste d'administratrice indépendante": "candidate for an independent director position",
    "La candidate à un poste d'administratrice indépendante": "The candidate for an independent director position",
    "la candidate à un poste d'administratrice indépendante": "the candidate for an independent director position",
    "Le candidat à un poste d'administrateur indépendant": "The candidate for an independent director position",
    "Le candidat à des postes d'administrateur": "The candidate for director positions",
    "La candidate à un poste d'administratrice": "The candidate for a director position",
    "Le candidat à un poste d'administrateur": "The candidate for a director position",
    "Candidate à un poste d'administratrice indépendante": "Candidate for an independent director position",
    "Candidat à un poste d'administrateur indépendant,": "Candidate for an independent director position,",
    "la candidate": "the candidate",
    "La candidate": "The candidate",
    "le candidat": "the candidate",
    "Le candidat": "The candidate",
    "Le candidat,": "The candidate,",
    "La candidate,": "The candidate,",
    "les candidats": "the candidates",

    # Specific page content phrases
    "sociétés Luxembourgeoises": "Luxembourg companies",
    "structures financières sous régulation Luxembourg": "financial structures under Luxembourg regulation",
    "carrière industrielle": "industrial career",
    "équipes internationales": "international teams",
    "équipes multiculturelles": "multicultural teams",
    "équipes multi-culturelles": "multicultural teams",
    "recherche and développement": "research and development",
    "diagnostics médicaux": "medical diagnostics",
    "médicaments anti-viraux": "antiviral drugs",
    "électronique de défense": "defence electronics",
    "domiciliation de sociétés": "company domiciliation",

    # Specific section headers found in the data
    "Hommes Candidats": "Male Candidates",
    "Notes and articles publiés par G&amp; S": "Notes and articles published by G&S",
    "Blogs liés à la gouvernance": "Blogs related to governance",
    "Relations presse de Gouvernance &amp; Structures": "Gouvernance & Structures press relations",
    "Notes and articles publiés par": "Notes and articles published by",

    # Months / dates
    "décembre": "December",
    "Décembre": "December",
    "novembre": "November",
    "Novembre": "November",
    "octobre": "October",
    "Octobre": "October",
    "septembre": "September",
    "Septembre": "September",
    "janvier": "January",
    "Janvier": "January",
    "février": "February",
    "Février": "February",
    "mars": "March",
    "Mars": "March",
    "avril": "April",
    "Avril": "April",
    "mai": "May",
    "Mai": "May",
    "juin": "June",
    "Juin": "June",
    "juillet": "July",
    "Juillet": "July",
    "août": "August",

    # ============================================================
    # FRENCH GRAMMAR PATTERN PHRASES
    # These handle the most common French constructions
    # ============================================================

    # Common verb constructions
    "a exercé": "has held",
    "a occupé": "has held",
    "a été": "has been",
    "a acquis": "has acquired",
    "a mené": "has led",
    "a dirigé": "has led",
    "a développé": "has developed",
    "a créé": "has created",
    "a fondé": "has founded",
    "a participé": "has participated",
    "a contribué": "has contributed",
    "a travaillé": "has worked",
    "a rejoint": "has joined",
    "a réalisé": "has carried out",
    "a assuré": "has managed",
    "a effectué": "has carried out",
    "a commencé": "has started",
    "a débuté": "has started",
    "a obtenu": "has obtained",
    "a vécu": "has experienced",
    "a suivi": "has followed",
    "a présenté": "has presented",
    "a siégé": "has served on",
    "a piloté": "has managed",
    "a passé": "has spent",
    "a levé": "has raised",
    "a tenu": "has held",
    "a mis en place": "has implemented",
    "a cité": "has cited",
    "a connu": "has known",
    "a permis": "has enabled",
    "a investi": "has invested",
    "a pu": "was able to",
    "ont pu": "were able to",
    "a intégré": "has joined",
    "a initié": "has initiated",

    "elle a exercé": "she has held",
    "elle a occupé": "she has held",
    "elle a acquis": "she has acquired",
    "elle a mené": "she has led",
    "elle a dirigé": "she has led",
    "elle a développé": "she has developed",
    "elle a participé": "she has participated",
    "elle a contribué": "she has contributed",
    "elle a travaillé": "she has worked",
    "elle a rejoint": "she has joined",
    "elle a réalisé": "she has carried out",
    "elle a assuré": "she has managed",
    "elle a effectué": "she has carried out",
    "elle a commencé": "she has started",
    "elle a débuté": "she has started",
    "elle a obtenu": "she has obtained",
    "elle a vécu": "she has experienced",
    "elle a piloté": "she has managed",
    "elle a passé": "she has spent",
    "elle a investi": "she has invested",
    "elle a intégré": "she has joined",

    "il a exercé": "he has held",
    "il a occupé": "he has held",
    "il a acquis": "he has acquired",
    "il a mené": "he has led",
    "il a dirigé": "he has led",
    "il a développé": "he has developed",
    "il a participé": "he has participated",
    "il a contribué": "he has contributed",
    "il a travaillé": "he has worked",
    "il a rejoint": "he has joined",
    "il a réalisé": "he has carried out",
    "il a assuré": "he has managed",
    "il a effectué": "he has carried out",
    "il a commencé": "he has started",
    "il a débuté": "he has started",
    "il a obtenu": "he has obtained",
    "il a vécu": "he has experienced",
    "il a piloté": "he has managed",
    "il a passé": "he has spent",
    "il a investi": "he has invested",
    "il a intégré": "he has joined",

    "elle a une": "she has",
    "il a une": "he has",
    "elle a un": "she has a",
    "il a un": "he has a",
    "elle est": "she is",
    "il est": "he is",
    "Elle a une": "She has",
    "Il a une": "He has",
    "Elle a un": "She has a",
    "Il a un": "He has a",
    "Elle est": "She is",
    "Il est": "He is",

    # Relative clauses and connectors
    "qui a été": "who has been",
    "qui a exercé": "who has held",
    "qui ont été": "who have been",
    "qui ont": "who have",
    "qui a": "who has",
    "qui est": "who is",
    "qui peut": "who can",
    "qui peuvent": "who can",
    "qui touche": "which affects",
    "qui se": "who",
    "qui ne": "who does not",
    "qui veulent": "who want",
    "qui veut": "who wants",
    "qui les pratiquent": "who practise them",
    "que le": "that the",
    "que la": "that the",
    "que les": "that the",
    "qu'il": "that he",
    "qu'elle": "that she",
    "qu'ils": "that they",
    "qu'elles": "that they",
    "que je suis": "that I am",
    "que nous": "that we",
    "que vous": "that you",

    "dont il": "of which he",
    "dont elle": "of which she",
    "dont les": "whose",
    "dont la": "whose",
    "dont le": "whose",
    "dont une": "of which one",

    "où il": "where he",
    "où elle": "where she",
    "où ont": "where",
    "où un": "where a",
    "où une": "where a",

    # Preposition + article combinations
    "de la": "of the",
    "de l'": "of the ",
    "de le": "of the",
    "de les": "of the",
    "de son": "of his",
    "de sa": "of her",
    "de ses": "of his/her",
    "de leur": "of their",
    "de leurs": "of their",
    "de cette": "of this",
    "de ces": "of these",
    "de ce": "of this",
    "de deux": "of two",
    "de trois": "of three",
    "de quatre": "of four",
    "de cinq": "of five",
    "de six": "of six",
    "de dix": "of ten",
    "de très": "of very",
    "de plus de": "of more than",
    "de quelques": "of some",
    "de plusieurs": "of several",
    "de nombreux": "of numerous",
    "de nombreuses": "of numerous",
    "de grands": "of large",
    "de grandes": "of large",
    "de nouveaux": "of new",
    "de nouvelles": "of new",
    "de différents": "of different",
    "de différentes": "of different",
    "de divers": "of various",
    "de diverses": "of various",

    "du monde": "in the world",
    "dans le monde": "worldwide",
    "dans le domaine": "in the field",
    "dans les domaines": "in the fields",
    "dans le secteur": "in the sector",
    "dans les secteurs": "in the sectors",
    "dans le cadre": "within the framework",
    "dans le contexte": "in the context",
    "dans un contexte": "in a context",
    "dans des environnements": "in environments",
    "dans un environnement": "in an environment",
    "dans la vie": "in life",
    "dans une société": "in a company",
    "dans des sociétés": "in companies",
    "dans plusieurs": "in several",
    "dans un cabinet": "in a firm",
    "dans des cabinets": "in firms",
    "dans un grand": "in a large",
    "dans une grande": "in a large",

    "à des postes": "in positions",
    "à un poste": "in a position",
    "à Paris": "in Paris",
    "à Londres": "in London",
    "à Madrid": "in Madrid",
    "à Bruxelles": "in Brussels",
    "à Oxford": "in Oxford",
    "à Washington": "in Washington",
    "à Berlin": "in Berlin",
    "à New York": "in New York",
    "à l'étranger": "abroad",
    "à l'international": "internationally",
    "à divers postes": "in various positions",

    "en France": "in France",
    "en Espagne": "in Spain",
    "en Allemagne": "in Germany",
    "en Angleterre": "in England",
    "en Belgique": "in Belgium",
    "en Italie": "in Italy",
    "en Chine": "in China",
    "en Europe": "in Europe",
    "en Asie": "in Asia",
    "en Inde": "in India",
    "en Russie": "in Russia",

    "aux USA": "in the USA",
    "aux Etats-Unis": "in the United States",
    "aux États-Unis": "in the United States",
    "aux Pays-Bas": "in the Netherlands",

    "sur le thème": "on the topic",
    "sur le thème de": "on the topic of",
    "sur les": "on the",
    "sur la": "on the",
    "sur le": "on the",
    "sur un": "on a",
    "sur une": "on a",
    "sur des": "on",
    "sur Euronext": "on Euronext",

    "par le": "by the",
    "par la": "by the",
    "par les": "by the",
    "par un": "by a",
    "par une": "by a",
    "par des": "by",

    "avec les": "with the",
    "avec la": "with the",
    "avec le": "with the",
    "avec un": "with a",
    "avec une": "with a",
    "avec des": "with",
    "avec ses": "with his/her",
    "avec son": "with his/her",
    "avec sa": "with his/her",

    "pour les": "for the",
    "pour la": "for the",
    "pour le": "for the",
    "pour un": "for a",
    "pour une": "for a",
    "pour des": "for",
    "pour y": "to",

    "sous le": "under the",
    "sous la": "under the",
    "sous les": "under the",

    "chez les": "with",
    "chez un": "at a",

    "vers les": "towards",
    "vers le": "towards the",
    "vers la": "towards the",

    "entre les": "between the",
    "entre la": "between the",
    "entre le": "between the",
    "entre des": "between",

    "depuis lors": "since then",
    "depuis le": "since the",
    "depuis la": "since the",
    "depuis les": "since the",

    "pendant le": "during the",
    "pendant la": "during the",
    "pendant les": "during the",
    "pendant plus de": "for more than",
    "pendant 4 ans": "for 4 years",
    "pendant 5 ans": "for 5 years",
    "pendant 6 ans": "for 6 years",
    "pendant 7 ans": "for 7 years",
    "pendant 10 ans": "for 10 years",
    "pendant 15 ans": "for 15 years",
    "pendant 20 ans": "for 20 years",
    "pendant 25 ans": "for 25 years",
    "pendant 30 ans": "for 30 years",

    "lors de": "during",

    # Duration / quantity patterns
    "plus de 10 ans": "over 10 years",
    "plus de 15 ans": "over 15 years",
    "plus de 20 ans": "over 20 years",
    "plus de 25 ans": "over 25 years",
    "plus de 30 ans": "over 30 years",
    "une vingtaine d'années": "about twenty years",
    "une trentaine de pays": "about thirty countries",
    "cinq dernières années": "last five years",
    "douze ans": "twelve years",

    # Common sentence fragments in CV texts
    "complétée par": "complemented by",
    "completée par": "complemented by",
    "s'appuyant sur": "drawing on",
    "s'appuyant sur sa longue": "drawing on his long",
    "se terminera": "will end",
    "se propose": "proposes",
    "se lisant facilement": "easy to read",
    "se déroulant": "taking place",
    "se situe": "is located",
    "se fait connaître": "become known",
    "se ferait": "would",
    "se sont procuré": "obtained",
    "se satisfont": "are satisfied",
    "se désaltérer": "quench one's thirst",
    "se substituer à": "substitute for",
    "se détournent": "turn away from",
    "se traduire par": "result in",
    "se trouve": "is",
    "se trouvent": "are",

    "il en déduit": "he derives from them",
    "et en déduit": "and derives from them",
    "il fait des commentaires": "he comments",
    "fait des commentaires": "provides comments",

    "tant en France qu'à l'étranger": "both in France and abroad",
    "tant en France qu'au Luxembourg": "both in France and in Luxembourg",
    "tant comme": "both as",
    "tant au Japon qu'en Chine": "both in Japan and in China",
    "tant au Japon": "both in Japan",
    "tant en période de croissance qu'en période de crise": "both during growth and during crisis",
    "tant en France": "both in France",

    "en mécanique and métallurgie": "in mechanics and metallurgy",
    "du domaine ci-dessus": "in the above-mentioned field",
    "ci-dessus mentionnés": "mentioned above",
    "ci-dessus": "above-mentioned",
    "ci-dessous": "below",

    "Il a commenté": "He commented on",
    "il a commenté": "he commented on",
    "Il a évoqué": "He mentioned",
    "il a évoqué": "he mentioned",
    "Il a résumé": "He summarised",
    "il a résumé": "he summarised",
    "Il a présenté": "He presented",
    "il a présenté": "he presented",
    "Il a conseillé": "He advised",
    "il a conseillé": "he advised",
    "elle a présenté": "she presented",

    "a été l'animateur": "was the moderator",
    "a été l'un des intervenants": "was one of the speakers",
    "est intervenu": "spoke",
    "sont ensuite successivement intervenus": "then spoke in succession",
    "sont intervenus": "spoke",
    "est intervenue": "spoke",

    "vient de récemment créer": "has recently created",
    "vient de créer": "has just created",

    # Common noun phrases
    "les sociétés du CAC40": "the CAC 40 companies",
    "les sociétés du CAC 40": "the CAC 40 companies",
    "les résultats principaux": "the main results",
    "les premières estimations": "the initial estimates",
    "les moyens disponibles": "the available means",
    "les exigences de la loi": "the requirements of the law",
    "les dangers de la": "the dangers of",
    "les raisons": "the reasons",
    "les bienfaits": "the benefits",
    "les profils des": "the profiles of",
    "les évolutions": "the developments",
    "les informations": "the information",
    "les avancées": "the advances",
    "les poids lourds": "the heavyweights",
    "la situation": "the situation",
    "la composition": "the composition",
    "la présence": "the presence",
    "la fonction": "the role",
    "la connaissance": "the knowledge",
    "le recrutement": "the recruitment",
    "le thème": "the topic",
    "le dialogue": "the dialogue",
    "le ratio moyen": "the average ratio",
    "le contrôle": "control",
    "le renouveau": "renewal",
    "le côté": "the side",
    "le coté": "the side",
    "une expérience": "experience",
    "une société": "a company",
    "un cabinet": "a firm",
    "un des leaders": "one of the leaders",
    "l'une des": "one of the",
    "l'un des": "one of the",
    "un des rares": "one of the few",

    # Person descriptions (common in CV texts)
    "de formation": "by training",
    "Formation:": "Education:",
    "Formation :": "Education:",
    "Diplômé": "Graduate",
    "diplômé": "graduate",
    "Diplômée": "Graduate",
    "diplômée": "graduate",
    "Titulaire du": "Holder of the",
    "titulaire du": "holder of the",
    "Titulaire de": "Holder of",
    "Créateur d'une": "Founder of a",
    "créateur d'une": "founder of a",
    "Créatrice d'une": "Founder of a",
    "créatrice de son propre": "founder of her own",
    "créatrice de son": "founder of her",
    "créatrice d'une": "founder of a",
    "co-fondateur d'une": "co-founder of a",
    "Co-fondateur d'une": "Co-founder of a",
    "co-fondatrice d'une": "co-founder of a",
    "issu d'une": "from a",
    "issus d'une": "from a",
    "issue d'une": "from a",

    "il fonde": "he founded",
    "Il fonde": "He founded",
    "elle fonde": "she founded",
    "il sera le": "he was the",
    "Il en sera le": "He was the",
    "pilotera un développement réussi": "led a successful development",

    "réside en": "resides in",
    "domicilié": "based",
    "domiciliée": "based",
    "implanté depuis longtemps": "long established",
    "implantée depuis longtemps": "long established",

    # Common complete micro-phrases
    "et en maîtrise les langues associées": "and has mastered the associated languages",
    "en maîtrise les langues": "has mastered the languages",
    "son expérience": "his/her experience",
    "Son expérience": "His/her experience",
    "son parcours": "his/her career path",
    "Son parcours": "His/her career path",
    "sa carrière": "his/her career",
    "son profil": "his/her profile",
    "sa compétence": "his/her expertise",
    "son livre": "his book",
    "son actif": "his/her credit",
    "son relationnel": "his/her network",
    "sa résidence": "his/her residence",
    "sa propre": "his/her own",
    "ses différentes fonctions": "his/her various functions",
    "ses nombreuses missions": "his/her numerous assignments",
    "ses clients": "his/her clients",
    "sa vision": "his/her vision",
    "ses responsabilités": "his/her responsibilities",
    "sa force de frappe marketing": "their marketing power",
    "sa longue expérience": "his long experience",

    "cette dernière": "the latter",
    "ce dernier": "the latter",
    "cette expérience": "this experience",
    "cette large expérience": "this broad experience",
    "ces secteurs": "these sectors",
    "ces domaines": "these fields",
    "ces nouveaux": "these new",
    "ce domaine": "this field",
    "ce guide": "this guide",

    "un phénomène": "a phenomenon",
    "un prototype": "a prototype",
    "un extrait": "an extract",
    "Un extrait": "An extract",
    "un tour d'horizon": "an overview",
    "Un tour d'horizon": "An overview",
    "un dossier": "a dossier",
    "un mandat": "a mandate",
    "un poste": "a position",
    "un réseau": "a network",
    "un grand groupe": "a major group",
    "un grand cabinet": "a major firm",
    "un important": "a significant",
    "un des premiers": "one of the first",
    "une sélection historique": "a historical selection",
    "une conférence inédite": "an original conference",
    "une conférence était organisée": "a conference was organised",
    "une matinale": "a morning meeting",
    "une large expérience": "broad experience",
    "une longue expérience": "long experience",
    "une riche expérience": "rich experience",
    "une véritable expertise": "genuine expertise",
    "une grande adaptabilité": "great adaptability",
    "une expérience approfondie": "in-depth experience",
    "une échange": "a discussion",
    "une opération": "an operation",
    "une start-up": "a start-up",
    "une filiale": "a subsidiary",
    "une des plus grandes": "one of the largest",
    "un des leaders mondiaux": "one of the world leaders",
    "un des leaders": "one of the leaders",

    "des postes de direction": "management positions",
    "des postes de responsabilité": "positions of responsibility",
    "des opérations de": "operations of",
    "des filiales de": "subsidiaries of",
    "des sociétés de": "companies in",
    "des entreprises de": "companies in",
    "des missions de": "assignments in",
    "des projets de": "projects in",
    "des secteurs d'activité": "business sectors",
    "des structures de tailles": "structures of various sizes",
    "des environnements internationaux": "international environments",
    "des environnements multi-culturels": "multicultural environments",

    "la candidate est": "the candidate is",
    "le candidat est": "the candidate is",
    "la candidate a": "the candidate has",
    "le candidat a": "the candidate has",
    "la candidate de formation": "the candidate, trained as",
    "le candidat de formation": "the candidate, trained as",

    # Very common verb forms in these texts
    "elle peut": "she can",
    "il peut": "he can",
    "elle pourrait": "she could",
    "il pourrait": "he could",
    "elle sait": "she knows",
    "il sait": "he knows",
    "elle connaît": "she knows",
    "elle connait": "she knows",
    "elle dispose": "she has",
    "il dispose": "he has",
    "elle possède": "she holds",
    "il possède": "he holds",
    "elle apporte": "she brings",
    "il apporte": "he brings",
    "elle envisage": "she plans",
    "il envisage": "he plans",
    "elle donne": "she gives",
    "il donne": "he gives",
    "elle partage": "she shares",
    "il partage": "he shares",
    "elle vit": "she lives",
    "il vit": "he lives",
    "elle parle": "she speaks",
    "il parle": "he speaks",
    "elle crée": "she creates",
    "il crée": "he creates",
    "elle assure": "she provides",
    "il assure": "he provides",
    "elle siège": "she sits",
    "il siège": "he sits",
    "elle intervient": "she works",
    "il intervient": "he works",
    "elle dirige": "she leads",
    "il dirige": "he leads",
    "elle mène": "she leads",
    "il mène": "he leads",

    # More structural patterns
    "il fut": "he was",
    "Il fut": "He was",
    "elle fut": "she was",
    "Elle fut": "She was",
    "il fût": "he was",
    "il y a": "there is",
    "il y voit": "he sees therein",
    "G &amp; S y voit": "G & S sees therein",
    "il en a mené": "he led",
    "elle en a mené": "she led",
    "il aussi travaillé": "he also worked",
    "il a aussi travaillé": "he has also worked",
    "elle a aussi travaillé": "she has also worked",

    # Infinitive constructions
    "afin de pouvoir": "in order to",
    "afin pouvoir de": "in order to",
    "afin de les connaître": "in order to know them",
    "afin après étude de pouvoir": "in order, after review, to",
    "pour y réaliser": "to carry out",
    "pour y assurer": "to provide",
    "pour aujourd'hui accompagner": "to support today",
    "pouvoir éventuellement": "potentially",
    "pouvoir de faire bénéficier": "share the benefit of",
    "pouvant être proposé (e)s": "who may be proposed",
    "pouvant être proposé": "who may be proposed",
    "susceptibles d'intéresser": "likely to interest",

    "dans une logique durable and équitable": "in a sustainable and equitable way",
    "comme fondement du succès": "as the foundation of success",
    "plus largement de notre société": "and more broadly, of our society",
    "parce qu'elle croit en": "because she believes in",
    "elle croit en": "she believes in",

    # Miscellaneous remaining patterns
    "d'un point de vue": "from the perspective of",
    "suivant le prisme de": "through the lens of",
    "y compris sur la compliance": "including compliance",
    "in extenso avec intérêt": "in extenso with interest",
    "j'y ai beaucoup appris": "I learned a great deal",
    "j'ai été sollicité pour relire": "I was asked to review",
    "le présent ouvrage": "this book",
    "les grands concepteurs/fournisseurs": "the major designers/providers",
    "d'IA dite « générative »": "of so-called 'generative' AI",
    "pour le grand public": "to the general public",
    "a été rendu disponible": "has been made available",
    "Beaucoup de personnes": "Many people",
    "pas nécessairement qualifiées": "not necessarily qualified",
    "ont vu une opportunité": "saw an opportunity",
    "de se faire connaître": "to make themselves known",
    "en prenant la parole": "by speaking out",
    "dans les médias": "in the media",
    "en publiant articles or livres": "by publishing articles or books",
    "Pour le béotien curieux que je suis": "For the curious layperson that I am",
    "c'est un peu comme se désaltérer à une bouche d'incendie": "it is somewhat like drinking from a fire hydrant",
    "la difficulté intrinsèque de vraiment comprendre « comment ça marche »": "the intrinsic difficulty of truly understanding 'how it works'",
    "à quoi cela peut servir en bien": "what it can be used for",
    "les risques de fausses routes à cause des biais sont des freins bien réels": "the risks of wrong turns due to biases are very real obstacles",
    "Quelques recherches ponctuelles pour trouver une réponse à mes questions ont été loin de m'éclairer": "A few ad hoc searches to find answers to my questions were far from enlightening",
    "la variété des systèmes d'IA": "the variety of AI systems",
    "la rapidité d'arrivée de nouveaux outils": "the speed at which new tools arrive",

    "Or la variété": "However, the variety",
    "Or, la variété": "However, the variety",

    "lorsque, as member du": "when, as a member of the",
    "lorsque, en tant que membre du": "when, as a member of the",

    # Legal page terms
    "conformément à": "in accordance with",
    "Conformément à": "In accordance with",
    "en vertu de": "pursuant to",
    "en application de": "pursuant to",
    "sous réserve de": "subject to",
    "en vigueur": "in force",
    "ladite": "said",
    "ledit": "said",
    "susvisé": "above-mentioned",
    "susvisée": "above-mentioned",

    # Shadow board page
    "entreprise libérée": "liberated company",
    "Entreprise libérée": "Liberated company",
    "instance dirigeante": "governing body",
    "instances dirigeantes": "governing bodies",
    "Instances dirigeantes": "Governing bodies",

    # Questionnaire / Survey terms
    "questionnaire": "questionnaire",
    "formulaire de candidature": "application form",
    "en remplissant": "by filling out",
    "les informations demandées": "the information requested",
    "les informations communiquées": "the information provided",
    "adéquation entre": "match between",
    "adéquation avec": "match with",
    "détecté": "detected",
    "détectée": "detected",
    "reviendra vers vous": "will get back to you",

    # Page specific phrases
    "explicite pourquoi": "explains why",
    "peut agir comme un vaccin": "can act as a vaccine",
    "en permettant d'éviter les crises": "by helping to avoid crises",
    "pour l'entreprise or de les atténuer": "for the company or mitigating them",
    "L'article du Cercle des Echos": "The article in Le Cercle des Echos",

    "Cet après-midi se situe à la fin des cours": "This afternoon session takes place at the end of the courses",
    "se déroulant actuellement du Certificat de": "currently being held as part of the Certificate from",
    "pour les membres en place or potentiels de Comex and Codir": "for current or potential members of the Executive Committee (Comex and Codir)",
    "les participants amélioreront leur connaissance des relations attendues entre les Comex/ouCodir and les": "the participants will improve their understanding of the expected relationships between the Comex/Codir and the",
    "paléoanthropologue de renom": "renowned paleoanthropologist",
    "une conférence inédite sur l'anthropologie and l'évolution des entreprises": "an original conference on anthropology and the evolution of companies",
    "accompagné de": "accompanied by",

    "avec Guy Le Péchon accompagné de Catherine Montagnon": "with Guy Le Péchon accompanied by Catherine Montagnon",
    "polytechnicienne, and son livre": "a graduate of Ecole Polytechnique, and his book",
    "à sortir très prochainement": "to be published very soon",

    "à l'origine de l'évènement proposé aux": "at the origin of the event proposed to the",
    "associations d'anciens de grandes écoles": "alumni associations of top universities",
    "poursuit la dynamique de la loi": "continues the momentum of the law",
    "Après avoir contribué à la conception de la soirée en présentiel du": "After contributing to the design of the in-person event of",
    "en présence de Madame la Députée": "in the presence of Member of Parliament",
    "nous avons le plaisir de partager l'invitation officielle": "we are pleased to share the official invitation",

    "Analyse des évolutions réglementaires and de leur impact sur la gouvernance des entreprises": "Analysis of regulatory developments and their impact on corporate governance",
    "and suggéré surtout penser à convaincre les Présidents d'élargir de façon professionnelle les cooptations des membres de leurs Conseils": "and primarily suggested thinking about convincing the Chairmen to professionally broaden the co-option of members of their Boards",
    "Il a évoqué les profils des directors": "He mentioned the profiles of directors",

    # Page mentions legales
    "Mentions légales": "Legal Notice",
    "conditions générales": "general terms",
    "Conditions générales": "General Terms",
    "politique de confidentialité": "privacy policy",
    "Politique de confidentialité": "Privacy Policy",
    "données personnelles": "personal data",
    "Données personnelles": "Personal Data",
    "propriété intellectuelle": "intellectual property",
    "responsabilité": "liability",
    "droit applicable": "applicable law",
    "hébergement": "hosting",
    "éditeur": "publisher",

    # Plan du site
    "plan du site": "sitemap",
    "Plan du site": "Sitemap",

    # More structural patterns for remaining CV text
    "elle y a": "she has therein",
    "il y a": "he has therein",
    "elle y demeurera": "she remained there",
    "il y demeurera": "he remained there",
    "elle fut la première femme": "she was the first woman",
    "elle fut la première": "she was the first",
    "il fut le premier": "he was the first",
    "chargée du lancement": "in charge of launching",
    "chargé du lancement": "in charge of launching",
    "en charge d'": "in charge of ",
    "en charge de": "in charge of",
    "chargée de": "in charge of",
    "chargé de": "in charge of",
    "responsable de": "responsible for",
    "Responsable de": "Responsible for",
    "responsable du": "responsible for the",
    "responsable des": "responsible for the",
    "responsable pour": "responsible for",

    "Elle en est": "She is",
    "Il en est": "He is",
    "elle en est": "she is",
    "il en est": "he is",

    "Il a une riche": "He has extensive",
    "il a une riche": "he has extensive",
    "Elle a une riche": "She has extensive",
    "elle a une riche": "she has extensive",

    "connaissance de l'international": "knowledge of international business",
    "Très bonne connaissance de l'international": "Very good knowledge of international business",
    "très bonne connaissance de": "very good knowledge of",
    "Très bonne connaissance de": "Very good knowledge of",
    "bonne connaissance de": "good knowledge of",
    "Bonne connaissance de": "Good knowledge of",
    "Connaissance de": "Knowledge of",
    "connaissance de": "knowledge of",
    "connaissant bien": "with good knowledge of",

    "elle pourra faire bénéficier le Conseil de": "she can bring to the Board her",
    "pourra faire bénéficier": "can bring the benefit of",
    "faire bénéficier de son expérience": "share his/her experience with",
    "faire bénéficier à d'autres de son expérience": "share his/her experience with others",
    "de faire bénéficier": "to share",
    "bénéficier de son": "benefit from his/her",
    "pourrait bénéficier de son expérience": "could benefit from his/her experience",

    "les accompagne": "supports them",
    "le conseille": "advises",
    "la conseille": "advises",
    "les conseille": "advises them",

    "Mentor au sein de": "Mentor at",
    "Langues :": "Languages:",
    "Langues:": "Languages:",
    "Langues courantes:": "Fluent languages:",
    "Langues courantes :": "Fluent languages:",
    "Ref:": "Ref:",
    "Ref :": "Ref:",
}


# Add regex-based translations for patterns that need flexibility
REGEX_PATTERNS = [
    # "N ans de/d'" -> "N years of"
    (r'(\d+)\s+ans?\s+de\b', r'\1 years of'),
    (r'(\d+)\s+ans?\s+d\'', r"\1 years of "),
    (r'(\d+)\s+ans?\b', r'\1 years'),
    (r'(\d+)\s+année?s?\b', r'\1 years'),
    (r'(\d+)\s+mois\b', r'\1 months'),

    # "du N month year" -> "of N month year"
    (r'\bdu\s+(\d)', r'of \1'),

    # "Le N month" -> "On N month" (dates)
    (r'\bLe\s+(\d+)\s+(January|February|March|April|May|June|July|August|September|October|November|December)', r'On \1 \2'),

    # Remove trailing "de" before proper nouns
    # "Il est membre de l'IFA" -> handled by phrases

    # "N° NNN" -> "No. NNN"
    (r'N°\s*', 'No. '),

    # "d'une/d'un" at word boundaries
    (r"\bd'une\b", "of a"),
    (r"\bd'un\b", "of a"),

    # Common "la/le/les + noun" patterns that are safe
    (r'\bles\s+premières\b', 'the first'),
    (r'\bles\s+principales\b', 'the main'),
    (r'\bles\s+premiers\b', 'the first'),
    (r'\bles\s+dernières\b', 'the last'),
    (r'\bles\s+derniers\b', 'the last'),
    (r'\bles\s+différents\b', 'the different'),
    (r'\bles\s+différentes\b', 'the different'),
    (r'\bles\s+grands\b', 'the major'),
    (r'\bles\s+grandes\b', 'the major'),
    (r'\bles\s+nouveaux\b', 'the new'),
    (r'\bles\s+nouvelles\b', 'the new'),
    (r'\bles\s+nombreux\b', 'the numerous'),
    (r'\bles\s+nombreuses\b', 'the numerous'),

    # "très + adj" patterns
    (r'\btrès\s+variés\b', 'very varied'),
    (r'\btrès\s+variée\b', 'very varied'),
    (r'\btrès\s+étendue\b', 'very extensive'),
    (r'\btrès\s+étendu\b', 'very extensive'),
    (r'\btrès\s+poussée\b', 'very advanced'),
    (r'\btrès\s+enrichissantes\b', 'very enriching'),
    (r'\btrès\s+majoritairement\b', 'overwhelmingly'),
    (r'\btrès\s+humoristique\b', 'very humorous'),
    (r'\btrès\s+opérationnelle\b', 'very hands-on'),
    (r'\btrès\s+nombreuses\b', 'very numerous'),
    (r'\btrès\s+bonne\b', 'very good'),
    (r'\btrès\s+prochainement\b', 'very soon'),

    # "de type/de taille" patterns
    (r'\bde\s+type\s+très\s+variés\b', 'of highly varied types'),
    (r'\bde\s+type\b', 'of type'),
    (r'\bde\s+taille\s+intermédiaire\b', 'of medium size'),
    (r'\bde\s+taille\b', 'of size'),
    (r'\bde\s+grande\s+taille\b', 'large-scale'),
    (r'\bde\s+grande\s+envergure\b', 'large-scale'),

    # "est un/une" patterns
    (r'\best un\s+dirigeant\b', 'is an experienced executive'),
    (r'\best une?\s+', 'is a '),

    # Handle remaining French articles in context (very careful)
    (r"\bl'auteur\b", "the author"),
    (r"\bl'intérêt\b", "the interest"),
    (r"\bl'image\b", "the image"),
    (r"\bl'effet\b", "the effect"),
    (r"\bl'ensemble\b", "all"),
    (r"\bl'accès\b", "access"),
    (r"\bl'Harmattan\b", "L'Harmattan"),
    (r"\bl'IFA\b", "the IFA"),
    (r"\bl'APIA\b", "APIA"),
    (r"\bl'ADAE\b", "ADAE"),
    (r"\bl'INSEAD\b", "INSEAD"),
    (r"\bl'Europe\b", "Europe"),
    (r"\bl'Asie\b", "Asia"),
    (r"\bl'Inde\b", "India"),
    (r"\bl'Allemagne\b", "Germany"),
    (r"\bl'Angleterre\b", "England"),
    (r"\bl'Espagne\b", "Spain"),
    (r"\bl'Italie\b", "Italy"),
    (r"\bl'immobilier\b", "real estate"),
    (r"\bl'informatique\b", "IT"),
    (r"\bl'industrie\b", "industry"),
    (r"\bl'énergie\b", "energy"),
    (r"\bl'innovation\b", "innovation"),
    (r"\bl'habillement\b", "clothing"),
    (r"\bl'environnement\b", "the environment"),
    (r"\bl'entreprise\b", "the company"),
    (r"\bl'activité\b", "the business"),
    (r"\bl'association\b", "the association"),
    (r"\bl'atelier\b", "the workshop"),
    (r"\bl'invitation\b", "the invitation"),
    (r"\bl'application\b", "the application"),
    (r"\bl'évolution\b", "the evolution"),
    (r"\bl'évaluation\b", "the evaluation"),
    (r"\bl'occasion\b", "the occasion"),
    (r"\bl'objectif\b", "the objective"),
    (r"\bl'originalité\b", "the originality"),
    (r"\bl'observatoire\b", "the observatory"),
    (r"\bl'analyse\b", "the analysis"),

    (r"\bL'article\b", "The article"),
    (r"\bL'accès\b", "Access"),
    (r"\bL'entreprise\b", "The company"),
    (r"\bL'auteur\b", "The author"),
    (r"\bL'observatoire\b", "The observatory"),
    (r"\bL'actualité\b", "Current events"),

    # "des + noun" -> "of the / some"
    (r'\bdes sociétés\b', 'of companies'),
    (r'\bdes entreprises\b', 'of companies'),
    (r'\bdes filiales\b', 'of subsidiaries'),
    (r'\bdes activités\b', 'of activities'),
    (r'\bdes équipes\b', 'of teams'),
    (r'\bdes missions\b', 'of assignments'),
    (r'\bdes projets\b', 'of projects'),
    (r'\bdes postes\b', 'of positions'),
    (r'\bdes résultats\b', 'of results'),
    (r'\bdes réflexions\b', 'of reflections'),
    (r'\bdes opérations\b', 'of operations'),
    (r'\bdes restructurations\b', 'of restructurings'),
    (r'\bdes responsabilités\b', 'of responsibilities'),
    (r'\bdes montages\b', 'of arrangements'),
    (r'\bdes actions\b', 'of actions'),
    (r'\bdes recommandations\b', 'of recommendations'),
    (r'\bdes informations\b', 'of information'),
    (r'\bdes contacts\b', 'of contacts'),
    (r'\bdes relations\b', 'of relations'),
    (r'\bdes problématiques\b', 'of issues'),
    (r'\bdes disponibilités\b', 'of availability'),
    (r'\bdes dossiers\b', 'of files'),
    (r'\bdes cours\b', 'of courses'),
    (r'\bdes compétences\b', 'of skills'),
    (r'\bdes certificats\b', 'of certificates'),
    (r'\bdes prix\b', 'of awards'),
    (r'\bdes distinctions\b', 'of distinctions'),
    (r'\bdes soutiens\b', 'of support'),
    (r'\bdes mesures\b', 'of measures'),
    (r'\bdes réductions\b', 'of reductions'),
    (r'\bdes transactions\b', 'of transactions'),
    (r'\bdes échanges\b', 'of exchanges'),
    (r'\bdes pays\b', 'of countries'),
    (r'\bdes participations\b', 'of investments'),
    (r'\bdes recherches\b', 'of research'),
    (r'\bdes mandats\b', 'of mandates'),
    (r'\bdes groupes\b', 'of groups'),
    (r'\bdes cabinets\b', 'of firms'),
    (r'\bdes fonds\b', 'of funds'),
    (r'\bdes axes\b', 'of areas'),
    (r'\bdes chantiers\b', 'of projects'),
    (r'\bdes partenariats\b', 'of partnerships'),
    (r'\bdes investissements\b', 'of investments'),
    (r'\bdes transferts\b', 'of transfers'),

    # Remaining common French function words in context
    (r'\bpour\s+les\b', 'for'),
    (r'\bpour\s+la\b', 'for'),
    (r'\bpour\s+le\b', 'for the'),
    (r'\bpour\s+des\b', 'for'),
    (r'\bpour\s+un\b', 'for a'),
    (r'\bpour\s+une\b', 'for a'),

    (r'\bdans\s+les\b', 'in'),
    (r'\bdans\s+la\b', 'in'),
    (r'\bdans\s+le\b', 'in the'),
    (r'\bdans\s+des\b', 'in'),
    (r'\bdans\s+un\b', 'in a'),
    (r'\bdans\s+une\b', 'in a'),
    (r'\bdans\s+plusieurs\b', 'in several'),
    (r'\bdans\s+de\b', 'in'),
    (r'\bdans\s+ce\b', 'in this'),
    (r'\bdans\s+cette\b', 'in this'),
    (r'\bdans\s+ces\b', 'in these'),

    (r'\bavec\s+les\b', 'with the'),
    (r'\bavec\s+la\b', 'with the'),
    (r'\bavec\s+le\b', 'with the'),
    (r'\bavec\s+des\b', 'with'),
    (r'\bavec\s+un\b', 'with a'),
    (r'\bavec\s+une\b', 'with a'),

    (r'\bsur\s+les\b', 'on the'),
    (r'\bsur\s+la\b', 'on the'),
    (r'\bsur\s+le\b', 'on the'),
    (r'\bsur\s+des\b', 'on'),
    (r'\bsur\s+un\b', 'on a'),
    (r'\bsur\s+une\b', 'on a'),

    (r'\bpar\s+les\b', 'by the'),
    (r'\bpar\s+la\b', 'by the'),
    (r'\bpar\s+le\b', 'by the'),
    (r'\bpar\s+des\b', 'by'),
    (r'\bpar\s+un\b', 'by a'),
    (r'\bpar\s+une\b', 'by a'),

    (r'\bsous\s+les\b', 'under the'),
    (r'\bsous\s+la\b', 'under the'),
    (r'\bsous\s+le\b', 'under the'),
]

# ============================================================
# WORD-LEVEL DICTIONARY - only safe whole-word replacements
# ============================================================
# These are applied with strict word boundary matching
# Be conservative: only include words that won't cause issues

WORDS = {
    # Very safe standalone word replacements
    "actuellement": "currently",
    "Actuellement": "Currently",
    "aujourd'hui": "today",
    "Aujourd'hui": "Today",
    "également": "also",
    "notamment": "notably",
    "Notamment": "Notably",
    "récemment": "recently",
    "Récemment": "Recently",
    "prochainement": "soon",
    "Ensuite": "Then",
    "ensuite": "then",
    "Également": "Also",
    "Maintenant": "Now",
    "maintenant": "now",
    "Cependant": "However",
    "cependant": "however",
    "Néanmoins": "Nevertheless",
    "néanmoins": "nevertheless",
    "Ainsi": "Thus",
    "ainsi": "thus",
    "Aussi": "Also",
    "aussi": "also",
    "Enfin": "Finally",
    "enfin": "finally",

    # Common nouns safe to replace
    "entreprise": "company",
    "entreprises": "companies",
    "société": "company",
    "sociétés": "companies",
    "filiale": "subsidiary",
    "filiales": "subsidiaries",
    "Filiale": "Subsidiary",
    "Filiales": "Subsidiaries",
    "expérience": "experience",
    "Expérience": "Experience",
    "carrière": "career",
    "gouvernance": "governance",
    "Gouvernance": "Governance",
    "compétence": "competence",
    "compétences": "competences",
    "conférence": "conference",
    "restructuration": "restructuring",
    "restructurations": "restructurings",
    "redressement": "turnaround",
    "opérationnel": "operational",
    "opérationnelle": "operational",
    "opérationnels": "operational",
    "opérationnelles": "operational",
    "stratégique": "strategic",
    "stratégiques": "strategic",
    "indépendant": "independent",
    "indépendante": "independent",
    "indépendants": "independent",
    "indépendantes": "independent",
    "international": "international",
    "internationale": "international",
    "internationaux": "international",
    "internationales": "international",
    "industriel": "industrial",
    "industrielle": "industrial",
    "industrielles": "industrial",
    "industriels": "industrial",
    "professionnel": "professional",
    "professionnelle": "professional",
    "professionnels": "professional",
    "professionnelles": "professional",
    "Administrateur": "Director",
    "administrateur": "director",
    "Administratrice": "Director",
    "administratrice": "director",
    "administrateurs": "directors",
    "Administrateurs": "Directors",
    "administratrices": "directors",
    "Administratrices": "Directors",
    "Président": "Chairman",
    "président": "chairman",
    "Présidente": "Chairwoman",
    "présidente": "chairwoman",
    "Présidents": "Chairmen",
    "Présidentes": "Chairwomen",
    "Directeur": "Director",
    "directeur": "director",
    "Directrice": "Director",
    "directrice": "director",
    "candidat": "candidate",
    "Candidat": "Candidate",
    "candidate": "candidate",
    "Candidate": "Candidate",
    "membre": "member",
    "Membre": "Member",
    "membres": "members",
    "Membres": "Members",
    "Ingénieur": "Engineer",
    "ingénieur": "engineer",
    "Avocate": "Lawyer",
    "avocate": "lawyer",
    "avocat": "lawyer",
    "avocats": "lawyers",
    "juriste": "legal professional",
    "salarié": "employee",
    "salariés": "employees",
    "actionnaire": "shareholder",
    "actionnaires": "shareholders",
    "actionnariat": "shareholding",
    "actionnariats": "shareholdings",
    "investisseur": "investor",
    "investisseurs": "investors",
    "Investisseur": "Investor",
    "fournisseur": "supplier",
    "fournisseurs": "suppliers",
    "banquier": "banker",
    "Commissaire": "Commissioner",
    "prestations": "services",
    "diagnostic": "assessment",
    "diagnostics": "assessments",
    "Diagnostic": "Assessment",
    "mandats": "mandates",
    "mandat": "mandate",

    # Industries
    "informatique": "IT",
    "Informatique": "IT",
    "numérique": "digital",
    "Numérique": "Digital",
    "cybersécurité": "cybersecurity",
    "télécommunications": "telecommunications",
    "Télécommunications": "Telecommunications",
    "télécoms": "telecoms",
    "Télécoms": "Telecoms",
    "aéronautique": "aerospace",
    "Aéronautique": "Aerospace",
    "nucléaire": "nuclear",
    "pétrole": "oil",
    "chimie": "chemicals",
    "pharmacie": "pharmaceuticals",
    "Pharmacie": "Pharmaceuticals",
    "cosmétique": "cosmetics",
    "agroalimentaire": "agri-food",
    "immobilier": "real estate",
    "Immobilier": "Real estate",

    # Common adjectives
    "français": "French",
    "française": "French",
    "Français": "French",
    "Française": "French",
    "américain": "American",
    "américaine": "American",
    "américains": "American",
    "européen": "European",
    "européenne": "European",
    "européens": "European",
    "européennes": "European",
    "anglais": "English",
    "anglaise": "English",
    "allemand": "German",
    "allemande": "German",
    "allemands": "German",
    "espagnol": "Spanish",
    "espagnole": "Spanish",
    "italien": "Italian",
    "italienne": "Italian",
    "suédois": "Swedish",
    "portugais": "Portuguese",
    "russe": "Russian",
    "Russe": "Russian",
    "norvégienne": "Norwegian",
    "Norvégienne": "Norwegian",
    "coréen": "Korean",
    "luxembourgeois": "Luxembourg",
    "Luxembourgeois": "Luxembourg",

    # Business terms
    "comptabilité": "accounting",
    "fiscalité": "taxation",
    "juridique": "legal",
    "innovation": "innovation",
    "stratégie": "strategy",
    "Stratégie": "Strategy",

    # Common verbs (past participle forms - safe as adjectives)
    "qualifié": "qualified",
    "qualifiée": "qualified",
    "qualifiés": "qualified",
    "qualifiées": "qualified",
    "spécialisé": "specialised",
    "spécialisée": "specialised",
    "spécialisés": "specialised",
    "certifié": "certified",
    "certifiée": "certified",
    "cotée": "listed",
    "cotées": "listed",
    "cotés": "listed",
    "cotée au": "listed on",
    "variés": "varied",
    "variée": "varied",
    "réussie": "successful",
    "réussi": "successful",
    "réussies": "successful",
    "diversifié": "diversified",
    "diversifiée": "diversified",
    "étendue": "extensive",
    "étendu": "extensive",
    "approfondie": "in-depth",
    "approfondi": "in-depth",
    "détaillée": "detailed",
    "détaillé": "detailed",
    "significatif": "significant",
    "significative": "significant",
    "remarquable": "remarkable",
    "intéressant": "interesting",
    "intéressante": "interesting",
    "intéressants": "interesting",
    "délicats": "delicate",
    "délicat": "delicate",
    "passionnant": "exciting",
    "publiés": "published",
    "publié": "published",
    "repérés": "identified",

    # Technology
    "logiciel": "software",
    "logiciels": "software",
}


def parse_untranslated_keys(filepath):
    """Parse the untranslated strings file and return a set of dotted keys."""
    keys = set()
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith("KEY: "):
                keys.add(line[5:])
    return keys


def get_nested_value(data, dotted_key):
    """Get a value from a nested dict using a dotted key."""
    parts = dotted_key.split(".", 1)
    if len(parts) == 1:
        return data.get(parts[0])
    if parts[0] in data and isinstance(data[parts[0]], dict):
        return get_nested_value(data[parts[0]], parts[1])
    return None


def set_nested_value(data, dotted_key, value):
    """Set a value in a nested dict using a dotted key."""
    parts = dotted_key.split(".", 1)
    if len(parts) == 1:
        data[parts[0]] = value
        return
    if parts[0] not in data:
        data[parts[0]] = {}
    if not isinstance(data[parts[0]], dict):
        return
    set_nested_value(data[parts[0]], parts[1], value)


def apply_phrase_translations(text):
    """Apply phrase-level translations, longest first."""
    # Sort by length descending to apply longest matches first
    sorted_phrases = sorted(PHRASES.items(), key=lambda x: -len(x[0]))
    for fr, en in sorted_phrases:
        if fr in text:
            text = text.replace(fr, en)
    return text


def apply_word_translations(text):
    """Apply word-level translations with strict word boundaries."""
    # Sort by length descending
    sorted_words = sorted(WORDS.items(), key=lambda x: -len(x[0]))

    for fr_word, en_word in sorted_words:
        # Build a word-boundary pattern
        # French word chars include accented chars
        fr_chars = r"a-zA-ZàâäéèêëïîôùûüÿçœæÀÂÄÉÈÊËÏÎÔÙÛÜŸÇŒÆ'\-"
        pattern = re.compile(
            r'(?<![' + fr_chars + r'])' +
            re.escape(fr_word) +
            r'(?![' + fr_chars + r'])',
            re.UNICODE
        )
        text = pattern.sub(en_word, text)

    return text


def apply_regex_translations(text):
    """Apply regex-based translations."""
    for pattern, replacement in REGEX_PATTERNS:
        text = re.sub(pattern, replacement, text)
    return text


def translate_text(text):
    """Translate a text string from French to English."""
    if not text or not text.strip():
        return text

    # Preserve leading/trailing whitespace
    leading_ws = text[:len(text) - len(text.lstrip())]
    trailing_ws = text[len(text.rstrip()):]
    core = text.strip()

    if not core:
        return text

    # Apply phrase-level translations first (longest first)
    result = apply_phrase_translations(core)

    # Apply regex-based pattern translations
    result = apply_regex_translations(result)

    # Then apply word-level translations
    result = apply_word_translations(result)

    # Second pass of phrase translations to catch newly exposed patterns
    result = apply_phrase_translations(result)

    # Second pass of regex
    result = apply_regex_translations(result)

    return leading_ws + result + trailing_ws


def translate_html_value(html_str):
    """
    Translate an HTML string, preserving all tags and only translating text nodes.
    """
    if not html_str or not html_str.strip():
        return html_str

    # Check if it contains HTML tags
    has_html = bool(re.search(r'<[a-zA-Z]', html_str))

    if not has_html:
        return translate_text(html_str)

    # Wrap in a container to handle fragments
    wrapped = f"<div id='_xwrap_'>{html_str}</div>"

    try:
        soup = BeautifulSoup(wrapped, 'html.parser')
    except Exception:
        return translate_text(html_str)

    wrapper = soup.find(id='_xwrap_')
    if not wrapper:
        return translate_text(html_str)

    _translate_node(wrapper)

    result = wrapper.decode_contents()
    return result


def _translate_node(node):
    """Recursively translate text nodes within a BeautifulSoup node."""
    for child in list(node.children):
        if isinstance(child, NavigableString):
            if isinstance(child, Comment):
                continue
            original = str(child)
            if original.strip():
                translated = translate_text(original)
                child.replace_with(NavigableString(translated))
        elif child.name:
            _translate_node(child)


def count_french_words(text):
    """Count French indicator words in text (for verification)."""
    if not isinstance(text, str):
        return 0
    # Remove HTML tags
    clean = re.sub(r'<[^>]+>', ' ', text).lower()

    french_indicators = [
        r"\bqu'", r"\bd'un\b", r"\bd'une\b", r"\bl'un\b",
        r"\bpour\b", r"\bdans\b", r"\bavec\b",
        r"\bleur\b", r"\bleurs\b", r"\bqui\b",
        r"\bdont\b", r"\bsur\b",
        r"\bégalement\b", r"\bnotamment\b",
        r"\baprès\b", r"\bpendant\b", r"\bdepuis\b",
        r"\bcette\b", r"\bces\b",
        r"\bexpérience\b", r"\bcarrière\b",
        r"\bprésident\b", r"\bdirecteur\b",
        r"\bentreprise\b", r"\bsociété\b",
        r"\badministrat\w+\b", r"\bconseil\b",
        r"\bmatière\b", r"\bdomaine\b",
        r"\bpermett\w+\b", r"\bconnai\w+\b",
        r"\bnombreux\b", r"\bnombreuses\b",
        r"\bparticulier\b", r"\bparticulière\b",
        r"\btravaillé\b", r"\bexercé\b",
        r"\boccupé\b", r"\bdirigé\b",
        r"\bcréé\b", r"\bdéveloppé\b",
        r"\bréalisé\b", r"\bacquis\b",
        r"\bprofessionnel\b", r"\bprofessionnelle\b",
        r"\binternational\b", r"\binternationale\b",
        r"\bfinancier\b", r"\bfinancière\b",
    ]

    count = 0
    for pattern in french_indicators:
        if re.search(pattern, clean):
            count += 1
    return count


def main():
    print(f"Reading en.json from: {EN_JSON}")
    with open(EN_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Reading untranslated keys from: {UNTRANSLATED_FILE}")
    untranslated_keys = parse_untranslated_keys(UNTRANSLATED_FILE)
    print(f"Found {len(untranslated_keys)} untranslated keys")

    translated_count = 0
    error_count = 0

    for key in sorted(untranslated_keys):
        value = get_nested_value(data, key)
        if value is None:
            print(f"  WARNING: Key not found: {key}")
            error_count += 1
            continue

        if not isinstance(value, str):
            continue

        try:
            translated = translate_html_value(value)
            if translated != value:
                set_nested_value(data, key, translated)
                translated_count += 1
        except Exception as e:
            print(f"  ERROR translating {key}: {e}")
            import traceback
            traceback.print_exc()
            error_count += 1

    print(f"\nTranslated {translated_count} strings ({error_count} errors)")

    # Write the updated JSON
    print(f"Writing updated en.json...")
    with open(EN_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Verification
    print("\n=== Verification ===")
    still_french = 0
    sample_issues = []
    for key in sorted(untranslated_keys):
        value = get_nested_value(data, key)
        if isinstance(value, str):
            fc = count_french_words(value)
            if fc >= 3:
                still_french += 1
                if len(sample_issues) < 5:
                    # Show a snippet
                    clean = re.sub(r'<[^>]+>', ' ', value)
                    clean = re.sub(r'\s+', ' ', clean).strip()[:120]
                    sample_issues.append(f"  {key}: ...{clean}...")

    print(f"Strings that still appear to contain significant French: {still_french}/{len(untranslated_keys)}")
    if sample_issues:
        print("Sample issues:")
        for s in sample_issues:
            print(s)
    print("\nDone!")


if __name__ == "__main__":
    main()
