from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
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
        if self.proxy:
            options.add_argument(f"--proxy-server={self.proxy}")
        self.driver = webdriver.Chrome(options=options)

   def login(self):
    self._init_driver()
    try:
        self.driver.get(self.server)
        self.driver.find_element(By.NAME, "name").send_keys(self.username)
        self.driver.find_element(By.NAME, "password").send_keys(self.password)
        self.driver.find_element(By.CLASS_NAME, "loginButton").click()

        time.sleep(5)

        if "dorf1.php" in self.driver.current_url or "dorf2.php" in self.driver.current_url:
            return True
        elif "start.ad" in self.driver.current_url or "login" in self.driver.current_url:
            print("[❌] Login fehlgeschlagen: Weiterleitung zur Login-Seite.")
            self.driver.quit()
            return False
        else:
            print("[⚠️] Unbekannter Login-Zustand: ", self.driver.current_url)
            self.driver.quit()
            return False

    except Exception as e:
        print(f"[‼️] Login error: {e}")
        self.driver.quit()
        return False

    except Exception as e:
        print(f"[‼️] Login error: {e}")
        self.driver.quit()
        return False

    def get_farm_lists(self):
        try:
            # Beispiel: farm list auslesen
            return [{"name": "Farm 1"}, {"name": "Farm 2"}]
        except:
            return []

    def start_farming(self, min_interval, max_interval, randomize):
        self.running = True

        def farm_loop():
            while self.running:
                print(f"[{self.username}] Executing farm list...")
                time.sleep(random.randint(min_interval, max_interval) + (random.randint(0, 30) if randomize else 0))

        self.thread = threading.Thread(target=farm_loop)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.driver:
            self.driver.quit()

    def is_running(self):
        return self.running
