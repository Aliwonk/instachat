import fastapi
# import os
# import dotenv
from classes.wazzup import Wazzup

# dotenv.load_dotenv()

app = fastapi.FastAPI()

# Инициализируем Wazzup только если переменные окружения существуют
wazzup_api_key = "64a39a928304492f89df4f7f8b16f692" # os.getenv("WAZZUP_API_KEY")
wazzup_api_url = "https://api.wazzup24.com/v3" # os.getenv("WAZZUP_API_URL")

if wazzup_api_key and wazzup_api_url:
    wazzup = Wazzup(wazzup_api_key, wazzup_api_url)
else:
    wazzup = None
    print("Предупреждение: WAZZUP_API_KEY или WAZZUP_API_URL не установлены")


@app.get("/", status_code=200)
def main():
    return fastapi.responses.PlainTextResponse(content="Сервер работает")


@app.post("/sub", status_code=200)
def response_sub(data: dict = fastapi.Body()):
    if wazzup is None:
        return fastapi.responses.PlainTextResponse(
            content="Wazzup не настроен", status_code=500
        )

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
