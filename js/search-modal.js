// Modale de recherche pour les sous-pages
(function() {
    'use strict';

    // Créer la modale de recherche
    function createSearchModal() {
        const modalHTML = `
            <div id="search-modal" class="search-modal" style="display: none;">
                <div class="search-modal-overlay"></div>
                <div class="search-modal-content">
                    <div class="search-modal-header">
                        <h3><i class="fas fa-search me-2"></i>Recherche</h3>
                        <button class="search-modal-close" aria-label="Fermer">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                    <div class="search-modal-body">
                        <div class="search-input-group">
                            <input type="text" id="modal-search-input" class="search-modal-input" placeholder="Rechercher dans les articles...">
                            <button id="modal-search-btn" class="search-modal-btn">
                                <i class="fas fa-search"></i>
                            </button>
                        </div>
                        <div id="search-results" class="search-results"></div>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHTML);

        // Styles CSS pour la modale
        const styles = `
            <style>
                .search-modal {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    z-index: 9999;
                }

                .search-modal-overlay {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0, 0, 0, 0.6);
                }

                .search-modal-content {
                    position: relative;
                    max-width: 800px;
                    margin: 50px auto;
                    background: white;
                    border: 1px solid #ccc;
                    max-height: 80vh;
                    display: flex;
                    flex-direction: column;
                }

                .search-modal-header {
                    background: #1e73be;
                    color: white;
                    padding: 20px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    border-bottom: 1px solid #ccc;
                }

                .search-modal-header h3 {
                    margin: 0;
                    font-size: 1.3rem;
                    font-weight: 600;
                }

                .search-modal-close {
                    background: none;
                    border: none;
                    color: white;
                    font-size: 1.5rem;
                    cursor: pointer;
                    padding: 0;
                    width: 30px;
                    height: 30px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }

                .search-modal-close:hover {
                    opacity: 0.8;
                }

                .search-modal-body {
                    padding: 20px;
                    overflow-y: auto;
                    flex: 1;
                }

                .search-input-group {
                    display: flex;
                    gap: 10px;
                    margin-bottom: 20px;
                }

                .search-modal-input {
                    flex: 1;
                    padding: 12px 15px;
                    border: 1px solid #ccc;
                    font-size: 1rem;
                }

                .search-modal-input:focus {
                    outline: none;
                    border-color: #1e73be;
                }

                .search-modal-btn {
                    padding: 12px 20px;
                    background: #1e73be;
                    color: white;
                    border: none;
                    cursor: pointer;
                    font-size: 1rem;
                }

                .search-modal-btn:hover {
                    background: #155a8a;
                }

                .search-results {
                    min-height: 100px;
                }

                .search-results-empty {
                    text-align: center;
                    padding: 40px 20px;
                    color: #666;
                }

                .search-results-table {
                    width: 100%;
                    border-collapse: collapse;
                    border: 1px solid #ddd;
                }

                .search-results-table th {
                    background: #f5f5f5;
                    padding: 12px;
                    text-align: left;
                    border: 1px solid #ddd;
                    font-weight: 600;
                    color: #333;
                }

                .search-results-table td {
                    padding: 12px;
                    border: 1px solid #ddd;
                }

                .search-results-table tr:hover {
                    background: #f9f9f9;
                }

                .search-results-table a {
                    color: #1e73be;
                    text-decoration: none;
                }

                .search-results-table a:hover {
                    text-decoration: underline;
                }

                .search-category-badge {
                    display: inline-block;
                    padding: 3px 8px;
                    background: #e3f2fd;
                    color: #1976d2;
                    border-radius: 3px;
                    font-size: 0.85rem;
                }

                @media (max-width: 768px) {
                    .search-modal-content {
                        margin: 20px;
                        max-height: calc(100vh - 40px);
                    }

                    .search-results-table {
                        font-size: 0.9rem;
                    }

                    .search-results-table th,
                    .search-results-table td {
                        padding: 8px;
                    }
                }
            </style>
        `;

        document.head.insertAdjacentHTML('beforeend', styles);
    }

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

    // Afficher les résultats de recherche
    function displayResults(results) {
        const resultsContainer = document.getElementById('search-results');

        if (!results || results.length === 0) {
            resultsContainer.innerHTML = '<div class="search-results-empty"><i class="fas fa-search" style="font-size: 3rem; color: #ddd; margin-bottom: 15px;"></i><p>Aucun résultat trouvé</p></div>';
            return;
        }

        // Calculer le basePath pour ajuster les URLs
        const currentPath = window.location.pathname;
        const isInSubfolder = currentPath.includes('/pages/');
        const basePath = isInSubfolder ? '../' : '';

        let tableHTML = `
            <table class="search-results-table">
                <thead>
                    <tr>
                        <th>Titre</th>
                        <th>Catégorie</th>
                    </tr>
                </thead>
                <tbody>
        `;

        results.forEach(result => {
            const categoryLabel = categoryNames[result.category] || result.category;
            const url = basePath + result.url;
            tableHTML += `
                <tr>
                    <td><a href="${url}">${result.title}</a></td>
                    <td><span class="search-category-badge">${categoryLabel}</span></td>
                </tr>
            `;
        });

        tableHTML += `
                </tbody>
            </table>
        `;

        resultsContainer.innerHTML = tableHTML;
    }

    // Effectuer la recherche
    function performSearch() {
        const searchInput = document.getElementById('modal-search-input');
        const searchTerm = searchInput.value.trim();

        if (!searchTerm) {
            document.getElementById('search-results').innerHTML = '<div class="search-results-empty"><p>Veuillez saisir un terme de recherche</p></div>';
            return;
        }

        if (typeof window.searchArticles === 'function') {
            const results = window.searchArticles(searchTerm);
            displayResults(results);
        } else {
            console.error('La fonction searchArticles n\'est pas disponible');
        }
    }

    // Ouvrir la modale
    function openSearchModal() {
        const modal = document.getElementById('search-modal');
        if (modal) {
            modal.style.display = 'block';
            document.getElementById('modal-search-input').focus();
        }
    }

    // Fermer la modale
    function closeSearchModal() {
        const modal = document.getElementById('search-modal');
        if (modal) {
            modal.style.display = 'none';
            document.getElementById('search-results').innerHTML = '';
            document.getElementById('modal-search-input').value = '';
        }
    }

    // Initialisation
    document.addEventListener('DOMContentLoaded', function() {
        // Créer la modale
        createSearchModal();

        // Event listeners
        document.querySelector('.search-modal-close').addEventListener('click', closeSearchModal);
        document.querySelector('.search-modal-overlay').addEventListener('click', closeSearchModal);
        document.getElementById('modal-search-btn').addEventListener('click', performSearch);

        // Recherche avec la touche Entrée
        document.getElementById('modal-search-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });

        // Fermer avec Échap
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeSearchModal();
            }
        });

        // Ouvrir la modale quand on clique sur le champ de recherche du header (sur les sous-pages uniquement)
        setTimeout(function() {
            const headerSearchInput = document.getElementById('header-search-input');
            const headerSearchBtn = document.getElementById('header-search-btn');

            // Sur les sous-pages, on peut soit cliquer sur le champ, soit utiliser le bouton
            if (!document.body.classList.contains('home-page')) {
                // Double-clic sur le champ de recherche ouvre la modale
                if (headerSearchInput) {
                    let clickCount = 0;
                    let clickTimer = null;

                    headerSearchInput.addEventListener('click', function(e) {
                        clickCount++;
                        if (clickCount === 1) {
                            clickTimer = setTimeout(function() {
                                clickCount = 0;
                            }, 300);
                        } else if (clickCount === 2) {
                            clearTimeout(clickTimer);
                            clickCount = 0;
                            e.preventDefault();
                            openSearchModal();
                        }
                    });
                }
            }
        }, 1000);
    });

    // Exposer la fonction d'ouverture globalement
    window.openSearchModal = openSearchModal;
})();
