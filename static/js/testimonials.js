document.addEventListener("DOMContentLoaded", function() {
  function initHomepageCarousel() {
    var carouselChild = document.getElementById("child-carousel");
    var carouselParent = document.querySelector(".testimonials-light .carousel-parent");
    if (!carouselChild || !carouselParent) return;
    if (typeof jQuery === "undefined" || typeof jQuery.fn.slick !== "function") {
      setTimeout(initHomepageCarousel, 50);
      return;
    }
    (function() {
      var $ = jQuery;
      var $child = $(carouselChild);
      var $parent = $(carouselParent);
      if ($child.hasClass("slick-initialized")) $child.slick("unslick");
      if ($parent.hasClass("slick-initialized")) $parent.slick("unslick");
      $parent.slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        asNavFor: "#child-carousel",
        arrows: false,
        dots: false,
        fade: true,
        infinite: true,
        autoplay: true,
        autoplaySpeed: 5000,
        swipe: false,
        adaptiveHeight: true
      });
      $child.slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        asNavFor: ".testimonials-light .carousel-parent",
        arrows: true,
        dots: false,
        centerMode: true,
        centerPadding: "60px",
        infinite: true,
        focusOnSelect: true,
        swipe: true,
        mobileFirst: true,
        responsive: [
          { breakpoint: 0, settings: { slidesToShow: 1 } },
          { breakpoint: 576, settings: { slidesToShow: 3 } },
          { breakpoint: 768, settings: { slidesToShow: 5 } },
          { breakpoint: 992, settings: { slidesToShow: 5 } },
          { breakpoint: 1200, settings: { slidesToShow: 5 } }
        ]
      });
      $parent.on("afterChange", function(e, slick, currentSlide) {
        $child.find(".slick-slide").removeClass("slick-current");
        $child.find(".slick-slide").eq(currentSlide).addClass("slick-current");
      });
      $child.find(".slick-slide").eq(0).addClass("slick-current");
    })();
  }
  setTimeout(initHomepageCarousel, 80);

  (function() {
    /* Testimonials page grid: IntersectionObserver only when .testimonials-page exists */
    var container = document.querySelector(".testimonials-page");
    if (!container) return;
    var observerOptions = { root: null, rootMargin: "0px", threshold: 0.1 };
    var observerCallback = function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) entry.target.classList.add("fade-in");
      });
    };
    var observer = new IntersectionObserver(observerCallback, observerOptions);
    container.querySelectorAll(".testimonial-card").forEach(function(card) { observer.observe(card); });
    var sectionHeader = container.querySelector(".section-header");
    if (sectionHeader) observer.observe(sectionHeader);
    var ctaSection = container.querySelector(".cta-section");
    if (ctaSection) observer.observe(ctaSection);
  })();
});
