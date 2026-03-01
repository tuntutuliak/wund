/**
 * Contacts page: smooth scroll for anchor links + scrollspy (active nav item).
 */
(function () {
  var navLinks = document.querySelectorAll(".contacts-nav-link");
  var sections = document.querySelectorAll(".contacts-section");
  var navItems = document.querySelectorAll(".js-contacts-nav-item");

  function scrollToSection(e) {
    var href = e.currentTarget.getAttribute("href");
    if (href && href.indexOf("#") === 0) {
      var id = href.slice(1);
      var el = document.getElementById(id);
      if (el) {
        e.preventDefault();
        el.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    }
  }

  function updateActiveNav() {
    var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    var offset = 120;
    var current = null;

    sections.forEach(function (section) {
      var slug = section.getAttribute("data-slug");
      if (!slug) return;
      var top = section.offsetTop - offset;
      var height = section.offsetHeight;
      if (scrollTop >= top && scrollTop < top + height) {
        current = slug;
      }
    });

    navItems.forEach(function (item) {
      var slug = item.getAttribute("data-slug");
      if (slug === current) {
        item.classList.add("active");
      } else {
        item.classList.remove("active");
      }
    });
  }

  navLinks.forEach(function (link) {
    link.addEventListener("click", scrollToSection);
  });

  window.addEventListener("scroll", function () {
    requestAnimationFrame(updateActiveNav);
  });
  window.addEventListener("load", updateActiveNav);
})();
