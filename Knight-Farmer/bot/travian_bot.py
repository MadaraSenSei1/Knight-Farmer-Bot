from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import time
import random


class TravianBot:
    def __init__(self, username, password, server, proxy=None):
        self.username = username
        self.password = password
        self.server = server
        self.proxy = proxy
        self.driver = None
        self.running = False
        self.thread = None

    def _init_driver(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        if self.proxy:
            options.add_argument(f'--proxy-server=http://{self.proxy}')

        try:
            self.driver = webdriver.Chrome(options=options)
        except Exception as e:
            print(f"[❌] WebDriver-Fehler: {e}")
            raise

    def login(self):
        try:
            self._init_driver()
            self.driver.get(self.server)
            wait = WebDriverWait(self.driver, 15)

            # 1. Versuch: modernes Login (z. B. internationaler Server)
            try:
                email_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
                password_field = self.driver.find_element(By.NAME, "password")
                login_button = self.driver.find_element(By.XPATH, '//button[contains(text(), "Log in")]')

                email_field.send_keys(self.username)
                password_field.send_keys(self.password)
                login_button.click()
            except:
                # 2. Fallback: arabischer oder klassischer Server mit Feld "name"
                name_field = wait.until(EC.presence_of_element_located((By.NAME, "name")))
                password_field = self.driver.find_element(By.NAME, "password")
                login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

                name_field.send_keys(self.username)
                password_field.send_keys(self.password)
                login_button.click()

            wait.until(EC.url_contains("dorf"))
            print("[✅] Login erfolgreich")
            return True

        except Exception as e:
            print(f"[❌] Login fehlgeschlagen: {e}")
            if self.driver:
                self.driver.quit()
            return False

    def get_farm_lists(self):
        try:
            # Platzhalter – DOM-Auslesen kann hier später eingebaut werden
            return [
                {"id": 1, "name": "Farm 1"},
                {"id": 2, "name": "Farm 2"},
            ]
        except Exception as e:
            print(f"[‼️] Fehler beim Abrufen der Farm-Listen: {e}")
            return []

    def run_all_farm_lists(self):
        try:
            # Stelle sicher, dass du auf der Farm-Listen-Seite bist
            self.driver.get(f"{self.server}/build.php?tt=99&id=39")  # id=39 = Rally Point
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "startButton")))

            start_buttons = self.driver.find_elements(By.CLASS_NAME, "startButton")

            print(f"[📋] {len(start_buttons)} Farm-Listen gefunden")

            for idx, button in enumerate(start_buttons):
                try:
                    button.click()
                    print(f"[✅] Farm-Liste {idx+1} gestartet")
                    time.sleep(1)  # etwas Wartezeit, um Server nicht zu überlasten
                except Exception as e:
                    print(f"[⚠️] Fehler beim Starten der Farm-Liste {idx+1}: {e}")

        except Exception as e:
            print(f"[‼️] Fehler beim Farm-Listen-Start: {e}")

        self.thread = threading.Thread(target=farm_loop)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass

    def is_running(self):
        return self.running
