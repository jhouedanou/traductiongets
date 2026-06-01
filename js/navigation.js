// Navigation enhancement for G-ET-S website
$(document).ready(function() {
    // Smooth scrolling for internal links
    function initializeSmoothScrolling() {
        $('a[href^="#"]').on('click', function(e) {
            const target = $(this.getAttribute('href'));
            
            if (target.length) {
                e.preventDefault();
                $('html, body').stop().animate({
                    scrollTop: target.offset().top - 100
                }, 800, 'swing');
            }
        });
    }
    
    // Active section highlighting
    function initializeActiveSection() {
        const sections = [];
        $('a[href^="#"]').each(function() {
            const href = $(this).attr('href');
            if (href !== '#' && $(href).length > 0) {
                sections.push(href);
            }
        });
        
        $(window).on('scroll', function() {
            let current = '';
            const scrollPos = $(window).scrollTop() + 150;
            
            sections.forEach(function(section) {
                const $section = $(section);
                if ($section.length > 0) {
                    const sectionTop = $section.offset().top;
                    if (sectionTop <= scrollPos) {
                        current = section;
                    }
                }
            });
            
            $('.nav-link-anchor').removeClass('active');
            if (current) {
                $(`a[href="${current}"]`).addClass('active');
            }
        });
    }
    
    // Navigation breadcrumb
    function createBreadcrumb() {
        const path = window.location.pathname;
        const pathParts = path.split('/').filter(part => part && part !== 'index.html');
        
        if (pathParts.length > 0) {
            let breadcrumbHtml = '<nav aria-label="breadcrumb" class="breadcrumb-nav mt-3"><ol class="breadcrumb">';
            breadcrumbHtml += '<li class="breadcrumb-item"><a href="index.html">Accueil</a></li>';
            
            let currentPath = '';
            pathParts.forEach(function(part, index) {
                currentPath += '/' + part;
                const isLast = index === pathParts.length - 1;
                const displayName = part.replace(/-/g, ' ').replace('.html', '').replace(/\b\w/g, l => l.toUpperCase());
                
                if (isLast) {
                    breadcrumbHtml += `<li class="breadcrumb-item active" aria-current="page">${displayName}</li>`;
                } else {
                    breadcrumbHtml += `<li class="breadcrumb-item"><a href="${currentPath}">${displayName}</a></li>`;
                }
            });
            
            breadcrumbHtml += '</ol></nav>';
            
            // Add breadcrumb after header if on a subpage
            if (pathParts.length > 0 && $('.main-container').length > 0) {
                $('.main-container').prepend(breadcrumbHtml);
            }
        }
    }
    
    // Mobile navigation improvements
    function improveMobileNavigation() {
        // Add click handler for mobile menu toggle
        $('.menu-toggle').on('click', function() {
            $('.main-nav').toggleClass('mobile-open');
            $(this).attr('aria-expanded', $('.main-nav').hasClass('mobile-open'));
        });
        
        // Close mobile menu when clicking outside
        $(document).on('click', function(e) {
            if (!$(e.target).closest('.main-navigation').length) {
                $('.main-nav').removeClass('mobile-open');
                $('.menu-toggle').attr('aria-expanded', 'false');
            }
        });
        
        // Improved submenu handling on mobile
        $('.menu-item-has-children > a').on('click', function(e) {
            if ($(window).width() <= 768) {
                e.preventDefault();
                const $submenu = $(this).siblings('.sub-menu');
                $submenu.slideToggle(300);
                $(this).toggleClass('submenu-open');
            }
        });
    }
    
    // Add back-to-top button
    function addBackToTop() {
        const backToTopHtml = `
            <button id="back-to-top" class="btn btn-primary" style="
                position: fixed;
                bottom: 30px;
                right: 30px;
                z-index: 1000;
                display: none;
                border-radius: 50%;
                width: 50px;
                height: 50px;
                padding: 0;
                font-size: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.3);
            " title="Retour en haut">
                <i class="fas fa-arrow-up"></i>
            </button>
        `;
        
        $('body').append(backToTopHtml);
        
        // Show/hide back-to-top button
        $(window).on('scroll', function() {
            if ($(window).scrollTop() > 300) {
                $('#back-to-top').fadeIn();
            } else {
                $('#back-to-top').fadeOut();
            }
        });
        
        // Back-to-top click handler
        $('#back-to-top').on('click', function() {
            $('html, body').animate({scrollTop: 0}, 800);
        });
    }
    
    // Navigation keyboard accessibility
    function improveKeyboardNavigation() {
        $('.nav-link-anchor').on('keydown', function(e) {
            if (e.keyCode === 13 || e.keyCode === 32) { // Enter or Space
                e.preventDefault();
                $(this)[0].click();
            }
        });
        
        // Skip to content link
        const skipLinkHtml = `
            <a href="#main-content" class="skip-link sr-only sr-only-focusable" style="
                position: absolute;
                top: 10px;
                left: 10px;
                z-index: 9999;
                padding: 8px 16px;
                background: #000;
                color: #fff;
                text-decoration: none;
            ">Passer au contenu principal</a>
        `;
        
        $('body').prepend(skipLinkHtml);
        $('main').attr('id', 'main-content');
    }
    
    // Page loading indicator
    function addLoadingIndicator() {
        // Show loading for external links
        $('a[href^="http"]:not([href*="g-et-s.com"])').on('click', function() {
            const $this = $(this);
            const originalText = $this.text();
            $this.html('<i class="fas fa-spinner fa-spin"></i> Chargement...');
            
            setTimeout(function() {
                $this.text(originalText);
            }, 3000);
        });
    }
    
    // Initialize all navigation enhancements
    initializeSmoothScrolling();
    initializeActiveSection();
    createBreadcrumb();
    improveMobileNavigation();
    addBackToTop();
    improveKeyboardNavigation();
    addLoadingIndicator();
    
    // Add CSS for mobile navigation
    const mobileNavCSS = `
        <style>
        @media (max-width: 768px) {
            .main-nav {
                display: none;
                position: absolute;
                top: 100%;
                left: 0;
                right: 0;
                background: #1e73be;
                flex-direction: column;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            
            .main-nav.mobile-open {
                display: flex;
            }
            
            .main-nav > li {
                width: 100%;
                border-bottom: 1px solid #035a9e;
            }
            
            .main-nav > li > a {
                display: block;
                padding: 15px 20px;
                color: white;
                text-decoration: none;
            }
            
            .sub-menu {
                display: none;
                position: static;
                box-shadow: none;
                background: #035a9e;
            }
            
            .submenu-open + .sub-menu {
                display: block;
            }
            
            .breadcrumb-nav {
                margin: 10px 0;
            }
            
            .breadcrumb {
                background: #f8f9fa;
                padding: 8px 15px;
                border-radius: 4px;
                font-size: 12px;
            }
        }
        
        .nav-link-anchor.active {
            background-color: rgba(30, 115, 190, 0.1);
            border-left-color: #1e73be;
            font-weight: 600;
        }
        
        .skip-link:focus {
            position: static !important;
        }
        </style>
    `;
    
    $('head').append(mobileNavCSS);
});