# Боты поддержки на Dialogflow (Telegram + VK)

Репозиторий содержит двух ботов технической поддержки - Telegram и ВКонтакте, 
которые отвечают пользователям через Google Dialogflow.

**Telegram-бот:** [@OnlinePublishersBot](https://t.me/OnlinePublishersBot)

**ВК-сообщество/бот:**[@VKBot](https://vk.ru/club241724042)

# Как установить
Операционная система: любая, где доступен Python 3 (Windows, macOS, Linux). Используем 'pip' для установки зависимостей (requests, python-dotenv):
```
pip install -r requirements.txt
```
Рекомендуется использовать virtualenv/env для изоляции проекта.

# Примеры запуска ботов (локально)

1) Telegram

```
python tg_bot.py
```

2) ВК

```
python vk_bot.py
```


# Переменные окружения
Программа использует нестандартные переменные окружения для настройки. Эти переменные не могут быть автоматически обнаружены и должны быть указаны в файле `.env` перед запуском программы.

**GOOGLE_CLOUD_PROJECT** - ID проекта Google Cloud / Dialogflow.

**GOOGLE_APPLICATION_CREDENTIALS** - путь к JSON-ключу сервисного аккаунта.

**DIALOGFLOW_API_KEY** - ключ API Dialogflow.

**TG_BOT_TOKEN** - токен Telegram-бота.

**TG_CHAT_ID** - ID пользователя Telegram.

**VK_BOT_TOKEN=** - токен сообщества ВКонтакте.

Пример результата для Telegram:

![speech_tg_bot](https://raw.githubusercontent.com/tomaa-dev/gif/main/speech.gif)
