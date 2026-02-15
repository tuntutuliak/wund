(function () {
  'use strict';

  function init() {
    var prevBtn = document.querySelector('.about-page .prev-btn');
    var nextBtn = document.querySelector('.about-page .next-btn');
    var pageNum = document.querySelector('.about-page .page-number');
    if (!prevBtn || !nextBtn || !pageNum) return;

    var currentPage = 1;
    var totalPages = 2;

    function updatePagination() {
      if (currentPage < 1) currentPage = 1;
      if (currentPage > totalPages) currentPage = totalPages;
      pageNum.textContent = currentPage + ' / ' + totalPages;
    }

    prevBtn.addEventListener('click', function () {
      if (currentPage > 1) {
        currentPage--;
        updatePagination();
      }
    });

    nextBtn.addEventListener('click', function () {
      if (currentPage < totalPages) {
        currentPage++;
        updatePagination();
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
