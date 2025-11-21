import httpx


class Wazzup:
    def __init__(self, api_key, url):
        self.URL = url
        self.API_KEY = api_key
        print("Создан экземпляр класса для работы с Wazzup API")

    def send_message(self, options):
        url = f"{self.URL}/message"

        payload = {
            "channelId": options.get("channelId"),
            "chatId": options.get("chatId"),
            "chatType": options.get("chatType"),
            "text": options.get("text"),
        }

        headers = {
            "Authorization": f"Bearer {self.API_KEY}",
            "Content-Type": "application/json",
        }

        try:
            with httpx.Client() as client:
                response = client.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                print("Сообщение успешно отправлено")
                return response.json()
            else:
                print(
                    f"Произошла ошибка при отправке: {response.status_code} - {response.text}"
                )
                return None

        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")
            return None

    def get_channels(self):
        try:
            with httpx.Client() as client:
                response = client.get(
                    f"{self.URL}/channels",
                    headers={
                        "Authorization": f"Bearer {self.API_KEY}",
                        "Content-Type": "application/json",
                    },
                )
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Произошла ошибка: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Ошибка при получении каналов: {e}")
            return None

    def get_channel_by_id(self, channel_id):
        channels = self.get_channels()
        if channels:
            for channel in channels:
                print(channel)
                if channel.get("channelId") == channel_id:
                    return channel
        return None

    # GETTERS
    def get_params_API(self):
        return {"URL": self.URL, "API_KEY": self.API_KEY}
