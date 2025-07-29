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
        self.server = server  # z. B. "https://ts9.x1.europe.travian.com"
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
            options.add_argument(f'--proxy-server={self.proxy}')
        self.driver = webdriver.Chrome(options=options)

    
    def login(self):
        self.driver.get(f"{self.server}/login.php")

        try:
            # Warten auf das Email-Feld (nicht name!)
            WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.NAME, "email")))

            email_input = self.driver.find_element(By.NAME, "email")
            password_input = self.driver.find_element(By.NAME, "password")
            login_button = self.driver.find_element(By.XPATH, '//button[@type="submit"]')

            email_input.send_keys(self.username)
            password_input.send_keys(self.password)
            login_button.click()

            # Prüfen ob Login erfolgreich war (z.B. Heldensymbol oder Dorfansicht lädt)
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "sidebarBoxHero"))  # oder ein anderes sicheres Element
            )

            print("✅ Login erfolgreich")
            return True
    
        except Exception as e:
            print(f"❌ Login fehlgeschlagen: {e}")
            return False

    def get_farm_lists(self):
        try:
            # Dies ist ein Platzhalter – du kannst hier echte Farm-Listen per DOM lesen
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
                    # → Hier Farm-Listen-Klicks automatisieren
                    # Beispiel:
                    # self.driver.find_element(By.ID, "raidList_1").click()
                    sleep_time = random.randint(min_interval, max_interval)
                    if randomize:
                        sleep_time += random.randint(0, 30)
                    print(f"[⏳] Nächster Lauf in {sleep_time} Sekunden")
                    time.sleep(sleep_time)
                except Exception as e:
                    print(f"[‼️] Farming-Fehler: {e}")
                    self.running = False
                    break

        self.thread = threading.Thread(target=farm_loop)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.driver:
            self.driver.quit()

    def is_running(self):
        return self.running
