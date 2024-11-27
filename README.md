# SendMailBot

### Проект представляет собой Telegram-бота, который позволяет отправлять сообщения на указанный email через SMTP-сервер Яндекса

## Установка и запуск

1. Склонируйте репозиторий и перейдите в директорию проекта:

    ```
    https://github.com/BessoSonia/SendMailBot
    cd SendMailBot
    ```

2. Установите зависимости

    ```
    pip install -r requirements.txt
    ```

3. Настройте переменные окружения

    - TELEGRAM_API_KEY: токен вашего Telegram-бота
    - SMTP_SERVER: адрес SMTP-сервера (smtp.yandex.ru)
    - SMTP_PORT: порт SMTP-сервера (587)
    - SMTP_USERNAME: email, который используется для авторизации и с которого будут отправляться письма
    - SMTP_PASSWORD: пароль приложения для SMTP

4. Запуск

    Запустите бот:

    ```
    python mail_bot.py 
    ``` 

    Найдите бота в Telegram и начните взаимодействие с командой /start.

    Следуйте инструкциям.
