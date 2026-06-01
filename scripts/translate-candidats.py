#!/usr/bin/env python3
"""Translate all remaining French strings in page_candidats_mandataires_sociaux."""
import json

TRANSLATIONS = {
    "aujourdhui_des_conseils_dadministration_peuve":
        "Today, Boards of Directors may need to recruit women and men qualified to co-opt as directors.",
    "gouvernance_structures_connait_deja_un_certai":
        "Gouvernance &amp; Structures already knows a number of candidates. Their anonymous mini CVs are listed below.",
    "pour_connaitre_leur_nom_et_leurs_coordonnees_":
        'To find out their names and contact details and to reach them, write to <a href="mailto:contact@g-et-s.com">contact@g-et-s.com</a> specifying the reference indicated.',
    "le_candidat_x_ensta_actuellement_expert_indep":
        "<strong>The candidate, X-Ensta, currently independent expert in mergers &amp; acquisitions, has 35 years of experience in balance sheet operations, including twenty years in energy and raw materials.</strong>",
    "apres_un_debut_de_carriere_dans_le_nucleaire_":
        "After starting his career in the nuclear sector, he was in charge of distressed businesses at the Ministry of Industry and at the Treasury. He was then responsible for 6 years for a significant multinational oil holding, then for 4 years was Deputy CEO of a major portfolio management structure, before joining one of the world leaders in nuclear energy to carry out restructuring of investments and activities, balance sheet operations, and strategic reflections.",
    "il_a_ete_administrateur_dun_grand_groupe_mini":
        "He has served as director of a major mining group and of a holding company, and until recently Chairman of the Supervisory Board of a company in which the BPI holds a stake.",
    "il_est_depuis_plusieurs_annees_expert_industr":
        "He has for several years been an industry-energy expert at a mergers and acquisitions firm.",
    "administrateur_independant_membre_du_comite_d":
        "<strong> Independent director, member of the Audit Committee, expert in risk management, digital transformation and cybersecurity</strong>",
    "aujourdhui_senior_manager_dans_un_cabinet_de_":
        "Today, Senior Manager at a consulting firm dealing with risk management, fraud and corruption. Looking back, in a regulated context (Solvency 2), he served as Director and Chairman of the Audit Committee of a Prévoyance company whose sale he led. In an industrial CAC40 company, he led a shared service center, was internal auditor and project manager for a merger and acquisition operation. Within a major American company, and previously, in a major French telecom group, he served as internal auditor.",
    "une_profonde_expertise_en_systeme_dinformatio":
        "– Deep expertise in information systems and digital transformation,",
    "diplome_de_lessec_et_de_telecom_paris_anglais":
        "Graduate of ESSEC and Télécom Paris, fluent English, Member of the IFA Audit Committee. Ref 732",
    "le_candidat_ingenieur_et_science_po_a_dans_le":
        '<span style="font-size: small;">The candidate, engineer and Science-Po, has in the above-mentioned countries and sectors experience as Chairman and director</span>',
    "candidat_a_un_poste_dadministrateur_independa":
        "<strong> Candidate for an independent director position. Long and broad experience as General Manager of an industrial family SME. European and Asian subsidiaries. Director of companies in the service sector</strong>",
    "ingenieur_43_ans_de_carriere_industrielle_don":
        "Engineer, 43 years of industrial career, including 13 in production, then 30 as General Manager and Chairman of an industrial family SME (turnover €40M), mechanical and metallurgy sector.",
    "creation_et_presidence_de_filiales_en_europe_":
        "Creation and Chairmanship of subsidiaries in Europe, China and India. Development of international alliances and networks. Strong commercial and managerial experience in Europe, the Middle East and Asia.",
    "23_ans_president_de_conseil_de_surveillance_e":
        "23 years Chairman of Supervisory Board as independent director of two service sector companies: publishing &amp; multimedia (€2M), catering &amp; seminars (€5M).",
    "experience_en_evaluation_acquisition_et_integ":
        "Experience in company valuation, acquisition and integration, and issues of governance, succession, and ownership transfers.",
    "connaissance_de_lenseignement_superieur_10_an":
        "Knowledge of Higher Education: 10 years as Chairman of an Advisory Board. English and German.",
    "le_candidat_ingenieur_commercial_dhec_liege_a":
        "The candidate, HEC Liège commercial engineer, worked for 25 years as Statutory Auditor and Chartered Accountant in Belgium and in the Grand Duchy of Luxembourg.",
    "certifie_comme_administrateur_de_societes_ifa":
        "Certified as Company Director (IFA/SC.PO) and in risk management strategy CEFAR/AMRAE. Member of the French and Luxembourg Institutes of Directors.",
    "fort_de_son_experience_internationale_au_sein":
        "Drawing on his international experience within Anglo-Saxon audit firms for commercial, industrial and financial companies (of intermediate size), he became an entrepreneur by creating and developing his own chartered accountancy, company domiciliation and audit firms (affiliated with an international network, Kreston).",
    "son_parcours_professionnel_lui_a_fait_connait":
        "His professional career has exposed him to very diverse sectors including construction and wealth management, structures of various sizes, with challenges and business models at various stages of development. He has participated in numerous restructuring assignments both in France and in Luxembourg.",
    "de_par_sa_nationalite_italienne_et_son_parcou":
        "By virtue of his Italian nationality and his European career, he has an in-depth knowledge of French, Italian and English cultures and has mastered the associated languages.",
    "25_ans_de_direction_generale_de_pme_eti_indus":
        "– 25 years of Senior Management of industrial SME/ETI of 10/50/120 million € in revenue, multi-site and multi-country – Industrial sectors: composite materials, aerospace coatings, printing, plastic packaging, wood processing, equipment parts for industry and the oil and gas sector. – Types of shareholdings: listed French and foreign groups, family groups, companies under LBO. – Experience in development, management, restructuring, insolvency proceedings, LBO takeovers and external growth. <span style=\"font-size: smaller;\">– Worked in Europe, India, Iran, China, South Africa. Knowledge of major export markets where industrial subsidiaries were established.</span> – Member IFA, APIA – UTC Engineer, Master of Sciences from Cranfield Institute of Technology, MBA from HEC Group – Fluent English",
    "candidat_a_un_poste_dadministrateur_independa_3":
        "<b>Candidate for an independent director position (Audit or Remuneration Committee). Extensive experience in Finance and Operational Management across several sectors.</b>",
    "dote_dune_triple_formation_mba_americain_inge":
        "With a triple background (American MBA, Engineer, Economics), the candidate for an independent director position, after serving as junior consultant in two renowned firms, pursued his career in French subsidiaries of two major international groups, one American then the other German. For the latter, he also worked within the parent company in Germany. He has rich experience of more than 20 years in extensive Finance Departments (finance, accounting, taxation, legal and IT) in international environments. In this capacity, he has participated, both in France and abroad, in numerous merger and acquisition operations and has served on more than ten supervisory or administrative boards of subsidiaries of the mentioned groups. The originality of his career lies in the fact that he has also been an operational CEO, notably in several successful turnaround operations of companies belonging to different sectors. The economic sectors where he could apply his experience notably include chemicals, pharmaceuticals, agri-food, flavours and fragrances as well as real estate. Trilingual French/English/German",
    "le_candidat_docteur_en_pharmacie_aihp_a_une_e":
        '<span style="font-size: small;">The candidate, Doctor of Pharmacy, AIHP, has experience in hospital research and R&amp;D Management positions in pharmaceutical companies including one of large scale with subsidiaries in the USA.</span>',
    "createur_dune_start_up_de_conseil_en_strategi":
        '<span style="font-size: small;">Founder of a start-up for pharmaceutical R&amp;D strategy consulting and co-founder of another in the design of new antiviral drugs.</span>',
    "le_candidat_de_formation_x_et_supaero_ensae_c":
        '<span style="color: #000000; font-size: small;">The candidate, trained at the École Polytechnique and Sup\'Aéro (ENSAé), with additional Strategic Management training (IFG-ICG), has held senior positions within the Defence Procurement Directorate of the Ministry of Defence. With extensive experience in defence electronics, he is one of the few senior officials mastering the French and European defence sector in the field of high technologies. Holder of the company director certificate (IFA)</span>.',
    "le_candidat_ingenieur_mba_bilingue_francais_a":
        '<span style="font-size: small;">The candidate, Engineer + MBA, bilingual French/English, has highly advanced experience: – of Asia/Pacific with 7 years of residence in Japan and the chairmanship of companies both in Japan and in China, Korea, Taiwan, Thailand, India, Australia. – Of Europe and the Commonwealth with 6 years of residence in London where director positions in these regions were added to those already held in Asia.</span>',
    "le_candidat_de_formation_economique_commerce_":
        '<span style="font-size: small;">The candidate, trained in Economics &amp; International Trade (London and Paris) complemented by Management (INSEAD) and Defence (IHEDN), has extensive international experience through the World Bank (Americas and Asia) then the French, European and American Aerospace/Space/Defence/Security industry for which he has held very senior operational and "Corporate" positions.</span><span style="font-size: small;"> He splits his residence between Washington and Paris and is particularly active in the indicated sectors across Europe, the Americas and the Middle East.</span>',
    "administrateur_de_filiales_anglaises_de_socie":
        '<b><span style="font-size: small;"> Director of English subsidiaries of French companies and vice versa</span></b>',
    "le_candidat_a_30_ans_dexperience_dans_quelque":
        '<span style="color: #000000; font-size: small;">The candidate has 30 years of experience in some of the largest companies in the United Kingdom, Germany, the United States and the Netherlands. A financier by training, accustomed to headquarters issues as well as operational ones, his expertise covers companies as varied as marine, chemicals, sustainable development and real estate. Of English origin, but long established in France, in Paris and in the Rhine region, he would be happy to build bridges between French subsidiaries and their British/German parent companies or vice versa.</span>',
    "le_candidat_de_formation_x_et_insead_a_une_la":
        '<span style="font-size: small;"><b>The candidate, trained at the École Polytechnique and INSEAD, has extensive experience in infrastructure, planning, construction, environment, sustainable development, engineering, public services, concessions and public-private partnerships.</b> In these sectors, he has held operational management positions including on major international construction sites (Algeria, China). He has served as director within highly diverse Boards of Directors and Supervisory Boards, and was CEO of a subsidiary of one of the leaders in engineering and consulting. He has recently created his own consulting firm in order to make his experience available to companies in these sectors, notably through independent director mandates.</span>',
    "le_candidat_expert_comptable_a_une_large_expe":
        '<span style="font-size: small;">The candidate, Chartered Accountant, has extensive experience in financial management, general secretariat and as director of </span><span style="font-size: small;">IT service companies and software publishers</span>',
    "apres_avoir_ete_aux_usa_manager_de_projets_ma":
        '<span style="font-size: small;">After serving in the USA as marketing project manager for a subsidiary of a major US pharmaceutical company, then for 4 years as International Marketing Director of a US company in Medical Engineering, he founded in France a start-up for medical assessments. He was CEO and led a successful development. The company operated in Europe and the USA, listed on Euronext. Extensive experience in high-level contacts and technology transfers (USA and Europe) with scientific and financial circles. Education: Master in Management from ISG</span>',
    "le_candidat_veterinaire_avec_une_formation_de":
        '<span style="font-size: small;">The candidate, a veterinarian with management training acquired at ESSEC, is an experienced executive in large groups, particularly American ones, both as operational (MD or Business Unit) and functional (Marketing) within subsidiaries marketing products for animal or human health (OTC). Experience as director of the Veterinary Medicine Industry Association. Knowledge of Russian.</span>',
    "equipements_pour_l_energie_le_petrole_et_le_g":
        '<span style="font-size: small;"><b>Equipment for energy, oil and gas</b></span>',
    "le_candidat_ingenieur_et_mba_hec_isa_a_une_ex":
        '<span style="font-size: small;">The candidate, engineer and MBA HEC-ISA, has experience as director in several companies in the above-mentioned sector.</span>',
    "experience_tres_etendue_produits_alimentaires":
        '<b><span style="font-size: small;">Very extensive experience (Fast-moving consumer food products) France and International for more than 15 years</span></b>',
    "le_candidat_a_des_postes_dadministrateur_est_":
        '<span style="font-size: small;"> The candidate for director positions is a graduate of a Business School. He served as CEO, Director and Operational Head of subsidiaries in several European countries and in the USA. He has carried out complex restructuring operations. In the context of his responsibilities, he has raised funds from major venture capital investors and led assignments in mergers &amp; acquisitions consulting (multinationals and start-ups).</span>',
    "experience_internationale_tres_etendue_high_t":
        '<b> </b><span style="font-size: small;"><b><span style="font-size: small;">Very extensive international experience (High Tech and IT)</span></b> </span>',
    "le_candidat_a_passe_plus_de_30_ans_dans_des_e":
        '<span style="font-size: small;">The candidate has spent over 30 years in international environments including over 10 years of living in the USA. </span><span style="font-size: small;">He has been CEO, Director or operational head of subsidiaries of large IT companies (generalist, service providers, enterprise software) and Vice Chairman of a start-up (biometrics). Responsibilities taken in the field of art trading and real estate have enriched his vision of business. Today, as an international consultant, he proposes, by becoming an independent director, to make his competence available to companies. </span><span style="font-size: small;">Education: Arts et Métiers Engineer and INSEAD</span>',
    "le_candidat_aujourdhui_consultant_internation":
        '<span style="font-size: small;">The candidate, today an international consultant, started as Director of the French Chamber of Commerce in a Nordic country, before representing French textile and clothing industries in international bodies. Then, within a major French press/media group, he was Subsidiary Director in Portugal, International Director notably in charge of joint venture arrangements, Managing Director of a subsidiary in France, Deputy Director with director positions. Potential corporate officer of press/media companies with international development (speaks several languages: Swedish, Portuguese, English and German). Education: Law, Oriental Languages (Russian).</span>',
    "questions_energetiques_et_gestion_des_risques":
        '<b><span style="font-size: small;"> Energy issues and associated risk management</span></b>',
    "le_candidat_a_une_longue_experience_des_affai":
        '<span style="font-size: small;">The candidate has long experience in energy matters (specialised civil engineering and heavy equipment/turbomachines...) and associated risk management. Over recent years, he has assimilated the particular status, inherent uncertainties, and working methods of senior executives and directors of companies and their increasing involvement in energy management and risk.</span>',
    "la_candidate_ecole_des_mines_et_biotechnologi":
        '<span style="font-family: georgia, palatino, serif;">The candidate (École des Mines and Biotechnology at MIT) has held 3 successive mandates on the Supervisory Board of an international family ETI: organic and external growth, challenges linked to rapid growth (manufacturing, supply chain, HR). More than 40 years outside France: USA + various European countries, in Germany since 2000. Strategy consulting at Bain, operational director at Pasteur-Mérieux. For two years, mentoring start-ups with the MassChallenge accelerator.</span>',
    "candidate_administratrice_independante_hotell":
        '<span style="font-size: small;"><b>Candidate independent director: Hospitality, Catering, Tourism; France and Europe</b> Multidisciplinary experience acquired within an international hotel group listed on the CAC 40. Over 30 years, including 12 years in public catering, the candidate has successively held executive positions in varied fields: management control, products, operations, marketing, internal audit, production, publishing and communication of international sales offices, and finally regarding the effectiveness of marketing &amp; distribution costs.</span>',
    "aujourdhui_elle_est_consultante_independante_":
        '<span style="font-size: small;">Today, she is an independent consultant in these fields. Very good knowledge of international matters. Education: Master\'s in Economics (Paris 2), DEA Monetary Theories and Policies (Paris 2), Executive Doctorate in Business Administration (Paris Dauphine, 2009). Member of the IFA and Secretary General of the European Association of Neuroeconomics.</span>',
    "docteur_en_economie_la_candidate_beneficie_du":
        "Doctor of Economics, the candidate has more than 30 years of professional experience. Her professional competences cover the banking/finance sector, organisational and strategy consulting, new technologies and digital transformation.",
    "membre_des_comites_de_direction_elle_a_assure":
        "Member of executive committees, she has successfully managed operational responsibilities (profit centres, development) within one of the world's largest banks, a leading consulting firm (big four) and a listed information systems specialist company (CAC 40). Given the projects she has carried out and her various functions, she is thoroughly familiar with the Europe zone (UK, Benelux, Hungary, Spain, Italy), the United States, India and Morocco.",
    "membre_du_cercle_des_administrateurs_de_lasso":
        "Member of the Circle of Directors, of the ATOS Alumni association, she also leads voluntary activities for V.E.C.V (Votre École Chez Vous), an association recognised as being of public utility and under contract with the national education authority.",
    "candidate_a_un_poste_dadministratrice_indepen":
        '<span style="font-size: small;"><b> Candidate for an independent director position, with good knowledge of construction, business services, healthcare, investment funds and communications.</b></span>',
    "ensuite_apres_avoir_ete_secretaire_general_du":
        "<span style=\"font-size: small;\">Then, after serving as Secretary General of a major Law Firm, she created her own consulting firm, putting her management and financial skills at the service of the strategy, governance and organisation of her clients.</span>",
    "la_candidate_membre_de_lifa_est_diplomee_de_l":
        '<span style="font-size: small;">The candidate, a member of the IFA, holds a degree from IEP Paris, Eco-fi, a DESS in banking-insurance and a management master\'s from Dauphine.</span>',
    "en_france_creatrice_de_son_propre_cabinet_de_":
        "<strong>In France</strong>, founder of her own IT/Digital market research and studies firm, developed to 150 people across Europe then sold to a major consulting group; then CEO of an IT research firm. <strong>Then in Europe</strong>, responsible for the development of a major HR consulting firm and then another in IT. <strong>Then, a long career in the USA</strong> as Executive Director in various positions for the development of a major international management consulting firm.",
    "de_retour_en_europe_membre_du_comite_executif":
        "<strong>Back in Europe</strong>, member of the European Executive Committee of a renowned consulting firm specialising in leadership and executive search",
    "cette_large_experience_internationale_vecue_d":
        "This extensive international experience gained in 6 countries has enabled her to know many B-to-B sectors, including digital and consumer goods. Her \"Business\" network (INSEAD, IOD, American Chamber of Commerce Zurich) can be put at the service of a Board. To note: Member for 5 years of the Board of CAWC, Connections for Abused Women and their Children in Chicago, Chairwoman of the Communications Commission",
    "candidate_a_un_poste_dadministratrice_indepen_2":
        '<b><span style="font-size: small;"> </span></b><strong>Candidate for an independent director position.</strong> She brings 30 years of experience in an international environment of public/private structures and in diverse fields such as research, production, strategy, risk management (human, capital and societal), project and team management, and start-up mentoring. Her key areas of expertise are the pharmaceutical and chemical industries in close and continuous collaboration with a network of local and international SMEs. Drawing on all these experiences and areas of expertise, she is able to intervene in many related or complementary industries (equipment manufacturers, cosmetics, agrochemicals...). Her interest in economic development in a sustainable and equitable way is her guiding thread because she believes in collective intelligence, co-construction and collaboration as the foundation of a company\'s success and more broadly of our society. The candidate has a PhD in Chemistry Engineering and is a certified Director from EM Lyon.',
    "la_candidate_a_un_poste_dadministratrice_inde":
        '<b><span style="font-size: small;"> The candidate for an independent director position</span></b> <span style="font-size: small;">is today a consultant and teacher in finance at the École Nationale des Ponts et Chaussées. She holds a DECS in Accounting and an Executive MBA in Management from New York University, Stern Business School. Bilingual French-English with 26 years of experience as CFO and Administrative Officer in international companies (including in the USA) in various sectors, notably consumer products and luxury. Very operational and close to the business, she has expertise in strategy, organisation, management and information systems. Representative of a corporate foundation and Member of the EPWN Board, she has experienced from the inside the workings of a Board of Directors. Member of the IFA, Women Corporate Directors and EPWN</span>',
    "la_candidate_ecole_des_mines_et_biotechnology":
        '<span style="font-size: small;">The candidate (École des Mines and Biotechnology at MIT), has lived in Germany since 2000, with many years outside France: USA + various European countries. Strategy consulting at Bain, operational director at Pasteur-Mérieux, notably for a spin-off / sale of a business unit. For 8 years, successfully working as an independent consultant for the international launch/development of start-ups (biotechnology and health).</span>',
    "la_candidate_est_de_formation_initiale_ingeni":
        "The candidate's initial training is as a PhD engineer in industrial engineering (INPG), then she obtained an \"Executive MBA\" and a doctorate in business administration (IAE, PSB). She has 15 years of experience in an international paper group managing cross-functionally the operational and strategic development of innovation (multiple international placements including Germany, the USA, Spain). For 9 years, she has developed her management consulting activity in innovation and in parallel supervises academic research on innovation culture: notably the management of collective creativity. She also has good knowledge of Boards of Directors, as she is certified as director by ADAE, of which she has become a member of the Comex and educational coordinator for the director training programme. She furthermore leads a collection of books on new value trends and Board performance.",
    "avec_une_longue_experience_de_direction_gener":
        '<span style="font-size: small;">With extensive experience in Senior Management, with telecom operators and suppliers, the candidate has supervised international and multidisciplinary teams (finance, marketing, commercial, product development). Member of the Executive Committee of a worldwide association of operators for more than 10 years, she has acquired a global knowledge of the industry and its players as well as experience in governance.</span>',
    "la_candidate_a_une_formation_deconomiste_aux_":
        '<span style="font-size: small;">The candidate has an economics background (in the United States and in Switzerland) and an INSEAD MBA. She is a Member of the INSEAD Circle of Directors and Women Corporate Directors, and holds dual French and American nationality.</span>',
    "candidate_a_un_poste_dadministratrice_indepen_3":
        '<span style="text-align: left; font-weight: bold;"><strong>Candidate for an independent director position.</strong> Varied international experience within major American and European groups (Space, Medical and Defence), but also for SMEs and start-ups.</span>',
    "apres_un_doctorat_en_mathematiques_appliquees":
        "After a doctorate in applied mathematics, for about twenty years, she managed major projects (over €10 million) for export (USA, South Africa, Spain, Italy, Indonesia, Thailand, etc.) and multicultural teams in high technology information and communication. Then, in the field of artificial intelligence, she worked to define a new development strategy for a start-up from the École Normale Supérieure.",
    "ayant_obtenu_des_certificats_pour_evaluation_":
        "Having obtained certificates for financial evaluation and the creation of technological start-ups (HEC and Polytechnique), she joined the industrial innovation agency then the major public investment bank to provide strategic analysis of major selected projects (up to €110 million) by these organisations. Today, as an independent, she provides strategy consulting assignments. Member of the Circle of Directors.",
    "la_candidate_de_formation_ingenieur_insead_a_":
        '<b><span style="font-size: small;"> The candidate, trained as Engineer + INSEAD, has extensive experience in senior management positions and as a director in the industrial sector, complemented by genuine expertise in the risk management of major international projects.</span></b>',
    "apres_10_ans_a_des_postes_de_responsabilite_t":
        '<span style="font-size: small;">After 10 years in positions of technical responsibility (design, production, testing, management of major projects), the candidate has held various Management functions involving amounts that could exceed €500M and including an international dimension: Strategy, Administration and Finance, Operations, Management Control, Supply Chain. This multidisciplinary experience (mechanical, electronic, IT, communications) has naturally led her to positions as industrial Business Unit Director, Director within General Management and as Director. The candidate has often in parallel exercised cross-functional responsibilities in multidisciplinary risk management of operational units and projects. This experience now allows her to be considered an expert in this field. She teaches management control courses (in English: "Management control") at various schools including ESSEC. The candidate is a member of the IFA and the INSEAD/Wharton/… Circle of Directors.</span>',
    "apres_avoir_ete_avocate_au_barreau_de_paris_s":
        "After serving as a lawyer at the Paris Bar, specialised in business law, for seven years, she led the family wine business based in Gascony. Her work was particularly focused on international commercial development and opening new markets. Building on this experience, for 4 years, she served as Secretary General of the Family Business Network France, where she developed a multidisciplinary educational programme of workshops and lectures for entrepreneurial families.",
    "aujourdhui_consultante_independante_elle_les_":
        "Today, as an independent consultant, she advises them, in the context of accelerated international change, on how best to organise their governance and plan succession, particularly within the family.",
    "elle_a_suivi_un_cursus_de_droit_des_affaires_":
        "She studied business law and philosophy of law, and holds the certificate of aptitude for the legal profession and a master's in coaching. She lives between France and Italy.",
    "administratrice_independante_de_nationalite_f":
        "<strong>Independent director of French nationality currently living in Madrid. Extensive operational experience in the telecommunications business, then in an International NGO and today as an entrepreneur.</strong>",
    "apres_un_dea_deconomie_a_paris_la_sorbonne_et":
        "After a DEA in economics from Paris La Sorbonne and an MBA from the University of San Francisco in the United States, the candidate worked for 7 years within a major French telecommunications operator. She was the first woman to join the International division, as an expatriate, responsible for launching commercial activities in Spain. She remained there to launch the activities of another group in the same sector and take responsibility for their subsidiary in Spain and Portugal. She then for four years was manager for the Iberian peninsula for subsidiaries of American telecommunications companies listed on Nasdaq (hardware and software).",
    "ensuite_durant_6_annees_elle_a_ete_responsabl":
        "Then, for 6 years, she was responsible for the Latin countries of a major international NGO aimed at promoting the presence of women in business in positions of responsibility and boards of directors. She has developed expertise in diversity management.",
    "aujourdhui_elle_a_cree_sa_propre_entreprise_d":
        "Today, she has created her own consulting company to develop, within companies such as a major cosmetics group, team spirit, leadership and facilitate organisational change, notably using coaching, music and rhythms. Mentor within the international association Professional Women Network (PWN) as well as member of the Spanish Women CEO Association. Languages: French, English, Spanish.",
    "apres_une_formation_de_juriste_en_espagne_et_":
        "After legal training in Spain and Germany, the candidate worked for 5 years in Brussels, Madrid and Barcelona in several business law firms, one Spanish and two American: handling very varied disputes upstream of court proceedings, including vis-à-vis the European Commission: customs duties, abuse of dominant position, commercial agreements, mergers and acquisitions... Then, for 6 years, she was part of the Cabinet of Mr Marcelino Oreja, member of the European Commission, responsible for directing the follow-up of Enterprises, responsible for concerted actions between the Commission and member states on policies to improve the environment and develop companies. Then in Madrid, she was the creator and manager of a major e-commerce platform project designed to facilitate international trade transactions, aiming to enable commercial exchanges with significant cost reductions in exports and imports. The project received financial support from the European Union, chambers of commerce and various associations from 8 European countries. An operational prototype was created. The project received several awards and distinctions.",
    "en_parallele_elle_a_ete_directrice_juridique_":
        "In parallel, she was Legal Director and adviser to the Chairman of a very large Spanish group in the field of food products and construction of hotel complexes. She notably participated in the creation of an internet portal to broaden the consumer base. Today, she has created her own consulting firm for both companies and public bodies. She can provide them with the benefit of her extensive European experience, as well as in establishing relations with China and Latin American countries.",
    "en_espagne_elle_a_ete_administratrice_de_la_c":
        "In Spain, she has served as director of the Spanish employers' confederation, Vice Chairwoman of Women CEO and, in a major city in the eastern USA, director of a major international school as well as an NGO aimed at improving living conditions for disadvantaged people. In 2013, she participated in the course <strong><em>\"</em></strong><em>Making corporate boards more effective</em>\" at Harvard Business School.",
    "la_candidate_a_un_poste_dadministratrice_inde_3":
        '<span style="font-weight: bold;">The candidate for an independent director position, of French and American nationality, is based in the USA and in France. An Anglo-Saxon career of 30 years at the crossroads of real estate and finance</span> at Bank of America, General Motors, EY, ... or in the service of institutional clients such as the World Bank or BlackRock. She has had in turn the roles of analyst, issuer, evaluator, lender, and investor.',
    "elle_a_mene_plusieurs_operations_de_fusion_ac":
        "She has led several merger and acquisition or company sale operations, and sat on several boards of directors of subsidiaries of a major group.",
    "aujourdhui_consultante_independante_connaissa":
        "Today, as an independent consultant, with good knowledge of the United States, Canada, Western European countries and Russia, she works internationally to help institutional actors to properly formulate and execute their real estate strategies. She sits on the board of several professional real estate associations.",
    "diplomee_de_liae_de_nice_de_paris_i_pantheon_":
        '<span style="font-weight: bold;">Graduate of IAE Nice, Paris I Panthéon Sorbonne and HEC, with an international, commercial and marketing orientation, the candidate of Franco-Bulgarian nationality has spent a third of her professional life abroad, in Bulgaria, Morocco, Italy, USA, France</span>, etc.',
    "elle_a_20_ans_dexperience_de_directions_opera":
        "She has 20 years of experience in operational and strategic management, in the sectors of pharmaceutical distribution, capital goods and services, in Italian, French and Japanese companies in Europe. She can claim several delicate turnarounds and has experienced two particular situations: listing on the NYSE and hostile takeover by a major Japanese group.",
    "elle_a_egalement_acquis_une_bonne_connaissanc":
        "She has also acquired good knowledge of how Boards work, on the one hand as a member of Executive Committees (presentations before directors), and on the other hand for having in several circumstances played the role of Board Secretary (preparation of files for the Board, knowledge of stakeholders, governance reports).",
    "elle_est_actuellement_conseil_independant_en_":
        "She is currently an independent advisor in strategy, supporting company or innovative activity creators from large groups, specialised in brand development &amp; enhancement, member of the strategic committee of a start-up and volunteer career advisor (HEC mentoring). Member of the French Institute of Directors, the French American Foundation, the Professional Women's Network and the HEC governance group.",
    "la_candidate_de_formation_ingenieur_insead_a__2":
        '<b><span style="font-size: small;"> The candidate, trained as Engineer + INSEAD, has extensive experience in senior management positions and as a director in the industrial sector, complemented by genuine expertise in the risk management of major international projects.</span></b>',
    "apres_10_ans_a_des_postes_de_responsabilite_t_2":
        '<span style="font-size: small;">After 10 years in positions of technical responsibility (design, production, testing, management of major projects), the candidate has held various Management functions involving amounts that could exceed €500M and including an international dimension: Strategy, Administration and Finance, Operations, Management Control, Supply Chain. This multidisciplinary experience (mechanical, electronic, IT, communications) has naturally led her to positions as industrial Business Unit Director, Director within General Management and as Director. The candidate has often in parallel exercised cross-functional responsibilities in multidisciplinary risk management of operational units and projects. This experience now allows her to be considered an expert in this field. She teaches courses on company control in English "Management control" at various schools including ESSEC.</span>',
    "la_candidate_est_membre_de_lifa_et_du_cercle_":
        "The candidate is a member of the IFA and the INSEAD/Wharton/… Circle of Directors.",
    "la_candidate_domiciliee_depuis_25_ans_a_paris":
        '<span style="font-size: small;">The candidate based in Paris for the last 25 years holds dual French and Spanish nationality. Her experience in managing highly strategic operations for major listed companies in the United Kingdom, France and Belgium has been accumulated over 30 years. First, and in depth, in the telecommunications sector, but also more recently in healthcare (hospitals) and the food industry (fishing). She can claim several delicate turnarounds as a Board member overseeing smooth operational execution, as a member of the Executive Committee, and as a consultant. Independent director of a Norwegian company, she has experienced two very enriching situations: stock exchange listing in London and hostile takeover by a major German group.</span>',
    "dans_un_contexte_franco_espagnol_tendu_elle_a":
        "In a tense Franco-Spanish context, she served as CEO, then Chairwoman of the Board of Directors of the Spanish joint venture of two groups (IBEX35 / CAC40). Her international experience is European and more particularly for Southern countries whose languages she speaks fluently, but extends to South America.",
    "formation_computing_sciences_engineer_cours_p":
        "Education: Computing Sciences Engineer, + Executive courses at INSEAD. Member of the International Board of the Global Telecommunications Women Network and in Spain of \"Plataforma de Expertas\". Member of \"Achieving Outstanding Performance\" (AoP) and TMT Group's INSEAD",
    "pendant_plus_de_15_ans_la_candidate_a_travail":
        '<span style="font-size: small;">For more than 15 years, the candidate worked in Consulting and Engineering (IT, electronics, process,...), within a listed international group, for the Development and Management of Major Accounts, notably in Industry (automotive, medical, defence,...) and Telecoms.</span>',
    "la_candidate_a_une_expertise_de_business_deve":
        "The candidate has expertise as a Business Developer as well as strong marketing and HR openness. Within subsidiaries (60 to 800 people with some having revenues of more than €500M), she served as Director (France and Spain), CEO and Chairwoman (SAS). She has furthermore exercised cross-functional responsibilities and contributed to organisational transformation, both during periods of growth and during periods of crisis.",
    "membre_de_leuropean_professionals_women_netwo":
        '<span style="font-size: small;">Member of the European Professional\'s Women Network, the Governance and Equilibre Circle, certified by ESSEC for the specific training to become a director "Women Be European Board Ready"</span>',
    "la_candidate_pharmacie_mba_actuellement_conse":
        '<b><span style="font-size: small;"> </span></b><b><span style="font-size: small;">The candidate, Pharmacy-MBA, currently an independent strategy advisor, has 30 years of experience in operational and strategic management in the consumer and pharmaceutical sectors. Her successful international experience, notably as a "high-level commercial executive", demonstrates great adaptability in multicultural environments.</span></b>',
    "la_candidate_a_un_poste_dadministratrice_inde_4":
        '<b></b><span style="font-size: small;">The candidate for an independent director position started her career in research and development in laboratory and pharmaceutical industry. She then became a strategy consultant at a major international firm where she led projects in several industries (Pharmaceuticals, Agri-food, Distribution, sectors from which she could benefit). Then, in an international leader group in the beverages sector, she spent more than 20 years in diverse operational (profit centres, sales-marketing, innovation) and strategic responsibilities in France and worldwide. In this capacity, she participated in Executive Committees, led major multicultural and functional teams. She knows what it means to carry out on the ground actions within the framework of a strategic vision. From an entrepreneurial family, she has invested in start-ups and supports them. She therefore knows how to adapt to organisations of different sizes. Trilingual French/English/German, member of the IFA</span><b><span style="font-size: small;">.</span></b>',
    "au_cours_des_22_dernieres_annees_cette_candid":
        '<span style="font-size: small;"><b>Over the last 22 years, this candidate for a director position has been a member of Executive Committees, with expertise in finance, strategy and transformation projects both in France and internationally in the sectors of financial services, infrastructure related to transport, energy, waste and leisure.</b></span>',
    "apres_10_ans_dexperience_en_financements_stru":
        "After 10 years of experience in structured financing in the utilities and transport sectors, she contributed to defining strategic developments for one of the leading French banking groups (investment evaluations, capital allocation, partnership conclusions) and led major transformation projects as CFO of international groups leading in the fields of asset management, investment banking and private banking. She served as director of several financial sector companies in France and abroad (Italy, UK, USA, Hong Kong), and is currently director of the national association of chief financial officers, the DFCG, of which she chairs the Île-de-France region. She is furthermore a member of the IFA and has initiated the IFA/DFCG working group on the theme \"CFO and Audit Committee\". She has taught financial analysis and management control at Dauphine and HEC. She is a graduate of Sciences Po Paris and Columbia University.",
    "directrice_financiere_et_des_operations_avec_":
        '<span style="font-size: small;"><b>CFO and Operations Director,</b> <b>with 25 years of experience in international listed industrial groups, in the Energy, Environment, Aluminium, Packaging, Chemicals and B2B Services sectors</b></span>',
}


def main():
    with open('data/translations/en.json', encoding='utf-8') as f:
        en = json.load(f)

    page = en.get('page_candidats_mandataires_sociaux', {})
    patched = 0
    for key, val in TRANSLATIONS.items():
        if key in page:
            page[key] = val
            patched += 1
        else:
            print(f'  WARNING: key not found: {key}')

    en['page_candidats_mandataires_sociaux'] = page

    with open('data/translations/en.json', 'w', encoding='utf-8') as f:
        json.dump(en, f, ensure_ascii=False, indent=2)

    print(f'Patched {patched} entries.')


if __name__ == '__main__':
    main()
