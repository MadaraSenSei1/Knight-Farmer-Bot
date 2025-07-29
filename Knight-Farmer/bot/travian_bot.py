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
        self.driver.get("https://lobby.travian.com")
        wait = WebDriverWait(self.driver, 10)

        # Neue Lobby-Felder:
        email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        password_input = self.driver.find_element(By.NAME, "password")
        login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

        email_input.send_keys(self.username)
        password_input.send_keys(self.password)
        login_button.click()

        # Optional: Cookie-Banner wegklicken
        try:
            cookie_button = wait.until(EC.element_to_be_clickable((By.ID, "cookieConsentButton")))
            cookie_button.click()
        except:
            pass

        # Warte auf Weiterleitung zur Lobby nach Login
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "world-list")))

        print("[✅] Login erfolgreich in die Lobby")
        return True
    except Exception as e:
        print(f"[‼️] Login error: {e}")
        if self.driver:
            self.driver.quit()
        return False
e

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
