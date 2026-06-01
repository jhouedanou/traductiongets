#!/usr/bin/env python3
"""
final-translate.py — Directly patch remaining untranslated strings in en.json.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_JSON = ROOT / "data" / "translations" / "en.json"
FR_JSON = ROOT / "data" / "translations" / "fr.json"

# Direct key → English value patches
PATCHES = {
    # actualites
    "page_actualites.la_lecture_duprogramme_detailledonne_tous_les": "Reading the detailed programme gives all the details.",
    "page_actualites.avecpascal_picq_paleoanthropologue_de_renom_u": "With Pascal Picq, renowned palaeoanthropologist: a unique lecture on anthropology and the evolution of businesses.",
    "page_actualites.photo_du_standavec_guy_le_pechon_accompagne_d": "Photo of the stand with Guy Le Péchon accompanied by Catherine Montagnon, polytechnician, and her book 'Humanity, Doctors and Work: Paradigm Shifts?' to be published very soon.",
    "page_actualites.presentation_par_guy_le_pechon_dextraits_des_": "Presentation by Guy Le Péchon of excerpts from the G & S study on the feminisation of Governance Bodies of CAC 40 companies as of end May 2025.",
    "page_actualites.puis_la_videode_valerie_lejeune_comment_le_ce": "Then, the video of Valérie Lejeune 'How the COMEX CODIR Governance 5.0 Certificate from Centrale Supélec Executive Education was developed'",
    "page_actualites.g_s_a_lorigine_de_levenement_propose_aux_comi": "G & S, the originator of the event proposed to the Career Committees of alumni associations of grandes écoles (G16+), continues the momentum of the Rixain law. After contributing to the design of the in-person evening of 14 October 2025 in the presence of Member of Parliament Marie-Pierre Rixain, we are pleased to share the official invitation.",
    "page_actualites.presentation_par_guy_le_pechon_dextraits_des__2": "Presentation by Guy Le Péchon of excerpts from the G & S study on the feminisation of Governance Bodies of CAC 40 companies as of end May 2025.",
    "page_actualites.puis_comment_le_certificat_comex_codir_gouver": "Then, how the COMEX CODIR Governance 5.0 Certificate was developed by Valérie Lejeune.",
    "page_actualites.7_juillet_2026": "7 July 2026",

    # mentions-legales
    "page_mentions_legales.cookies": "Cookies",
    "page_mentions_legales.le_site_g_s_na_pas_de_mecanismes_denregistrem": "The G & S website does not use 'cookies' recording mechanisms.",
    "page_mentions_legales.danscette_page_gouvernance_structures_precise": "On this page, Gouvernance & Structures specifies the legal information relating to its website.",
    "page_mentions_legales.loi_informatique_fichiers_et_libertes": "Data Protection and Civil Liberties Act",
    "page_mentions_legales.conformement_a_la_loi_du_6_janvier_1978_relat": "In accordance with the French Act of 6 January 1978 on Information Technology, Data Files and Civil Liberties and its subsequent amendments, every person may obtain communication of, and where appropriate, correct or request deletion of information concerning them by contacting G & S.",
    "page_mentions_legales.les_utilisateurs_du_site_g_et_s_com_sont_tenu": "Users of the G-et-S.com website must comply with the provisions of the Data Protection Act, breach of which is punishable by criminal penalties.",
    "page_mentions_legales.politique_de_g_s_pour_la_gestion_des_donnees_": "G & S Policy on Personal Data Management",
    "page_mentions_legales.lirele_texte_detaille": "Read the detailed text",
    "page_mentions_legales.utilisation_des_donnees_collectees": "Use of Collected Data",
    "page_mentions_legales.les_informations_telles_que_les_noms_adresses": "Information such as names, addresses, etc. collected on the site will not be used for purposes other than those provided for.",
    "page_mentions_legales.confidentialite_des_donnees": "Data Confidentiality",
    "page_mentions_legales.les_informations_fournies_par_linternaute_lor": "Information provided by the user, when recorded by G & S, is treated as confidential.",
    "page_mentions_legales.les_informations_figurant_sur_le_site_g_s_non": "The information on the G & S website is not confidential but may not be used without the prior written consent of G & S.",
    "page_mentions_legales.responsabilite_de_g_s": "G & S Liability",
    "page_mentions_legales.en_permanence_g_s_fait_tous_ses_efforts_pour_": "G & S makes every effort to ensure that the information presented on its site is accurate and up to date.",
    "page_mentions_legales.le_contenu_mis_en_ligne_par_g_s_constitue_une": "The content published by G & S constitutes a work of the mind within the meaning of the Intellectual Property Code.",
    "page_mentions_legales.liens_internet_vers_g_s_et_reciproquement": "Internet Links to G & S and Vice Versa",
    "page_mentions_legales.g_s_se_rejouira_de_letablissement_de_liens_in": "G & S welcomes the establishment of internet links to its site, provided they are for informational purposes.",
    "page_mentions_legales.g_s_examinera_avec_attention_toutes_les_deman": "G & S will carefully examine all requests for reciprocal links. Contact the Webmaster.",

    # plan-du-site
    "page_plan_du_site.generalites_corporate_governance": "Corporate Governance Overview",
    "page_plan_du_site.pour_mandataires": "For Board Members",
    "page_plan_du_site.pour_societes": "For Companies",
    "page_plan_du_site.prestations_de_gouvernance_et_structures": "G & S Governance Services",
    "page_plan_du_site.page_daccueil": "Home Page",
    "page_plan_du_site.formation_aux_comex_codir": "Comex/Codir Training",
    "page_plan_du_site.formations_au_c_a": "Board Training",
    "page_plan_du_site.article_presse": "Press Article",
    "page_plan_du_site.introduction": "Introduction",
    "page_plan_du_site.plan_du_site": "Sitemap",
    "page_plan_du_site.contributions_de_guy_le_pechon": "Contributions by Guy Le Péchon",
    "page_plan_du_site.documents_utiles": "Useful Documents",
    "page_plan_du_site.contributions_de_guy_le_pechon_2": "Contributions by Guy Le Péchon",
    "page_plan_du_site.documents_utiles_2": "Useful Documents",
    "page_plan_du_site.plan_du_site_2": "Sitemap",

    # administrateur-independant
    "page_administrateur_independant.criteres_dindependance": "Independence Criteria",
    "page_administrateur_independant.lactualite_nannihile_pas_les_ecrits_passes_im": "Current events do not invalidate important past writings",
    "page_administrateur_independant.ni_lien_familial_proche_avec_un_mandataire_so": "No close family ties with a corporate officer.",
    "page_administrateur_independant.ni_administrateur_de_lentreprise_depuis_plus_": "Not a director of the company for more than twelve years.",
    "page_administrateur_independant.inferieur_a_10_independant_si_ne_participe_pa": "Below 10%: independent if does not participate in control.",
    "page_administrateur_independant.nous_contacter": "Contact Us",

    # apports-ia-compliance
    "page_apports_ia_compliance.avant_propos_reflexions_dun_beotien_de_lia_et": "FOREWORD: REFLECTIONS OF A LAYPERSON ON AI AND COMPLIANCE",
    "page_apports_ia_compliance.nayant_pas_de_competences_particulieres_sur_l": "Not having any particular expertise in AI, I have simply written the following foreword.",
    "page_apports_ia_compliance.generalites": "General",

    # articles-presse
    "page_articles_presse.cette_page_est_actuellement_en_cours_de_const": "This page is currently under construction.",
    "page_articles_presse.nous_contacter": "Contact Us",

    # assises-parite-new
    "page_assises_parite_new.objectifs_de_levenement": "Event Objectives",
    "page_assises_parite_new.9h00_ouverture": "9:00 AM - Opening",
    "page_assises_parite_new.9h30_table_ronde_1": "9:30 AM - Panel 1",
    "page_assises_parite_new.11h00_table_ronde_2": "11:00 AM - Panel 2",
    "page_assises_parite_new.14h00_table_ronde_3": "2:00 PM - Panel 3",
    "page_assises_parite_new.16h00_networking": "4:00 PM - Networking",
    "page_assises_parite_new.intervenants_prestigieux": "Distinguished Speakers",
    "page_assises_parite_new.resultats_et_impact": "Results and Impact",
    "page_assises_parite_new.participants": "Participants",
    "page_assises_parite_new.intervenants_experts": "Expert Speakers",
    "page_assises_parite_new.de_conferences": "Lectures",
    "page_assises_parite_new.tables_rondes": "Panel Discussions",
    "page_assises_parite_new.retour_dexperience_sur_les_initiatives_reussi": "Feedback on successful professional equality initiatives.",
    "page_assises_parite_new.leadership_feminin_et_performance": "Female Leadership and Performance",
    "page_assises_parite_new.echanges_et_opportunites": "Exchanges and Opportunities",
    "page_assises_parite_new.promouvoir_legalite_professionnelle": "Promote professional equality",
    "page_assises_parite_new.echanger_les_bonnes_pratiques": "Share best practices",
    "page_assises_parite_new.sensibiliser_aux_enjeux_de_diversite": "Raise awareness of diversity issues",
    "page_assises_parite_new.accompagner_les_transformations": "Support transformations",
    "page_assises_parite_new.creation_dun_reseau_de_mentoring": "Creation of a mentoring network",
    "page_assises_parite_new.lancement_dun_observatoire_de_legalite": "Launch of an equality observatory",
    "page_assises_parite_new.rendez_vous_trimestriels_programmes": "Quarterly meetings scheduled",
    "page_assises_parite_new.indicateurs_de_suivi_definis": "Monitoring indicators defined",
    "page_assises_parite_new.prochaines_assises_prevues_en_2025": "Next conference planned for 2025",
    "page_assises_parite_new.engagements_pris": "Commitments made",
    "page_assises_parite_new.suivi_des_actions": "Action monitoring",
    "page_assises_parite.obtenir_le_rapport_complet": "Obtain the full report",

    # bibliographie
    "page_bibliographie.actions_diverses_de_g_s": "G&S VARIOUS ACTIVITIES",
    "page_bibliographie.lactualite_nannihile_pas_les_ecrits_passes_im": "Current events do not invalidate important past writings",
    "page_bibliographie.notes_et_articles_publies_par_g_s": "Articles and papers published by G & S",
    "page_bibliographie.relations_presse_de_gouvernance_structures_fl": "Gouvernance & Structures Press Relations (RSS Feed) Click here",

    # boards-et-comex
    "page_boards_et_comex.boards_et_comex": "Boards and Comex",

    # candidats-mandataires-sociaux (CV content — partial translations)
    "page_candidats_mandataires_sociaux.candidat_e_s_mandatairesadministratrices_admi": "BOARD MEMBER CANDIDATES — FEMALE AND MALE DIRECTORS",
    "page_candidats_mandataires_sociaux.pour_connaitre_leur_nom_et_leurs_coordonnees_": "To learn their names and contact details and reach them, write to contact@g-et-s.com quoting the reference shown.",
    "page_candidats_mandataires_sociaux.diplome_de_lessec_et_de_telecom_paris_anglais": "Graduate of ESSEC and Télécom Paris, fluent in English, IFA Audit member. Ref 732",
    "page_candidats_mandataires_sociaux.non_executive_director_in_european_companies_": "Non Executive Director in European companies and family offices with a focus and presence in Asia.",
    "page_candidats_mandataires_sociaux.this_male_candidate_has_a_successful_track_re": "This male candidate has a successful track record of over twenty-two years advising Fortune 500 companies on strategy, mergers and acquisitions.",
    "page_candidats_mandataires_sociaux.de_par_sa_nationalite_italienne_et_son_parcou": "By virtue of his Italian nationality and his European career, he has in-depth knowledge of French, Italian and other European cultures.",
    "page_candidats_mandataires_sociaux.industrie_pharmaceutique": "Pharmaceutical Industry",
    "page_candidats_mandataires_sociaux.equipements_et_appareillages_industriels_ener": "Industrial Equipment (Energy, Transport, High Technology)",
    "page_candidats_mandataires_sociaux.aviation_aeronautique_spatial_defense_securit": "Aviation, Aeronautics, Space, Defence & Security",
    "page_candidats_mandataires_sociaux.edition_de_logiciel": "Software Publishing",
    "page_candidats_mandataires_sociaux.genie_medical_france_et_usa": "Medical Engineering France and USA",
    "page_candidats_mandataires_sociaux.experience_tres_etendue_produits_alimentaires": "Extensive experience (FMCG Food Products) in France and internationally for over 15 years",
    "page_candidats_mandataires_sociaux.presse_et_medias_developpement_international": "Press and Media — International Development",
    "page_candidats_mandataires_sociaux.woman_european_company_board_ready": "Woman European Company Board Ready",
    "page_candidats_mandataires_sociaux.langues_etrangeres_anglais_allemand_notions_e": "Foreign languages: English, German — Basic: Spanish, Italian",
    "page_candidats_mandataires_sociaux.langues_francais_anglais_italien": "Languages: French — English — Italian",
    "page_candidats_mandataires_sociaux.administratrice_independante_grande_societe_e": "Independent female director, large European company",
    "page_candidats_mandataires_sociaux.femmes_candidates": "Female Candidates",

    # candidats-mandataires (form)
    "page_candidats_mandataires.adresse_electronique": "Email Address *",
    "page_candidats_mandataires.adresse_partie_1": "Address Line 1",
    "page_candidats_mandataires.adresse_partie_2": "Address Line 2",
    "page_candidats_mandataires.adresse_partie_3": "Address Line 3",
    "page_candidats_mandataires.code_postal": "Postal Code",
    "page_candidats_mandataires.site_internet": "Website",
    "page_candidats_mandataires.secteur_dactivite_1": "Business Sector 1",
    "page_candidats_mandataires.secteur_dactivite_2": "Business Sector 2",
    "page_candidats_mandataires.secteur_dactivite_3": "Business Sector 3",
    "page_candidats_mandataires.langue_maternelle_1": "Mother Tongue 1",
    "page_candidats_mandataires.langue_maternelle_2": "Mother Tongue 2",
    "page_candidats_mandataires.langue_courante_1": "Working Language 1",
    "page_candidats_mandataires.langue_courante_2": "Working Language 2",
    "page_candidats_mandataires.langue_courante_3": "Working Language 3",
    "page_candidats_mandataires.organisation": "Organisation",
    "page_candidats_mandataires.organisation_2": "Organisation",
    "page_candidats_mandataires.organisation_3": "Organisation",
    "page_candidats_mandataires.bac_3": "≤ bac + 3",
    "page_candidats_mandataires.bac_5_1": "≤ bac + 5 (1)",
    "page_candidats_mandataires.bac_5_2": "≤ bac + 5 (2)",
    "page_candidats_mandataires.commentaires_succincts_eventuels": "Brief optional comments",
    "page_candidats_mandataires.a_ce_stade_un_cv_est_inutile": "At this stage a CV is not necessary.",
    "page_candidats_mandataires.les_elements_figurant_en_bleu_sont_indispensa": "Items shown in blue are required, others are recommended.",
    "page_candidats_mandataires.postuler_a_des_postes_dadministrateurs": "APPLY FOR DIRECTOR POSITIONS",
    "page_candidats_mandataires.utilisation_par_g_s_des_informations_du_formu": "USE BY G & S OF FORM INFORMATION",
    "page_candidats_mandataires.indications_pour_le_remplissage_du_formulaire": "Instructions for completing the form",
    "page_candidats_mandataires.un_secteur_dactivite_correspond_en_general_a_": "A business sector generally corresponds to a market (e.g. banking, packaging, consumer electronics...).",
    "page_candidats_mandataires.un_pays_dactivite_est_un_pays_ou_vous_avez_ve": "A country of activity is a country where you have lived at least one year and know the professional and cultural life.",
    "page_candidats_mandataires.candidature_comme_mandataire": "APPLICATION AS BOARD MEMBER",

    # catalogue-documents
    "page_catalogue_documents.documents_disponibles_en_telechargement": "Documents available for download",
    "page_catalogue_documents.documents_utiles_pour_ladministrateur": "Useful documents for the director",
    "page_catalogue_documents.une_fois_les_caracteristiques_fixees_le_docum": "Once the characteristics are set, the document becomes a generic document such as the 'Annual Income Statement'.",
    "page_catalogue_documents.le_contrat_dassurance_de_protection_de_ladmin": "The director's liability insurance contract",
    "page_catalogue_documents.la_revue_de_presse_hebdomadaire": "The weekly press review",
    "page_catalogue_documents.nous_contacter": "Contact Us",
    "page_catalogue_documents.catalogue_de_documents": "Document Catalogue",

    # certificat-centrale
    "page_certificat_centrale.centrale_supelec_executive_education": "Centrale Supélec Executive Education",
    "page_certificat_centrale.pour_decouvrir_ce_programme_il_vous_est_possi": "To discover this programme, you can view:",
    "page_certificat_centrale.la_brochuredonne_tous_les_details": "The brochure gives all the details.",
    "page_certificat_centrale.certificat_pour_les_membres_de_comex_codiren_": "Certificate for current or potential COMEX CODIR members",

    # construction pages (many share the same text)
    **{f"page_{p}.cette_page_est_actuellement_en_cours_de_const": "This page is currently under construction."
       for p in ["conseils_numerique", "couverture_harmattan", "diagnostics_ca",
                 "directive_europeenne", "entreprise_liberee", "generalites_corporate_governance",
                 "ia_compliance", "information_administrateurs", "livre_gouvernance_ca",
                 "missions_conseil", "monde_numerique", "observatoire_genres",
                 "ouvrage_collectif_ca", "plateforme_formation", "recherche_administrateur",
                 "soiree_lancement", "video_glp_vl", "webinaires_passes", "articles_presse"]},

    **{f"page_{p}.nous_contacter": "Contact Us"
       for p in ["conseils_numerique", "couverture_harmattan", "diagnostics_ca",
                 "directive_europeenne", "entreprise_liberee", "etude_juin_2025",
                 "generalites_corporate_governance", "glossaire_prestations",
                 "ia_compliance", "information_administrateurs", "livre_gouvernance_ca",
                 "missions_conseil", "monde_numerique", "observatoire_genres",
                 "ouvrage_collectif_ca", "plateforme_formation", "recherche_administrateur",
                 "soiree_lancement", "video_glp_vl", "webinaires_passes",
                 "administrateur_independant", "articles_presse", "catalogue_documents"]},

    # page-specific titles for construction pages
    "page_couverture_harmattan.couverture_lharmattan": "L'Harmattan Cover",
    "page_directive_europeenne.directive_europeenne": "European Directive",
    "page_generalites_corporate_governance.generalites_corporate_governance": "Corporate Governance Overview",
    "page_ia_compliance.ia_et_la_compliance_avant_propos": "AI and Compliance (Foreword)",
    "page_missions_conseil.missions_conseil": "Consulting Assignments",
    "page_plateforme_formation.plateforme_de_formation": "Training Platform",
    "page_recherche_administrateur.recherche_administrateur": "Director Search",
    "page_video_glp_vl.video_glp_vl": "Video GLP VL",

    # cours-inseec
    "page_cours_inseec.intervention_similaire_possible_en_intra_pour": "Similar in-company intervention possible for a business.",

    # dsi-conseils-administration
    "page_dsi_conseils_administration.generalites": "General",
    "page_dsi_conseils_administration.comment_les_dsi_peuvent_impliquer_les_ca": "How CIOs Can Engage Boards of Directors",

    # facilities-management
    "page_facilities_management_normes_europeennes.generalites": "General",

    # formations-administrateurs
    "page_formations_administrateurs.international_directors_program": "International Directors Program",
    "page_formations_administrateurs.executive_educationvision_tres_internationale": "Executive Education — Highly international vision",
    "page_formations_administrateurs.divers_programmes_certifiants": "Various certification programmes",
    "page_formations_administrateurs.women_be_european_board_ready": "Women Be European Board Ready",
    "page_formations_administrateurs.institute_of_directors": "Institute of Directors",
    "page_formations_administrateurs.formations_institutionnelles": "INSTITUTIONAL TRAINING",
    "page_formations_administrateurs.inseadinternational_directors_programexecutiv_2": "INSEAD — International Directors Program — Executive Education — Highly international vision",

    # glossaire-prestations
    "page_glossaire_prestations.le_resultat_est_larticle_redige_par_g_s_voir_": "The result is the article written by G & S. See Page 8 of the newsletter.",
    "page_glossaire_prestations.images_generees_par_intelligence_artificielle": "Images generated by Artificial Intelligence",

    # historique
    "page_historique.site_internet_http_www_g_et_s_com": "Website: http://www.g-et-s.com",
    "page_historique.contacts_info_g_et_s_com": "Contact: info@g-et-s.com",
    "page_historique.a_rassemble_plus_dune_soixantaine_de_particip": "brought together over sixty participants",
    "page_historique.voir_les_photos_dans_la_colonne_de_gauche": "See photos in the left column",
    "page_historique.le_theme_a_ete_introduit_par_guy_le_pechon_as": "The topic was introduced by Guy Le Péchon, Managing Partner of",

    # informatique
    "page_informatique.cloud_visite_guidee_gros_data_center": "'Cloud' — Guided tour of a large Data Centre",
    "page_informatique.internet_des_objets": "Internet of Things",
    "page_informatique.gestion_des_documents_pour_conseils": "Document Management for Boards",
    "page_informatique.big_data_et_relation_client": "Big Data and Customer Relations",
    "page_informatique.la_cryptographie_et_les_mots_de_passe": "Cryptography and Passwords",
    "page_informatique.realite_virtuelle": "Virtual Reality",
    "page_informatique.salle_de_gestion_de_crise": "Crisis Management Room",
    "page_informatique.intelligence_artificielle": "Artificial Intelligence",
    "page_informatique.des_formations_originales_proposees_par_g_s": "ORIGINAL TRAINING PROGRAMMES OFFERED BY G & S",

    # intelligence-collective
    "page_intelligence_collective.la_video_de_mon_intervention_que_je_crois_ass": "The video of my presentation (which I believe is quite original) is available on the page:",
    "page_intelligence_collective.atelier_intelligence_collective": "Collective Intelligence Workshop",
    "page_intelligence_collective.intelligence_collective": "Collective Intelligence",

    # livre-eti-new
    "page_livre_eti_new.salon_du_livre_des_polytechniciens": "Polytechnicians' Book Fair",
    "page_livre_eti_new.atelier_ethic": "ETHIC Workshop",
    "page_livre_eti_new.sceaux_smart": "Sceaux-Smart",
    "page_livre_eti_new.dedicaces_et_evenements": "Book signings and events",
    "page_livre_eti_new.editeur_lharmattan_collection_advalorem": "Publisher: L'Harmattan, AdValorem collection",
    "page_livre_eti_new.coordination_guy_le_pechon_g_s_et_valerie_lej": "Coordination: Guy Le Péchon (G&S) and Valérie Lejeune",
    "page_livre_eti_new.lieu_mairie_du_6eme_arrondissement_de_paris": "Venue: Town Hall of the 6th arrondissement of Paris",

    # livre-eti
    "page_livre_eti.salon_du_livre_des_polytechniciens": "Polytechnicians' Book Fair",
    "page_livre_eti.interview_de_valerie_lejeune_sur_eti_radio": "Interview with Valérie Lejeune on ETI Radio",
    "page_livre_eti.la_soiree_de_lancement": "The launch evening",
    "page_livre_eti.editeur_lharmattan_collection_advalorem": "Publisher: L'Harmattan, AdValorem collection",
    "page_livre_eti.coordination_guy_le_pechon_g_s_et_valerie_lej": "Coordination: Guy Le Péchon (G&S) and Valérie Lejeune",
    "page_livre_eti.lieu_mairie_du_6eme_arrondissement_de_paris": "Venue: Town Hall of the 6th arrondissement of Paris",

    # loi-rixain-new
    "page_loi_rixain_new.impact_sur_la_gouvernance_dentreprise": "Impact on Corporate Governance",
    "page_loi_rixain_new.mesures_cles_de_la_loi": "Key Measures of the Law",
    "page_loi_rixain_new.calendrier_dapplication": "Implementation Timeline",
    "page_loi_rixain_new.accompagnement_g_et_s": "G-ET-S Support",
    "page_loi_rixain_new.quota_minimum_de_femmes_dans_les_instances_di": "Minimum quota of women in governing bodies",
    "page_loi_rixain_new.obligations_de_reporting_renforcees": "Strengthened reporting obligations",
    "page_loi_rixain_new.diversification_des_profils_dirigeants": "Diversification of leadership profiles",
    "page_loi_rixain_new.amelioration_de_la_prise_de_decision": "Improved decision-making",
    "page_loi_rixain_new.renforcement_de_la_performance_economique": "Strengthened economic performance",
    "page_loi_rixain_new.meilleure_representativite_societale": "Better societal representation",
    "page_loi_rixain_new.transparence_salariale": "Pay transparency",
    "page_loi_rixain_new.equilibre_vie_professionnelle": "Work-life balance",
    "page_loi_rixain_new.formation_et_sensibilisation": "Training and awareness",
    "page_loi_rixain_new.plan_daction_personnalise": "Customised action plan",

    # loi-rixain
    "page_loi_rixain.impact_sur_la_gouvernance_dentreprise": "Impact on Corporate Governance",
    "page_loi_rixain.mesures_cles_de_lensemble_de_la_loi": "Key Measures of the Entire Law",
    "page_loi_rixain.calendrier_dapplication": "Implementation Timeline",
    "page_loi_rixain.accompagnement_g_et_s": "G-ET-S Support",
    "page_loi_rixain.en_mars_2029": "By March 2029",
    "page_loi_rixain.quota_minimum_de_femmes_dans_les_instances_di": "Minimum quota of women in governing bodies",
    "page_loi_rixain.chiffres_du_ministere_du_travail": "Ministry of Labour figures",
    "page_loi_rixain.obligation_datteindre_40_dans_ces_deux_groupe": "Obligation to reach 40% in these two groups of executives.",
    "page_loi_rixain.obligations_de_reporting_renforcees": "Strengthened reporting obligations",
    "page_loi_rixain.diversification_des_profils_dirigeants": "Diversification of leadership profiles",
    "page_loi_rixain.amelioration_de_la_prise_de_decision": "Improved decision-making",
    "page_loi_rixain.renforcement_de_la_performance_economique": "Strengthened economic performance",
    "page_loi_rixain.meilleure_representativite_societale": "Better societal representation",
    "page_loi_rixain.transparence_salariale": "Pay transparency",
    "page_loi_rixain.equilibre_vie_professionnelle": "Work-life balance",
    "page_loi_rixain.formation_et_sensibilisation": "Training and awareness",
    "page_loi_rixain.plan_daction_personnalise": "Customised action plan",

    # monde-numerique-relation-client
    "page_monde_numerique_relation_client.lutilisation_de_lintelligence_artificielle_de": "The use of Artificial Intelligence should facilitate the collection and organisation of this 'grey' data.",
    "page_monde_numerique_relation_client.generalites": "General",

    # organisation-gs
    "page_organisation_gs.diagnostics_quant_au_fonctionnement_ou_de_la_": "Diagnostics on the functioning or composition of Boards of Directors or Supervisory Boards, Comex or Codir",
    "page_organisation_gs.recrutement_de_dirigeants": "Executive Recruitment",
    "page_organisation_gs.gouvernance_et_structures": "Gouvernance et Structures",

    # questionnaire-rixain-societes
    "page_questionnaire_rixain_societes.a_titre_dexemple_voici_deux_premieres_questio": "As an example, here are the first two questions from the questionnaire:",
    "page_questionnaire_rixain_societes.pour_obtenir_le_questionnaire_complet": "To obtain the full questionnaire",
    "page_questionnaire_rixain_societes.instance_dirigeante": "GOVERNING BODY",
    "page_questionnaire_rixain_societes.il_sagit_de_vos_instances_dirigeantes_hors_du": "This refers to your governing bodies other than the Board of Directors or Supervisory Board.",
    "page_questionnaire_rixain_societes.envisagez_vous_une_evolution_du_nombre_de_mem": "Do you anticipate a change in the number of members of this governing body? *Only one answer possible.",
    "page_questionnaire_rixain_societes.reduction_du_nombre": "○ Reduction in number",
    "page_questionnaire_rixain_societes.augmentation_du_nombre": "○ Increase in number",

    # salarie-dirigeants-confiance
    "page_salarie_dirigeants_confiance.generalites": "General",

    # shadow-conseil
    "page_shadow_conseil.pourquoi_est_ce_possible_comment": "Why? Is it possible? How?",
    "page_shadow_conseil.une_approche_innovante_le_conseil_dadministra": "An innovative approach: The Youth Board of Directors",
    "page_shadow_conseil.alors_comment_proceder": "So, how to proceed?",
    "page_shadow_conseil.plus_de_jeunes_dans_les_conseils_dadministrat": "MORE YOUNG PEOPLE ON BOARDS OF DIRECTORS?",

    # travaux-ifa-digital
    "page_travaux_ifa_digital.de_quelles_informations_ladministrateur_a_t_i": "What Information Does a Director Need?",
}


def main():
    print("=" * 60)
    print("Final Translation Patch")
    print("=" * 60)

    with open(FR_JSON, 'r', encoding='utf-8') as f:
        fr_dict = json.load(f)
    with open(EN_JSON, 'r', encoding='utf-8') as f:
        en_dict = json.load(f)

    patched = 0
    for full_key, en_value in PATCHES.items():
        parts = full_key.split(".", 1)
        if len(parts) != 2:
            continue
        ns, key = parts

        if ns in en_dict and isinstance(en_dict[ns], dict):
            if key in en_dict[ns]:
                fr_val = fr_dict.get(ns, {}).get(key, "")
                en_val = en_dict[ns][key]
                # Only patch if still untranslated (EN == FR)
                if en_val == fr_val or en_val == en_value:
                    en_dict[ns][key] = en_value
                    patched += 1

    with open(EN_JSON, 'w', encoding='utf-8') as f:
        json.dump(en_dict, f, ensure_ascii=False, indent=2)

    # Count remaining
    remaining = 0
    for ns_key, ns_data in fr_dict.items():
        if not ns_key.startswith("page_"):
            continue
        en_ns = en_dict.get(ns_key, {})
        if isinstance(ns_data, dict):
            for k, v in ns_data.items():
                en_v = en_ns.get(k, "")
                if en_v == v and len(v) > 10:
                    remaining += 1

    print(f"\n  Patched: {patched} strings")
    print(f"  Remaining untranslated: {remaining} strings")
    print(f"  Updated: {EN_JSON.relative_to(ROOT)}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
