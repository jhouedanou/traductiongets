// Search functionality for G-ET-S website
$(document).ready(function() {
    // Enhanced search functionality for the homepage
    function initializeSearch() {
        // Add search capability to navigation links
        $('.nav-link-anchor').each(function() {
            const $link = $(this);
            const linkText = $link.text().toLowerCase();
            
            // Generate keywords automatically from link text
            const keywords = generateSearchKeywords(linkText);
            $link.attr('data-search-keywords', keywords.join(' '));
        });
    }
    
    // Generate search keywords from text
    function generateSearchKeywords(text) {
        const keywords = new Set();
        
        // Original text
        keywords.add(text);
        
        // Remove common French articles and prepositions
        const stopWords = ['le', 'la', 'les', 'de', 'du', 'des', 'et', 'ou', 'un', 'une', 'dans', 'pour', 'avec', 'sur', 'par', 'à', 'au', 'aux'];
        
        // Split into words and clean
        const words = text.split(/[\s\-\(\)\"\']+/).filter(word => {
            word = word.trim();
            return word.length > 2 && !stopWords.includes(word.toLowerCase());
        });
        
        // Add individual words
        words.forEach(word => {
            keywords.add(word.toLowerCase());
            
            // Add word without accents
            const withoutAccents = removeAccents(word.toLowerCase());
            if (withoutAccents !== word.toLowerCase()) {
                keywords.add(withoutAccents);
            }
        });
        
        // Add acronyms (words in uppercase)
        const acronyms = text.match(/\b[A-Z]{2,}\b/g);
        if (acronyms) {
            acronyms.forEach(acronym => {
                keywords.add(acronym.toLowerCase());
            });
        }
        
        // Add partial matches for compound words
        words.forEach(word => {
            if (word.length > 6) {
                // Add substrings of longer words
                for (let i = 0; i <= word.length - 4; i++) {
                    const substring = word.substring(i, i + 4);
                    if (substring.length >= 4) {
                        keywords.add(substring);
                    }
                }
            }
        });
        
        // Add specific domain keywords based on content
        const domainKeywords = extractDomainKeywords(text);
        domainKeywords.forEach(keyword => keywords.add(keyword));
        
        return Array.from(keywords);
    }
    
    // Remove accents from text
    function removeAccents(str) {
        return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    }
    
    // Extract domain-specific keywords
    function extractDomainKeywords(text) {
        const keywords = [];
        const lowerText = text.toLowerCase();
        
        // Corporate governance keywords
        const governanceTerms = {
            'corporate governance': ['gouvernance', 'corporate', 'ca', 'conseil', 'administration'],
            'administrateur': ['admin', 'mandataire', 'dirigeant'],
            'conseil d\'administration': ['ca', 'conseil', 'board'],
            'gouvernance': ['governance', 'corporate'],
            'mandataire': ['administrateur', 'dirigeant', 'social'],
            'formation': ['cours', 'certificat', 'enseignement'],
            'diagnostic': ['evaluation', 'audit', 'analyse'],
            'parite': ['feminisation', 'egalite', 'femme'],
            'loi': ['reglementation', 'juridique', 'legal'],
            'etude': ['enquete', 'recherche', 'analyse'],
            'numerique': ['digital', 'informatique', 'tech']
        };
        
        Object.entries(governanceTerms).forEach(([term, synonyms]) => {
            if (lowerText.includes(term)) {
                keywords.push(...synonyms);
            }
        });
        
        return keywords;
    }
    
    // Filter navigation links based on search term (conserve pour d'autres pages)
    function filterNavigation(searchTerm) {
        const term = searchTerm.toLowerCase().trim();
        let visibleCount = 0;
        
        if (!term) {
            // Show all links if search is empty
            $('.nav-link-item').show();
            $('.nav-sub-section').show();
            $('#search-results-count').hide();
            return;
        }
        
        $('.nav-link-item').each(function() {
            const $item = $(this);
            const $link = $item.find('.nav-link-anchor');
            const linkText = $link.text().toLowerCase();
            const keywords = $link.attr('data-search-keywords') || '';
            
            // Check if the search term matches
            if (linkText.includes(term) || keywords.includes(term)) {
                $item.show();
                visibleCount++;
                // Also show parent sub-section if this is a sub-item
                $item.closest('.nav-sub-section').show();
            } else {
                $item.hide();
            }
        });
        
        // Hide empty sub-sections
        $('.nav-sub-section').each(function() {
            const $subSection = $(this);
            const visibleItems = $subSection.find('.nav-link-item:visible').length;
            
            if (visibleItems === 0) {
                $subSection.hide();
            }
        });
        
        // Update results count
        const countText = visibleCount === 0 ? 'Aucun résultat trouvé' : 
                         visibleCount === 1 ? '1 résultat trouvé' : 
                         `${visibleCount} résultats trouvés`;
        $('#search-results-count').text(countText).show();
    }
    
    // Highlight search results
    function highlightSearchResults(searchTerm) {
        const term = searchTerm.toLowerCase().trim();
        
        if (!term) return;
        
        $('.nav-link-anchor:visible').each(function() {
            const $link = $(this);
            const originalText = $link.text();
            const highlightedText = originalText.replace(
                new RegExp(`(${term})`, 'gi'),
                '<mark>$1</mark>'
            );
            
            if (originalText.toLowerCase().includes(term)) {
                $link.html(highlightedText);
            }
        });
    }
    
    // Clear highlights
    function clearHighlights() {
        $('.nav-link-anchor mark').each(function() {
            const $mark = $(this);
            $mark.replaceWith($mark.text());
        });
    }
    
    // Initialize search functionality
    initializeSearch();
    
    // Navigate to homepage with AJAX
    function navigateToHomepage() {
        // Determine the correct path to index.html based on current location
        const currentPath = window.location.pathname;
        let indexPath = 'index.html';
        
        // If we're in a subdirectory, adjust the path
        if (currentPath.includes('/pages/')) {
            indexPath = '../index.html';
        } else if (currentPath.includes('/missions/')) {
            if (currentPath.includes('/missions/') && currentPath.split('/').length > 3) {
                // We're in a subfolder of missions (like /missions/subfolder/)
                indexPath = '../../index.html';
            } else {
                // We're directly in missions folder
                indexPath = '../index.html';
            }
        } else if (currentPath.includes('/') && !currentPath.endsWith('/') && !currentPath.endsWith('index.html')) {
            // We're in some other subdirectory
            indexPath = '../index.html';
        }
        
        console.log('Navigating to homepage from:', currentPath, 'using path:', indexPath);
        
        // Use AJAX to load homepage content
        $.ajax({
            url: indexPath,
            type: 'GET',
            success: function(data) {
                // Extract the main content from the response
                const $newContent = $(data).find('main').html();
                if ($newContent) {
                    $('main').html($newContent);
                    
                    // Update URL without page reload - always go to root index
                    if (history.pushState) {
                        const rootPath = window.location.origin + window.location.pathname.split('/').slice(0, -1).join('/').replace(/\/[^\/]*$/, '') + '/index.html';
                        history.pushState(null, null, rootPath);
                    }
                    
                    // Re-initialize search functionality for new content
                    setTimeout(function() {
                        initializeSearch();
                    }, 100);
                    
                    // Show success message
                    const $toast = $('<div class="alert alert-success alert-dismissible fade show position-fixed" style="top: 20px; right: 20px; z-index: 9999;">' +
                        '<i class="fas fa-home me-2"></i>Page d\'accueil chargée' +
                        '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>' +
                        '</div>');
                    $('body').append($toast);
                    
                    // Auto-hide toast after 3 seconds
                    setTimeout(function() {
                        $toast.alert('close');
                    }, 3000);
                }
            },
            error: function() {
                // Fallback to regular navigation with correct path
                window.location.href = indexPath;
            }
        });
    }

    // Search input event handler — sur la page d'accueil, filtrer les colonnes
    $(document).on('input', '#nav-search-input', function() {
        const searchTerm = $(this).val() || '';
        const isHome = !!document.querySelector('.home-navigation');
        
        if (isHome) {
            // Alimenter le champ de recherche principal si présent
            const mainSearch = document.getElementById('search-input');
            if (mainSearch && mainSearch.value !== searchTerm) {
                mainSearch.value = searchTerm;
            }
            if (typeof window.applyColumnFilters === 'function') {
                window.applyColumnFilters();
            }
        } else {
            // Ancien comportement: filtrer la navigation
            clearHighlights();
            filterNavigation(searchTerm);
            if (searchTerm.trim()) {
                highlightSearchResults(searchTerm);
                $('#clear-search').show();
            } else {
                $('#clear-search').hide();
            }
        }
    });

    // Focus handler: sur l'accueil, ne pas naviguer; ailleurs, charger l'accueil
    $(document).on('focus', '#nav-search-input', function() {
        const isHome = !!document.querySelector('.home-navigation');
        if (!isHome) {
            navigateToHomepage();
        }
    });
    
    // Clear search button handler
    $(document).on('click', '#clear-search', function() {
        $('#nav-search-input').val('');
        clearHighlights();
        filterNavigation('');
        $('#clear-search').hide();
        $('#search-results-count').hide();
    });
    
    // Keyboard shortcuts
    $(document).on('keydown', function(e) {
        // Ctrl+F or Cmd+F for search focus
        if ((e.ctrlKey || e.metaKey) && e.keyCode === 70) {
            e.preventDefault();
            $('#nav-search-input').focus();
        }
        
        // Escape to clear search
        if (e.keyCode === 27) {
            $('#nav-search-input').val('');
            clearHighlights();
            filterNavigation('');
            $('#clear-search').hide();
            $('#search-results-count').hide();
        }
    });
    
    // Export functions for use by other scripts
    window.G_ET_S_Search = {
        filterNavigation: filterNavigation,
        highlightResults: highlightSearchResults,
        clearHighlights: clearHighlights
    };
});