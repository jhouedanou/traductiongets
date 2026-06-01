// Système de suggestions de recherche pour le header
(function() {
    'use strict';

    // Noms des catégories en français
    const categoryNames = {
        'generalites-contrib': 'Généralités - Contributions',
        'generalites-docs': 'Généralités - Documents',
        'feminisation-contrib': 'Féminisation - Contributions',
        'feminisation-docs': 'Féminisation - Documents',
        'qui': 'Qui est G & S',
        'pour-mandataires': 'Pour mandataires',
        'pour-societes': 'Pour Sociétés'
    };

    // Normaliser le texte (enlever les accents)
    function normalizeText(text) {
        return text.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
    }

    // Mettre en surbrillance le terme recherché
    function highlightMatch(text, searchTerm) {
        if (!searchTerm) return text;

        const normalizedText = normalizeText(text);
        const normalizedTerm = normalizeText(searchTerm);
        const index = normalizedText.indexOf(normalizedTerm);

        if (index === -1) return text;

        const before = text.substring(0, index);
        const match = text.substring(index, index + searchTerm.length);
        const after = text.substring(index + searchTerm.length);

        return `${before}<span class="suggestion-highlight">${match}</span>${after}`;
    }

    // Rechercher des suggestions
    function getSuggestions(searchTerm) {
        if (!searchTerm || searchTerm.trim().length < 2) {
            return [];
        }

        if (typeof window.searchArticles !== 'function') {
            console.warn('searchArticles function not available');
            return [];
        }

        const results = window.searchArticles(searchTerm);
        // Limiter à 8 suggestions maximum
        return results.slice(0, 8);
    }

    // Afficher les suggestions
    function displaySuggestions(suggestions, searchTerm) {
        const suggestionsContainer = document.getElementById('search-suggestions');
        const suggestionsList = suggestionsContainer ? suggestionsContainer.querySelector('.suggestions-list') : null;

        if (!suggestionsContainer || !suggestionsList) return;

        // Vider la liste
        suggestionsList.innerHTML = '';

        if (suggestions.length === 0) {
            suggestionsList.innerHTML = '<div class="no-suggestions">Aucune suggestion</div>';
            suggestionsContainer.style.display = 'block';
            return;
        }

        // Déterminer si on est dans le dossier /pages/ ou à la racine
        const currentPath = window.location.pathname;
        const isInPagesFolder = currentPath.includes('/pages/');

        // Créer les éléments de suggestion
        suggestions.forEach(function(item) {
            const suggestionDiv = document.createElement('div');
            suggestionDiv.className = 'suggestion-item';

            // Toutes les suggestions pointent vers le dossier pages/
            // Construire le chemin en fonction de notre position
            let targetUrl;
            if (isInPagesFolder) {
                // On est déjà dans /pages/, donc juste utiliser le nom du fichier
                targetUrl = item.url.replace('pages/', '');
            } else {
                // On est à la racine ou ailleurs, utiliser le chemin complet
                targetUrl = item.url;
            }

            suggestionDiv.setAttribute('data-url', targetUrl);

            const categoryLabel = categoryNames[item.category] || item.category;
            const highlightedTitle = highlightMatch(item.title, searchTerm);

            suggestionDiv.innerHTML = `
                <div class="suggestion-item-title">${highlightedTitle}</div>
                <div class="suggestion-item-category">${categoryLabel}</div>
            `;

            // Clic sur une suggestion
            suggestionDiv.addEventListener('click', function() {
                window.location.href = this.getAttribute('data-url');
            });

            suggestionsList.appendChild(suggestionDiv);
        });

        suggestionsContainer.style.display = 'block';
    }

    // Masquer les suggestions
    function hideSuggestions() {
        const suggestionsContainer = document.getElementById('search-suggestions');
        if (suggestionsContainer) {
            suggestionsContainer.style.display = 'none';
        }
    }

    // Initialisation après le chargement du header
    function initSearchSuggestions() {
        const headerSearchInput = document.getElementById('header-search-input');
        const headerSearchBtn = document.getElementById('header-search-btn');
        const headerSearchClear = document.getElementById('header-search-clear');
        const suggestionsContainer = document.getElementById('search-suggestions');

        if (!headerSearchInput) {
            console.warn('Header search input not found');
            return;
        }

        // Gestion de la visibilité du bouton de fermeture
        function toggleClearButton() {
            if (headerSearchClear) {
                if (headerSearchInput.value.trim().length > 0) {
                    headerSearchClear.style.display = 'block';
                } else {
                    headerSearchClear.style.display = 'none';
                }
            }
        }

        // Bouton de fermeture
        if (headerSearchClear) {
            headerSearchClear.addEventListener('click', function() {
                headerSearchInput.value = '';
                this.style.display = 'none';
                hideSuggestions();

                // Effacer aussi le champ de recherche de la page d'accueil si présent
                const searchInput = document.getElementById('search-input');
                if (searchInput) {
                    searchInput.value = '';
                }

                // Effacer la recherche du sessionStorage
                sessionStorage.removeItem('pendingSearch');

                // Réappliquer les filtres pour tout afficher
                if (window.applyColumnFilters) {
                    window.applyColumnFilters();
                }

                headerSearchInput.focus();
            });
        }

        // Debounce pour limiter les appels
        let debounceTimer;

        // Événement input pour afficher les suggestions
        headerSearchInput.addEventListener('input', function() {
            toggleClearButton();
            clearTimeout(debounceTimer);
            const searchValue = this.value.trim();

            if (searchValue.length < 2) {
                hideSuggestions();
                return;
            }

            debounceTimer = setTimeout(function() {
                const suggestions = getSuggestions(searchValue);
                displaySuggestions(suggestions, searchValue);
            }, 300);
        });

        // Événement focus pour afficher les suggestions si du texte est déjà saisi
        headerSearchInput.addEventListener('focus', function() {
            toggleClearButton();
            const searchValue = this.value.trim();
            if (searchValue.length >= 2) {
                const suggestions = getSuggestions(searchValue);
                displaySuggestions(suggestions, searchValue);
            }
        });

        // Vérifier au chargement si le champ a déjà du texte
        toggleClearButton();

        // Cacher les suggestions quand on clique ailleurs
        document.addEventListener('click', function(e) {
            if (!headerSearchInput.contains(e.target) &&
                (!suggestionsContainer || !suggestionsContainer.contains(e.target))) {
                hideSuggestions();
            }
        });

        // Touche Escape pour fermer les suggestions
        headerSearchInput.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                hideSuggestions();
                this.blur();
            }
        });

        // Bouton de recherche
        if (headerSearchBtn) {
            headerSearchBtn.addEventListener('click', function() {
                const searchValue = headerSearchInput.value.trim();
                const isHomePage = document.body.classList.contains('home-page');

                if (isHomePage) {
                    // Sur la page d'accueil, appliquer le filtre
                    if (window.applyColumnFilters) {
                        const searchInput = document.getElementById('search-input');
                        if (searchInput) {
                            searchInput.value = searchValue;
                        }
                        window.applyColumnFilters();
                    }
                    hideSuggestions();
                } else {
                    // Sur les autres pages, ouvrir la modale de recherche
                    if (typeof window.openSearchModal === 'function') {
                        window.openSearchModal();
                        // Remplir le champ de recherche de la modale
                        setTimeout(function() {
                            const modalSearchInput = document.getElementById('modal-search-input');
                            if (modalSearchInput) {
                                modalSearchInput.value = searchValue;
                                // Déclencher la recherche automatiquement
                                const searchBtn = document.getElementById('modal-search-btn');
                                if (searchBtn) {
                                    searchBtn.click();
                                }
                            }
                        }, 100);
                    }
                    hideSuggestions();
                }
            });
        }
    }

    // Attendre que le DOM soit prêt et que le header soit chargé
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(initSearchSuggestions, 1000);
        });
    } else {
        setTimeout(initSearchSuggestions, 1000);
    }

    // Exposer les fonctions globalement si nécessaire
    window.initSearchSuggestions = initSearchSuggestions;
})();
