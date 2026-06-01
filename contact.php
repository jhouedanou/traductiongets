<?php session_start(); if (empty($_SESSION['csrf_token'])) $_SESSION['csrf_token'] = bin2hex(random_bytes(32)); ?>
<!DOCTYPE html>
<html lang="fr">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Contact - G-ET-S</title>
	<link href="css/theme.css" rel="stylesheet" type="text/css">
	<link href="styles.css" rel="stylesheet" type="text/css">
	<link rel="stylesheet" href="bootstrap/css/bootstrap.min.css" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
	<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css" rel="stylesheet">
	<script src="bootstrap/js/bootstrap.min.js" integrity="sha384-0pUGZvbkm6XF6gxjEnlmuGrJXVbNuzT9qBBavbLwCsOGabYfZo0T0to5eqruptLy" crossorigin="anonymous"></script>
	<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
	<script src="js/includes.js"></script>
	<style>
		body { background-color: #efefef; }
		.contact-wrapper { max-width: 900px; margin: 40px auto; background: #fff; border-radius: 12px; box-shadow: 0 10px 24px rgba(0,0,0,0.08); }
		.contact-header { padding: 24px; border-bottom: 1px solid #e9ecef; text-align: center; }
		.contact-body { padding: 24px; }
	</style>
</head>
<body>
	<div id="header-placeholder"></div>
	<div id="nav-placeholder"></div>
	<main class="container">
		<div class="contact-wrapper">
			<div class="contact-header">
				<h1 class="h4 mb-0">FORMULAIRE POUR CANDIDATS</h1>
			</div>
			<div class="contact-body">
				<div class="row">
					<div class="col-lg-6">
						<div class="p-3">
							<p class="text-center">Pour communiquer à Gouvernance &amp; Structures<br>votre projet personnel<br><strong>MERCI</strong><br>de remplir le formulaire ci-dessous</p>
							<p class="text-center">&nbsp;</p>
							<p class="text-center">À ce stade un CV est inutile.</p>
							<p class="text-center">&nbsp;</p>
							<p class="text-center">Les éléments figurant en bleu sont indispensables,<br>les autres sont souhaités.</p>
							<p class="text-center">&nbsp;</p>
							<p class="text-center">Le formulaire paraît long du seul fait que certaines rubriques peuvent être, mais ne le sont pas nécessairement, remplies plusieurs fois différemment.</p>

							<div class="mt-4">
								<p><img decoding="async" class="d-block mx-auto" src="./../wp-content/uploads/2020/01/saisie3-235x300.jpg" alt="" width="235" height="300"></p>
								<div>
									<p><strong style="color:#000066;">POSTULER À DES POSTES D'ADMINISTRATEURS</strong></p>
									<p><strong>Pour favoriser les Conseils d'Administration composés d'administrateurs qualifiés et professionnels,</strong> G &amp; S souhaite connaître des postulants à un poste d'administrateur susceptibles d'intéresser des entreprises.</p>
								</div>
								<p style="font-size: small;">Si, en tant que personne physique, vous envisagez de devenir un administrateur qualifié d'un Conseil d'Administration, G &amp; S vous invite à parcourir son site. Celui-ci vous donnera des informations vraisemblablement utiles pour votre recherche.</p>
								<p style="font-size: small;">G &amp; S est intéressé à connaître votre projet et votre profil pour les recherches d'administrateurs menées par G &amp; S pour le compte d'entreprises. Si vous êtes dans ce cas, remplissez le formulaire à droite.</p>
								
								<p><strong>UTILISATION PAR G &amp; S DES INFORMATIONS DU FORMULAIRE</strong></p>
								<p style="font-size: small;">Les informations communiquées par ce formulaire à G &amp; S permettront à G &amp; S de rapidement détecter une adéquation entre votre profil et ceux des administrateurs recherchés par G &amp; S pour le compte de ses clients et, si tel est le cas, de pouvoir éventuellement vous contacter.</p>
								<p style="font-size: small;">Les informations demandées dans ce formulaire sont donc volontairement limitées à l'essentiel. G &amp; S veillera, dès que cela sera utile, à les enrichir avec vous lors de contacts ultérieurs.</p>
								<p style="font-size: small;">Votre identité ne sera pas révélée à quiconque en dehors des consultants de G &amp; S sans votre accord.</p>
								<p style="font-size: small;">Voir <a href="https://www.g-et-s.com/french/legal.htm" target="_blank" rel="noopener">éléments juridiques</a>.</p>
								
								<p><strong style="color:#0000cc;">Indications pour le remplissage du formulaire</strong></p>
								<ul style="font-size: small; color:#0000cc;">
									<li>Un secteur d'activité correspond en général à un marché (ex. secteur bancaire, emballage, électronique grand public...).</li>
									<li>Un pays d'activité est un pays où vous avez vécu au moins une année et dont vous connaissez la vie professionnelle et la culture.</li>
									<li>Une langue sera considérée comme courante si vous pouvez la pratiquer sans problème par oral et écrit dans la vie professionnelle.</li>
								</ul>
							</div>
						</div>
					</div>
					<div class="col-lg-6">
						<form class="row g-3" action="send-contact.php" method="post">
							<input type="hidden" name="csrf_token" value="<?php echo $_SESSION['csrf_token']; ?>">
							<!-- Honeypot anti-spam -->
							<div style="position:absolute;left:-9999px;" aria-hidden="true">
								<input type="text" name="website_url" tabindex="-1" autocomplete="off">
							</div>
							<div class="col-md-6">
								<label class="form-label text-primary fw-bold" for="email">Adresse électronique *</label>
								<input type="email" class="form-control" id="email" name="Email" placeholder="Email" required>
							</div>
							<div class="col-md-6">
								<label class="form-label text-primary fw-bold" for="civilite">Civilité *</label>
								<select id="civilite" name="Civilite" class="form-select" required>
									<option value="Mr.">Mr.</option>
									<option value="Mde.">Mde.</option>
									<option value="Mlle.">Mlle.</option>
								</select>
							</div>
							<div class="col-md-6">
								<label class="form-label" for="nom">Nom</label>
								<input type="text" class="form-control" id="nom" name="Nom" placeholder="Nom">
							</div>
							<div class="col-md-6">
								<label class="form-label" for="prenom">Prénom</label>
								<input type="text" class="form-control" id="prenom" name="Prenom" placeholder="Prénom">
							</div>
							<div class="col-12">
								<label class="form-label" for="adr1">Adresse Partie 1</label>
								<input type="text" class="form-control" id="adr1" name="Adresse_Partie_1" placeholder="Adresse Partie 1">
							</div>
							<div class="col-md-6">
								<label class="form-label" for="adr2">Adresse Partie 2</label>
								<input type="text" class="form-control" id="adr2" name="Adresse_Partie_2" placeholder="Adresse Partie 2">
							</div>
							<div class="col-md-6">
								<label class="form-label" for="adr3">Adresse Partie 3</label>
								<input type="text" class="form-control" id="adr3" name="Adresse_Partie_3" placeholder="Adresse Partie 3">
							</div>
							<div class="col-md-4">
								<label class="form-label" for="cp">Code Postal</label>
								<input type="text" class="form-control" id="cp" name="Code_Postal" placeholder="Code Postal">
							</div>
							<div class="col-md-4">
								<label class="form-label" for="ville">Ville</label>
								<input type="text" class="form-control" id="ville" name="Ville" placeholder="Ville">
							</div>
							<div class="col-md-4">
								<label class="form-label" for="pays">Pays</label>
								<input type="text" class="form-control" id="pays" name="Pays" placeholder="Pays">
							</div>
							<div class="col-md-4">
								<label class="form-label" for="telfixe">Tél. fixe</label>
								<input type="tel" class="form-control" id="telfixe" name="Tel_fixe" placeholder="Tél. fixe" pattern="[0-9()#&+*\-=.]+" title="Seuls les caractères de numéros de téléphone (#, -, *, etc.) sont acceptés.">
							</div>
							<div class="col-md-4">
								<label class="form-label" for="telfax">Tél. fax</label>
								<input type="tel" class="form-control" id="telfax" name="Tel_fax" placeholder="Tél. fax" pattern="[0-9()#&+*\-=.]+" title="Seuls les caractères de numéros de téléphone (#, -, *, etc.) sont acceptés.">
							</div>
							<div class="col-md-4">
								<label class="form-label" for="telmob">Tél. mobile</label>
								<input type="tel" class="form-control" id="telmob" name="Tel_mobile" placeholder="Tél. mobile" pattern="[0-9()#&+*\-=.]+" title="Seuls les caractères de numéros de téléphone (#, -, *, etc.) sont acceptés.">
							</div>
							<div class="col-12">
								<label class="form-label" for="site">Site internet</label>
								<input type="url" class="form-control" id="site" name="Site_internet" placeholder="https://">
							</div>
							<div class="col-md-4">
								<label class="form-label" for="sect1">Secteur d'activité 1</label>
								<input type="text" class="form-control" id="sect1" name="Secteur_activite_1" placeholder="Secteur d'activité 1">
							</div>
							<div class="col-md-4">
								<label class="form-label" for="sect2">Secteur d'activité 2</label>
								<input type="text" class="form-control" id="sect2" name="Secteur_activite_2" placeholder="Secteur d'activité 2">
							</div>
							<div class="col-md-4">
								<label class="form-label" for="sect3">Secteur d'activité 3</label>
								<input type="text" class="form-control" id="sect3" name="Secteur_activite_3" placeholder="Secteur d'activité 3">
							</div>
							<div class="col-md-6">
								<label class="form-label" for="langm1">Langue maternelle 1</label>
								<input type="text" class="form-control" id="langm1" name="Langue_maternelle_1" placeholder="Langue maternelle 1">
							</div>
							<div class="col-md-6">
								<label class="form-label" for="langm2">Langue maternelle 2</label>
								<input type="text" class="form-control" id="langm2" name="Langue_maternelle_2" placeholder="Langue maternelle 2">
							</div>
							<div class="col-md-4">
								<label class="form-label" for="langc1">Langue courante 1</label>
								<input type="text" class="form-control" id="langc1" name="Langue_courante_1" placeholder="Langue courante 1">
							</div>
							<div class="col-md-4">
								<label class="form-label" for="langc2">Langue courante 2</label>
								<input type="text" class="form-control" id="langc2" name="Langue_courante_2" placeholder="Langue courante 2">
							</div>
							<div class="col-md-4">
								<label class="form-label" for="langc3">Langue courante 3</label>
								<input type="text" class="form-control" id="langc3" name="Langue_courante_3" placeholder="Langue courante 3">
							</div>

							<div class="col-12"><strong>Expérience de mandataire social 1</strong></div>
							<div class="col-md-6">
								<label class="form-label" for="fonction1">Fonction</label>
								<input type="text" class="form-control" id="fonction1" name="Fonction_1" placeholder="Fonction">
							</div>
							<div class="col-md-6">
								<label class="form-label" for="orga1">Organisation</label>
								<input type="text" class="form-control" id="orga1" name="Organisation_1" placeholder="Organisation">
							</div>

							<div class="col-12"><strong>Expérience de mandataire social 2</strong></div>
							<div class="col-md-6">
								<label class="form-label" for="fonction2">Fonction</label>
								<input type="text" class="form-control" id="fonction2" name="Fonction_2" placeholder="Fonction">
							</div>
							<div class="col-md-6">
								<label class="form-label" for="orga2">Organisation</label>
								<input type="text" class="form-control" id="orga2" name="Organisation_2" placeholder="Organisation">
							</div>

							<div class="col-12"><strong>Expérience de mandataire social 3</strong></div>
							<div class="col-md-6">
								<label class="form-label" for="fonction3">Fonction</label>
								<input type="text" class="form-control" id="fonction3" name="Fonction_3" placeholder="Fonction">
							</div>
							<div class="col-md-6">
								<label class="form-label" for="orga3">Organisation</label>
								<input type="text" class="form-control" id="orga3" name="Organisation_3" placeholder="Organisation">
							</div>

							<div class="col-12"><strong>Formation, indiquer le diplôme</strong></div>
							<div class="col-md-6">
								<label class="form-label" for="bac">&lt; = bac</label>
								<input type="text" class="form-control" id="bac" name="Formation_bac" placeholder="&lt; = bac">
							</div>
							<div class="col-md-6">
								<label class="form-label" for="bac3">&lt; = bac + 3</label>
								<input type="text" class="form-control" id="bac3" name="Formation_bac3" placeholder="&lt; = bac + 3">
							</div>
							<div class="col-md-6">
								<label class="form-label" for="bac5_1">&lt; = bac + 5 (1)</label>
								<input type="text" class="form-control" id="bac5_1" name="Formation_bac5_1" placeholder="&lt; = bac + 5 (1)">
							</div>
							<div class="col-md-6">
								<label class="form-label" for="bac5_2">&lt; = bac + 5 (2)</label>
								<input type="text" class="form-control" id="bac5_2" name="Formation_bac5_2" placeholder="&lt; = bac + 5 (2)">
							</div>

							<div class="col-12">
								<label class="form-label" for="comments">Commentaires succincts éventuels</label>
								<textarea class="form-control" id="comments" name="Commentaires" rows="4" placeholder="Commentaires succincts éventuels"></textarea>
							</div>

							<div class="col-12">
								<button type="submit" class="btn btn-primary">Envoyer</button>
								<button type="reset" class="btn btn-outline-secondary ms-2">Effacer</button>
							</div>
						</form>
						<p class="small text-muted mt-3">En cliquant sur Envoyer, votre candidature sera transmise directement à <strong>contact@g-et-s.com</strong>.</p>
					</div>
				</div>
			</div>
		</div>
	</main>
	<div id="footer-placeholder"></div>
</body>
</html>

