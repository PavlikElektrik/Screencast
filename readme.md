# Проект Catalog

Это учебный проект на Django, реализующий базовый каталог с главной страницей и страницей контактов.

## Структура проекта

- `screencast/` — основной Django-проект
- `catalog/` — приложение каталога
- `templates/` — шаблоны HTML
- `.gitignore`, `pyproject.toml`, `poetry.lock` — конфигурации

## Требования

- Python 3.9+
- Django
- Bootstrap 5 (через CDN)

## Установка

```bash
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver