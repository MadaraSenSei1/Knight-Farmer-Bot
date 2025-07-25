from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading, time, random

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
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        if self.proxy:
            options.add_argument(f"--proxy-server={self.proxy}")
        self.driver = webdriver.Chrome(options=options)

    def login(self):
        self._init_driver()
        try:
            print(f"[ℹ️] Opening URL: {self.server}")
            self.driver.get(self.server)

            # Cookie-Banner klicken, falls vorhanden
            try:
                accept = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.ID, "cookieConsentButton"))
                )
                accept.click()
                print("[✔️] Cookie-Banner akzeptiert.")
            except:
                pass  # Kein Banner

            # Auf Login-Felder warten
            wait = WebDriverWait(self.driver, 15)
            username_input = wait.until(EC.presence_of_element_located((By.NAME, "name")))
            password_input = self.driver.find_element(By.NAME, "password")
            login_button = self.driver.find_element(By.CLASS_NAME, "loginButton")

            username_input.send_keys(self.username)
            password_input.send_keys(self.password)
            login_button.click()

            # Login prüfen
            time.sleep(5)
            if "dorf1.php" in self.driver.current_url or "dorf2.php" in self.driver.current_url:
                print("[✅] Login erfolgreich!")
                return True
            else:
                print(f"[❌] Login fehlgeschlagen. URL nach Login: {self.driver.current_url}")
                self.driver.quit()
                return False

        except Exception as e:
            print(f"[‼️] Login error: {e}")
            self.driver.quit()
            return False

    def get_farm_lists(self):
        try:
            # Beispielhafte Rückgabe
            return [{"name": "Farm 1"}, {"name": "Farm 2"}]
        except:
            return []

    def start_farming(self, min_interval, max_interval, randomize):
        self.running = True

        def farm_loop():
            while self.running:
                print(f"[{self.username}] Executing farm list...")
                interval = random.randint(min_interval, max_interval)
                if randomize:
                    interval += random.randint(0, 30)
                time.sleep(interval)

        self.thread = threading.Thread(target=farm_loop)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.driver:
            self.driver.quit()

    def is_running(self):
        return self.running
