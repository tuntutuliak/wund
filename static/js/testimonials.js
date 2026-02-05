/**
 * Инициализация карусели отзывов: аватары (горизонтально) + синхронный текст снизу
 * Требует: jQuery, Slick (подключаются в core.min.js)
 */
(function () {
  'use strict';

  function initTestimonialsCarousel() {
    var $child = $('#child-carousel');
    var $parent = $('.testimonials-light .carousel-parent');

    if (!$child.length || !$parent.length) return;
    if (typeof $child.slick !== 'function') return;

    // Удаляем предыдущую инициализацию, если есть
    if ($child.hasClass('slick-initialized')) $child.slick('unslick');
    if ($parent.hasClass('slick-initialized')) $parent.slick('unslick');

    // Сначала инициализируем родительский слайдер (текст)
    $parent.slick({
      slidesToShow: 1,
      slidesToScroll: 1,
      asNavFor: '#child-carousel',
      arrows: false,
      dots: false,
      fade: true,
      infinite: true,
      autoplay: true,
      autoplaySpeed: 5000,
      swipe: false,
      adaptiveHeight: true
    });

    // Затем дочерний (аватары) — синхрон с родителем
    $child.slick({
      slidesToShow: 1,
      slidesToScroll: 1,
      asNavFor: '.testimonials-light .carousel-parent',
      arrows: true,
      dots: false,
      centerMode: true,
      centerPadding: '60px',
      infinite: true,
      focusOnSelect: true,
      swipe: true,
      mobileFirst: true,
      responsive: [
        { breakpoint: 0,   settings: { slidesToShow: 1 } },
        { breakpoint: 576, settings: { slidesToShow: 3 } },
        { breakpoint: 768, settings: { slidesToShow: 5 } },
        { breakpoint: 992, settings: { slidesToShow: 5 } },
        { breakpoint: 1200, settings: { slidesToShow: 5 } }
      ]
    });

    // Подсветка активного аватара
    $parent.on('afterChange', function (e, slick, currentSlide) {
      $child.find('.slick-slide').removeClass('slick-current');
      $child.find('.slick-slide').eq(currentSlide).addClass('slick-current');
    });
    $child.find('.slick-slide').eq(0).addClass('slick-current');
  }

  function run() {
    if (typeof jQuery === 'undefined' || typeof jQuery.fn.slick === 'undefined') {
      setTimeout(run, 50);
      return;
    }
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function () { setTimeout(initTestimonialsCarousel, 80); });
    } else {
      setTimeout(initTestimonialsCarousel, 80);
    }
  }
  run();
})();
