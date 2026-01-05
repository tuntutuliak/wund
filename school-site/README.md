# School Site

Проект сайта школы с поддержкой нескольких тем.

## Структура проекта

```
school-site/
├─ templates/          # HTML шаблоны (Jinja2)
├─ static/            # Статические файлы
│   ├─ img/          # Изображения
│   ├─ css/          # Скомпилированные CSS файлы
│   └─ js/           # JavaScript файлы
├─ scss/             # Исходные SCSS файлы
└─ README.md         # Документация
```

## Компиляция SCSS

Для компиляции SCSS в CSS используйте один из следующих методов:

### Использование sass (Dart Sass)
```bash
sass scss/style.scss static/css/style.css
```

### Использование node-sass
```bash
node-sass scss/style.scss -o static/css/
```

### Автоматическая компиляция с watch
```bash
sass --watch scss/style.scss:static/css/style.css
```

## Темы

Проект поддерживает две темы:
- `_theme-school.scss` - тема для школьного сайта
- `_theme-cruise.scss` - тема для круизного сайта

## Разработка

1. Установите зависимости для компиляции SCSS
2. Настройте watch режим для автоматической компиляции
3. Редактируйте файлы в папке `scss/`
4. Скомпилированные файлы будут в `static/css/style.css`

