/**
 * Teachers catalog: open photo in modal (vanilla JS, no frameworks).
 */
(function () {
  var modal = document.getElementById("teacher-photo-modal");
  var modalImage = document.getElementById("teacher-modal-image");
  var modalCaption = document.getElementById("teacher-modal-title");
  var openButtons = document.querySelectorAll(".js-teacher-photo");
  var closeButtons = document.querySelectorAll(".js-modal-close");

  function openModal(photoUrl, name) {
    if (!modal || !modalImage || !modalCaption) return;
    modalImage.src = photoUrl;
    modalImage.alt = name;
    modalCaption.textContent = name;
    modal.setAttribute("aria-hidden", "false");
    modal.classList.add("is-open");
    document.body.style.overflow = "hidden";
  }

  function closeModal() {
    if (!modal) return;
    modal.classList.remove("is-open");
    modal.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
  }

  openButtons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var url = btn.getAttribute("data-photo-url");
      var name = btn.getAttribute("data-name") || "";
      if (url) openModal(url, name);
    });
  });

  closeButtons.forEach(function (btn) {
    btn.addEventListener("click", closeModal);
  });

  modal.addEventListener("click", function (e) {
    if (e.target === modal || e.target.classList.contains("teacher-modal-backdrop")) {
      closeModal();
    }
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && modal && modal.classList.contains("is-open")) {
      closeModal();
    }
  });
})();
