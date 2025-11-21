from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from classes.postgres import Postgres


class TelegramBOT:
    _app = None
    _postgres = Postgres()
    _list_commands = {
        "/start": "Начать работу с ботом",
        "/help": "Получить справку по командам",
    }

    def __init__(self, TOKEN, URL):
        self._TOKEN = TOKEN
        self._URL = URL
        print("Создан экземпляр класса для работы с Telegram BOT API")

    # METHODS

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print("Запущен команда /start")
        keyboards = [
            [InlineKeyboardButton("Оставить заявку", callback_data="register")],
            [InlineKeyboardButton("Подробнее", callback_data="info")],
        ]
        inline_keyboards = InlineKeyboardMarkup(keyboards)
        print(update.message.from_user)
        await update.message.reply_text(
            "Здравствуйте! Вас приветствует чат-бот сервиса chatrun. Я помогаю бизнесам автоматизировать продажи и поддержку клиентов в мессенджерах.\n\n"
            "Могу проанализировать вашу задачу и подсказать, как:\n"
            "✅ Автоматически обрабатывать запросы о статусе заказов, наличии товаров и акциях.\n"
            "✅ Отвечать клиентам 24/7, используя анализ их сообщений и данных.\n"
            "✅ Конвертировать входящие сообщения в готовые заявки, сокращая нагрузку на операторов.\n"
            "✅ Перенаправлять беседы из одного мессенджера для общения в другое.\n\n"
            "Можете оставить заявку на консультацию, нажав кнопку ниже или подробнее узнать о возможностях сервиса",
            reply_markup=inline_keyboards,
        )

    async def text_message_handler(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        user_message = update.message.text
        print(f"Получено сообщение от пользователя: {user_message}")
        await update.message.reply_text(
            "Спасибо за ваше сообщение! Мы свяжемся с вами в ближайшее время."
        )

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        if query.data == "register":
            text = "Отлично! Сперва нам нужно узнать о вашей деятельности немного больше. Выберите, пожалуйста, чем занимается ваша компания?"
            keyboard = [
                [InlineKeyboardButton("Продажа", callback_data="bid_category_sale")],
                [InlineKeyboardButton("Сервис", callback_data="bid_category_service")],
            ]
            await query.edit_message_text(
                text, reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif query.data == "bid_category_sale":
            await query.edit_message_text(
                "Спасибо за информацию! Теперь, пожалуйста, расскажите кратко какие товары вы продаете и в каких мессенджерах общаетесь с клиентами?"
            )
        elif query.data == "help":
            help_text = "Доступные команды:\n"
            for command, description in self._list_commands.items():
                help_text += f"{command} - {description}\n"
            await query.edit_message_text(text=help_text)

    def run(self):
        self._app = Application.builder().token(self._TOKEN).build()
        print(f"Запущен телеграм бот: {self._URL}")
        self._app.add_handler(CommandHandler("start", self.start))
        self._app.add_handler(CallbackQueryHandler(self.button_callback))
        self._app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.text_message_handler)
        )
        self._app.run_polling()

    # GETTERS

    def get_params_BOT(self):
        return {"TOKEN": self._TOKEN, "URL": self._URL}

    # SETTERS

    def set_token(self, token):
        self._TOKEN = token

    def set_url(self, url):
        self._URL = url
