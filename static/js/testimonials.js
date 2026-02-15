document.addEventListener("DOMContentLoaded", function() {
  (function() {
    var container = document.querySelector(".testimonials-page");
    if (!container) return;

    var observerOptions = {
      root: null,
      rootMargin: "0px",
      threshold: 0.1
    };

    var observerCallback = function(entries, observer) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("fade-in");
        }
      });
    };

    var observer = new IntersectionObserver(observerCallback, observerOptions);

    var cards = container.querySelectorAll(".testimonial-card");
    cards.forEach(function(card) {
      observer.observe(card);
    });

    var sectionHeader = container.querySelector(".section-header");
    if (sectionHeader) observer.observe(sectionHeader);

    var ctaSection = container.querySelector(".cta-section");
    if (ctaSection) observer.observe(ctaSection);
  })();
});
