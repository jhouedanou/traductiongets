/**
 * i18n — Translation system for G & S
 *
 * Approach: on first run, captures the original innerHTML of every [data-i18n]
 * element as the FR source. When switching to EN, swaps innerHTML with the
 * EN translation from the JSON file. Preserves all HTML formatting.
 *
 * Usage in HTML:
 *   <p data-i18n="page_certificat_centrale.intro">Contenu français <strong>ici</strong></p>
 *   <input data-i18n-placeholder="search.placeholder">
 *
 * Usage in JS:
 *   i18n.t('nav.home')           // → translated string
 *   i18n.setLang('en')           // switch and re-render
 *   i18n.getLang()                // current lang code
 *   i18n.translateElement(el)     // translate a subtree (after dynamic load)
 */
(function (root) {
    'use strict';

    var SUPPORTED_LANGS = ['fr', 'en'];
    var DEFAULT_LANG = 'fr';
    var STORAGE_KEY = 'g-et-s-lang';

    var _translations = {};   // { en: {...}, fr: {...} }
    var _originals = {};      // key → original innerHTML (captured from DOM = FR source)
    var _currentLang = DEFAULT_LANG;
    var _ready = false;
    var _readyCallbacks = [];

    // ---- helpers ----

    function computeBasePath() {
        try {
            var scriptEl = document.querySelector('script[src*="js/i18n.js"]');
            if (!scriptEl) return '';
            var scriptPath = decodeURIComponent(new URL(scriptEl.src, document.baseURI).pathname);
            var anchor = '/js/i18n.js';
            var idx = scriptPath.lastIndexOf(anchor);
            if (idx < 0) return '';
            var siteRootPath = scriptPath.substring(0, idx + 1);
            var pagePath = decodeURIComponent(window.location.pathname);
            if (pagePath.indexOf(siteRootPath) !== 0) return '';
            var remainder = pagePath.substring(siteRootPath.length);
            var parts = remainder.split('/').filter(function (p) { return p.length > 0; });
            var depth = Math.max(0, parts.length - 1);
            return depth > 0 ? Array(depth + 1).join('../') : '';
        } catch (e) {
            return '';
        }
    }

    function resolve(obj, key) {
        if (!obj || !key) return undefined;
        var parts = key.split('.');
        var cur = obj;
        for (var i = 0; i < parts.length; i++) {
            if (cur === undefined || cur === null) return undefined;
            cur = cur[parts[i]];
        }
        return cur;
    }

    function detectLang() {
        var params = new URLSearchParams(window.location.search);
        var urlLang = params.get('lang');
        if (urlLang && SUPPORTED_LANGS.indexOf(urlLang) !== -1) return urlLang;
        try {
            var stored = localStorage.getItem(STORAGE_KEY);
            if (stored && SUPPORTED_LANGS.indexOf(stored) !== -1) return stored;
        } catch (e) {}
        return DEFAULT_LANG;
    }

    // ---- translation loading ----

    function loadTranslation(lang, cb) {
        if (_translations[lang]) { cb(); return; }
        var basePath = computeBasePath();
        var url = basePath + 'data/translations/' + lang + '.json';
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState !== 4) return;
            if (xhr.status === 200 || xhr.status === 0) {
                try { _translations[lang] = JSON.parse(xhr.responseText); }
                catch (e) { console.error('[i18n] Parse error ' + lang, e); }
            } else {
                console.error('[i18n] Load error ' + url + ' (' + xhr.status + ')');
            }
            cb();
        };
        xhr.send();
    }

    // ---- core translate ----

    /**
     * Capture the original FR innerHTML of an element if not already stored,
     * then apply the current language.
     */
    function translateNode(el) {
        var key = el.getAttribute('data-i18n');
        if (key) {
            // Capture original HTML on first encounter (this IS the FR content)
            if (!_originals[key] && !el.getAttribute('data-i18n-captured')) {
                _originals[key] = el.innerHTML;
                el.setAttribute('data-i18n-captured', '1');
            }

            if (_currentLang === 'fr') {
                // Restore original French HTML
                if (_originals[key] !== undefined) {
                    el.innerHTML = _originals[key];
                }
            } else {
                // Apply EN translation
                var val = resolve(_translations[_currentLang], key);
                if (val !== undefined && typeof val === 'string') {
                    el.innerHTML = val;
                    // If the injected HTML itself contains data-i18n elements,
                    // translate them immediately (handles container keys)
                    var nested = el.querySelectorAll('[data-i18n],[data-i18n-placeholder],[data-i18n-alt],[data-i18n-title],[data-i18n-aria-label]');
                    for (var ni = 0; ni < nested.length; ni++) {
                        translateNode(nested[ni]);
                    }
                }
                // If no translation found, keep original (FR fallback)
            }
        }

        // Handle attribute translations: placeholder, alt, title, aria-label
        var attrs = ['placeholder', 'alt', 'title', 'aria-label'];
        attrs.forEach(function (attr) {
            var attrKey = el.getAttribute('data-i18n-' + attr);
            if (attrKey) {
                // Capture original attr
                var origAttrKey = '_i18n_orig_' + attr;
                if (!el.getAttribute(origAttrKey)) {
                    el.setAttribute(origAttrKey, el.getAttribute(attr) || '');
                }

                if (_currentLang === 'fr') {
                    el.setAttribute(attr, el.getAttribute(origAttrKey) || '');
                } else {
                    var attrVal = resolve(_translations[_currentLang], attrKey);
                    if (attrVal !== undefined) {
                        el.setAttribute(attr, attrVal);
                    }
                }
            }
        });
    }

    function translateDOM(rootEl) {
        rootEl = rootEl || document;
        var selector = '[data-i18n], [data-i18n-placeholder], [data-i18n-alt], [data-i18n-title], [data-i18n-aria-label]';
        var els = rootEl.querySelectorAll(selector);
        for (var i = 0; i < els.length; i++) {
            translateNode(els[i]);
        }
        document.documentElement.lang = _currentLang;

        // Update <title>
        var titleMeta = document.querySelector('meta[name="i18n-title-key"]');
        if (titleMeta) {
            if (_currentLang === 'fr') {
                // Restore original title
                if (!titleMeta.getAttribute('data-orig-title')) {
                    titleMeta.setAttribute('data-orig-title', document.title);
                }
                document.title = titleMeta.getAttribute('data-orig-title') || document.title;
            } else {
                if (!titleMeta.getAttribute('data-orig-title')) {
                    titleMeta.setAttribute('data-orig-title', document.title);
                }
                var titleVal = resolve(_translations[_currentLang], titleMeta.getAttribute('content'));
                if (titleVal) document.title = titleVal;
            }
        }
    }

    // ---- public API ----

    function t(key, fallback) {
        var val = resolve(_translations[_currentLang], key);
        return val !== undefined ? val : (fallback !== undefined ? fallback : key);
    }

    function getLang() { return _currentLang; }

    function setLang(lang) {
        if (SUPPORTED_LANGS.indexOf(lang) === -1) return;
        _currentLang = lang;
        try { localStorage.setItem(STORAGE_KEY, lang); } catch (e) {}
        document.documentElement.lang = lang;
        updateLangFlags();

        if (!_translations[lang]) {
            loadTranslation(lang, function () {
                translateDOM();
                document.dispatchEvent(new CustomEvent('langchanged', { detail: { lang: lang } }));
            });
        } else {
            translateDOM();
            document.dispatchEvent(new CustomEvent('langchanged', { detail: { lang: lang } }));
        }
    }

    function updateLangFlags() {
        var frFlag = document.querySelector('a[data-lang="fr"]') ||
                     document.querySelector('a[title*="fran"]');
        var enFlag = document.querySelector('a[data-lang="en"]') ||
                     document.querySelector('a[title*="English"]');
        if (frFlag) frFlag.classList.toggle('lang-active', _currentLang === 'fr');
        if (enFlag) enFlag.classList.toggle('lang-active', _currentLang === 'en');
    }

    function hookLanguageFlags() {
        document.querySelectorAll('a[title*="fran"], a[data-lang="fr"]').forEach(function (flag) {
            flag.setAttribute('data-lang', 'fr');
            flag.addEventListener('click', function (e) {
                e.preventDefault();
                setLang('fr');
            });
        });
        document.querySelectorAll('a[title*="English"], a[data-lang="en"]').forEach(function (flag) {
            flag.setAttribute('data-lang', 'en');
            flag.addEventListener('click', function (e) {
                e.preventDefault();
                setLang('en');
            });
        });
        updateLangFlags();
    }

    function onReady(cb) {
        if (_ready) { cb(); return; }
        _readyCallbacks.push(cb);
    }

    function _fireReady() {
        _ready = true;
        _readyCallbacks.forEach(function (cb) { try { cb(); } catch (e) { console.error(e); } });
        _readyCallbacks = [];
    }

    // ---- init ----

    function init() {
        _currentLang = detectLang();

        var loaded = 0;
        var total = SUPPORTED_LANGS.length;

        SUPPORTED_LANGS.forEach(function (lang) {
            loadTranslation(lang, function () {
                loaded++;
                if (loaded === total) {
                    // Only translate if user previously selected EN
                    if (_currentLang !== DEFAULT_LANG) {
                        translateDOM();
                    } else {
                        // Still capture originals for later switching
                        var els = document.querySelectorAll('[data-i18n]');
                        for (var i = 0; i < els.length; i++) {
                            var key = els[i].getAttribute('data-i18n');
                            if (key && !_originals[key]) {
                                _originals[key] = els[i].innerHTML;
                                els[i].setAttribute('data-i18n-captured', '1');
                            }
                        }
                    }
                    _fireReady();
                }
            });
        });
    }

    root.i18n = {
        t: t,
        getLang: getLang,
        setLang: setLang,
        translateDOM: translateDOM,
        translateElement: function (el) {
            if (!el) return;
            var selector = '[data-i18n], [data-i18n-placeholder], [data-i18n-alt], [data-i18n-title], [data-i18n-aria-label]';
            var els = el.querySelectorAll(selector);
            for (var i = 0; i < els.length; i++) translateNode(els[i]);
            if (el.hasAttribute && el.hasAttribute('data-i18n')) translateNode(el);
        },
        hookLanguageFlags: hookLanguageFlags,
        onReady: onReady,
        init: init
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})(window);
