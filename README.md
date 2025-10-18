
# courier_bot_ozon_tikhaya_2

Бот для курьеров на `aiogram 3` с Supabase (Postgres).

## Быстрый старт (локально)

```bash
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows
pip install -r requirements.txt

cp .env.example .env
# заполни переменные окружения

python -m app.main
```

## Переменные окружения

Смотри `.env.example`.

## Структура

```
app/
  main.py
  config/
  routers/
  services/
  utils/
migrations/
.github/workflows/ci.yml
```

## Заметки
- Дата создания шаблона: 2025-10-18T14:11:32.256475 UTC.
- По умолчанию — long polling. Под вебхук можно добавить профиль позже.
