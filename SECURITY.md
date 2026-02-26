# Безопасность и секреты (Security)

## Переменные окружения

Все чувствительные данные вынесены в `.env`. Файл `.env` **не коммитируется** (см. `.gitignore`).

### Первый запуск

```bash
cp .env.example .env
# Отредактируйте .env и задайте DJANGO_SECRET_KEY (минимум 50 символов).
```

Генерация нового секретного ключа:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Обязательные переменные

| Переменная | Описание |
|------------|----------|
| `DJANGO_SECRET_KEY` | Секретный ключ Django. Обязателен. |

### Опциональные

- `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS` — режим отладки и хосты.
- `DJANGO_DB_ENGINE=postgresql` + `POSTGRES_*` — БД PostgreSQL.
- `RECAPTCHA_SITE_KEY`, `RECAPTCHA_SECRET_KEY` — reCAPTCHA.
- `EMAIL_*` — настройки почты.

Полный список и примеры — в `.env.example`.

---

## Очистка истории Git от секретов

Если `SECRET_KEY` или другие секреты **уже попали в коммиты**, их нужно считать скомпрометированными и:

1. **Сменить все секреты** (новый `DJANGO_SECRET_KEY`, пароли БД, reCAPTCHA, ключи API).
2. **Удалить секреты из истории** (переписать историю).

### Вариант A: BFG Repo-Cleaner

```bash
# Установка (Homebrew): brew install bfg
# Скачать: https://rtyley.github.io/bfg-repo-cleaner/

# Клонировать репо как mirror
git clone --mirror https://github.com/your-org/wunder.git wunder-clean
cd wunder-clean

# Подставить реальный ключ, который был в коде
bfg --replace-text <(echo 'django-insecure-io2hwegleq+%iqkug_k3=$3c6-3+(3ftjhf(p_65xd=7^xn+%y')
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force
```

### Вариант B: git filter-repo (рекомендуется)

```bash
pip install git-filter-repo

# В копии репозитория
git filter-repo --path wunder/settings.py --invert-paths
# Затем заново добавить settings.py из текущей версии (без секретов) и закоммитить.
# Либо использовать --replace-text для подстановки плейсхолдера.
```

### Вариант C: Ручной rebase (для 1–2 последних коммитов)

```bash
git rebase -i HEAD~2
# Пометить коммит с секретом как edit
# Исправить файл, убрать секрет
git add wunder/settings.py
git commit --amend --no-edit
git rebase --continue
git push --force-with-lease
```

### После переписывания истории

- Все разработчики должны сделать **новый клон** или `git fetch origin && git reset --hard origin/master`.
- Предупреждайте команду: **force-push меняет историю**, согласуйте с остальными.

---

## Рекомендации

- **Production:** не используйте `DJANGO_DEBUG=True`. Задайте `DJANGO_ALLOWED_HOSTS` явно.
- **Секреты:** храните только в `.env` или в секретном менеджере (Vault, AWS Secrets Manager). Никогда не коммитьте `.env`.
- **Ротация:** периодически меняйте `DJANGO_SECRET_KEY` и пароли БД; после утечки — немедленно.
- **Права на файлы:** `chmod 600 .env` на сервере.
- **Проверка:** перед каждым деплоем убедитесь, что `SECRET_KEY` и пароли не в коде:  
  `git grep -E 'SECRET_KEY|password\s*=\s*["\']' -- '*.py'` (должно быть пусто в репозитории).
