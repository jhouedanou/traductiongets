// Debug script to visualize generated keywords
$(document).ready(function() {
    
    // Add debug functionality
    function debugKeywords() {
        console.log('=== DEBUG: Generated Keywords ===');
        
        $('.nav-link-anchor').each(function(index) {
            const $link = $(this);
            const originalText = $link.text();
            const keywords = $link.attr('data-search-keywords');
            
            console.log(`${index + 1}. "${originalText}"`);
            console.log(`   Keywords: ${keywords}`);
            console.log('   ---');
        });
        
        console.log('=== End Debug ===');
    }
    
    // Add debug button to page (only in development)
    function addDebugButton() {
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            const debugButton = `
                <div class="debug-controls position-fixed" style="bottom: 20px; right: 20px; z-index: 9999;">
                    <button id="debug-keywords-btn" class="btn btn-warning btn-sm">
                        <i class="fas fa-bug"></i> Debug Keywords
                    </button>
                    <button id="export-keywords-btn" class="btn btn-info btn-sm mt-1">
                        <i class="fas fa-download"></i> Export Keywords
                    </button>
                </div>
            `;
            $('body').append(debugButton);
        }
    }
    
    // Export keywords to JSON
    function exportKeywords() {
        const keywordsData = [];
        
        $('.nav-link-anchor').each(function() {
            const $link = $(this);
            const originalText = $link.text();
            const keywords = $link.attr('data-search-keywords');
            const href = $link.attr('href');
            
            keywordsData.push({
                text: originalText,
                href: href,
                keywords: keywords ? keywords.split(' ') : []
            });
        });
        
        // Create downloadable JSON file
        const dataStr = JSON.stringify(keywordsData, null, 2);
        const dataBlob = new Blob([dataStr], {type: 'application/json'});
        const url = URL.createObjectURL(dataBlob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = 'search-keywords.json';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }
    
    // Test search functionality
    function testSearch(term) {
        console.log(`=== Testing search for: "${term}" ===`);
        
        let matches = 0;
        $('.nav-link-anchor').each(function() {
            const $link = $(this);
            const originalText = $link.text();
            const keywords = $link.attr('data-search-keywords') || '';
            
            if (originalText.toLowerCase().includes(term.toLowerCase()) || 
                keywords.toLowerCase().includes(term.toLowerCase())) {
                matches++;
                console.log(`✓ Match: "${originalText}"`);
                console.log(`  Keywords: ${keywords}`);
            }
        });
        
        console.log(`Total matches: ${matches}`);
        console.log('=== End Test ===');
    }
    
    // Initialize debug functionality
    setTimeout(function() {
        addDebugButton();
        
        // Event handlers for debug buttons
        $(document).on('click', '#debug-keywords-btn', function() {
            debugKeywords();
        });
        
        $(document).on('click', '#export-keywords-btn', function() {
            exportKeywords();
        });
        
        // Add console commands
        window.debugKeywords = debugKeywords;
        window.testSearch = testSearch;
        window.exportKeywords = exportKeywords;
        
        console.log('Debug functions available:');
        console.log('- debugKeywords() - Show all generated keywords');
        console.log('- testSearch("term") - Test search for a specific term');
        console.log('- exportKeywords() - Download keywords as JSON');
        
    }, 1000);
});