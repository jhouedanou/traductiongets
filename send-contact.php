<?php
/**
 * send-contact.php — Traitement sécurisé du formulaire de contact G-ET-S
 *
 * Sécurité : CSRF token, honeypot, rate limiting, sanitisation, validation
 */

session_start();

// ── Configuration ────────────────────────────────────────────────────────────
define('RECIPIENT_EMAIL', 'contact@g-et-s.com');
define('SENDER_NAME',     'Formulaire G&S');
define('SUBJECT_PREFIX',  '[G&S Candidature]');
define('RATE_LIMIT_DELAY', 60); // secondes entre deux envois

// ── Fonctions utilitaires ────────────────────────────────────────────────────

function sanitize(string $input): string {
    return htmlspecialchars(trim($input), ENT_QUOTES, 'UTF-8');
}

function sanitize_email(string $input): string {
    return filter_var(trim($input), FILTER_SANITIZE_EMAIL);
}

function sanitize_phone(string $input): string {
    // N'autorise que les caractères de téléphone
    return preg_replace('/[^0-9()+\-.\s]/', '', trim($input));
}

function sanitize_url(string $input): string {
    $url = filter_var(trim($input), FILTER_SANITIZE_URL);
    if ($url && !filter_var($url, FILTER_VALIDATE_URL)) {
        return '';
    }
    return $url;
}

