import fastapi
import uvicorn
import threading
import os
from dotenv import load_dotenv
from classes.postgres import Postgres
from classes.wazzup import Wazzup
from classes.bot import TelegramBOT

load_dotenv()

app = fastapi.FastAPI()
wazzup = Wazzup(os.getenv("WAZZUP_API_KEY"), os.getenv("WAZZUP_API_URL"))
postgres = Postgres(
    {
        "dbname": os.getenv("POSTGRES_DB_NAME"),
        "user": os.getenv("POSTGRES_DB_USER"),
        "password": os.getenv("POSTGRES_DB_PASSWORD"),
        "host": os.getenv("POSTGRES_DB_HOST"),
        "port": os.getenv("POSTGRES_DB_PORT"),
    }
)
telegram_bot = TelegramBOT(
    os.getenv("TELEGRAM_BOT_TOKEN"), os.getenv("TELEGRAM_BOT_URL")
)


@app.post("/sub", status_code=200)
def response_sub(data=fastapi.Body()):
    options = {}
    message = data["messages"][0]
    if message.get("isEcho") == False:
        options["channelId"] = message["channelId"]
        options["chatType"] = message["chatType"]
        options["chatId"] = message["chatId"]
        options["text"] = (
            "Здравствуйте! Наши консультанты будут рады ответить на все ваши вопросы в Телеграм чате! https://t.me/+ETTFVnzsHMY2NTBi"
        )
        wazzup.send_message(options)
    print(f"Уведомление: {data}")
    return fastapi.responses.PlainTextResponse(content="Подключение webhook")


# if __name__ == "__main__":
    # config = uvicorn.Config(
    #     "index:app",
    #     host=os.getenv("HOST"),
    #     port=int(os.getenv("PORT")),
    #     log_level="info",
    #     reload=True,
    # )
    # server = uvicorn.Server(config)
    # server.run()
    # connect_db = postgres.connect()
    # if connect_db is None:
    #     print("Не удалось подключиться к базе данных PostgreSQL. Сервер не запущен")
    # else:
    # telegram_bot.run()
    # Запуск Telegram бота в отдельном потоке
    # threading.Thread(target=telegram_bot.run, daemon=True).start()

    # # Запусе веб-серверая
