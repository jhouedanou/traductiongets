/**
 * Auto Dataset Generator - Détecte automatiquement les item-link dans le DOM
 * et génère le dataset correspondant basé sur les spans
 */

(function() {
    'use strict';

    // Mapping des IDs de liste vers leurs clés de dataset
    const listIdToDataKey = {
        'list-generalites-contrib': 'generalites-contrib',
        'list-generalites-docs': 'generalites-docs',
        'list-feminisation-contrib': 'feminisation-contrib',
        'list-feminisation-docs': 'feminisation-docs',
        'list-qui': 'qui',
        'list-pour-mandataires': 'pour-mandataires',
        'list-pour-societes': 'pour-societes'
    };

    /**
     * Scan le DOM et génère le dataset à partir des item-link existants
     */
    function generateDatasetFromDOM() {
        const generatedDataset = {};

        // Parcourir chaque colonne/liste
        Object.keys(listIdToDataKey).forEach(listId => {
            const dataKey = listIdToDataKey[listId];
            const ul = document.getElementById(listId);

            if (!ul) {
                console.warn(`Liste non trouvée: ${listId}`);
                generatedDataset[dataKey] = [];
                return;
            }

            const items = [];
            const links = ul.querySelectorAll('.item-link');

            links.forEach((link, index) => {
                const span = link.querySelector('span');
                const title = span ? span.textContent.trim() : '';
                const url = link.getAttribute('href') || '#';

                // Détecter si c'est en construction
                const construction = link.classList.contains('construction') ||
                                   link.closest('li')?.classList.contains('construction') ||
                                   url === '#';

                // Créer l'objet item
                const item = {
                    title: title,
                    url: url
                };

                if (construction) {
                    item.construction = true;
                }

                // Ajouter une date de création basée sur l'ordre
                const now = new Date();
                item.dateCreation = new Date(now.getTime() - (index * 86400000)).toISOString().split('T')[0];

                items.push(item);
            });

            generatedDataset[dataKey] = items;
        });

        return generatedDataset;
    }

    /**
     * Observer pour détecter les changements dans le DOM
     */
    function setupMutationObserver(callback) {
        const observer = new MutationObserver((mutations) => {
            let shouldUpdate = false;

            mutations.forEach((mutation) => {
                // Vérifier si des item-link ont été ajoutés/modifiés
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach(node => {
                        if (node.nodeType === 1) { // Element node
                            if (node.classList?.contains('item-link') ||
                                node.querySelector?.('.item-link')) {
                                shouldUpdate = true;
                            }
                        }
                    });
                }
            });

            if (shouldUpdate && callback) {
                console.log('DOM changé - Mise à jour du dataset');
                callback();
            }
        });

        // Observer toutes les listes de contenu
        Object.keys(listIdToDataKey).forEach(listId => {
            const ul = document.getElementById(listId);
            if (ul) {
                observer.observe(ul, {
                    childList: true,
                    subtree: true,
                    attributes: true,
                    attributeFilter: ['href', 'class']
                });
            }
        });

        return observer;
    }

    /**
     * Merge le dataset généré avec un dataset existant
     */
    function mergeDatasets(generated, existing) {
        const merged = {};

        Object.keys(generated).forEach(key => {
            merged[key] = [...generated[key]];

            // Ajouter les items existants qui ne sont pas dans le DOM
            if (existing[key]) {
                existing[key].forEach(existingItem => {
                    const found = merged[key].find(item =>
                        item.title === existingItem.title || item.url === existingItem.url
                    );
                    if (!found) {
                        merged[key].push(existingItem);
                    }
                });
            }
        });

        return merged;
    }

    /**
     * Initialisation
     */
    function init() {
        // Attendre que le DOM soit chargé
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
            return;
        }

        // Générer le dataset initial
        const generatedDataset = generateDatasetFromDOM();
        console.log('Dataset généré:', generatedDataset);

        // Mettre à jour le dataset global si disponible
        if (window.dataSets) {
            window.dataSets = mergeDatasets(generatedDataset, window.dataSets);
            console.log('Dataset global mis à jour');
        } else {
            window.dataSets = generatedDataset;
        }

        // Configurer l'observer pour les changements futurs
        const observer = setupMutationObserver(() => {
            const newDataset = generateDatasetFromDOM();
            if (window.dataSets) {
                window.dataSets = mergeDatasets(newDataset, window.dataSets);
            }

            // Déclencher un événement personnalisé pour notifier les autres scripts
            window.dispatchEvent(new CustomEvent('datasetUpdated', {
                detail: { dataset: window.dataSets }
            }));
        });

        console.log('Auto Dataset Generator initialisé');
    }

    // Exposer les fonctions utiles
    window.AutoDatasetGenerator = {
        generate: generateDatasetFromDOM,
        merge: mergeDatasets,
        init: init
    };

    // Auto-init
    init();
})();