function generate_csrf_token(): string {
    if (empty($_SESSION['csrf_token'])) {
        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf_token'];
}

function verify_csrf_token(string $token): bool {
    return isset($_SESSION['csrf_token']) && hash_equals($_SESSION['csrf_token'], $token);
}

function check_rate_limit(): bool {
    $now = time();
    if (isset($_SESSION['last_submit']) && ($now - $_SESSION['last_submit']) < RATE_LIMIT_DELAY) {
        return false;
    }
    $_SESSION['last_submit'] = $now;
    return true;
}

function render_page(string $title, string $icon, string $color, string $message, string $details = '', bool $success = true): void {
    $status_class = $success ? 'success' : 'danger';
    $btn_text = $success ? 'Retour au site' : 'Corriger le formulaire';
    $btn_link = $success ? 'index.html' : 'javascript:history.back()';

    echo '<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>' . sanitize($title) . ' - G-ET-S</title>
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
        .contact-body { padding: 48px 24px; }
        .result-icon { font-size: 4rem; margin-bottom: 24px; }
        .result-message { font-size: 1.25rem; font-weight: 600; margin-bottom: 12px; }
        .result-details { color: #6c757d; margin-bottom: 32px; line-height: 1.6; }
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
            <div class="contact-body text-center">
                <div class="result-icon text-' . $status_class . '">' . $icon . '</div>
                <p class="result-message text-' . $status_class . '">' . sanitize($message) . '</p>
                ' . ($details ? '<p class="result-details">' . sanitize($details) . '</p>' : '') . '
                <a href="' . $btn_link . '" class="btn btn-' . ($success ? 'primary' : 'outline-secondary') . ' px-4 py-2">
                    <i class="fas fa-' . ($success ? 'home' : 'arrow-left') . ' me-2"></i>' . $btn_text . '
                </a>
            </div>
        </div>
    </main>
    <div id="footer-placeholder"></div>
</body>
</html>';
}

// ── Vérifications de sécurité ────────────────────────────────────────────────

// 1. Méthode POST uniquement
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    render_page('Erreur', '<i class="fas fa-ban"></i>', 'danger',
        'Méthode non autorisée',
        'Ce formulaire doit être soumis via le bouton Envoyer.', false);
    exit;
}

// 2. Vérification du token CSRF
$csrf_token = $_POST['csrf_token'] ?? '';
if (!verify_csrf_token($csrf_token)) {
    http_response_code(403);
    render_page('Erreur de sécurité', '<i class="fas fa-shield-halved"></i>', 'danger',
        'Session expirée ou invalide',
        'Veuillez recharger la page du formulaire et remplir de nouveau.', false);
    exit;
}

// 3. Honeypot anti-spam (champ caché qui doit rester vide)
if (!empty($_POST['website_url'])) {
    // Bot détecté, on simule un succès pour ne pas alerter
    http_response_code(200);
    render_page('Message envoyé', '<i class="fas fa-check-circle"></i>', 'success',
        'Votre candidature a bien été envoyée !',
        'Nous vous recontacterons dans les meilleurs délais.');
    exit;
}

// 4. Rate limiting
if (!check_rate_limit()) {
    http_response_code(429);
    render_page('Envoi trop fréquent', '<i class="fas fa-clock"></i>', 'danger',
        'Veuillez patienter avant de renvoyer le formulaire',
        'Pour des raisons de sécurité, un délai de ' . RATE_LIMIT_DELAY . ' secondes est requis entre chaque envoi.', false);
    exit;
}

// Régénérer le token CSRF après utilisation
unset($_SESSION['csrf_token']);

// ── Récupération et validation des données ───────────────────────────────────

$email    = sanitize_email($_POST['Email'] ?? '');
$civilite = sanitize($_POST['Civilite'] ?? '');

// Validation de l'email (obligatoire)
if (empty($email) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    render_page('Erreur de validation', '<i class="fas fa-exclamation-triangle"></i>', 'danger',
        'Adresse email invalide',
        'Veuillez fournir une adresse email valide.', false);
    exit;
}

// Validation civilité (obligatoire)
$civilites_valides = ['Mr.', 'Mde.', 'Mlle.'];
if (!in_array($civilite, $civilites_valides, true)) {
    render_page('Erreur de validation', '<i class="fas fa-exclamation-triangle"></i>', 'danger',
        'Civilité invalide',
        'Veuillez sélectionner une civilité valide.', false);
    exit;
}

// Champs texte
$nom    = sanitize($_POST['Nom'] ?? '');
$prenom = sanitize($_POST['Prenom'] ?? '');
$adr1   = sanitize($_POST['Adresse_Partie_1'] ?? '');
$adr2   = sanitize($_POST['Adresse_Partie_2'] ?? '');
$adr3   = sanitize($_POST['Adresse_Partie_3'] ?? '');
$cp     = sanitize($_POST['Code_Postal'] ?? '');
$ville  = sanitize($_POST['Ville'] ?? '');
$pays   = sanitize($_POST['Pays'] ?? '');

// Téléphones
$tel_fixe   = sanitize_phone($_POST['Tel_fixe'] ?? '');
$tel_fax    = sanitize_phone($_POST['Tel_fax'] ?? '');
$tel_mobile = sanitize_phone($_POST['Tel_mobile'] ?? '');

// URL
$site = sanitize_url($_POST['Site_internet'] ?? '');

// Secteurs, langues
$sect1  = sanitize($_POST['Secteur_activite_1'] ?? '');
$sect2  = sanitize($_POST['Secteur_activite_2'] ?? '');
$sect3  = sanitize($_POST['Secteur_activite_3'] ?? '');
$langm1 = sanitize($_POST['Langue_maternelle_1'] ?? '');
$langm2 = sanitize($_POST['Langue_maternelle_2'] ?? '');
$langc1 = sanitize($_POST['Langue_courante_1'] ?? '');
$langc2 = sanitize($_POST['Langue_courante_2'] ?? '');
$langc3 = sanitize($_POST['Langue_courante_3'] ?? '');

// Expériences
$fonction1 = sanitize($_POST['Fonction_1'] ?? '');
$orga1     = sanitize($_POST['Organisation_1'] ?? '');
$fonction2 = sanitize($_POST['Fonction_2'] ?? '');
$orga2     = sanitize($_POST['Organisation_2'] ?? '');
$fonction3 = sanitize($_POST['Fonction_3'] ?? '');
$orga3     = sanitize($_POST['Organisation_3'] ?? '');

// Formation
$bac    = sanitize($_POST['Formation_bac'] ?? '');
$bac3   = sanitize($_POST['Formation_bac3'] ?? '');
$bac5_1 = sanitize($_POST['Formation_bac5_1'] ?? '');
$bac5_2 = sanitize($_POST['Formation_bac5_2'] ?? '');

// Commentaires (limité à 2000 caractères)
$comments = sanitize(mb_substr($_POST['Commentaires'] ?? '', 0, 2000));

// ── Construction de l'email ──────────────────────────────────────────────────

$identite = trim("$civilite $prenom $nom");
$subject  = SUBJECT_PREFIX . ' ' . ($identite ?: 'Candidature anonyme');

$body = "=== NOUVELLE CANDIDATURE ===\n\n";
$body .= "Date : " . date('d/m/Y H:i') . "\n";
$body .= "IP : " . ($_SERVER['REMOTE_ADDR'] ?? 'inconnue') . "\n\n";

$body .= "--- IDENTITE ---\n";
$body .= "Civilite : $civilite\n";
$body .= "Nom : $nom\n";
$body .= "Prenom : $prenom\n";
$body .= "Email : $email\n\n";

$body .= "--- COORDONNEES ---\n";
$body .= "Adresse : $adr1\n";
if ($adr2) $body .= "          $adr2\n";
if ($adr3) $body .= "          $adr3\n";
$body .= "Code postal : $cp\n";
$body .= "Ville : $ville\n";
$body .= "Pays : $pays\n";
$body .= "Tel. fixe : $tel_fixe\n";
$body .= "Tel. fax : $tel_fax\n";
$body .= "Tel. mobile : $tel_mobile\n";
$body .= "Site internet : $site\n\n";

$body .= "--- SECTEURS D'ACTIVITE ---\n";
$body .= "Secteur 1 : $sect1\n";
$body .= "Secteur 2 : $sect2\n";
$body .= "Secteur 3 : $sect3\n\n";

$body .= "--- LANGUES ---\n";
$body .= "Maternelle 1 : $langm1\n";
$body .= "Maternelle 2 : $langm2\n";
$body .= "Courante 1 : $langc1\n";
$body .= "Courante 2 : $langc2\n";
$body .= "Courante 3 : $langc3\n\n";

$body .= "--- EXPERIENCE MANDATAIRE SOCIAL ---\n";
$body .= "1) $fonction1 - $orga1\n";
$body .= "2) $fonction2 - $orga2\n";
$body .= "3) $fonction3 - $orga3\n\n";

$body .= "--- FORMATION ---\n";
$body .= "<= bac : $bac\n";
$body .= "<= bac+3 : $bac3\n";
$body .= "<= bac+5 (1) : $bac5_1\n";
$body .= "<= bac+5 (2) : $bac5_2\n\n";

$body .= "--- COMMENTAIRES ---\n";
$body .= $comments . "\n";

// ── En-têtes sécurisés ──────────────────────────────────────────────────────

// Protection contre l'injection d'en-têtes
$safe_email = str_replace(["\r", "\n"], '', $email);

$headers  = "From: " . SENDER_NAME . " <noreply@g-et-s.com>\r\n";
$headers .= "Reply-To: $safe_email\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
$headers .= "X-Mailer: G-ET-S Contact Form\r\n";
$headers .= "MIME-Version: 1.0\r\n";

// ── Envoi ────────────────────────────────────────────────────────────────────

$sent = mail(RECIPIENT_EMAIL, $subject, $body, $headers);

if ($sent) {
    render_page('Message envoyé', '<i class="fas fa-check-circle"></i>', 'success',
        'Votre candidature a bien été envoyée !',
        'Merci ' . ($prenom ?: '') . '. Nous avons bien reçu votre candidature et nous vous recontacterons dans les meilleurs délais à l\'adresse ' . $email . '.');
} else {
    error_log("Echec envoi email formulaire contact G&S - destinataire: " . RECIPIENT_EMAIL . " - expediteur: $email");
    render_page('Erreur d\'envoi', '<i class="fas fa-times-circle"></i>', 'danger',
        'Une erreur est survenue lors de l\'envoi',
        'Veuillez réessayer ultérieurement ou nous contacter directement à ' . RECIPIENT_EMAIL . '.', false);
}
