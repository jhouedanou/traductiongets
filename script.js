// Gestion du menu mobile
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.menu-toggle');
    const mainNav = document.querySelector('.main-nav');
    
    if (menuToggle && mainNav) {
        menuToggle.addEventListener('click', function() {
            const isExpanded = this.getAttribute('aria-expanded') === 'true';
            this.setAttribute('aria-expanded', !isExpanded);
            
            if (isExpanded) {
                mainNav.style.display = 'none';
            } else {
                mainNav.style.display = 'flex';
            }
        });
    }
    
    // Gestion des sous-menus sur mobile
    const menuItemsWithChildren = document.querySelectorAll('.menu-item-has-children');
    
    menuItemsWithChildren.forEach(item => {
        const link = item.querySelector('a');
        const subMenu = item.querySelector('.sub-menu');
        
        if (link && subMenu) {
            link.addEventListener('click', function(e) {
                if (window.innerWidth <= 768) {
                    e.preventDefault();
                    subMenu.style.display = subMenu.style.display === 'block' ? 'none' : 'block';
                }
            });
        }
    });
    
    // Gestion de la recherche
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const searchField = this.querySelector('.search-field');
            const searchTerm = searchField.value.trim();
            
            if (searchTerm) {
                // Simulation d'une recherche
                alert('Recherche pour : ' + searchTerm);
                // Ici vous pourriez rediriger vers une page de résultats
                // window.location.href = '/recherche?q=' + encodeURIComponent(searchTerm);
            }
        });
    }
    
    // Animation des icônes sociales
    const socialIcons = document.querySelectorAll('.social-icon');
    socialIcons.forEach(icon => {
        icon.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1)';
        });
        
        icon.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
    
    // Gestion du responsive pour les sous-menus
    function handleResize() {
        if (window.innerWidth > 768) {
            mainNav.style.display = 'flex';
            const subMenus = document.querySelectorAll('.sub-menu');
            subMenus.forEach(subMenu => {
                subMenu.style.display = 'none';
            });
        } else {
            mainNav.style.display = 'none';
        }
    }
    
    window.addEventListener('resize', handleResize);
    
    // Initialisation
    handleResize();
});

// Fonction pour faire défiler vers le haut de la page
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Ajout d'un bouton "Retour en haut" si la page est longue
document.addEventListener('DOMContentLoaded', function() {
    if (document.body.scrollHeight > window.innerHeight * 2) {
        const backToTopButton = document.createElement('button');
        backToTopButton.innerHTML = '↑';
        backToTopButton.className = 'back-to-top';
        backToTopButton.onclick = scrollToTop;
        
        // Styles pour le bouton
        backToTopButton.style.cssText = `
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 50px;
            height: 50px;
            background-color: #1e73be;
            color: white;
            border: none;
            border-radius: 50%;
            font-size: 20px;
            cursor: pointer;
            z-index: 1000;
            opacity: 0.8;
            transition: opacity 0.3s ease;
        `;
        
        backToTopButton.addEventListener('mouseenter', function() {
            this.style.opacity = '1';
        });
        
        backToTopButton.addEventListener('mouseleave', function() {
            this.style.opacity = '0.8';
        });
        
        document.body.appendChild(backToTopButton);
        
        // Afficher/masquer le bouton selon le scroll
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopButton.style.display = 'block';
            } else {
                backToTopButton.style.display = 'none';
            }
        });
        
        backToTopButton.style.display = 'none';
    }
});

// Amélioration de l'accessibilité
document.addEventListener('DOMContentLoaded', function() {
    // Ajout de focus visible pour la navigation
    const navLinks = document.querySelectorAll('.main-nav a, .sub-menu a');
    navLinks.forEach(link => {
        link.addEventListener('focus', function() {
            this.style.outline = '2px solid #ffffff';
            this.style.outlineOffset = '2px';
        });
        
        link.addEventListener('blur', function() {
            this.style.outline = 'none';
        });
    });
    
    // Amélioration de la navigation au clavier
    const menuItems = document.querySelectorAll('.menu-item-has-children');
    menuItems.forEach(item => {
        const link = item.querySelector('a');
        const subMenu = item.querySelector('.sub-menu');
        
        if (link && subMenu) {
            link.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    if (window.innerWidth <= 768) {
                        subMenu.style.display = subMenu.style.display === 'block' ? 'none' : 'block';
                    }
                }
            });
        }
    });
});
