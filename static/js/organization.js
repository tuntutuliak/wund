/**
 * Organization page: smooth scroll for anchor links + scrollspy (active nav link).
 */
(function () {
  var navLinks = document.querySelectorAll(".js-org-nav-link");
  var sections = document.querySelectorAll(".organization-section");

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

  function updateActiveLink() {
    var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    var headerOffset = 100;
    var current = null;

    sections.forEach(function (section) {
      var slug = section.getAttribute("data-slug");
      var top = section.offsetTop - headerOffset;
      var height = section.offsetHeight;
      if (scrollTop >= top && scrollTop < top + height) {
        current = slug;
      }
    });

    navLinks.forEach(function (link) {
      var slug = link.getAttribute("data-slug");
      if (slug === current) {
        link.classList.add("is-active");
      } else {
        link.classList.remove("is-active");
      }
    });
  }

  navLinks.forEach(function (link) {
    link.addEventListener("click", scrollToSection);
  });

  window.addEventListener("scroll", function () {
    requestAnimationFrame(updateActiveLink);
  });

  window.addEventListener("load", updateActiveLink);
})();
