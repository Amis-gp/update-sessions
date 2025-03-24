#   python3 autoClicker.py                 - старт
#   python3 autoClicker.py --start 3       - старт з 3 ого аккаунта або будь-якого тільки змінити цифру
#   python3 autoClicker.py --with-failed   - пройтись по всім невдалими сесіями
#   cntrl+c - вихід

import json
import time
import random
import pickle
import instaloader
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import argparse
import requests

def load_session_credentials():
    with open('credentials.json', 'r') as f:
        credentials = json.load(f)
    return credentials

def human_like_sleep(min_time=1, max_time=3):
    time.sleep(random.uniform(min_time, max_time))

def login(login_index,with_failed, results):
    alternate_login = False
    credentials = load_session_credentials()
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument("--headless")  # Uncomment if needed for headless mode
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36"
    )

    service = Service(os.path.join(os.getcwd(), 'chromedriver'))
    storage_directory = 'sessions'
    os.makedirs(storage_directory, exist_ok=True)

    if(with_failed):
        credentials = check_accounts(credentials)

    for i in range(login_index, len(credentials)):
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get('https://www.instagram.com/')
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//button[div[text()="Увійти"]]'))
            ).click()
        except Exception:
            pass  # Ignore if the button is not present

        # Locate username and password fields
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password_field = driver.find_element(By.NAME, "password")

        # Fill in the credentials
        try:
            username_field.send_keys(credentials[i]['login'])
            password_field.send_keys(credentials[i]['password'])
        except IndexError:
            print("Credentials index out of range.")
            results.append({credentials[i]['login']: 'failed'})
            driver.quit()
            continue

        human_like_sleep()

        # Submit login form
        try:
            password_field.submit()
        except Exception:
            # Attempt alternate login if the first method fails
            try:
                WebDriverWait(driver, 25).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div/div/div/div[3]/div/div/div/div/div[2]/div[3]/div[3]/div/div/div'))
                ).click()
                alternate_login = True
            except Exception:
                print("Alternate login failed.")
                results.append({credentials[i]['login']: 'failed'})
                driver.quit()
                continue

        if alternate_login:
            time.sleep(10)
        try:
            WebDriverWait(driver, 9).until(
                EC.element_to_be_clickable((By.XPATH, '//div[text()="Не зараз"]'))
            ).click()
        except Exception:
            if "challenge" in driver.current_url:
                try:
                    WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Відхилити"]'))
                    ).click()
                    time.sleep(3)
                    print('Dismissed label')
                except Exception:
                    print(f"Аккаунт заблоковано або треба номер: {credentials[i]['login']}")
                    results.append({credentials[i]['login']: 'failed'})
                    driver.quit()
                    continue
            else:
                # якщо потрібно щоб аккаунт був відкритий довше то змінити тут цифру з 5 на будь-яку більшу час в секундах
                time.sleep(20)
        time.sleep(4)
        session_data = driver.get_cookies()
        formatted_cookies = {cookie['name']: cookie['value'] for cookie in session_data}
        pickle_file_path = os.path.join(storage_directory, credentials[i]['session'])

        with open(pickle_file_path, 'wb') as pickle_file:
            pickle.dump(formatted_cookies, pickle_file)

        laravel_url = "http://167.172.43.122/api/add-session"
        send_session_file_to_laravel(pickle_file_path, laravel_url)

        ig = instaloader.Instaloader(rate_controller=lambda ctx: instaloader.RateController(ctx))
        try:
            ig.load_session_from_file(credentials[i]['login'], pickle_file_path)
        except instaloader.exceptions.AbortDownloadException as e:
            print(f"Download aborted: {e}")
        except instaloader.exceptions.TooManyRequestsException as e:
            print(f"Rate limit exceeded: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

        ig.save_session_to_file(pickle_file_path)
        print(f"Saved session for: {credentials[i]['login']}, session: {credentials[i]['session']}")
        results.append({credentials[i]['login']: 'success'})
        alternate_login = False
        driver.quit()

    return results

def send_session_file_to_laravel(file_path, laravel_url):
    with open(file_path, 'rb') as f:
        response = requests.post(laravel_url, files={'file': f})
    if response.status_code == 200:
        print(f"Файл {file_path} успішно відправлено на Laravel-сервер.")
    else:
        print(f"Помилка при відправці файла: {response.status_code}, {response.text}")

def check_accounts(credentials):
    failed_credentials = []
    for account in credentials:
        ig = instaloader.Instaloader()
        login = account.get("login")
        session_file = os.path.join('sessions/', account.get("session"))

        try:
            ig.load_session_from_file(login, session_file)
            profile = instaloader.Profile.from_username(ig.context, login)
        except instaloader.exceptions.AbortDownloadException:
            failed_credentials.append(account)
        except instaloader.exceptions.TooManyRequestsException:
            failed_credentials.append(account)
        except Exception as e:
            failed_credentials.append(account)
    return failed_credentials

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Instagram Session Manager")
    parser.add_argument(
        "--start", type=int, default=0,
        help="Start processing from the specified account index"
    )
    parser.add_argument(
        "--with-failed", action="store_true",
        help="Only process accounts with failed sessions"
    )
    args = parser.parse_args()

    start_index = args.start
    with_failed = args.with_failed
    results = []
    results = login(start_index,with_failed, results)
    print(results)
