# Courier Bot

## Запуск локально
```bash
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows
pip install -r requirements.txt
cp .env.example .env
# заполни .env своими данными
python -m src.main
