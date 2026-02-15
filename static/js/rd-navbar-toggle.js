/**
 * RD Navbar toggle — vanilla JS, no jQuery.
 * Binds to all [data-rd-navbar-toggle], toggles target element and trigger with class "active".
 * Runs on DOMContentLoaded; one listener per toggle; click-outside closes panel.
 *
 *(function () {
 * 'use strict';
 *
 * var PAIRS = [];
*
 * function init() {
  *  var toggles = document.querySelectorAll('[data-rd-navbar-toggle]:not(button.rd-navbar-toggle)');
   * if (!toggles.length) return;
*
 *   toggles.forEach(function (trigger) {
  *    var selector = trigger.getAttribute('data-rd-navbar-toggle');
   *   if (!selector) return;
    *  var target = document.querySelector(selector);
     * if (!target) return;
*
 *     PAIRS.push({ trigger: trigger, target: target });
*
 *     target.querySelectorAll('.rd-nav-link').forEach(function (link) {
  *      link.addEventListener('click', function () {
   *       trigger.classList.remove('active');
    *      target.classList.remove('active');
     *   });
      *});
*
 *     trigger.addEventListener('click', function (e) {
  *      e.preventDefault();
   *     trigger.classList.toggle('active');
    *    target.classList.toggle('active');
     * });
    *});
*
 *   document.addEventListener('click', function (e) {
  *    PAIRS.forEach(function (pair) {
   *     if (!pair.target.classList.contains('active')) return;
    *    if (pair.target.contains(e.target) || pair.trigger.contains(e.target)) return;
     *   pair.trigger.classList.remove('active');
      *  pair.target.classList.remove('active');
      *});
    *});
  *}
*
 * if (document.readyState === 'loading') {
  *  document.addEventListener('DOMContentLoaded', init);
  *} else {
  *  init();
  *}
*})();
*/