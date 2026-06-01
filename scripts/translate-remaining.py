#!/usr/bin/env python3
"""
translate-remaining.py — Translate all 314 remaining untranslated strings in en.json.
Direct key→value patches with proper HTML-aware English translations.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_JSON = ROOT / "data" / "translations" / "en.json"

# Direct translations: namespace.key → English value
PATCHES = {
    # page_actualites
    "page_actualites.soiree_hi_team": '<span>Hi-Team Evening</span> <a class="hiteam-logo-link" href="https://t.ly/4o3Tq" rel="noopener" target="_blank"> <img alt="Hi-Team Logo" class="hiteam-logo" onerror="this.style.display=\'none\'" src="images/hiteam-logo.png"/> </a>',
    "page_actualites.guy_le_pechon_sera_lun_des_deux_animateurs_de": "Guy Le Péchon will be one of the two facilitators for the afternoon dedicated to simulations with role-playing exercises for two Board of Directors meetings.",

    # page_administrateur_independant
    "page_administrateur_independant.un_extrait_du_rapport_bouton_concernant_les_c": 'An excerpt from the Bouton Report concerning the criteria for qualifying a director as "independent" is recalled here:',
    "page_administrateur_independant.ni_administrateur_croise": 'Not a "cross-directorship" director.',
    "page_administrateur_independant.ni_administrateur_de_lentreprise_depuis_plus_": "Not a director of the company for more than twelve years.",

    # page_apports_ia_compliance
    "page_apports_ia_compliance.nayant_pas_de_competences_particulieres_sur_l": "Not having particular expertise in AI, I limited myself to writing the foreword that follows.",
    "page_apports_ia_compliance.une_interessante_approche_possible_consiste_a": "An interesting possible approach consists of starting from examples of AI use in a speciality, such as Compliance, an activity normally known to executives.",

    # page_articles_presse
    "page_articles_presse.notre_equipe_travaille_activement_sur_ce_cont": "Our team is actively working on this content to offer you the best possible experience.",

    # page_assises_parite
    "page_assises_parite.forum_de_la_mixite_21_decembre_2012": '<i class="fas fa-calendar text-primary me-2"></i>Gender Diversity Forum - 21 December 2012',
    "page_assises_parite.webinaire_8_mars_2023": '<i class="fas fa-video text-primary me-2"></i>Webinar - 8 March 2023',
    "page_assises_parite.presentation_de_letude": '<i class="fas fa-chart-line text-primary me-2"></i>Presentation of the study',
    "page_assises_parite.au_forum_de_la_mixite_du_21_decembre_2012_guy": 'At the Gender Diversity Forum on 21 December 2012, Guy Le Péchon was one of the speakers in the <strong>Leyders Associates</strong> workshop on the theme:',
    "page_assises_parite.copie_de_lune_des_planches_majeures_projetees": '<strong>Copy of one of the major slides presented</strong>',
    "page_assises_parite.se_positionner_pour_etre_administrable_femini": '"Positioning yourself to be board-ready. Feminising your board."',

    # page_assises_parite_new
    "page_assises_parite_new.programme": '<i class="fas fa-list-alt text-primary me-2"></i>Programme',
    "page_assises_parite_new.participants": "Participants",
    "page_assises_parite_new.de_conferences": "Conferences",
    "page_assises_parite_new.retour_dexperience_sur_les_initiatives_reussi": "Feedback on successful initiatives in professional equality.",
    "page_assises_parite_new.la_parite_dans_les_conseils_dadministration": "Parity in boards of directors",
    "page_assises_parite_new.creer_des_synergies_entre_acteurs": '<i class="fas fa-arrow-right text-primary me-2"></i>Create synergies between stakeholders',
    "page_assises_parite_new.proposer_des_solutions_concretes": '<i class="fas fa-arrow-right text-primary me-2"></i>Propose concrete solutions',
    "page_assises_parite_new.20_entreprises_se_sont_engagees_dans_une_dema": "20 companies have committed to a parity initiative",
    "page_assises_parite_new.les_assises_de_la_parite": "The Parity Conference",

    # page_bibliographie
    "page_bibliographie.articles_interessants_publies_dans_la_presse_": 'Interesting articles published in the press on "Corporate Governance"',
    "page_bibliographie.actions_diverses_de_g_s": '<span style="color: #ff0000;">VARIOUS ACTIONS BY G&amp;S</span>',
    "page_bibliographie.un_extrait_du_rapport_bouton_concernantles_cr": '<span style="color: #000099;"><b>An excerpt from the Bouton Report concerning<br/>the criteria for qualifying<br/>a director as "independent"<br/>is recalled here:</b></span>',
    "page_bibliographie.salon_du_livre_des_polytechniciens": "Polytechnicians\u2019 Book Fair",
    "page_bibliographie.une_liste_dautres_livres_reperes_par_g_scomme": '<span style="color: #000000;">A list of other books identified by G &amp; S<br/>                                                 as interesting for corporate governance can be downloaded here.</span>',

    # page_candidats_mandataires (form fields)
    "page_candidats_mandataires.civilite": "Title *",
    "page_candidats_mandataires.prenom": "First Name",
    "page_candidats_mandataires.adresse_partie_1": "Address Line 1",
    "page_candidats_mandataires.adresse_partie_2": "Address Line 2",
    "page_candidats_mandataires.adresse_partie_3": "Address Line 3",
    "page_candidats_mandataires.code_postal": "Postal Code",
    "page_candidats_mandataires.tel_fixe": "Landline",
    "page_candidats_mandataires.tel_fax": "Fax",
    "page_candidats_mandataires.tel_mobile": "Mobile",
    "page_candidats_mandataires.fonction": "Position",
    "page_candidats_mandataires.organisation": "Organisation",
    "page_candidats_mandataires.fonction_2": "Position",
    "page_candidats_mandataires.organisation_2": "Organisation",
    "page_candidats_mandataires.fonction_3": "Position",
    "page_candidats_mandataires.organisation_3": "Organisation",
    "page_candidats_mandataires.les_elements_figurant_en_bleu_sont_indispensa": "Items shown in blue are mandatory,<br/>the others are desirable.",
    "page_candidats_mandataires.le_formulaire_parait_long_du_seul_fait_que_ce": "The form appears long solely because some sections can be, but are not necessarily, filled in multiple times differently.",
    "page_candidats_mandataires.voirelements_juridiques": 'See <a href="https://www.g-et-s.com/french/legal.htm" rel="noopener" target="_blank">legal elements</a>.',
    "page_candidats_mandataires.en_cliquant_sur_envoyer_votre_client_mail_sou": 'By clicking Send, your email client will open to transmit the message to <strong>contact@g-et-s.com</strong>.',

    # page_candidats_mandataires_sociaux
    "page_candidats_mandataires_sociaux.candidat_e_s_mandatairesadministratrices_admi": "CANDIDATE(S) OFFICERS<br/> FEMALE AND MALE DIRECTORS",
    "page_candidats_mandataires_sociaux.ref_920": "Ref: 920",
    "page_candidats_mandataires_sociaux.a_loccasion_de_ses_nombreuses_missions_il_a_a": "Through his numerous assignments, he has acquired:",
    "page_candidats_mandataires_sociaux.une_experience_internationale_tres_etendue_un": "– Extensive international experience: around thirty countries, across 5 continents, with a predominance for Africa where he also worked 2 years as a cooperation volunteer (Kenya) for the Ministry of Foreign Affairs.",
    "page_candidats_mandataires_sociaux.une_connaissance_de_secteurs_dactivite_tres_v": "– Knowledge of a wide variety of business sectors, in particular: industry, construction, telecommunications, environment, energy, defence, research, insurance, asset management.",
    "page_candidats_mandataires_sociaux.ref_881": '<span style="font-size: small;">Ref: 881</span>',
    "page_candidats_mandataires_sociaux.industries_a_destination_du_btp_securite_fran": '<b><span style="font-size: small;"> Industries serving the construction/security sector (France, Netherlands, Egypt)</span></b>',
    "page_candidats_mandataires_sociaux.ref_871": '<span style="font-size: small;">Ref: 871</span>',
    "page_candidats_mandataires_sociaux.ref_544": '<span style="font-size: small;">Ref: 544</span>',
    "page_candidats_mandataires_sociaux.administrateur_independant_grande_experience_": "<strong>Independent director, extensive audit experience</strong>",
    "page_candidats_mandataires_sociaux.aujourdhui_il_est_administrateur_de_societes_": "Today, he is a director of Luxembourg companies and an internal auditor within regulated Luxembourg financial structures.",
    "page_candidats_mandataires_sociaux.ref_532": '<span style="font-size: small;">Ref: 532</span>',
    "page_candidats_mandataires_sociaux.candidat_a_un_poste_dadministrateur_independa_2": "<b>Candidate for an independent director position,</b> long experience as a CEO of SMEs/Mid-caps including internationally and the Far East",
    "page_candidats_mandataires_sociaux.ref_678": '<span style="font-size: small;">Ref: 678</span>',
    "page_candidats_mandataires_sociaux.ref_503": '<span style="font-size: small;">Ref: 503</span>',
    "page_candidats_mandataires_sociaux.ref_561": '<span style="font-size: small;">Ref: 561</span>',
    "page_candidats_mandataires_sociaux.ref_462": '<span style="font-size: small;">Ref: 462</span>',
    "page_candidats_mandataires_sociaux.ref_261": '<span style="font-size: small;">Ref: 261</span>',
    "page_candidats_mandataires_sociaux.aviation_aeronautique_spatial_defense_securit": '<span style="font-size: small;"><b> </b></span><span style="font-size: small;">.</span><b><span style="font-size: small;">Aviation, Aeronautics, Space, Defence &amp; Security.</span></b>',
    "page_candidats_mandataires_sociaux.ref_513": '<span style="font-size: small;">Ref: 513 </span>',
    "page_candidats_mandataires_sociaux.ref_203": '<span style="color: #000000; font-size: small;">Ref: 203</span>',
    "page_candidats_mandataires_sociaux.ref_508": '<span style="color: #000000; font-size: small;">Ref: 508</span>',
    "page_candidats_mandataires_sociaux.edition_de_logiciel": '<b><span style="font-size: small;"> Software Publishing</span></b>',
    "page_candidats_mandataires_sociaux.ref_909": '<span style="font-size: small;">Ref: 909</span>',
    "page_candidats_mandataires_sociaux.ref_104": '<span style="font-size: small;">Ref: 104</span>',
    "page_candidats_mandataires_sociaux.ref_115": '<span style="font-size: small;">Ref: 115</span>',
    "page_candidats_mandataires_sociaux.ref_845": '<span style="font-size: small;">Ref: 845</span>',
    "page_candidats_mandataires_sociaux.ref_101": '<span style="font-size: small;">Ref: 101 </span>',
    "page_candidats_mandataires_sociaux.ref_402": '<span style="font-size: small;">Ref: 402</span>',
    "page_candidats_mandataires_sociaux.candidate_administratrice_independante_grande": '<span style="font-family: georgia, palatino, serif;"><b>Female candidate for independent director: Extensive international experience</b></span>',
    "page_candidats_mandataires_sociaux.ref_303": '<span style="font-size: small;">Ref: 303</span>',
    "page_candidats_mandataires_sociaux.candidate_au_poste_dadministratrice_independa": '<span style="font-size: small;"><b> </b></span><span style="font-weight: bold;">Candidate for independent director position.</span>',
    "page_candidats_mandataires_sociaux.ref_324": "Ref: 324",
    "page_candidats_mandataires_sociaux.apres_avoir_mene_des_travaux_daudit_chez_erns": '<span style="font-size: small;">After conducting audit work at Ernst &amp; Young, the candidate, over the following 13 years, successively gained experience in managing a business unit, directing an industrial branch, and managing a company. She brings extensive knowledge of governance, compliance, and financial oversight.</span>',
    "page_candidats_mandataires_sociaux.ref_825": '<span style="font-size: small;">Ref: 825 </span>',
    "page_candidats_mandataires_sociaux.ref_304": "Ref: 304",
    "page_candidats_mandataires_sociaux.ref_299": "Ref 299",
    "page_candidats_mandataires_sociaux.ref_302": '<span style="font-size: small;">Ref: 302</span>',
    "page_candidats_mandataires_sociaux.la_candidate_a_un_poste_dadministratrice_inde_2": '<b><span style="font-size: small;"> Female candidate for independent director position. Very broad international experience in business development, Biotechnologies</span></b>',
    "page_candidats_mandataires_sociaux.ref_603": '<span style="font-size: small;">Ref: 603</span>',
    "page_candidats_mandataires_sociaux.candidate_a_un_poste_de_directrice_de_linnova": "<strong>Candidate for Innovation Director position, Knowledge of Boards of Directors</strong>",
    "page_candidats_mandataires_sociaux.langues_etrangeres_anglais_allemand_notions_e": "Foreign languages: English, German – Basic: Spanish, Italian",
    "page_candidats_mandataires_sociaux.ref_756": "Ref:756",
    "page_candidats_mandataires_sociaux.ref_108": '<span style="font-size: small;">Ref: 108</span>',
    "page_candidats_mandataires_sociaux.ref_109": '<span style="font-size: small;">Ref: 109</span>',
    "page_candidats_mandataires_sociaux.ref_754": '<span style="font-size: small;">Ref: 754</span>',
    "page_candidats_mandataires_sociaux.consultante_franco_suisse_experte_en_gouverna": '<b><span style="font-size: small;"> </span></b><strong>Consultant, French-Swiss, expert in family business governance</strong>',
    "page_candidats_mandataires_sociaux.langues_francais_anglais_italien": "Languages: French – English – Italian",
    "page_candidats_mandataires_sociaux.ref_832": '<span style="font-size: small;">Ref: 832</span>',
    "page_candidats_mandataires_sociaux.ref_723": "Ref 723",
    "page_candidats_mandataires_sociaux.administratrice_independante_experimentee_jur": "<strong>Experienced independent female director, Spanish lawyer with extensive European business experience including via Internet</strong>",
    "page_candidats_mandataires_sociaux.ref_762": "Ref 762",
    "page_candidats_mandataires_sociaux.certifications_immobilieres_courantes_avec_ob": '<strong style="font-weight: normal;">Current real estate certifications, with continuing education requirements: </strong> In the USA: MAI (Member of the Appraisal Institute), CRE (Counselors of Real Estate)',
    "page_candidats_mandataires_sociaux.formation_sciences_po_paris_institut_durbanis": "<strong>Education</strong>: Sciences-Po Paris, Paris Institute of Urban Planning, New York University, Certified Director (IFA)",
    "page_candidats_mandataires_sociaux.ref_320": "Ref: 320",
    "page_candidats_mandataires_sociaux.ref_617": "Ref: 617",
    "page_candidats_mandataires_sociaux.ref_754_2": '<span style="font-size: small;">Ref: 754</span>',
    "page_candidats_mandataires_sociaux.administratrice_independante_grande_societe_e": '<b><span style="font-size: small;"> Independent female director, Large European Company</span></b>',
    "page_candidats_mandataires_sociaux.ref_753": '<span style="font-size: small;">Ref: 753 </span>',
    "page_candidats_mandataires_sociaux.actuellement_directeur_grands_comptes_dans_un": '<b><span style="font-size: small;">Currently Key Account Director in a listed international telecommunications company, the candidate is seeking, with her employer\'s agreement, a director position in a Board of Directors.</span></b>',
    "page_candidats_mandataires_sociaux.ref_604": '<span style="font-size: small;">Ref: 604</span>',
    "page_candidats_mandataires_sociaux.ref_632": '<span style="font-size: small;">Ref: 632</span>',
    "page_candidats_mandataires_sociaux.ref_813": '<span style="font-size: small;">Ref: 813</span>',
    "page_candidats_mandataires_sociaux.ref_803": '<span style="font-size: small;">Ref: 803 .</span><b><span style="font-size: small;"> </span> </b>',
    "page_candidats_mandataires_sociaux.candidate_administratrice_independante_experi": '<b><span style="font-size: small;"> Independent director candidate. International experience. Telecoms, Space, R&amp;D Consulting, IT Services. Excellent command of governance issues.</span></b>',
    "page_candidats_mandataires_sociaux.ref_504": '<span style="font-size: small;">Ref: 504</span>',
    "page_candidats_mandataires_sociaux.ref_107": '<span style="font-size: small;">Ref: 107</span>',
    "page_candidats_mandataires_sociaux.formation_doctorat_de_gestion_universite_de_p": '<span style="font-size: small;">Education: Doctorate in Management, University of Paris 1, MBA, Master 2 Coaching, Assas.</span>',
    "page_candidats_mandataires_sociaux.ref_152": '<span style="font-size: small;">Ref: 152</span>',
    "page_candidats_mandataires_sociaux.ref_365": '<span style="font-size: small;">Ref: 365</span>',
    "page_candidats_mandataires_sociaux.femme_ingenieur_supelec_candidate_comme_admin": '<b><span style="font-size: small;">Female Supelec engineer, candidate as independent director</span></b>e',
    "page_candidats_mandataires_sociaux.aujourdhui_elle_travaille_dans_le_domaine_des": "Today, she works in the investment funds sector.",
    "page_candidats_mandataires_sociaux.ref_612": '<span style="font-size: small;">Ref: 612</span>',
    "page_candidats_mandataires_sociaux.ref_512": '<span style="font-size: small;">Ref: 512 </span>',
    "page_candidats_mandataires_sociaux.experience_approfondie_du_domaine_des_ventes_": '<b></b><span style="font-size: small;">Extensive experience in consumer sales including electronic products. As a lawyer, then as legal manager, she is familiar with regulatory issues, compliance, and corporate governance.</span>',
    "page_candidats_mandataires_sociaux.ref_635": '<span style="font-size: small;">Ref: 635</span>',
    "page_candidats_mandataires_sociaux.ref_303_2": '<span style="font-size: small;">Ref: 303</span>',
    "page_candidats_mandataires_sociaux.hommes_candidats": '<span style="color: #ff0000;"><b> <span style="font-size: 14px;">Male Candidates</span></b></span>',
    "page_candidats_mandataires_sociaux.non_executive_director_in_european_companies__2": '<div align="center"> </div> <table align="center" border="0" cellpadding="0" cellspacing="0" width="95%"><tbody><tr><td><b><span style="font-size: small;"> </span></b><strong>Non Executive Director in European companies and family offices with a focus and presence in Asia.</strong></td></tr></tbody></table>',
    "page_candidats_mandataires_sociaux.non_executive_director_in_european_companies__3": '<p><b><span style="font-size: small;"> </span></b><strong>Non Executive Director in European companies and family offices with a focus and presence in Asia.</strong></p>',
    "page_candidats_mandataires_sociaux.mba_insead_certificate_and_diploma_in_company": "MBA INSEAD, Certificate and Diploma in Company Direction from Institute of Directors (IOD London)",

    # page_catalogue_documents
    "page_catalogue_documents.une_fois_les_caracteristiques_fixees_le_docum": 'Once the characteristics are set, the document becomes a generic document such as the "Annual Profit and Loss Statement".',
    "page_catalogue_documents.les_nombres_de_documents_classiques_selon_les": '<strong>The numbers of "standard documents" according to the 5 major areas are:</strong>',
    "page_catalogue_documents.a_partir_de_ce_catalogue_generique_un_catalog": "From this generic catalogue, a customised catalogue for the company in question can easily be developed.",
    "page_catalogue_documents.la_video_de_la_derniere_conference_du_road_sh": 'The video of the last conference from the Chairman\'s "Road-show"',

    # page_certificat_centrale
    "page_certificat_centrale.centrale_supelec_executive_education": "Centrale Supélec Executive Education",

    # page_conseils_numerique
    "page_conseils_numerique.notre_equipe_travaille_activement_sur_ce_cont": "Our team is actively working on this content to offer you the best possible experience.",

    # page_cours_inseec
    "page_cours_inseec.certificat_centrale_supelec": '<i class="fas fa-award text-primary me-2"></i>Centrale Supélec Certificate',
    "page_cours_inseec.cours_inseec_les_instances_de_gouvernance": '<i class="fas fa-university text-primary me-3"></i>                     INSEEC Course - Governance Bodies',

    # page_couverture_harmattan
    "page_couverture_harmattan.notre_equipe_travaille_activement_sur_ce_cont": "Our team is actively working on this content to offer you the best possible experience.",
    "page_couverture_harmattan.couverture_lharmattan": '<i class="fas fa-tools text-primary me-3"></i>                     L\'Harmattan Cover',

    # page_diagnostics_ca
    "page_diagnostics_ca.notre_equipe_travaille_activement_sur_ce_cont": "Our team is actively working on this content to offer you the best possible experience.",
    "page_diagnostics_ca.diagnostics_ca": '<i class="fas fa-tools text-primary me-3"></i>                     Board Assessments',

    # page_directive_europeenne
    "page_directive_europeenne.notre_equipe_travaille_activement_sur_ce_cont": "Our team is actively working on this content to offer you the best possible experience.",
    "page_directive_europeenne.directive_europeenne": '<i class="fas fa-tools text-primary me-3"></i>                     European Directive',

    # page_dsi_conseils_administration
    "page_dsi_conseils_administration.comment_les_dsi_peuvent_impliquer_les_ca": "How CIOs Can Engage Boards of Directors",
    "page_dsi_conseils_administration.comment_les_directeurs_des_systemes_dinformat": "How Chief Information Officers can engage the Boards of Directors of their company",

    # page_entreprise_liberee
    "page_entreprise_liberee.notre_equipe_travaille_activement_sur_ce_cont": "Our team is actively working on this content to offer you the best possible experience.",

    # page_etude_juin_2025
    "page_etude_juin_2025.la_presentation_correspondant_a_la_date_coupe": 'The presentation corresponding to the deadline of the Copé-Zimmerman Law, namely in 2017, 40% of women in Boards of Directors, was the subject of a presentation, <a href="https://www.youtube.com/watch?v=example" rel="noopener" target="_blank">viewable here</a>.',
    "page_etude_juin_2025.la_derniere_etude_pour_juin_2025_a_fait_lobje": 'The latest study for June 2025 was the subject of a short presentation of excerpts at a Hi-Team dinner on 15 October. To watch the video of the speech click <a href="https://www.youtube.com/watch?v=example" rel="noopener" target="_blank">here</a>.',
    "page_etude_juin_2025.ci_dessous_la_planche_majeure_pour_les_comex_": "<strong>Below the key slide for the Comex Codir</strong>",
    "page_etude_juin_2025.lanalyse_detaillee_des_profils_individuels_de": "The detailed analysis of the individual profiles of female directors,",

    # page_facilities_management_normes_europeennes
    "page_facilities_management_normes_europeennes.les_5_normes_europeennes_ont_servi_de_point_d": "The 5 European standards served as the starting point for similar ISO standards.",
    "page_facilities_management_normes_europeennes.pour_incorporation_dans_une_lettre_de_lassoci": "For incorporation in a letter from the XMP Consult association, I wrote an article",
    "page_facilities_management_normes_europeennes.un_beotien_egare_dans_la_fabrication_de_norme": '<strong>"A novice lost in the making of European Standards"</strong>',

    # page_formations_administrateurs
    "page_formations_administrateurs.insead": '<b><span style="color: #0000a0;">INSEAD</span></b>',
    "page_formations_administrateurs.international_directors_program": '<a href="https://www.insead.edu/executive-education/corporate-governance/aspiring-directors-programme?_ref=finder"><span style="color: #000000;">International Directors Program</span></a>',
    "page_formations_administrateurs.executive_educationvision_tres_internationale": '<span style="color: #0000ff;">Executive Education<br/>Highly international vision</span>',
    "page_formations_administrateurs.ifa_cdainstitut_francais_des_administrateurs": '<b><span style="color: #0000a0;">IFA - CDA<br/>French Institute of Directors</span></b>',
    "page_formations_administrateurs.essec": '<b><span style="color: #0000a0;">ESSEC</span></b>',
    "page_formations_administrateurs.women_be_european_board_ready": '<a href="https://www.club-adae.fr/%F0%9F%9A%80-devenez-un-administrateur-qualifie-independant-avec-ladae/"><span style="color: #000000;">Women Be European Board Ready</span></a>',
    "page_formations_administrateurs.reserve_aux_femmes": '<span style="color: #0000ff;">Reserved for women </span>',
    "page_formations_administrateurs.m_lyon_business_schoolcertificat": '<span style="color: #000000;"><b><span style="color: #0000cc;">M LYON BUSINESS SCHOOL</span><span style="color: #0000cc;">Certificate </span></b></span>',
    "page_formations_administrateurs.voir_presentation": '<a href="https://executive.em-lyon.com/Formations/Certificats/OA-Objectif-Administratrice">See presentation</a>',
    "page_formations_administrateurs.institute_of_directors": '<b><span style="color: #0000a0;">Institute Of Directors</span></b>',
    "page_formations_administrateurs.formation_pour_la_certification_commechartere": '<span style="color: #000000;">Training for certification as <a href="http://www.iod.com/Home/Training-and-Development/Chartered-Director/">"Chartered Director"</a>, for experienced directors</span>',
    "page_formations_administrateurs.inseadinternational_directors_programexecutiv_2": '<div align="center"> <p><b><span style="color: #0000a0;">INSEAD</span></b></p> <p align="center"><a href="https://www.insead.edu/executive-education/corporate-governance/aspiring-directors-programme?_ref=finder"><span style="color: #000000;">International Directors Program</span></a></p> <p align="center"><span style="color: #0000ff;">Executive Education<br/>Highly international vision</span></p> </div>',
    "page_formations_administrateurs.essecwomen_be_european_board_readyreserve_aux": '<div align="center"> <p><b><span style="color: #0000a0;">ESSEC</span></b></p> <p align="center"><a href="https://www.club-adae.fr/%F0%9F%9A%80-devenez-un-administrateur-qualifie-independant-avec-ladae/"><span style="color: #000000;">Women Be European Board Ready</span></a></p> <p align="center"><span style="color: #0000ff;">Reserved for women</span></p> </div>',
    "page_formations_administrateurs.m_lyon_business_schoolcertificatvoir_presenta": '<p align="center"><span style="color: #000000;"><b><span style="color: #0000cc;">M LYON BUSINESS SCHOOL</span><span style="color: #0000cc;">Certificate</span></b></span></p> <p align="center"><a href="https://executive.em-lyon.com/Formations/Certificats/OA-Objectif-Administratrice">See presentation</a></p>',
    "page_formations_administrateurs.institute_of_directorsformation_pour_la_certi": '<div align="center"> <p><b><span style="color: #0000a0;">Institute Of Directors</span></b></p> <p align="center"><span style="color: #000000;">Training for certification as <a href="http://www.iod.com/Home/Training-and-Development/Chartered-Director/">"Chartered Director"</a>, for experienced directors</span></p> </div>',

    # page_generalites_corporate_governance
    "page_generalites_corporate_governance.notre_equipe_travaille_activement_sur_ce_cont": "Our team is actively working on this content to offer you the best possible experience.",

    # page_glossaire_prestations
    "page_glossaire_prestations.tant_un_conseil_dadministration_que_des_manag": "Both a board of directors and executive managers may need to use consulting services.",
    "page_glossaire_prestations.images_generees_par_intelligence_artificielle": "Images generated by Artificial Intelligence",

    # page_historique
    "page_historique.contacts_info_g_et_s_com": '<strong>Contacts:</strong> <a href="mailto:info@g-et-s.com" style="color: #1e73be;">info@g-et-s.com</a>',
    "page_historique.tel_06_16_31_07_15": "<strong>Phone:</strong> 06 16 31 07 15",
    "page_historique.le_petit_dejeuner_organise_debut_juillet_2009": '<span style="color: #0033cc;">The breakfast event organised in early July 2009</span>',
    "page_historique.par": '<span style="color: #0033cc;"><br/>by</span>',
    "page_historique.la_place_des_femmes_administrateurs_dans_les_": '<br/><b><span style="color: #000066;">"The place of women directors in French listed companies"</span></b>',
    "page_historique.a_rassemble_plus_dune_soixantaine_de_particip": "<br/>brought together more than sixty participants",
    "page_historique.le_theme_a_ete_introduit_par_guy_le_pechon_as": "The theme was introduced by Guy Le Péchon, Associate/Managing Partner of",

    # page_ia_compliance
    "page_ia_compliance.notre_equipe_travaille_activement_sur_ce_cont": "Our team is actively working on this content to offer you the best possible experience.",

    # page_information_administrateurs
    "page_information_administrateurs.notre_equipe_travaille_activement_sur_ce_cont": "Our team is actively working on this content to offer you the best possible experience.",
    "page_information_administrateurs.linformation_des_administrateurs": '<i class="fas fa-tools text-primary me-3"></i>                     Directors\' Information',

    # page_informatique
    "page_informatique.codages": '<i class="fas fa-code me-2" style="color: #1e73be;"></i>Coding',
    "page_informatique.cybersecurite_avec_un_hacker_reconverti": '<i class="fas fa-shield-alt me-2" style="color: #1e73be;"></i>Cybersecurity with a Reformed Hacker',
    "page_informatique.cloud_visite_guidee_gros_data_center": '<i class="fas fa-cloud me-2" style="color: #1e73be;"></i>"Cloud" Guided Tour of a Large Data Centre',
    "page_informatique.gestion_des_documents_pour_conseils": '<i class="fas fa-folder-open me-2" style="color: #1e73be;"></i>Document Management for Boards',
    "page_informatique.big_data_interfaces_avec_si_classiques": '<i class="fas fa-exchange-alt me-2" style="color: #1e73be;"></i>Big Data Interfaces with Traditional IT Systems',
    "page_informatique.reglement_europeen_sur_les_donnees_personnell": '<i class="fas fa-user-shield me-2" style="color: #1e73be;"></i>European Regulation on Personal Data',
    "page_informatique.realite_virtuelle": '<i class="fas fa-vr-cardboard me-2" style="color: #1e73be;"></i>Virtual Reality',
    "page_informatique.blockchain": '<i class="fas fa-link me-2" style="color: #1e73be;"></i>Blockchain',
    "page_informatique.mooc": '<i class="fas fa-graduation-cap me-2" style="color: #1e73be;"></i>MOOC',
    "page_informatique.salle_de_gestion_de_crise": '<i class="fas fa-exclamation-triangle me-2" style="color: #1e73be;"></i>Crisis Management Room',

    # page_intelligence_collective
    "page_intelligence_collective.impliquer_le_conseil_dadministration_dans_la_": '"<strong>Engaging the Board of Directors in the digital transformation of its company. Why? How</strong>"',
    "page_intelligence_collective.la_video_de_mon_intervention_que_je_crois_ass": '<i class="fas fa-video text-primary me-2"></i>The video of my presentation (which I believe is quite original) is available on the page:',
    "page_intelligence_collective.voir_la_video_sur_youtube": '<a class="btn btn-outline-primary" href="https://www.youtube.com/watch?v=SDEhRSL2KWg" rel="noopener" target="_blank"> <i class="fab fa-youtube me-2"></i>Watch the video on YouTube',
    "page_intelligence_collective.jai_aussi_un_pdf_du_texte_transparents_pour_c": '<i class="fas fa-file-pdf text-danger me-2"></i>I also have a .pdf of the text + slides for those who would like it by emailing me:                     <a href="mailto:guy.le-pechon@g-et-s.com">guy.le-pechon@g-et-s.com</a>',
    "page_intelligence_collective.intelligence_collective": '<i class="fas fa-brain text-primary me-3"></i>                     Collective Intelligence',

    # page_livre_eti
    "page_livre_eti.salon_du_livre_des_polytechniciens": "Polytechnicians' Book Fair",
    "page_livre_eti.presentation_video_du_livre": '<i class="fas fa-video me-2"></i>                     Video Presentation of the Book',
    "page_livre_eti.dedicaces": '<i class="fas fa-calendar-alt me-2"></i>                     Book Signings',
    "page_livre_eti.creation_de_valeur_des_conseils_des_eti_confr": "<strong>Value Creation by Mid-Cap Boards Facing Major Global Changes</strong>",
    "page_livre_eti.editeur_lharmattan_collection_advalorem": "<strong>Publisher:</strong> L'Harmattan, AdValorem collection",
    "page_livre_eti.une_video_danimation_de_5_minutes_resume_le_c": "A 5-minute animated video summarises the content of the book.",
    "page_livre_eti.cliquez_sur_la_vignette_pour_visionner_la_vid": "<em>Click on the thumbnail to watch the video</em>",
    "page_livre_eti.date_15_novembre_2025_de_maniere_similaire_au": "<strong>Date:</strong> 15 November 2025, similarly to 25 November 2023",

    # page_livre_eti_new
    "page_livre_eti_new.salon_du_livre_des_polytechniciens": '<i class="fas fa-book-open text-primary me-2"></i>Polytechnicians\' Book Fair',
    "page_livre_eti_new.sceaux_smart": '<i class="fas fa-lightbulb text-primary me-2"></i>Sceaux-Smart',
    "page_livre_eti_new.a_propos_du_livre": '<i class="fas fa-book text-primary me-2"></i>About the Book',
    "page_livre_eti_new.presentation_video_du_livre": '<i class="fas fa-video text-primary me-2"></i>Video Presentation of the Book',
    "page_livre_eti_new.creation_de_valeur_des_conseils_des_eti_confr": "Value Creation by Mid-Cap Boards Facing Major Global Changes",
    "page_livre_eti_new.editeur_lharmattan_collection_advalorem": '<strong><i class="fas fa-building me-2"></i>Publisher:</strong> L\'Harmattan, AdValorem collection',
    "page_livre_eti_new.ou_se_procurer_le_livre_lharmattan_collection": '<strong><i class="fas fa-shopping-cart me-2"></i>Where to get the book:</strong><br/> <a class="btn btn-outline-warning btn-sm mt-2" href="http://www.editions-harmattan.fr/index.asp?navig=catalogue" rel="noopener" target="_blank">L\'Harmattan</a>',
    "page_livre_eti_new.une_video_danimation_de_5_minutes_resume_le_c": "A 5-minute animated video summarises the content of the book:",
    "page_livre_eti_new.cliquez_sur_la_vignette_pour_visionner_la_vid": "<em>Click on the thumbnail to watch the video</em>",
    "page_livre_eti_new.date_25_novembre": "<strong>Date:</strong> 25 November",
    "page_livre_eti_new.petit_dejeuner_avec_presentation_du_chapitre_": 'Breakfast with presentation of the "Collective Intelligence" chapter',

    # page_livre_gouvernance_ca
    "page_livre_gouvernance_ca.notre_equipe_travaille_activement_sur_ce_cont": "Our team is actively working on this content to offer you the best possible experience.",
    "page_livre_gouvernance_ca.livre_gouvernance_ca": '<i class="fas fa-tools text-primary me-3"></i>                     Book: Board Governance',

    # page_loi_rixain
    "page_loi_rixain.presentation_de_la_loi": '<i class="fas fa-gavel text-primary me-2"></i>Presentation of the Law',
    "page_loi_rixain.mesures_cles_de_lensemble_de_la_loi": '<i class="fas fa-bullseye text-primary me-2"></i>Key Measures of the Law',
    "page_loi_rixain.date_dadoption_24_decembre_2021": "<strong>Date of adoption:</strong> 24 December 2021",
    "page_loi_rixain.entreprises_concernees_par_les_nouvelles_obli": "Companies concerned by the new obligations",
    "page_loi_rixain.echeance_pour_la_mise_en_conformite": "Deadline for compliance",
    "page_loi_rixain.chiffres_du_ministere_du_travail": '<a href="../docs/ministere-travail-chiffres.pdf" rel="noopener" target="_blank"><i class="fas fa-file-pdf me-1"></i>Figures from the Ministry of Labour</a>',
    "page_loi_rixain.obligation_datteindre_40_dans_ces_deux_groupe": "Obligation to reach 40% in these two groups of executives.",
    "page_loi_rixain.mise_en_place_de_programmes_de_formation_sur_": "Implementation of training programmes on professional equality.",
    "page_loi_rixain.entree_en_vigueur_des_premieres_dispositions": "Entry into force of the first provisions",
    "page_loi_rixain.echeance_finale_pour_la_parite_dans_les_insta": "Final deadline for parity in governing bodies",
    "page_loi_rixain.cette_loi_marque_une_evolution_majeure_dans_l": "This law marks a major development in the governance of French companies:",
    "page_loi_rixain.evaluation_de_votre_situation_actuelle_au_reg": "Assessment of your current situation with regard to the requirements of the Rixain Law.",
    "page_loi_rixain.elaboration_dune_strategie_sur_mesure_pour_at": "Development of a tailored strategy to achieve parity objectives.",
    "page_loi_rixain.diagnostic_de_conformite": '<i class="fas fa-search text-success me-2"></i>Compliance Assessment',

    # page_loi_rixain_new
    "page_loi_rixain_new.presentation_de_la_loi": '<i class="fas fa-gavel text-primary me-2"></i>Presentation of the Law',
    "page_loi_rixain_new.mesures_cles_de_la_loi": '<i class="fas fa-bullseye text-primary me-2"></i>Key Measures of the Law',
    "page_loi_rixain_new.date_dadoption_24_decembre_2021": "<strong>Date of adoption:</strong> 24 December 2021",
    "page_loi_rixain_new.entreprises_concernees_par_les_nouvelles_obli": "Companies concerned by the new obligations",
    "page_loi_rixain_new.echeance_pour_la_mise_en_conformite": "Deadline for compliance",
    "page_loi_rixain_new.mise_en_place_de_programmes_de_formation_sur_": "Implementation of training programmes on professional equality.",
    "page_loi_rixain_new.entree_en_vigueur_des_premieres_dispositions": "Entry into force of the first provisions",
    "page_loi_rixain_new.echeance_finale_pour_la_parite_dans_les_insta": "Final deadline for parity in governing bodies",
    "page_loi_rixain_new.cette_loi_marque_une_evolution_majeure_dans_l": "This law marks a major development in the governance of French companies:",
    "page_loi_rixain_new.evaluation_de_votre_situation_actuelle_au_reg": "Assessment of your current situation with regard to the requirements of the Rixain Law.",
    "page_loi_rixain_new.elaboration_dune_strategie_sur_mesure_pour_at": "Development of a tailored strategy to achieve parity objectives.",
    "page_loi_rixain_new.parite_dans_les_instances_dirigeantes": '<i class="fas fa-users text-success me-2"></i>Parity in Governing Bodies',
    "page_loi_rixain_new.diagnostic_de_conformite": '<i class="fas fa-search text-success me-2"></i>Compliance Assessment',

    # page_mentions_legales
    "page_mentions_legales.danscette_page_gouvernance_structures_precise": '<span style="color: #000099;">In</span> <b><span style="color: #000099;">this page, Gouvernance &amp; Structures specifies the legal elements relating to its website</span></b>',
    "page_mentions_legales.lirele_texte_detaille": 'Read <a href="documents/2022-07-11-texte-RDGP-final-pour-site-G-S.pdf" target="_blank">the detailed text</a>',
    "page_mentions_legales.copyright": "<b>Copyright</b>",
    "page_mentions_legales.cookies": '<b>"Cookies"</b>',
    "page_mentions_legales.mentions_legales": '<i class="fas fa-gavel me-3"></i>Legal Notice',

    # page_missions_conseil
    "page_missions_conseil.notre_equipe_travaille_activement_sur_ce_cont": "Our team is actively working on this content to offer you the best possible experience.",
    "page_missions_conseil.missions_conseil": '<i class="fas fa-tools text-primary me-3"></i>                     Consulting Assignments',

    # page_monde_numerique
    "page_monde_numerique.notre_equipe_travaille_activement_sur_ce_cont": "Our team is actively working on this content to offer you the best possible experience.",

    # page_monde_numerique_relation_client
    "page_monde_numerique_relation_client.cette_video_insiste_sur_les_nouveautes_induit": 'This video emphasises the innovations brought about in the customer relationship by making customer data available on the Web outside of information systems known as "Legacy".',

    # page_observatoire_genres
    "page_observatoire_genres.notre_equipe_travaille_activement_sur_ce_cont": "Our team is actively working on this content to offer you the best possible experience.",

    # page_organisation_gs
    "page_organisation_gs.enquete_pour_des_benchmarkings": 'Survey for "benchmarkings"',

    # page_ouvrage_collectif_ca
    "page_ouvrage_collectif_ca.notre_equipe_travaille_activement_sur_ce_cont": "Our team is actively working on this content to offer you the best possible experience.",

    # page_plan_du_site
    "page_plan_du_site.pour_mandataires": "For Officers",
    "page_plan_du_site.pour_societes": "For Companies",
    "page_plan_du_site.informations_legales": '<i class="fas fa-gavel me-2"></i>Legal Information',
    "page_plan_du_site.page_daccueil": '<a href="index.html">Home Page</a>',
    "page_plan_du_site.formation_aux_comex_codir": '<a href="pages/certificat-centrale.html">COMEX/CODIR Training</a>',
    "page_plan_du_site.formations_au_c_a": '<a href="pages/formations-administrateurs.html">Board Training</a>',
    "page_plan_du_site.bibliographie": '<a href="pages/bibliographie.html">Bibliography</a>',
    "page_plan_du_site.etudes_g_s_2010_a_2025": '<a href="pages/etude-juin-2025.html">G &amp; S Studies 2010 to 2025</a>',
    "page_plan_du_site.article_presse": '<a href="la-presse-parle-de-gouvernance-structures/index.html">Press Articles</a>',
    "page_plan_du_site.introduction": '<a href="pages/organisation-gs.html">Introduction</a>',
    "page_plan_du_site.contact": '<a href="contact.html">Contact</a>',
    "page_plan_du_site.diagnostics": '<a href="pages/diagnostics-ca.html">Assessments</a>',
    "page_plan_du_site.mentions_legales_confidentialite": '<a href="mentions-legales.html">Legal Notice - Privacy</a>',
    "page_plan_du_site.plan_du_site": '<a href="plan-du-site.html">Sitemap</a>',
    "page_plan_du_site.contributions_de_guy_le_pechon": "Contributions by Guy Le Péchon",
    "page_plan_du_site.documents_utiles": "Useful Documents",
    "page_plan_du_site.contributions_de_guy_le_pechon_2": "Contributions by Guy Le Péchon",
    "page_plan_du_site.documents_utiles_2": "Useful Documents",
    "page_plan_du_site.plan_du_site_2": '<i class="fas fa-sitemap me-3"></i>Sitemap',

    # page_plateforme_formation
    "page_plateforme_formation.notre_equipe_travaille_activement_sur_ce_cont": "Our team is actively working on this content to offer you the best possible experience.",
    "page_plateforme_formation.plateforme_de_formation": '<i class="fas fa-tools text-primary me-3"></i>                     Training Platform',

    # page_questionnaire_rixain_societes
    "page_questionnaire_rixain_societes.a_titre_dexemple_voici_deux_premieres_questio": "As an example, here are the first two questions from the questionnaire:",
    "page_questionnaire_rixain_societes.malheureusement_tres_peu_dentreprise_ont_repo": "Unfortunately, very few companies responded to this questionnaire.",
    "page_questionnaire_rixain_societes.quel_est_le_nom_de_linstance_dirigeante_majeu": "<strong>What is the NAME of the main governing body of your company? *</strong>",
    "page_questionnaire_rixain_societes.envisagez_vous_une_evolution_du_nombre_de_mem": '<strong>Do you envisage a change in the number of members of this governing body? *</strong><br/> <em>Only one answer possible.</em>',
    "page_questionnaire_rixain_societes.contactez_nous_avec_vos_coordonnees_pour_rece": "Contact us with your details to receive the full questionnaire in PDF format:",
    "page_questionnaire_rixain_societes.stable": "○ Stable",

    # page_recherche_administrateur
    "page_recherche_administrateur.notre_equipe_travaille_activement_sur_ce_cont": "Our team is actively working on this content to offer you the best possible experience.",
    "page_recherche_administrateur.recherche_administrateur": '<i class="fas fa-tools text-primary me-3"></i>                     Director Search',

    # page_salarie_dirigeants_confiance
    "page_salarie_dirigeants_confiance.preface": "Preface",
    "page_salarie_dirigeants_confiance.en_tant_que_membre_du_comite_scientifique_de_": "As a member of the Scientific Committee of the Ad Valorem collection by L'Harmattan publishers, I was asked to write the preface for the book being written, \"The Liberated Company\".",
    "page_salarie_dirigeants_confiance.lorsque_a_la_demande_de_valerie_lejeune_direc": "When, at the request of Valérie Lejeune, Director of the Ad Valorem collection, I began reading the book, I was somewhat disconcerted to read a kind of autobiography of the author describing his career as an operational manager.",
    "page_salarie_dirigeants_confiance.lhypothese_sous_jacente_est_que_les_motivatio": "The underlying hypothesis is that people's motivations are considered to be at a high level in the classic Maslow diagram, a diagram that the author discusses in depth. The author considers that the company should create conditions for personal fulfilment.",

    # page_shadow_conseil
    "page_shadow_conseil.une_approche_innovante_le_conseil_dadministra": "An innovative approach: The Youth Board of Directors",
    "page_shadow_conseil.quelle_societe_sera_la_premiere_a_la_tenter": "Which company will be the first to try it?",
    "page_shadow_conseil.par_manque_de_connaissance_de_la_realite_pour": "Through lack of knowledge of reality, for the general public a Board of Directors is still often imagined as a group of people of a certain age.",
    "page_shadow_conseil.ce_nest_pas_tout_a_fait_vrai_mais_il_nempeche": "This is not entirely true, but the fact remains that even by simple common sense, the contribution of new ideas from younger generations would surely be an asset.",
    "page_shadow_conseil.lentreprise_pourrait_incidemment_dans_ce_cadr": "The company could incidentally, in this context, identify young talents to recruit later.",
    "page_shadow_conseil.la_societe_pourrait_utiliser_de_cette_approch": "The company could use this approach to improve its brand image, particularly among young people.",

    # page_soiree_lancement
    "page_soiree_lancement.notre_equipe_travaille_activement_sur_ce_cont": "Our team is actively working on this content to offer you the best possible experience.",

    # page_travaux_ifa_digital
    "page_travaux_ifa_digital.de_quelles_informations_ladministrateur_a_t_i": '<i class="fas fa-info-circle me-2"></i>                     What Information Does a Director Need',
    "page_travaux_ifa_digital.sous_la_houlette_du_president_de_lifa_daniel_": "Under the leadership of the IFA Chairman, Daniel Lebègue, I was able to actively participate in 2 successive working groups that produced 2 reports whose content was advanced for the time.",
    "page_travaux_ifa_digital.le_point_de_depart_du_groupe_de_travail_a_ete": "The starting point of the working group was to address the risks involved, but it became apparent as work progressed that it was important to highlight the positive stakes for the company of this digital transformation.",

    # page_video_glp_vl
    "page_video_glp_vl.notre_equipe_travaille_activement_sur_ce_cont": "Our team is actively working on this content to offer you the best possible experience.",
    "page_video_glp_vl.video_glp_vl": '<i class="fas fa-tools text-primary me-3"></i>                     Video GLP VL',

    # page_webinaires_passes
    "page_webinaires_passes.notre_equipe_travaille_activement_sur_ce_cont": "Our team is actively working on this content to offer you the best possible experience.",
}

# Handle bibliographie entries that need HTML preserved but have complex link structures
# These are mostly link entries - keep them as-is since they're press article titles
BIBLIO_KEEP_AS_IS = [
    "page_bibliographie.harvard_business_review_france_11_12_2014_la_",
    "page_bibliographie.la_tribune_5_9_12_bientot_des_quotas_de_femme",
    "page_bibliographie.financial_times_electroniceveryone_benefits_o",
    "page_bibliographie.lexpress8_septembre_2010valerie_liongouvernan",
    "page_bibliographie.challengesdes_quotas_pour_etablir_legalite11_",
    "page_bibliographie.le_gouvernement_veut_feminiser_lencadrement_d",
    "page_bibliographie.jean_francois_cope_sengage_pour_legalite_homm",
    "page_bibliographie.lobservatoire_de_la_gouvernance_altedia_la_tr",
    "page_bibliographie.au_cours_de_la_reunion_du_27_novembre_2016de1_2",
    "page_bibliographie.le_16_decembre_2011participation_de_g_s_a_lat",
    "page_bibliographie.blogs_lies_a_la_gouvernancearcafi_notesfinanc",
    "page_bibliographie.actions_diverses_de_g_squelques_unes_des_inte",
]


def main():
    with open(EN_JSON, 'r', encoding='utf-8') as f:
        en = json.load(f)

    patched = 0
    for full_key, en_val in PATCHES.items():
        ns, key = full_key.split('.', 1)
        if ns not in en:
            en[ns] = {}
        if not isinstance(en[ns], dict):
            continue
        en[ns][key] = en_val
        patched += 1

    with open(EN_JSON, 'w', encoding='utf-8') as f:
        json.dump(en, f, ensure_ascii=False, indent=2)

    print(f"Patched {patched} translations in en.json")

    # Verify remaining untranslated
    with open(ROOT / "data" / "translations" / "fr.json", 'r', encoding='utf-8') as f:
        fr = json.load(f)

    still = 0
    for ns in sorted(fr.keys()):
        if not ns.startswith('page_'):
            continue
        fr_ns = fr.get(ns, {})
        en_ns = en.get(ns, {})
        if not isinstance(fr_ns, dict):
            continue
        for k, v in fr_ns.items():
            en_v = en_ns.get(k, '')
            if en_v == v and len(v) > 5:
                full = f"{ns}.{k}"
                if full not in BIBLIO_KEEP_AS_IS:
                    still += 1
                    print(f"  Still untranslated: {full}")

    print(f"\nRemaining untranslated: {still}")


if __name__ == "__main__":
    main()
