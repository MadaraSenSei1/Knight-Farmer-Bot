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

    def start_farming(self, min_interval, max_interval, randomize):
        self.running = True

        def farm_loop():
            while self.running:
                try:
                    print(f"[⚔️] {self.username}: Sende Farm-Listen ...")
                    # Hier kannst du Klicks auf Farm-Listen einfügen
                    # Beispiel:
                    # self.driver.find_element(By.ID, "raidList_1").click()

                    sleep_time = random.randint(min_interval, max_interval)
                    if randomize:
                        sleep_time += random.randint(0, 30)
                    print(f"[⏳] Nächster Angriff in {sleep_time} Sekunden")
                    time.sleep(sleep_time)
                except Exception as e:
                    print(f"[‼️] Fehler im Farming-Loop: {e}")
                    self.running = False
                    break

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
