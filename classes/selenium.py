from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
)
import time
import random


LOGIN = "mebel_modno_stilno"
PASSWORD = "mebel1990"
TELEGRAM_LINK = "https://t.me/+ETTFVnzsHMY2NTBi"
KEYWORD = "+"


class InstaBotSelenium:
    def __init__(self, login, password):
        print("Экземпляр класса")
        self.login = login
        self.password = password

    def safe_click(self, driver, element, description=""):
        """Безопасный клик с обработкой перехвата"""
        try:
            # Пробуем обычный клик
            element.click()
            print(f"✅ Успешный клик: {description}")
            return True
        except ElementClickInterceptedException:
            print(f"⚠️  Обычный клик не сработал, пробуем JavaScript...")
            try:
                # Клик через JavaScript
                driver.execute_script("arguments[0].click();", element)
                print(f"✅ JavaScript клик сработал: {description}")
                return True
            except Exception as e:
                print(f"❌ JavaScript клик тоже не сработал: {e}")
                return False

    def readCommentAndReplyByKeyword(self, keyword, reply):
        # Более простые настройки - убираем сложные опции
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )

        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 15)

        try:
            print("🔄 Открываем Instagram...")
            driver.get("https://www.instagram.com/")
            time.sleep(3)

            # Логин
            print("🔐 Входим в аккаунт...")
            try:
                # Ждем появления полей ввода
                username = wait.until(
                    EC.presence_of_element_located((By.NAME, "username"))
                )
                password = wait.until(
                    EC.presence_of_element_located((By.NAME, "password"))
                )

                username.send_keys(self.login)
                password.send_keys(self.password)

                # Клик на кнопку входа через JavaScript
                login_btn = driver.find_element(
                    By.CSS_SELECTOR, "button[type='submit']"
                )
                driver.execute_script("arguments[0].click();", login_btn)

            except TimeoutException:
                print("❌ Не найдены поля для входа")
                return

            # Ждем загрузки
            print("⏳ Ждем загрузки...")
            time.sleep(15)

            # ПРОСТОЙ ПОДХОД - сразу переходим к конкретному посту
            print("📱 Переходим к конкретному посту...")

            # Переход к вашим постам
            driver.get(f"https://www.instagram.com/{self.login}/")
            time.sleep(3)

            # Клик на первый пост
            first_post = driver.find_element(By.CSS_SELECTOR, "div._aagw")
            first_post.click()
            time.sleep(2)

            # МОНИТОРИНГ КОММЕНТАРИЕВ В КОНКРЕТНОМ ПОСТЕ
            print("🔍 Начинаем мониторинг комментариев...")

            processed_comments = set()

            while True:
                try:
                    # Обновляем список комментариев
                    driver.refresh()
                    time.sleep(3)

                    # Ищем комментарии
                    comments = driver.find_elements(By.CSS_SELECTOR, "span")

                    new_comments_found = False

                    for comment in comments:
                        try:
                            comment_text = comment.text.lower()
                            comment_id = comment.id

                            if (
                                comment_id not in processed_comments
                                and keyword in comment_text
                            ):
                                print(
                                    f"✅ Найден комментарий с '{keyword}': {comment_text}"
                                )

                                # Пробуем найти кнопку ответа рядом
                                try:
                                    # Ищем родительский контейнер комментария
                                    comment_container = comment.find_element(
                                        By.XPATH,
                                        "./ancestor::div[contains(@class, 'x9f619')]",
                                    )

                                    # Ищем кнопку ответа в этом контейнере
                                    reply_buttons = comment_container.find_elements(
                                        By.CSS_SELECTOR,
                                        "button, svg, div[role='button']",
                                    )

                                    for btn in reply_buttons:
                                        btn_text = btn.get_attribute("outerHTML")
                                        if (
                                            "ответ" in btn_text.lower()
                                            or "reply" in btn_text.lower()
                                        ):
                                            print(
                                                "🖱️ Найдена кнопка ответа, пробуем клик..."
                                            )

                                            # Прокручиваем к элементу
                                            driver.execute_script(
                                                "arguments[0].scrollIntoView(true);",
                                                btn,
                                            )
                                            time.sleep(1)

                                            # Безопасный клик
                                            if self.safe_click(
                                                driver, btn, "кнопка ответа"
                                            ):
                                                time.sleep(2)

                                                # Ищем поле для ввода ответа
                                                reply_inputs = driver.find_elements(
                                                    By.TAG_NAME, "textarea"
                                                )
                                                for reply_input in reply_inputs:
                                                    if reply_input.is_displayed():
                                                        print(
                                                            "📝 Найдено поле для ответа..."
                                                        )
                                                        reply_input.clear()
                                                        reply_input.send_keys(reply)
                                                        time.sleep(1)

                                                        # Ищем кнопку отправки
                                                        send_buttons = (
                                                            driver.find_elements(
                                                                By.CSS_SELECTOR,
                                                                "button[type='submit']",
                                                            )
                                                        )
                                                        for send_btn in send_buttons:
                                                            if (
                                                                send_btn.is_enabled()
                                                                and send_btn.is_displayed()
                                                            ):
                                                                self.safe_click(
                                                                    driver,
                                                                    send_btn,
                                                                    "отправка ответа",
                                                                )
                                                                print(
                                                                    "✅ Ответ отправлен!"
                                                                )
                                                                break

                                                        break

                                                # Добавляем в обработанные
                                                processed_comments.add(comment_id)
                                                new_comments_found = True

                                                # Пауза между ответами
                                                time.sleep(random.randint(30, 60))
                                                break

                                except Exception as e:
                                    print(f"❌ Ошибка при обработке комментария: {e}")
                                    continue

                        except Exception as e:
                            continue

                    if not new_comments_found:
                        print(f"⏳ Новых комментариев с '{keyword}' не найдено...")

                    # Пауза между проверками
                    time.sleep(30)

                except Exception as e:
                    print(f"❌ Ошибка в основном цикле: {e}")
                    # Продолжаем работу после ошибки
                    time.sleep(30)
                    continue

        except Exception as e:
            print(f"❌ Критическая ошибка: {e}")
        finally:
            print("🛑 Закрываем браузер...")
            driver.quit()
