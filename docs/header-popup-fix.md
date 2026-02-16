# Header popup — анализ и правки

## 1. Краткое техническое объяснение

В оригинале (temp/site/index.html) кнопка «Book now» и блок с формой связаны через `data-rd-navbar-toggle="#rd-navbar-login-NaN"` и `id="rd-navbar-login-NaN"`. Обработка клика и показ/скрытие popup выполняются скриптами темы (core.min.js). В Django-версии ID заменены на `rd-navbar-application-school`; в base.html добавлен отдельный inline-скрипт, который вешает свой обработчик на этот popup. Логика RD Navbar (один триггер — один target по селектору) сохранена, но для стабильной работы нужно синхронно переключать класс `active` и у popup, и у кнопки, а также гарантировать закрытие по клику вне области.

## 2. Список обнаруженных проблем

| # | Проблема | Деталь |
|---|----------|--------|
| 1 | Класс `active` только на popup | В теме кнопка подсвечивается через `.list-inline-bordered button.active`; без добавления `active` на триггер кнопка не отражает состояние «открыто». |
| 2 | Закрытие по клику вне | При закрытии по клику вне снимается `active` только с popup; с триггера не снимается — при следующем открытии состояние кнопки и панели может рассинхронизироваться. |
| 3 | Возможный конфликт с core.min.js | core.min.js содержит RD Navbar и может тоже обрабатывать `[data-rd-navbar-toggle]`. Если он вешает обработчик на тот же элемент, возможен двойной toggle (открытие и мгновенное закрытие). Использование `e.stopPropagation()` в нашем скрипте уменьшает риск. |
| 4 | Селектор в скрипте жёстко привязан к ID | Селектор `#rd-navbar-application-school` зашит в base.html; при смене ID в header.html скрипт перестанет находить элементы. ID в header и в скрипте должны совпадать. |

Структура HTML (триггер и popup внутри одного `<li>`, правильные классы и атрибуты) совпадает с оригиналом; несовпадений по ID между кнопкой и блоком нет.

## 3. Минимально необходимые исправления

- В inline-скрипте в base.html при клике на триггер переключать `active` и у popup, и у кнопки.
- В обработчике «клик вне» снимать `active` и с popup, и с триггера.

## 4. Исправленные фрагменты кода

### HTML (templates/includes/header.html)

Структура уже соответствует оригиналу; менять разметку не требуется. Проверьте, что ID и data-атрибут совпадают:

- Кнопка: `data-rd-navbar-toggle="#rd-navbar-application-school"`
- Блок: `id="rd-navbar-application-school"`

Фрагмент для проверки:

```html
<li>
  <button class="rd-navbar-popup-toggle text-uppercase font-weight-light" data-rd-navbar-toggle="#rd-navbar-application-school" type="button">...</button>
  <div class="rd-navbar-popup" id="rd-navbar-application-school">
    ...
  </div>
</li>
```

### JS (templates/base.html) — заменить блок скрипта

Заменить текущий блок «Выпадающая форма заявки» на:

```html
    <!-- RD Navbar: popup «Оставить заявку» — data-rd-navbar-toggle + class .active -->
    <script>
      (function() {
        var toggle = document.querySelector('.rd-navbar-popup-toggle[data-rd-navbar-toggle="#rd-navbar-application-school"]');
        var popup = document.getElementById('rd-navbar-application-school');
        if (!toggle || !popup) return;
        function closePopup() {
          popup.classList.remove('active');
          toggle.classList.remove('active');
        }
        toggle.addEventListener('click', function(e) {
          e.preventDefault();
          e.stopPropagation();
          popup.classList.toggle('active');
          toggle.classList.toggle('active');
        });
        document.addEventListener('click', function(e) {
          if (popup.classList.contains('active') && !popup.contains(e.target) && !toggle.contains(e.target)) {
            closePopup();
          }
        });
      })();
    </script>
```

## 5. Рекомендации по структуре

- Не удалять классы `rd-navbar-popup`, `rd-navbar-popup-toggle` и атрибут `data-rd-navbar-toggle` — от них зависят стили и поведение темы.
- Не подключать отдельную модальную систему для этой формы — popup должен оставаться нативным блоком RD Navbar.
- При смене ID popup (например, с `rd-navbar-application-school` на другой) обязательно обновить тот же ID в селекторе в base.html.
- Файл `static/js/rd-navbar-toggle.js` в проекте закомментирован; общая логика toggles идёт из core.min.js. Inline-скрипт оставить в base.html как явную привязку к нашему popup, чтобы не зависеть от внутренней реализации core.min.js.

После этих правок кнопка «Оставить заявку» должна открывать/закрывать popup без скачка прокрутки, на десктопе и мобильных, с подсветкой кнопки в открытом состоянии и закрытием по клику вне.
