#!/usr/bin/env python3
"""Translate all remaining French strings in en.json (non-candidats pages)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_JSON = ROOT / "data" / "translations" / "en.json"

PATCHES = {

# ── page_actualites ──────────────────────────────────────────────────────────
"page_actualites.avecpascal_picq_paleoanthropologue_de_renom_u":
    'With <strong>Pascal Picq</strong>, renowned paleoanthropologist: an unprecedented conference on anthropology and the evolution of companies.',

# ── page_bibliographie ───────────────────────────────────────────────────────
"page_bibliographie.grace_a_une_serie_detudes_de_cas_se_lisant_fa":
    'Thanks to a series of case studies as easy to read as short detective novels, the author, drawing on his long practical experience as a director, presents the delicate and exciting side of the director\'s role. For each case, he comments and derives best governance practices.',

"page_bibliographie.1_ni_mandataire_social_ni_salarie_actuel_ou_a":
    '<span style="font-size: small;">\n'
    '                                                                        1- Neither corporate officer nor current (or past five years) employee.<br/>\n'
    '                                                                        2- Not a cross-director.<br/>\n'
    '                                                                        3- Not a significant client, supplier or banker (for business or financing purposes) or representing a significant share of the company\'s activity.<br/>\n'
    '                                                                        4- No close family ties with a corporate officer.<br/>\n'
    '                                                                        5- Neither partner nor current (or past five years) collaborator of the Statutory Auditors.<br/>\n'
    '                                                                        6- Not a director of the company for more than twelve years.<br/>\n'
    '                                                                        7- Shareholders:<br/>\n'
    '                                                                        – Below 10%: independent if not participating in control.<br/>\n'
    '                                                                        – Above 10%: review by the board, depending on the ownership structure and the existence of potential conflicts of interest.\n'
    '                                                                    </span>',

"page_bibliographie.on_directorshipshareholder_advocates_are_keen":
    '<div>\n<table class="table">\n<tbody>\n<tr>\n'
    '<td class="article-cell" data-i18n="page_bibliographie.on_directorshipshareholder_advocates_are_keen_2">\n'
    '<a href="http://ondirectorship.com/ondirectorship/j3xb9xcqpivwnw6dktyde495k7ktr0">\n'
    '<span style="text-decoration: underline;"><strong><span style="color: #000080; text-transform: uppercase;">On Directorship</span></strong></span><br/>\n'
    '<span style="color: blue;">Shareholder advocates are keen to point out the risk of company directors becoming captured by "groupthink".</span><br/>\n'
    '<span style="color: black;">Peter Tunjic, Lawyer/Writer/Creator, Melbourne, Australia</span>\n'
    '</a><br/>\n'
    '<span style="color: #808080;">Original article explaining the reasons, the presence and the dangers of "groupthink" within boards of directors</span>\n'
    '</td>\n</tr>\n'
    '<tr>\n<td class="article-cell" data-i18n="page_bibliographie.harvard_business_review_france_11_12_2014_la_">\n'
    '<a href="http://www.hbrfrance.fr/chroniques-experts/2014/12/5477-la-feminisation-une-source-de-renouveau-pour-les-conseils-dadministration/">\n'
    '<span style="text-decoration: underline;"><strong><span style="color: #000080;">Harvard Business Review France (11/12/2014)</span></strong></span><br/>\n'
    '<span style="color: blue;">Feminisation, a source of renewal for boards of directors.</span><br/>\n'
    '<span style="color: black;">Viviane de Beaufort (Professor at ESSEC) (Women Be European Board Ready Training)</span>\n'
    '</a><br/>\n'
    '<span style="color: #808080;">Detailed arguments on the benefits of the presence of female directors on Boards</span>\n'
    '</td>\n</tr>\n'
    '<tr>\n<td class="article-cell" data-i18n="page_bibliographie.liberation_29_05_2014_presenteisme_alibi_masc">\n'
    '<span style="text-decoration: underline;"><strong><span style="color: #000080;"><a href="http://www.ft.com/intl/cms/s/0/3bdb9b68-f0cb-11e0-aec8-00144feab49a.html#axzz1bURIcX45" style="color: #000080;"><span style="text-transform: uppercase;">LIBERATION (29/05/2014)</span></a></span></strong></span><br/>\n'
    '<a href="http://www.liberation.fr/societe/2014/05/26/presenteisme-alibi-masculin-pour-eviter-les-taches-menageres_1027387">\n'
    '<span style="color: blue;">"Presenteeism: a male alibi to avoid household chores?"</span>\n'
    '</a><br/>\n'
    '<span style="color: black;">François Fatoux, Member of the equality laboratory</span><br/>\n'
    '<span style="color: #808080;">A remarkable and in-depth analysis of the five forms of presenteeism at work, the fifth form being "totally taboo, which overwhelmingly affects men who are relieved, without wanting to admit it, to have to stay \'stuck\' at work because going home early means preparing dinner, monitoring children\'s homework, feeding them, doing housework. It is still more pleasant to come home when everything is done."<br/>\n'
    '                                                G &amp; S sees this as one of the causes of the glass ceiling. Indeed, these accumulated late working hours, over a year for example, can result in good professional results. However, these good results, rather than the presence itself, will positively influence assessments and consequently the career progression of those who practise them.</span>\n'
    '</td>\n</tr>\n'
    '<tr>\n<td class="article-cell" data-i18n="page_bibliographie.la_tribune_5_9_12_bientot_des_quotas_de_femme">\n'
    '<span style="text-decoration: underline;"><span style="color: #000080;"><strong><a href="http://www.ft.com/intl/cms/s/0/3bdb9b68-f0cb-11e0-aec8-00144feab49a.html#axzz1bURIcX45" style="color: #000080;"><span style="text-transform: uppercase;">LA TRIBUNE (5/9/12)</span></a></strong></span></span><br/>\n'
    '<span style="color: blue;"><a href="http://www.latribune.fr/actualites/economie/union-europeenne/20120904trib000717652/bientot-des-quotas-de-femmes-administratrices-dans-toute-l-ue.html?goback=.gde_3816734_member_158951768">"Soon quotas for female directors throughout the EU"</a></span><br/>\n'
    '<span style="color: black;">Marina Torre</span><br/>\n'
    '<span style="color: #808080;">Measures which, according to a document obtained by the Financial Times, the services of Viviane Reding, EU Commissioner for Justice, are studying.</span>\n'
    '</td>\n</tr>\n'
    '<tr>\n<td class="article-cell" data-i18n="page_bibliographie.lentreprisefemmes_administratrices_je_vous_ai">\n'
    '<a href="http://www.ft.com/intl/cms/s/0/3bdb9b68-f0cb-11e0-aec8-00144feab49a.html#axzz1bURIcX45">\n'
    '<span style="text-decoration: underline; color: #000080;"><strong>L\'ENTREPRISE</strong></span>\n'
    '</a><br/>\n'
    '<span style="color: blue;">"Women directors: I love you"</span>\n'
    '<span style="color: #808080;">CAC 40 companies are drawing from the pool of women business owners of SMEs to improve gender diversity on their board. Why not you?</span><br/>\n'
    '<span style="color: blue;">L\'Entreprise November 2010 No. 294</span><br/>\n'
    '<span style="color: black;">Corinne Corniou</span><br/>\n'
    '<span style="color: #808080;">An overview of the advances in CAC 40 boards and their directors</span>\n'
    '</td>\n</tr>\n'
    '<tr>\n<td class="article-cell" data-i18n="page_bibliographie.financial_times_electroniceveryone_benefits_o">\n'
    '<span style="text-decoration: underline;"><strong><span style="color: #000080;"><a href="http://www.hbrfrance.fr/chroniques-experts/2014/12/5477-la-feminisation-une-source-de-renouveau-pour-les-conseils-dadministration/" style="color: #000080;"><span style="text-transform: uppercase;">FINANCIAL TIMES ELECTRONIC</span></a></span></strong></span><br/>\n'
    '<span style="color: blue;">"Everyone benefits of a beast in the boardroom"<br/>1 October 2010</span><br/>\n'
    '<span style="color: black;">Lucy Kellaway</span><br/>\n'
    '<span style="color: #808080;">A very humorous analysis of the value of having an "iconoclastic villain" as a board member. By amusing analogy with quotas for other minorities including women, the journalist asks "Should there be quotas for villains?"</span>\n'
    '</td>\n</tr>\n'
    '<tr>\n<td class="article-cell" data-i18n="page_bibliographie.challengesje_suis_top_ou_comment_briser_le_pl">\n'
    '<span style="text-decoration: underline;"><span style="color: #000080;"><strong><a href="http://www.jesuistop.fr/" style="color: #000080;"><span style="text-transform: uppercase;">CHALLENGES</span></a></strong></span></span><br/>\n'
    '<span style="color: blue;">"Je suis top", or how to break the glass ceiling"<br/>1 December 2010</span><br/>\n'
    '<span style="color: black;">Anne-Marie Rocco</span><br/>\n'
    '<span style="color: #808080;">Positive analysis of the play "Je suis au top" by Blandine Métayer performed in December 2010 at the Théâtre de 10 heures. The play follows the adventures of a woman trying to reach executive positions by breaking the glass ceiling.</span>\n'
    '</td>\n</tr>\n'
    '<tr>\n<td class="article-cell" data-i18n="page_bibliographie.lexpress8_septembre_2010valerie_liongouvernan">\n'
    '<span style="color: #000080;"><strong><span style="text-decoration: underline;"><a href="./../wp-content/uploads/2020/01/vlionexpresssept.pdf" style="color: #000080;"><span style="text-transform: uppercase;">L\'EXPRESS</span></a></span></strong></span><br/>\n'
    '<span style="color: blue;">8 September 2010</span><br/>\n'
    '<span style="color: black;">Valérie Lion</span><br/>\n'
    '<span style="color: #808080;">Governance, Eternal Masculine<br/>The heavyweights of the CAC 40 have feminised their boards. But behind the scenes, immobility reigns, as revealed by an exclusive study\u2026.</span>\n'
    '</td>\n</tr>\n'
    '<tr>\n<td class="article-cell" data-i18n="page_bibliographie.challengesdes_quotas_pour_etablir_legalite11_">\n'
    '<span style="text-decoration: underline; color: #000080;"><strong><a href="http://www.challenges.fr/magazine/international/0199.28686/" style="color: #000080;"><span style="text-transform: uppercase;">CHALLENGES</span></a></strong></span><br/>\n'
    '<span style="color: blue;">Quotas to establish equality<br/>11 February 2010</span><br/>\n'
    '<span style="color: black;">Richard Descoings</span><br/>\n'
    '<span style="color: #808080;">This editorial article defends the idea that the law on quotas for female directors should be temporary. G &amp; S shares the same opinion.</span>\n'
    '</td>\n</tr>\n'
    '<tr>\n<td class="article-cell" data-i18n="page_bibliographie.lexpressou_sont_les_femmes_conseils_dadminist">\n'
    '<span style="text-decoration: underline;"><strong><span style="color: #000080;"><a href="http://www.lexpress.fr/actualite/economie/ou-sont-les-femmes_841709.html" style="color: #000080;"><span style="text-transform: uppercase;">L\'EXPRESS</span></a></span></strong></span><br/>\n'
    '<span style="color: blue;">Where are the women? Boards of Directors<br/>13 January 2010</span><br/>\n'
    '<span style="color: black;">Valérie Lion</span><br/>\n'
    '<span style="color: #808080;">Many articles appeared before and after the debate in the National Assembly on 19 January 2010 on the bill on gender parity in boards of directors and supervisory boards of companies. This one, <a href="http://www.lexpress.fr/actualite/economie/ou-sont-les-femmes_841709.html">available online</a>, is interesting as it provides a structured summary with examples and explanations of the situation regarding CAC 40 companies.</span>\n'
    '</td>\n</tr>\n'
    '<tr>\n<td class="article-cell" data-i18n="page_bibliographie.sur_119_societes_cotees_sur_alternext_trois_s">\n'
    '<span style="text-decoration: underline; color: #000080;"><strong><span style="text-transform: uppercase;">Of 119 listed companies on Alternext, three are led by women!</span></strong></span><br/>\n'
    '<span style="color: blue;">Challenges No. 193, 17 December 2009</span><br/>\n'
    '<span style="color: black;">Marc Fiorentino</span><br/>\n'
    '<span style="color: #808080;">After discussing his search for female executives in Alternext companies and noting their small number, he recommends buying shares in the three companies led by women.</span>\n'
    '</td>\n</tr>\n'
    '<tr>\n<td class="article-cell" data-i18n="page_bibliographie.le_gouvernement_veut_feminiser_lencadrement_d">\n'
    '<a href="http://www.hbrfrance.fr/chroniques-experts/2014/12/5477-la-feminisation-une-source-de-renouveau-pour-les-conseils-dadministration/">\n'
    '<span style="text-decoration: underline; color: #000080;"><strong>The government wants to feminise corporate management</strong></span>\n'
    '</a><br/>\n'
    '<span style="color: blue;">Le Monde, 6 November 2009</span><br/>\n'
    '<span style="color: #808080;">A very humorous analysis of the value of having an "iconoclastic villain" as a board member. By amusing analogy with quotas for other minorities including women, the journalist asks "Should there be quotas for villains?"</span>\n'
    '</td>\n</tr>\n'
    '<tr>\n<td class="article-cell" data-i18n="page_bibliographie.jean_francois_cope_sengage_pour_legalite_homm">\n'
    '<span style="color: #000080;"><a href="http://www.hbrfrance.fr/chroniques-experts/2014/12/5477-la-feminisation-une-source-de-renouveau-pour-les-conseils-dadministration/" style="color: #000080;">\n'
    '<span style="text-decoration: underline;"><strong>Jean-François Copé commits to gender equality at work</strong></span>\n'
    '</a></span><br/>\n'
    '<span style="color: blue;">Lefigaro.fr, 25 October 2009</span><br/>\n'
    '<span style="color: #808080;">In an interview with the Journal du Dimanche, he expresses his wish that "in the coming days, a bill be introduced providing that 40%, and eventually 50%, of seats on the boards of directors of large companies be reserved for women."</span>\n'
    '</td>\n</tr>\n'
    '<tr>\n<td class="article-cell" data-i18n="page_bibliographie.quotas_de_femmes_la_cle_de_la_paritelefigaro_">\n'
    '<span style="color: #000080;"><a href="http://madame.lefigaro.fr/societe/en-kiosque/2257-la-cle-de-la-parite/2" style="color: #000080;">\n'
    '<span style="text-decoration: underline;"><strong>Quotas for women directors, the key to parity</strong></span>\n'
    '</a></span><br/>\n'
    '<span style="color: blue;">Lefigaro.fr, 29 September 2009</span><br/>\n'
    '<span style="color: black;">Clara Dufour</span><br/>\n'
    '<span style="color: #808080;">Results of a poll on the introduction of gender quotas in Boards of Directors and comments by personalities active in this field.</span>\n'
    '</td>\n</tr>\n'
    '<tr>\n<td class="article-cell" data-i18n="page_bibliographie.une_image_approfondie_sur_internet_cela_senca">\n'
    '<a href="http://madame.lefigaro.fr/societe/en-kiosque/2257-la-cle-de-la-parite/2">\n'
    '<span style="text-decoration: underline;"><span style="color: #000080;"><strong>Managing your online image in depth</strong></span></span>\n'
    '</a><br/>\n'
    '<span style="color: blue;">Challenges No. 22, October 2009</span><br/>\n'
    '<span style="color: black;">Gilles Fontaine</span><br/>\n'
    '<span style="color: #808080;">Recommendations useful for Chairmen and directors of companies who want to prevent their image being damaged via the Web.</span>\n'
    '</td>\n</tr>\n'
    '<tr>\n<td class="article-cell" style="text-align: center;">\n'
    '<img alt="en couverture" decoding="async" src="./../wp-content/uploads/2020/01/chalengfem-300x201.jpg" style="max-width: 100%; height: auto;"/>\n'
    '</td>\n</tr>\n'
    '<tr>\n<td class="article-cell" data-i18n="page_bibliographie.dossier_approfondi_sur_les_femmes_administrat">\n'
    '<span style="text-decoration: underline;"><strong><span style="color: #000080; text-transform: uppercase;">In-depth dossier on female directors, 50 women qualified to sit on Boards of Directors and foreseeable trends</span></strong></span><br/>\n'
    '<span style="color: blue;">Challenges No. 15, October 2009</span><br/>\n'
    '<span style="color: black;">Anne-Marie Rocco</span>\n'
    '</td>\n</tr>\n'
    '<tr>\n<td class="article-cell" data-i18n="page_bibliographie.les_hedge_funds_sont_le_trou_noir_de_la_finan">\n'
    '<span style="text-decoration: underline;"><span style="color: #000080;"><strong><span style="text-transform: uppercase;">Hedge funds are the black hole of global finance</span></strong></span></span><br/>\n'
    '<span style="color: blue;">Interview with Daniel Le Bègue, Chairman of the IFA<br/>Le Monde, economics section, 23 September 2008</span><br/>\n'
    '<span style="color: #808080;">He recommends that all major economic and political actors issue "an appeal to the thirty largest global banks to turn away from the least reputable tax havens."</span>\n'
    '</td>\n</tr>\n'
    '<tr>\n<td class="article-cell" data-i18n="page_bibliographie.lobservatoire_de_la_gouvernance_altedia_la_tr">\n'
    '<span style="text-decoration: underline; color: #000080;"><strong><span style="text-transform: uppercase;">The Altedia-La Tribune Governance Observatory</span></strong></span><br/>\n'
    '<span style="color: blue;">La Tribune \u2013 16 October 2007 \u2013 Survey</span><br/>\n'
    '<span style="color: #808080;">The board of directors put to the test of practice<br/>Surveyed for the 5th consecutive year, French listed companies confirm their progress in governance. The strengthening of the role of committees reinforces the power of the board. But its functioning is far from optimal.</span>\n'
    '</td>\n</tr>\n'
    '<tr>\n<td class="article-cell" data-i18n="page_bibliographie.soft_regulation_not_rulesby_bruce_kogutnumero">\n'
    '<a href="http://madame.lefigaro.fr/societe/en-kiosque/2257-la-cle-de-la-parite/2">\n'
    '<span style="text-decoration: underline; color: #000080;"><strong>"Soft Regulation, not rules"</strong></span>\n'
    '</a><br/>\n'
    '<span style="color: blue;">by Bruce Kogut<br/>October 2006 issue of World Business</span><br/>\n'
    '<span style="color: black;">Gilles Fontaine</span><br/>\n'
    '<span style="color: #808080;">Strict laws and prison cannot substitute for adequate Boards of Directors and shareholders in steering managers.</span>\n'
    '</td>\n</tr>\n'
    '<tr>\n<td class="article-cell" data-i18n="page_bibliographie.dans_le_domaine_de_la_gouvernance_souvent_on_" style="text-align: center;">\n'
    '<span style="color: blue;">In the field of governance, it is often noted that ideas and recommendations have not yet been put into practice.<br/>If a historical list of articles identified by G &amp; S interests you, you can download it <a href="./../wp-content/uploads/2020/01/bibliopassee.doc" style="color: lightblue;">by clicking here</a></span>\n'
    '</td>\n</tr>\n</tbody>\n</table>\n</div>',

"page_bibliographie.liberation_29_05_2014_presenteisme_alibi_masc":
    '<span style="text-decoration: underline;"><strong><span style="color: #000080;"><a href="http://www.ft.com/intl/cms/s/0/3bdb9b68-f0cb-11e0-aec8-00144feab49a.html#axzz1bURIcX45" style="color: #000080;"><span style="text-transform: uppercase;">LIBERATION (29/05/2014)</span></a></span></strong></span><br/>\n'
    '<a href="http://www.liberation.fr/societe/2014/05/26/presenteisme-alibi-masculin-pour-eviter-les-taches-menageres_1027387">\n'
    '<span style="color: blue;">"Presenteeism: a male alibi to avoid household chores?"</span>\n'
    '</a><br/>\n'
    '<span style="color: black;">François Fatoux, Member of the equality laboratory</span><br/>\n'
    '<span style="color: #808080;">A remarkable and in-depth analysis of the five forms of presenteeism at work, the fifth form being "totally taboo, which overwhelmingly affects men who are relieved, without wanting to admit it, to have to stay \'stuck\' at work because going home early means preparing dinner, monitoring children\'s homework, feeding them, doing housework. It is still more pleasant to come home when everything is done."<br/>\n'
    '                                                G &amp; S sees this as one of the causes of the glass ceiling. Indeed, these accumulated late working hours, over a year for example, can result in good professional results. However, these good results, rather than the presence itself, will positively influence assessments and consequently the career progression of those who practise them.</span>',

"page_bibliographie.lentreprisefemmes_administratrices_je_vous_ai":
    '<a href="http://www.ft.com/intl/cms/s/0/3bdb9b68-f0cb-11e0-aec8-00144feab49a.html#axzz1bURIcX45">\n'
    '<span style="text-decoration: underline; color: #000080;"><strong>L\'ENTREPRISE</strong></span>\n'
    '</a><br/>\n'
    '<span style="color: blue;">"Women directors: I love you"</span>\n'
    '<span style="color: #808080;">CAC 40 companies are drawing from the pool of women business owners of SMEs to improve gender diversity on their board. Why not you?</span><br/>\n'
    '<span style="color: blue;">L\'Entreprise November 2010 No. 294</span><br/>\n'
    '<span style="color: black;">Corinne Corniou</span><br/>\n'
    '<span style="color: #808080;">An overview of the advances in CAC 40 boards and their directors</span>',

"page_bibliographie.sur_119_societes_cotees_sur_alternext_trois_s":
    '<span style="text-decoration: underline; color: #000080;"><strong><span style="text-transform: uppercase;">Of 119 listed companies on Alternext, three are led by women!</span></strong></span><br/>\n'
    '<span style="color: blue;">Challenges No. 193, 17 December 2009</span><br/>\n'
    '<span style="color: black;">Marc Fiorentino</span><br/>\n'
    '<span style="color: #808080;">After discussing his search for female executives in Alternext companies and noting their small number, he recommends buying shares in the three companies led by women.</span>',

"page_bibliographie.les_hedge_funds_sont_le_trou_noir_de_la_finan":
    '<span style="text-decoration: underline;"><span style="color: #000080;"><strong><span style="text-transform: uppercase;">Hedge funds are the black hole of global finance</span></strong></span></span><br/>\n'
    '<span style="color: blue;">Interview with Daniel Le Bègue, Chairman of the IFA<br/>Le Monde, economics section, 23 September 2008</span><br/>\n'
    '<span style="color: #808080;">He recommends that all major economic and political actors issue "an appeal to the thirty largest global banks to turn away from the least reputable tax havens."</span>',

"page_bibliographie.soft_regulation_not_rulesby_bruce_kogutnumero":
    '<a href="http://madame.lefigaro.fr/societe/en-kiosque/2257-la-cle-de-la-parite/2">\n'
    '<span style="text-decoration: underline; color: #000080;"><strong>"Soft Regulation, not rules"</strong></span>\n'
    '</a><br/>\n'
    '<span style="color: blue;">by Bruce Kogut<br/>October 2006 issue of World Business</span><br/>\n'
    '<span style="color: black;">Gilles Fontaine</span><br/>\n'
    '<span style="color: #808080;">Strict laws and prison cannot substitute for adequate Boards of Directors and shareholders in steering managers.</span>',

"page_bibliographie.dans_le_domaine_de_la_gouvernance_souvent_on_":
    '<span style="color: blue;">In the field of governance, it is often noted that ideas and recommendations have not yet been put into practice.<br/>If a historical list of articles identified by G &amp; S interests you, you can download it <a href="./../wp-content/uploads/2020/01/bibliopassee.doc" style="color: lightblue;">by clicking here</a></span>',

"page_bibliographie.au_cours_de_la_reunion_du_27_novembre_2016de1":
    '<div>\n<table class="table">\n<tbody>\n<tr>\n'
    '<td class="article-cell" data-i18n="page_bibliographie.au_cours_de_la_reunion_du_27_novembre_2016de1_2" style="text-align: left;">\n'
    '<a href="http://www.100womeninhedgefunds.org/pages/event.php?e=1225&amp;inc=A&amp;yr=0&amp;loc=12&amp;kw=&amp;p=1">\n'
    '<span style="color: red;">During the meeting on 27 November 2016</span> of<br/>\n'
    '<span style="color: blue;">100 Women in Hedge Funds on the topic</span><br/>\n'
    '<span style="color: black;">Women on Boards in Paris and Abroad \u2013 Where are We?</span>\n'
    '</a><br/>\n'
    '<span style="color: #808080;">Guy Le Péchon spoke as part of the panel discussion. He previewed the main results of G &amp; S studies on the 1,000 female directors of Boards of 400 companies listed on Euronext Paris tracked for 7 years by G &amp; S, <a href="./../wp-content/uploads/2020/01/wihf%20flyer.pdf">see leaflet</a></span>\n'
    '</td>\n</tr>\n'
    '<tr>\n<td class="article-cell" data-i18n="page_bibliographie.au_cours_de_la_matinale_du_23_juin_2014tenue_" style="text-align: left;">\n'
    '<span style="color: red;">During the morning event on 23 June 2014</span> held by the IFA<br/>\n'
    '<span style="color: blue;">"First lessons from the 2014 Annual General Meetings"</span><br/>\n'
    '<span style="color: #808080;">chaired by Caroline De La Marinière of Capital Com, she cited the initial estimates from G &amp; S concerning CAC 40 companies after reading the annual reports and 2014 AGM convening notices: the average ratio now slightly exceeds 30%. <a href="./../wp-content/uploads/2020/01/cb%20%25%202013%202014.pdf">See Charts</a></span>\n'
    '</td>\n</tr>\n'
    '<tr>\n<td class="article-cell" data-i18n="page_bibliographie.auforum_de_la_mixitedu_21_decembre_2012guy_le" style="text-align: left;">\n'
    '<span style="color: red;">At the <a href="http://www.forumdelamixite.com/" style="color: red;">Gender Diversity Forum</a> on 21 December 2012</span><br/>\n'
    '<span style="color: blue;">Guy Le Péchon was one of the speakers in the Leyders Associates workshop</span><br/>\n'
    '<span style="color: #808080;">"Positioning yourself to be board-ready. Feminising your board."<br/>\n'
    '                                                He mentioned the profiles of directors in numerous listed companies on Euronext and above all suggested convincing Chairmen to broaden co-optations of board members professionally.</span>\n'
    '</td>\n</tr>\n'
    '<tr>\n<td class="article-cell" data-i18n="page_bibliographie.le_29_mars_2012objectifcasha_organise_un_peti" style="text-align: left;">\n'
    '<span style="color: red;">On 29 March 2012</span><br/>\n'
    '<span style="color: blue;"><a href="http://www.objectifcash.com/">ObjectifCash</a> organised a Breakfast event "Chairwomen, Chairmen, Shareholders, stop waiting to co-opt qualified directors!"</span><br/>\n'
    '<span style="color: #808080;">Guy Le Péchon was the moderator. Find the "Finyear" article from one of the participants in <a href="https://g-et-s.com/la-presse-parle-de-gouvernance-structures/">the press kit</a></span>\n'
    '</td>\n</tr>\n'
    '<tr>\n<td class="article-cell" data-i18n="page_bibliographie.le_16_decembre_2011participation_de_g_s_a_lat" style="text-align: left;">\n'
    '<span style="color: red;">On 16 December 2011</span><br/>\n'
    '<span style="color: #808080;">Participation of G &amp; S in the "Board" workshop at the Gender Diversity Forum, to read the workshop report click <a href="https://www.g-et-s.com/french/docdech/formix.pdf">here</a></span>\n'
    '</td>\n</tr>\n'
    '<tr>\n<td class="article-cell" data-i18n="page_bibliographie.le_7_decembre_2011madame_la_deputee_marie_jos" style="text-align: left;">\n'
    '<span style="color: red;">On 7 December 2011</span><br/>\n'
    '<span style="color: blue;">MP Marie-José Zimmermann organised a morning meeting in the Salon Lamartine of the National Assembly on the theme:</span><br/>\n'
    '<span style="color: black;">« Chairmen and Chairwomen, where do we stand in the application of the Law of 27 January 2011 on the balanced representation of women and men on the boards of listed companies? »</span><br/>\n'
    '<span style="color: #808080;">Guy Le Péchon presented the G &amp; S study on the situation as of 30 June 2011 regarding directors on Boards of Directors and Supervisory Boards of 500 French listed companies on Euronext Paris.<br/>\n'
    '                                                The summary page highlighting the key elements presented can be downloaded by clicking <a href="./../wp-content/uploads/2020/01/synth712.pdf">here</a>.<br/>\n'
    '                                                Mr Jean-François Coppé, Ms Anne-Marie Rocco of the Challenges review and Ms Maryam SALEHI, Deputy Managing Director and Director of NRJ, then spoke in succession. An exchange with the audience followed. One of the conclusions of this morning event was that the Law was already today prompting reflection on the composition of Boards of Directors and Supervisory Boards, and would ultimately lead to better "Corporate Governance" of companies.<br/>\n'
    '                                                For any information send an email to <a href="mailto:info@g-et-s.com">info@g-et-s.com</a></span>\n'
    '</td>\n</tr>\n'
    '<tr>\n<td class="article-cell" data-i18n="page_bibliographie.le_10_octobre_2011a_lessec_viviane_de_beaufor" style="text-align: left;">\n'
    '<span style="color: red;">On 10 October 2011</span><br/>\n'
    '<span style="color: blue;">At ESSEC (Viviane De Beaufort) Launch meeting of the second session of the "Women Be European Board Ready" training.</span><br/>\n'
    '<span style="color: #808080;">The theme of this meeting was the recruitment of directors in France and England. Guy Le Péchon, representing the Institute of Directors, summarised the situation in England. To receive the slides from his presentation, simply send an email with your contact details to <a href="mailto:info@g-et-s.com">info@g-et-s.com</a></span>\n'
    '</td>\n</tr>\n'
    '<tr>\n<td class="article-cell" data-i18n="page_bibliographie.le_9_juin_2011une_conference_etait_organisee_" style="text-align: left;">\n'
    '<span style="color: red;">On 9 June 2011</span><br/>\n'
    '<span style="color: blue;">a conference was organised by the <a href="http://www.fbn-france.fr/">Business Family Network</a> association on the subject of the Law of 27 January 2011,</span><br/>\n'
    '<span style="color: #808080;">Ms Caroline Ressot, Secretary General of the Gender Parity Observatory and Guy Le Péchon of G &amp; S were able to present the previous situation, the Law and the developments taking shape.</span>\n'
    '</td>\n</tr>\n'
    '<tr>\n<td class="article-cell" data-i18n="page_bibliographie.le_29_avril_2011une_conference_etait_organise" style="text-align: left;">\n'
    '<span style="color: red;">On 29 April 2011</span><br/>\n'
    '<span style="color: blue;">a conference was organised by NYSE Euronext on "What kind of director for tomorrow?"</span><br/>\n'
    '<span style="color: #808080;">The dialogue initiated with Ms Maryse Aulagnon, Chairman and CEO, Groupe Affine, and director of Air France-KLM, Mr Alain Martel, Secretary General of the IFA, Ms Viviane Neiter, Director of Dolphin Intégration, of Prodware and non-voting member of Ginger Grontmij France, and Mr Guy Le Péchon, Managing Partner, G&amp;S, enabled the presentation to listed companies of the available means to meet the requirements of the gender parity law in boards.</span>\n'
    '</td>\n</tr>\n</tbody>\n</table>\n</div>\n'
    '<div class="mt-3">\n<table class="table">\n<tbody>\n<tr>\n'
    '<td data-i18n="page_bibliographie.notes_et_articles_publies_par_g_s" style="color: #0000ff; font-weight: 900; text-align: center;">Notes and articles published by G&amp; S</td>\n'
    '</tr>\n<tr>\n<td class="article-cell" data-i18n="page_bibliographie.relations_presse_de_gouvernance_structures_fl">\n'
    '<span style="color: red;">Press relations of Gouvernance &amp; Structures (<a href="http://g-et-s.agence-presse.net/feed/">RSS Feed</a>)</span><br/>\n'
    '<a href="https://g-et-s.com/exposes-articles-et-notes-publies-par-g-s/">Click here</a>\n'
    '</td>\n</tr>\n<tr>\n<td class="article-cell" data-i18n="page_bibliographie.blogs_lies_a_la_gouvernancearcafi_notesfinanc">\n'
    '<span style="color: red;">Governance-related blogs</span><br/>\n'
    '<a href="http://www.arcafi-notes.blogspot.com/">Arcafi-notes</a> <span style="color: #808080;">Finance-Business-Economics</span>\n'
    '</td>\n</tr>\n</tbody>\n</table>\n</div>\n'
    '<div class="mt-3">\n<table class="table">\n<tbody>\n<tr>\n'
    '<td data-i18n="page_bibliographie.rapports" style="color: #0000ff; font-weight: 900; text-align: center;">Reports</td>\n'
    '</tr>\n<tr>\n<td class="article-cell" data-i18n="page_bibliographie.lacces_des_femmes_aux_responsabilites_dans_le">\n'
    '<a href="http://ondirectorship.com/ondirectorship/j3xb9xcqpivwnw6dktyde495k7ktr0">\n'
    '<span style="color: blue;">Women\'s access to positions of responsibility in companies</span>\n'
    '</a><br/>\n'
    '<span style="color: black;">by Ms Marie-Jo Zimmermann, MP, Activity report</span><br/>\n'
    '<span style="color: #808080;">for 2009, submitted pursuant to Article 6 septies of Ordinance No. 58-1100 of 17 November 1958 relating to the functioning of parliamentary assemblies on behalf of the delegation for women\'s rights and equal opportunities between women and men.</span><br/>\n'
    '<span style="color: #000000; font-weight: bold;">A historical selection of reports identified by G &amp; S as interesting for corporate governance can be downloaded by <a href="./../wp-content/uploads/2020/01/rapports.doc">clicking here</a></span><br/>\n'
    '<span style="color: #000000;">For others, the websites of the <a href="http://www.ifa-asso.com/bonnes-pratiques/md/documents-utiles.php">IFA</a>, <a href="http://www.apia.asso.fr/373_p_10216/publications.html">APIA</a>, <a href="http://www.adae.asso.fr/accueil.php">ADAE</a> can be consulted.</span>\n'
    '</td>\n</tr>\n</tbody>\n</table>\n</div>\n'
    '<div class="mt-3">\n<table class="table">\n<tbody>\n<tr>\n'
    '<td data-i18n="page_bibliographie.livres" style="color: #0000ff; font-weight: 900; text-align: center;">Books</td>\n'
    '</tr>\n<tr>\n<td class="article-cell" data-i18n="page_bibliographie.administrateur_de_societe_pourquoi_pas_moi_me">\n'
    '                                                Company Director: Why not me?<br/>\n'
    '                                                Method and advice for searching for and obtaining a directorship mandate<br/>\n'
    '<a href="http://www.editions-eyrolles.com/Livre/9782212564198/administrateur-de-societes-pourquoi-pas-moi">(Yves Dumont, Eyrolles, 2016)</a>\n'
    '</td>\n</tr>\n<tr>\n<td class="article-cell" data-i18n="page_bibliographie.administrateur_e_au_femininguide_pour_devenir">\n'
    '<b><span style="color: #0000ff;">Women on Boards</span></b><br/>\n'
    '                                                Guide to becoming a female director<br/>\n'
    '                                                Collective work published by <a href="http://www.europeanpwn.net/paris">European Professional Women Network</a> (Paris)<br/>\n'
    '                                                March 2011<br/>\n'
    '<span style="color: #ff0000;">This guide can also be very useful for men wishing to become directors.</span>\n'
    '</td>\n</tr>\n<tr>\n<td class="article-cell" data-i18n="page_bibliographie.profession_administrateurscenes_de_vie_et_bon">\n'
    '<b><span style="color: #0000ff;">Profession: Director</span></b><br/>\n'
    '<span style="color: #0000cc;">Scenes from corporate life and best practices in companies (Guy Ferré, Editions du Palio)</span>\n'
    '<p data-i18n="page_bibliographie.grace_a_une_serie_detudes_de_cas_se_lisant_fa">Thanks to a series of case studies as easy to read as short detective novels, the author, drawing on his long practical experience as a director, presents the delicate and exciting side of the director\'s role. For each case, he comments and derives best governance practices.</p>\n'
    '</td>\n</tr>\n<tr>\n<td class="article-cell" data-i18n="page_bibliographie.une_liste_dautres_livres_reperes_par_g_scomme" style="font-weight: bold;">\n'
    '<span style="color: #000000;">A list of other books identified by G &amp; S<br/>\n'
    '                                                as interesting for corporate governance can be downloaded by <a href="./../wp-content/uploads/2020/01/livres.pdf">clicking here</a></span>\n'
    '</td>\n</tr>\n</tbody>\n</table>\n</div>\n'
    '<div class="mt-3">\n<table align="center" bgcolor="#CCCCCC" border="1" cellpadding="0" cellspacing="3" width="97%">\n<tbody>\n<tr>\n'
    '<td bgcolor="#CCCCCC" data-i18n="page_bibliographie.lactualite_nannihile_pas_les_ecrits_passes_im_2">\n'
    '<div align="center">\n<table border="0" cellpadding="0" cellspacing="3" width="99%">\n<tbody>\n<tr>\n'
    '<td bgcolor="#CCCCCC" data-i18n="page_bibliographie.lactualite_nannihile_pas_les_ecrits_passes_im_3">\n'
    '<p align="center" data-i18n="page_bibliographie.lactualite_nannihile_pas_les_ecrits_passes_im"><span style="color: #ff0000;"><b>Current events do not invalidate important past writings</b></span></p>\n'
    '<p align="center" data-i18n="page_bibliographie.un_extrait_du_rapport_bouton_concernantles_cr"><span style="color: #000099;"><b>An extract from the Bouton Report concerning<br/>the criteria for qualifying<br/>a director as "independent"<br/>is recalled here:</b></span></p>\n'
    '<p align="left" data-i18n="page_bibliographie.1_ni_mandataire_social_ni_salarie_actuel_ou_a"><span style="font-size: small;">\n'
    '                                                                        1- Neither corporate officer nor current (or past five years) employee.<br/>\n'
    '                                                                        2- Not a cross-director.<br/>\n'
    '                                                                        3- Not a significant client, supplier or banker (for business or financing purposes) or representing a significant share of the company\'s activity.<br/>\n'
    '                                                                        4- No close family ties with a corporate officer.<br/>\n'
    '                                                                        5- Neither partner nor current (or past five years) collaborator of the Statutory Auditors.<br/>\n'
    '                                                                        6- Not a director of the company for more than twelve years.<br/>\n'
    '                                                                        7- Shareholders:<br/>\n'
    '                                                                        \u2013 Below 10%: independent if not participating in control.<br/>\n'
    '                                                                        \u2013 Above 10%: review by the board, depending on the ownership structure and the existence of potential conflicts of interest.\n'
    '                                                                    </span></p>\n'
    '</td>\n</tr>\n</tbody>\n</table>\n</div>\n'
    '</td>\n</tr>\n</tbody>\n</table>\n</div>',

"page_bibliographie.le_29_mars_2012objectifcasha_organise_un_peti":
    '<span style="color: red;">On 29 March 2012</span><br/>\n'
    '<span style="color: blue;"><a href="http://www.objectifcash.com/">ObjectifCash</a> organised a Breakfast event "Chairwomen, Chairmen, Shareholders, stop waiting to co-opt qualified directors!"</span><br/>\n'
    '<span style="color: #808080;">Guy Le Péchon was the moderator. Find the "Finyear" article from one of the participants in <a href="https://g-et-s.com/la-presse-parle-de-gouvernance-structures/">the press kit</a></span>',

"page_bibliographie.le_7_decembre_2011madame_la_deputee_marie_jos":
    '<span style="color: red;">On 7 December 2011</span><br/>\n'
    '<span style="color: blue;">MP Marie-José Zimmermann organised a morning meeting in the Salon Lamartine of the National Assembly on the theme:</span><br/>\n'
    '<span style="color: black;">« Chairmen and Chairwomen, where do we stand in the application of the Law of 27 January 2011 on the balanced representation of women and men on the boards of listed companies? »</span><br/>\n'
    '<span style="color: #808080;">Guy Le Péchon presented the G &amp; S study on the situation as of 30 June 2011 regarding directors on Boards of Directors and Supervisory Boards of 500 French listed companies on Euronext Paris.<br/>\n'
    '                                                The summary page highlighting the key elements presented can be downloaded by clicking <a href="./../wp-content/uploads/2020/01/synth712.pdf">here</a>.<br/>\n'
    '                                                Mr Jean-François Coppé, Ms Anne-Marie Rocco of the Challenges review and Ms Maryam SALEHI, Deputy Managing Director and Director of NRJ, then spoke in succession. An exchange with the audience followed. One of the conclusions of this morning event was that the Law was already today prompting reflection on the composition of Boards of Directors and Supervisory Boards, and would ultimately lead to better "Corporate Governance" of companies.<br/>\n'
    '                                                For any information send an email to <a href="mailto:info@g-et-s.com">info@g-et-s.com</a></span>',

"page_bibliographie.le_29_avril_2011une_conference_etait_organise":
    '<span style="color: red;">On 29 April 2011</span><br/>\n'
    '<span style="color: blue;">a conference was organised by NYSE Euronext on "What kind of director for tomorrow?"</span><br/>\n'
    '<span style="color: #808080;">The dialogue initiated with Ms Maryse Aulagnon, Chairman and CEO, Groupe Affine, and director of Air France-KLM, Mr Alain Martel, Secretary General of the IFA, Ms Viviane Neiter, Director of Dolphin Intégration, of Prodware and non-voting member of Ginger Grontmij France, and Mr Guy Le Péchon, Managing Partner, G&amp;S, enabled the presentation to listed companies of the available means to meet the requirements of the gender parity law in boards.</span>',

"page_bibliographie.lacces_des_femmes_aux_responsabilites_dans_le":
    '<a href="http://ondirectorship.com/ondirectorship/j3xb9xcqpivwnw6dktyde495k7ktr0">\n'
    '<span style="color: blue;">Women\'s access to positions of responsibility in companies</span>\n'
    '</a><br/>\n'
    '<span style="color: black;">by Ms Marie-Jo Zimmermann, MP, Activity report</span><br/>\n'
    '<span style="color: #808080;">for 2009, submitted pursuant to Article 6 septies of Ordinance No. 58-1100 of 17 November 1958 relating to the functioning of parliamentary assemblies on behalf of the delegation for women\'s rights and equal opportunities between women and men.</span><br/>\n'
    '<span style="color: #000000; font-weight: bold;">A historical selection of reports identified by G &amp; S as interesting for corporate governance can be downloaded by <a href="./../wp-content/uploads/2020/01/rapports.doc">clicking here</a></span><br/>\n'
    '<span style="color: #000000;">For others, the websites of the <a href="http://www.ifa-asso.com/bonnes-pratiques/md/documents-utiles.php">IFA</a>, <a href="http://www.apia.asso.fr/373_p_10216/publications.html">APIA</a>, <a href="http://www.adae.asso.fr/accueil.php">ADAE</a> can be consulted.</span>',

"page_bibliographie.profession_administrateurscenes_de_vie_et_bon":
    '<b><span style="color: #0000ff;">Profession: Director</span></b><br/>\n'
    '<span style="color: #0000cc;">Scenes from corporate life and best practices in companies (Guy Ferré, Editions du Palio)</span>\n'
    '<p data-i18n="page_bibliographie.grace_a_une_serie_detudes_de_cas_se_lisant_fa">Thanks to a series of case studies as easy to read as short detective novels, the author, drawing on his long practical experience as a director, presents the delicate and exciting side of the director\'s role. For each case, he comments and derives best governance practices.</p>',

"page_bibliographie.lactualite_nannihile_pas_les_ecrits_passes_im_2":
    '<div align="center">\n<table border="0" cellpadding="0" cellspacing="3" width="99%">\n<tbody>\n<tr>\n'
    '<td bgcolor="#CCCCCC" data-i18n="page_bibliographie.lactualite_nannihile_pas_les_ecrits_passes_im_3">\n'
    '<p align="center" data-i18n="page_bibliographie.lactualite_nannihile_pas_les_ecrits_passes_im"><span style="color: #ff0000;"><b>Current events do not invalidate important past writings</b></span></p>\n'
    '<p align="center" data-i18n="page_bibliographie.un_extrait_du_rapport_bouton_concernantles_cr"><span style="color: #000099;"><b>An extract from the Bouton Report concerning<br/>the criteria for qualifying<br/>a director as "independent"<br/>is recalled here:</b></span></p>\n'
    '<p align="left" data-i18n="page_bibliographie.1_ni_mandataire_social_ni_salarie_actuel_ou_a"><span style="font-size: small;">\n'
    '                                                                        1- Neither corporate officer nor current (or past five years) employee.<br/>\n'
    '                                                                        2- Not a cross-director.<br/>\n'
    '                                                                        3- Not a significant client, supplier or banker (for business or financing purposes) or representing a significant share of the company\'s activity.<br/>\n'
    '                                                                        4- No close family ties with a corporate officer.<br/>\n'
    '                                                                        5- Neither partner nor current (or past five years) collaborator of the Statutory Auditors.<br/>\n'
    '                                                                        6- Not a director of the company for more than twelve years.<br/>\n'
    '                                                                        7- Shareholders:<br/>\n'
    '                                                                        \u2013 Below 10%: independent if not participating in control.<br/>\n'
    '                                                                        \u2013 Above 10%: review by the board, depending on the ownership structure and the existence of potential conflicts of interest.\n'
    '                                                                    </span></p>\n'
    '</td>\n</tr>\n</tbody>\n</table>\n</div>',

"page_bibliographie.lactualite_nannihile_pas_les_ecrits_passes_im_3":
    '<p align="center" data-i18n="page_bibliographie.lactualite_nannihile_pas_les_ecrits_passes_im"><span style="color: #ff0000;"><b>Current events do not invalidate important past writings</b></span></p>\n'
    '<p align="center" data-i18n="page_bibliographie.un_extrait_du_rapport_bouton_concernantles_cr"><span style="color: #000099;"><b>An extract from the Bouton Report concerning<br/>the criteria for qualifying<br/>a director as "independent"<br/>is recalled here:</b></span></p>\n'
    '<p align="left" data-i18n="page_bibliographie.1_ni_mandataire_social_ni_salarie_actuel_ou_a"><span style="font-size: small;">\n'
    '                                                                        1- Neither corporate officer nor current (or past five years) employee.<br/>\n'
    '                                                                        2- Not a cross-director.<br/>\n'
    '                                                                        3- Not a significant client, supplier or banker (for business or financing purposes) or representing a significant share of the company\'s activity.<br/>\n'
    '                                                                        4- No close family ties with a corporate officer.<br/>\n'
    '                                                                        5- Neither partner nor current (or past five years) collaborator of the Statutory Auditors.<br/>\n'
    '                                                                        6- Not a director of the company for more than twelve years.<br/>\n'
    '                                                                        7- Shareholders:<br/>\n'
    '                                                                        \u2013 Below 10%: independent if not participating in control.<br/>\n'
    '                                                                        \u2013 Above 10%: review by the board, depending on the ownership structure and the existence of potential conflicts of interest.\n'
    '                                                                    </span></p>',

# ── page_candidats_mandataires ────────────────────────────────────────────────
"page_candidats_mandataires.les_informations_communiquees_par_ce_formulai":
    'The information provided through this form to G &amp; S will enable G &amp; S to quickly identify a match between your profile and those of the directors sought by G &amp; S on behalf of its clients and, if so, to potentially contact you.',

"page_candidats_mandataires.les_informations_demandees_dans_ce_formulaire":
    'The information requested in this form is therefore deliberately limited to the essentials. G &amp; S will take care, as soon as it becomes useful, to enrich it with you during subsequent contacts.',

"page_candidats_mandataires.une_langue_sera_consideree_comme_courante_si_":
    'A language will be considered as fluent if you are able to use it without difficulty, both orally and in writing, in a professional context.',

# ── page_catalogue_documents ──────────────────────────────────────────────────
"page_catalogue_documents.lapplication_considere_que_pour_chaque_sujet_":
    'The application considers that for each subject covered, there is a "standard document", essentially a generic document called "Income Statement", to which it is possible to associate, depending on the use cases, particular characteristics such as the publication frequency, the level of completion or confidentiality.',

"page_catalogue_documents.une_centaine_de_ces_documents_generiques_docu":
    'About one hundred of these generic documents, "standard documents", have been catalogued.<br/>\n'
    '                    The catalogue presents for each of them the title and the various parameters identified as associated with that document.<br/>\n'
    '                    The application allows sorting, queries and list printing.',

"page_catalogue_documents.les_explications_detaillees_dans_un_document_":
    'Detailed explanations in a .pdf document as well as a demonstration appointment can be obtained from G &amp; S by sending a request email with contact details and the position of the person to contact to <a href="mailto:contact@g-et-s.com">contact@g-et-s.com</a>',

# ── page_dsi_conseils_administration ─────────────────────────────────────────
"page_dsi_conseils_administration.le_rappel_de_cette_intervention_souligne_comb":
    'This reminder of the presentation highlights how the dialogue between the IT management and the board of directors has become a major issue for companies engaged in their digital transformation.',

# ── page_formations_administrateurs ──────────────────────────────────────────
"page_formations_administrateurs.inseadinternational_directors_programexecutiv":
    '<table align="center" border="0" cellpadding="0" cellspacing="3" width="95%">\n<tbody>\n'
    '<tr>\n<td data-i18n="page_formations_administrateurs.inseadinternational_directors_programexecutiv_2" style="border: solid 1px #c7d1dac7;">\n'
    '<div align="center">\n'
    '<p data-i18n="page_formations_administrateurs.insead"><b><span style="color: #0000a0;">INSEAD</span></b></p>\n'
    '<p align="center" data-i18n="page_formations_administrateurs.international_directors_program"><a href="https://www.insead.edu/executive-education/corporate-governance/aspiring-directors-programme?_ref=finder"><span style="color: #000000;">International Directors Program</span></a></p>\n'
    '<p align="center" data-i18n="page_formations_administrateurs.executive_educationvision_tres_internationale"><span style="color: #0000ff;">Executive Education<br/>Highly international vision</span></p>\n'
    '</div>\n</td>\n</tr>\n'
    '<tr>\n<td data-i18n="page_formations_administrateurs.ifa_cdainstitut_francais_des_administrateursd" style="border: solid 1px #c7d1dac7;">\n'
    '<p align="center" data-i18n="page_formations_administrateurs.ifa_cdainstitut_francais_des_administrateurs"><b><span style="color: #0000a0;">IFA - CDA<br/>French Institute of Directors</span></b></p>\n'
    '<p align="center" data-i18n="page_formations_administrateurs.divers_programmes_certifiants"><span style="color: #0000a0;"><a href="https://www.ifa-asso.com/formations/les-programmes-certifiants/"><span style="color: #000000;">Various certification programmes</span></a></span></p>\n'
    '<p align="center"><a href="https://lnk.pmlto-etao-3.ovh/vbqjJ3cXSr3KAnaWWHGzuhTVA/103117121046108101045112101099104111110064103045101116045115046099111109/m97rV1700661/versionWeb.html" rel="noopener" target="_blank"><img alt="IFA Formation" src="../images/image002.png" style="max-width: 100%; height: auto;"/></a></p>\n'
    '</td>\n</tr>\n'
    '<tr>\n<td data-i18n="page_formations_administrateurs.adaeass_des_administrateurs_et_dirigeants_den_2" style="border: solid 1px #c7d1dac7;">\n'
    '<p align="center" data-i18n="page_formations_administrateurs.adaeass_des_administrateurs_et_dirigeants_den"><a align="center" href="https://www.club-adae.fr/%F0%9F%9A%80-devenez-un-administrateur-qualifie-independant-avec-ladae/" target="_blank"><span style="color: #000000;"><b><span style="color: #0000cc;">ADAE </span><span style="color: #0000cc;">Ass. of Directors and Company Executives</span></b></span></a></p>\n'
    '</td>\n</tr>\n'
    '<tr>\n<td data-i18n="page_formations_administrateurs.essecwomen_be_european_board_readyreserve_aux" style="border: solid 1px #c7d1dac7;">\n'
    '<div align="center">\n'
    '<p data-i18n="page_formations_administrateurs.essec"><b><span style="color: #0000a0;">ESSEC</span></b></p>\n'
    '<p align="center" data-i18n="page_formations_administrateurs.women_be_european_board_ready"><a href="https://www.club-adae.fr/%F0%9F%9A%80-devenez-un-administrateur-qualifie-independant-avec-ladae/"><span style="color: #000000;">Women Be European Board Ready</span></a></p>\n'
    '<p align="center" data-i18n="page_formations_administrateurs.reserve_aux_femmes"><span style="color: #0000ff;">Reserved for women</span></p>\n'
    '</div>\n</td>\n</tr>\n'
    '<tr>\n<td data-i18n="page_formations_administrateurs.m_lyon_business_schoolcertificatvoir_presenta" height="89" style="border: solid 1px #c7d1dac7;">\n'
    '<p align="center" data-i18n="page_formations_administrateurs.m_lyon_business_schoolcertificat"><span style="color: #000000;"><b><span style="color: #0000cc;">M LYON BUSINESS SCHOOL</span><span style="color: #0000cc;">Certificate</span></b></span></p>\n'
    '<p align="center" data-i18n="page_formations_administrateurs.voir_presentation"><a href="https://executive.em-lyon.com/Formations/Certificats/OA-Objectif-Administratrice">See presentation</a></p>\n'
    '</td>\n</tr>\n'
    '<tr>\n<td data-i18n="page_formations_administrateurs.institute_of_directorsformation_pour_la_certi" style="border: solid 1px #c7d1dac7;">\n'
    '<div align="center">\n'
    '<p data-i18n="page_formations_administrateurs.institute_of_directors"><b><span style="color: #0000a0;">Institute Of Directors</span></b></p>\n'
    '<p align="center" data-i18n="page_formations_administrateurs.formation_pour_la_certification_commechartere"><span style="color: #000000;">Training for certification as <a href="http://www.iod.com/Home/Training-and-Development/Chartered-Director/">"Chartered Director"</a>, for directors of UK companies</span></p>\n'
    '</div>\n</td>\n</tr>\n</tbody>\n</table>',

# ── page_glossaire_prestations ────────────────────────────────────────────────
"page_glossaire_prestations.dans_le_cadre_dune_enquete_menee_par_une_equi":
    'As part of a survey conducted by a team from the <a href="https://www.xmp-consult.org/agenda/webinar-intelligence-collective-10196" style="color: #1e73be;" target="_blank">XMP Consult</a> association, an association of independent consultants from top universities, among such executives, and the publication of the results of this survey in their <a href="https://www.xmp-consult.org/global/gene/link.php?doc_id=150&amp;fg=1" style="color: #1e73be;" target="_blank">annual letter of February 2025</a>, in which G &amp; S contributed two articles, it was deemed useful to include a glossary of consulting services to facilitate the choice between this type of service.',

"page_glossaire_prestations.larticle_propose_une_classification_des_diffe":
    'The article proposes a classification of the different types of consulting services and for each a summary explaining their content.',

"page_glossaire_prestations.quand_un_dirigeant_est_face_a_un_probleme_et_":
    'When an executive faces a problem and asks themselves which consulting service to call upon to help solve it, quickly reviewing this glossary should provide useful guidance.',

# ── page_historique ───────────────────────────────────────────────────────────
"page_historique.ainsi_dernierement_g_s_a_mene_une_etude_appro":
    'Most recently G&amp;S has led an in-depth study on the place of women corporate officers in 550 French companies listed on Euronext, and previously an original survey — at the time — on the topic of "governance, performance and modernity", a survey conducted in collaboration with ADAE and the company Acadys among a sample comprising mid-sized companies and subsidiaries of foreign groups.',

"page_historique.le_petit_dejeuner_organise_debut_juillet_2009_2":
    '<div align="center">\n'
    '<p align="center" data-i18n="page_historique.le_petit_dejeuner_organise_debut_juillet_2009"><span style="color: #0033cc;">The breakfast event organised in early July 2009</span></p>\n'
    '<p align="center" data-i18n="page_historique.par"><span style="color: #0033cc;"><br/>by</span></p>\n'
    '<p align="center" data-i18n="page_historique.le_club_mixite_et_le_cercle_des_administrateu"><span style="color: #0033cc;"><br/>the Gender Diversity Club, and the Directors\' Circle<br/>INSEAD ALUMNI ASSOCIATION FRANCE<br/>on the topic:</span></p>\n'
    '<p align="center" data-i18n="page_historique.la_place_des_femmes_administrateurs_dans_les_"><br/><b><span style="color: #000066;">« The place of women directors in French listed companies »</span></b></p>\n'
    '<p align="center" data-i18n="page_historique.a_rassemble_plus_dune_soixantaine_de_particip"><br/>brought together more than sixty participants</p>\n'
    '<p align="center" data-i18n="page_historique.voir_les_photos_dans_la_colonne_de_gauche">See photos in the left column</p>\n'
    '<p align="center" data-i18n="page_historique.le_theme_a_ete_introduit_par_guy_le_pechon_as">The theme was introduced by Guy Le Péchon, Associate/Managing Partner of</p>\n'
    '<p align="center" data-i18n="page_historique.gouvernance_structures_par_une_presentation_d"><br/>Gouvernance &amp; Structures through a presentation of the main results of the in-depth study he conducted in more than 500 French listed companies on the A, B and C markets of Euronext</p>\n'
    '<p align="center" data-i18n="page_historique.pour_teledecharger_le_programme_de_cet_evenem"><span style="color: #ff0000;">To download the programme of this event</span> <a href="./../wp-content/uploads/2020/01/invifad.pdf">click here</a><br/><span style="color: #ff0000;">To browse the first slides of the presentation</span> <a href="./../wp-content/uploads/2020/01/debpres.pdf">click here.</a><br/><span style="color: #ff0000;">To obtain extracts from the study, send an email to</span> <a href="mailto:info@g-et-s.com">info@g-et-s.com</a> specifying your full name, contact details and position.</p>\n'
    '</div>',

# ── page_informatique ─────────────────────────────────────────────────────────
"page_informatique.g_s_a_en_tete_des_ateliers_dune_journee_selon":
    'G &amp; S has in mind one-day workshops following an original "hands-on" approach with qualified partners, each time on a specific topic such as:',

"page_informatique.en_sappuyant_sur_des_ateliers_proposes_dans_l":
    'Drawing on workshops offered in the past, such as the behaviour of men and women in Boards or the use of personal computers, today the focus would be on the use of social media; G &amp; S can organise specific workshops.',

# ── page_intelligence_collective ─────────────────────────────────────────────
"page_intelligence_collective.un_atelier_en_presentiel_ou_distanciel_peut_e":
    'An in-person or remote workshop can be organised by G &amp; S to introduce the use of collective intelligence within a company or an organisation, <a href="https://www.xmp-consult.org/agenda/webinar-intelligence-collective-10196">along the lines of this one conducted remotely</a> for around thirty members of the association of independent consultants from top universities <strong><a href="https://www.xmp-consult.org/">XMP Consult</a></strong>.',

# ── page_livre_eti ────────────────────────────────────────────────────────────
"page_livre_eti.pour_chaque_evolution_du_monde_etudiee_vous_d":
    'For each major global development studied, you will discover how mid-cap companies (ETIs) can adapt and create value through appropriate governance.',

# ── page_livre_eti_new ────────────────────────────────────────────────────────
"page_livre_eti_new.pour_chaque_evolution_du_monde_etudiee_vous_d":
    'For each major global development studied, you will discover how mid-cap companies (ETIs) can adapt and create value through appropriate governance.',

# ── page_mentions_legales ─────────────────────────────────────────────────────
"page_mentions_legales.les_utilisateurs_du_site_g_et_s_com_sont_tenu":
    'Users of the G-et-S.com website are required to comply with the provisions of the Data Protection and Civil Liberties Act, the violation of which is subject to criminal penalties.<br/>They must notably refrain, with regard to personal data they may access, from any collection, any misuse, and in general, from any act likely to infringe the privacy or reputation of individuals.<br/>In accordance with Article 34 of the "IT and Liberties" Law No. 78-17 of 6 January 1978, the user has the right of access, modification, rectification and deletion of data concerning them. G &amp; S is committed to complying with the GDPR Law of May 2018. This right can be exercised by sending a letter <a href="contact.html">to our registered office of G &amp; S</a> specifying the nature of the request.',

"page_mentions_legales.les_informations_fournies_par_linternaute_lor":
    'Information provided by the user, when recorded by G &amp; S, is considered by G &amp; S as not to be disclosed to a third party without the user\'s consent, but G &amp; S, despite the precautions taken (SSL encryption), cannot absolutely guarantee confidentiality during the internet transmission process of messages. In the event that the user wishes to transmit strictly confidential information, they must contact G &amp; S directly (see <a href="contact.html">contacts</a>).',

"page_mentions_legales.en_permanence_g_s_fait_tous_ses_efforts_pour_":
    'G &amp; S constantly makes every effort to ensure that the information presented on its website is accurate, but the user will in no way be able to consider G &amp; S responsible for any inaccuracy or error and will not be able to claim any damages from G &amp; S in the event that such an error has caused them prejudice.',

"page_mentions_legales.le_contenu_mis_en_ligne_par_g_s_constitue_une":
    'The content published online by G &amp; S constitutes a work of the mind within the meaning of the Intellectual Property Code. G &amp; S owns the texts and data, as well as the trademarks, illustrations and graphic elements such as logos, designs and models, or has obtained the right to use them. G &amp; S holds all related intellectual property rights. Any total or partial reproduction of this website and its content, by any means whatsoever, without prior written express authorisation from the company G &amp; S, is prohibited and would constitute an infringement punishable under Articles L335-2 et seq. of the Intellectual Property Code.',

# ── page_questionnaire_rixain_societes ───────────────────────────────────────
"page_questionnaire_rixain_societes.lapplication_de_la_loi_rixain_ayant_commence_":
    'With the application of the Rixain Law having begun, G &amp; S felt it would be very interesting for all stakeholders in the field to have access to the results of a survey of the companies concerned by this Law, in order to understand how they were progressively organising themselves to comply with it.',

"page_questionnaire_rixain_societes.g_s_a_elabore_un_questionnaire_et_la_mis_en_l":
    'G &amp; S developed a questionnaire and put it online. Then, via a mailing, proposed to companies completing it anonymously to subsequently retrieve the survey results in order to benchmark themselves against their peers and obtain ideas to improve their own process for achieving the objectives of the Law.',

"page_questionnaire_rixain_societes.votre_societe_peut_avoir_plusieurs_instances_":
    'Your company may have several governing bodies; for the sake of simplification and consistency in the survey, we ask you to answer the questions about the governing body considered as the main one.<br/>\n'
    '                The members of the other governing bodies are part of the group studied further on, in the "Senior Executives" section.',

"page_questionnaire_rixain_societes.g_s_en_particulier_par_sesgouvernance_advisor":
    'G &amp; S, in particular through its <a href="../gouvernance-advisors/index.html" style="color: #1e73be; text-decoration: underline;">Governance Advisors</a> specialising in HR and communications, is available to provide advice to companies having to implement the Rixain Law, in particular regarding the planned composition of their Executive Committees or CODIRs and how to build their talent pools.',

# ── page_salarie_dirigeants_confiance ─────────────────────────────────────────
"page_salarie_dirigeants_confiance.je_fus_aussi_amuse_de_retrouver_des_anecdotes":
    'I was also amused to find anecdotes similar to my own, for example, seeing the author convince people, by putting it into practice, of the value of the "PERT" method for planning multiple nested tasks within a project. The author had to show great tenacity to obtain computing time! The PERT method, innovative at the time, was made practicable thanks to the still very limited power of existing computers. Data had to be entered using punched cards and at least one hour of calculation was required to process a network of 500 tasks. Today, on a personal computer, once the data has been entered on screen, a few seconds suffice to process and display the coloured results on screen.',

"page_salarie_dirigeants_confiance.lattention_du_lecteur_ayant_ete_ainsi_acquise":
    'Having thus captured the reader\'s attention, the latter, particularly if they lead a company and wish to broaden their knowledge of corporate governance, will find in the remainder of the book an in-depth analysis of company models derived from or related to the "Liberated Company" approach, with an exemplary implementation by the company FAVI. Models that place extensive trust in staff members organised in autonomous units.',

"page_salarie_dirigeants_confiance.utilisant_cette_experience_personnelle_y_comp":
    'Drawing on this personal experience, including as a professor and lecturer as well as his intimate knowledge of these models, the author then describes the model he advocates. He called it "Janus", perhaps in reference to the Roman god Janus, the two-headed god capable of opening both doors towards the past and the future. In a detailed and very open manner, he describes his model with tables on how to apply it. A very useful section, for those — consultants rather than executives themselves, no doubt — who wish to implement his model to transform a company.',

"page_salarie_dirigeants_confiance.le_livre_contient_divers_schemas_illustrant_l":
    'The book contains various diagrams illustrating the author\'s vision, which I readily share: "a complex idea only truly exists if it can be presented through a diagram." A deeply underlying question: "Can one think and communicate without words?" Personally, I believe one can.',

"page_salarie_dirigeants_confiance.lauteur_regrette_de_voir_que_ces_modeles_sont":
    'The author regrets seeing that these models are rarely applied in France. Given the numerous contacts he has cultivated, could he dedicate time to producing an assessment explaining the reasons for executives\' lack of interest in putting these models — including his own! — into practice, and suggest recommendations? That could be the subject of his next book.',

# ── page_shadow_conseil ───────────────────────────────────────────────────────
"page_shadow_conseil.sans_doute_pas_vraiment_en_effet_sauf_cas_tou":
    'Probably not really, except in truly exceptional cases, essentially in the field of new technologies, given the experience required to be a qualified director; these young board members would be at least 35 years old and would therefore no longer be truly young. Furthermore, in the under-60 age bracket, qualified candidates often have an intense full-time professional career, for example as an employed Director of their company. Being simultaneously a board member should develop, but still raises practical problems of availability, employer agreement, possible conflicts of interest, etc.',

"page_shadow_conseil.lapproche_suggeree_par_ce_billet_par_gouverna":
    'The approach suggested in this article by Gouvernance &amp; Structures is, under the stewardship of the Board of Directors, to create a <strong>Youth Board</strong>. With slightly different objectives, some Municipalities use this approach. This Youth Board would be composed of around ten volunteers aged 18 to 25, with their expenses covered. They would be recruited through "internet" announcements for 3 years (with renewal of one third each year), aiming for gender parity and a wide diversity of backgrounds. They would be supervised by the Secretary of the Board of Directors assisted by an HR manager.',

"page_shadow_conseil.le_conseil_en_leur_fournissant_la_documentati":
    'The Board, by providing them with the necessary documentation, would ask them, say three times a year, to reflect on a topic to be examined at an upcoming Board meeting and to make proposals. One can think of questions on which young people can be particularly sensitive: new technologies including social media and data protection, ecology, ethics, international matters\u2026 Once a year, one of these topics would be the subject of a half-day direct exchange with the physical presence of board members at one of their meetings.',

"page_shadow_conseil.la_formule_serait_legere_et_nentrainerait_pas":
    'The formula would be light and would not incur significant expenditure; it would allow board members in a flexible and convivial setting to be positively and concretely exposed to the ideas of young people and, why not, to retain some of them for implementation.',

"page_shadow_conseil.les_jeunes_en_tireraient_surement_un_profit_p":
    'Young people would surely derive personal benefit from it, and indirectly their close ones too. Indeed, they would thus gain an opening onto "Corporate Governance" of companies and their senior executives.',

# ── page_travaux_ifa_digital ──────────────────────────────────────────────────
"page_travaux_ifa_digital.ce_rapport_a_fait_lobjet_dune_etude_specifiqu":
    'This report was the subject of a specific study by G &amp; S with a pilot of an online IT application offering a catalogue of around one hundred documents identified for directors.',

}


def main():
    with open(EN_JSON, 'r', encoding='utf-8') as f:
        en = json.load(f)

    patched = 0
    for full_key, val in PATCHES.items():
        ns, key = full_key.split('.', 1)
        if ns not in en:
            en[ns] = {}
        en[ns][key] = val
        patched += 1

    with open(EN_JSON, 'w', encoding='utf-8') as f:
        json.dump(en, f, ensure_ascii=False, indent=2)

    print(f"Patched {patched} entries.")


if __name__ == '__main__':
    main()
