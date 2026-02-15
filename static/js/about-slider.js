(function () {
  'use strict';

  function init() {
    var slider = document.querySelector('.about-page .hero-slider');
    if (!slider) return;

    var slides = slider.querySelectorAll('.hero-slide');
    var prevBtn = slider.querySelector('.prev-btn');
    var nextBtn = slider.querySelector('.next-btn');
    var pageNum = slider.querySelector('.page-number');
    if (!slides.length || !prevBtn || !nextBtn || !pageNum) return;

    var total = slides.length;
    var current = 0;

    function goTo(index) {
      current = (index + total) % total;
      slides.forEach(function (slide, i) {
        slide.classList.toggle('active', i === current);
      });
      pageNum.textContent = (current + 1) + ' / ' + total;
    }

    prevBtn.addEventListener('click', function () {
      goTo(current - 1);
    });

    nextBtn.addEventListener('click', function () {
      goTo(current + 1);
    });

    goTo(0);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
