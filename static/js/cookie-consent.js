(function () {
  var STORAGE_KEY = 'cookieConsent.v1'; // accept | reject

  function getChoice() {
    try {
      return localStorage.getItem(STORAGE_KEY);
    } catch (e) {
      return null;
    }
  }

  function setChoice(value) {
    try {
      localStorage.setItem(STORAGE_KEY, value);
    } catch (e) {
      // ignore
    }
  }

  function showBanner() {
    var el = document.getElementById('cookie-consent');
    if (!el) return;
    el.hidden = false;
  }

  function hideBanner() {
    var el = document.getElementById('cookie-consent');
    if (!el) return;
    el.hidden = true;
  }

  function activateDeferredScripts(category) {
    var selector = 'script[type="text/plain"][data-cookiecategory="' + category + '"]';
    var nodes = document.querySelectorAll(selector);
    nodes.forEach(function (node) {
      var s = document.createElement('script');
      // copy attrs
      for (var i = 0; i < node.attributes.length; i++) {
        var a = node.attributes[i];
        if (a.name === 'type') continue;
        if (a.name === 'data-cookiecategory') continue;
        s.setAttribute(a.name, a.value);
      }
      if (node.src) {
        s.src = node.src;
        s.async = node.async;
        s.defer = node.defer;
      }
      if (node.textContent && node.textContent.trim()) {
        s.text = node.textContent;
      }
      node.parentNode.insertBefore(s, node);
      node.parentNode.removeChild(node);
    });
  }

  function enableNonEssential() {
    // Здесь включаем аналитику/маркетинг ТОЛЬКО после согласия.
    // Поддержка "отложенных" скриптов:
    // <script type="text/plain" data-cookiecategory="analytics"> ... </script>
    // <script type="text/plain" data-cookiecategory="marketing" src="..."></script>
    activateDeferredScripts('analytics');
    activateDeferredScripts('marketing');
    window.dispatchEvent(new CustomEvent('cookie-consent:accept'));
  }

  function disableNonEssential() {
    // Мы ничего не грузим. Если в будущем появятся cookie-скрипты,
    // их надо подключать как type="text/plain" и активировать только после accept.
    window.dispatchEvent(new CustomEvent('cookie-consent:reject'));
  }

  function applyChoice(choice) {
    if (choice === 'accept') enableNonEssential();
    if (choice === 'reject') disableNonEssential();
  }

  function bindButtons() {
    var root = document.getElementById('cookie-consent');
    if (!root) return;
    root.addEventListener('click', function (e) {
      var btn = e.target && e.target.closest ? e.target.closest('[data-cookie-consent]') : null;
      if (!btn) return;
      var value = btn.getAttribute('data-cookie-consent');
      if (value !== 'accept' && value !== 'reject') return;
      setChoice(value);
      hideBanner();
      applyChoice(value);
    });
  }

  function bindSettingsLinks() {
    var links = document.querySelectorAll('[data-cookie-settings-open]');
    links.forEach(function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        try {
          localStorage.removeItem(STORAGE_KEY);
        } catch (err) {
          // ignore
        }
        showBanner();
      });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    bindButtons();
    bindSettingsLinks();

    var choice = getChoice();
    if (!choice) {
      showBanner();
      return;
    }
    // Баннер не показываем, а решение применяем.
    applyChoice(choice);
  });
})();

