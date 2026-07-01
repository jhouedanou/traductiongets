/**
 * pdf-i18n — Swaps embedded / linked PDFs to their English version when the
 * site language is EN, and back to the French version for FR.
 *
 * Driven by js/i18n.js: re-applies on the `langchanged` event and on i18n ready.
 * Falls back to the stored language if i18n is not (yet) available.
 *
 * Mark any <embed> / <iframe> / <object> / <a> with:
 *   data-pdf-fr="path/to/french.pdf"     (also keep this as the initial src/href)
 *   data-pdf-en="path/to/english.pdf"
 *
 * FR is the default, so the element's hardcoded src/href should be the FR PDF;
 * this keeps the page working even with JavaScript disabled.
 */
(function () {
    'use strict';

    function currentLang() {
        try { if (window.i18n && typeof i18n.getLang === 'function') return i18n.getLang(); } catch (e) {}
        try { var s = localStorage.getItem('g-et-s-lang'); if (s === 'en' || s === 'fr') return s; } catch (e) {}
        return 'fr';
    }

    function apply() {
        var lang = currentLang();
        var els = document.querySelectorAll('[data-pdf-fr]');
        for (var i = 0; i < els.length; i++) {
            var el = els[i];
            var fr = el.getAttribute('data-pdf-fr');
            var en = el.getAttribute('data-pdf-en') || fr;
            var url = (lang === 'en') ? en : fr;
            var tag = el.tagName.toUpperCase();

            if (tag === 'A') {
                if (el.getAttribute('href') !== url) el.setAttribute('href', url);
            } else if (tag === 'EMBED' || tag === 'IFRAME' || tag === 'OBJECT') {
                var attr = (tag === 'OBJECT') ? 'data' : 'src';
                if (el.getAttribute(attr) !== url) {
                    el.setAttribute(attr, url);
                    // <embed> / <object> don't reliably reload on attribute change —
                    // re-insert a clone (keeps data-pdf-* attrs) to force a reload.
                    if (tag !== 'IFRAME' && el.parentNode) {
                        el.parentNode.replaceChild(el.cloneNode(true), el);
                    }
                }
            }
        }
    }

    function start() {
        apply();
        document.addEventListener('langchanged', apply);
        try { if (window.i18n && typeof i18n.onReady === 'function') i18n.onReady(apply); } catch (e) {}
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', start);
    } else {
        start();
    }
})();
