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
from webdriver_manager.chrome import ChromeDriverManager

def load_session_credentials():
    with open('credentials.json', 'r') as f:
        credentials = json.load(f)
    return credentials

def human_like_sleep(min_time=0.5, max_time=1.5):
    time.sleep(random.uniform(min_time, max_time))

def login(login_index,with_failed, results):
    alternate_login = False
    credentials = load_session_credentials()
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36"
    )

    # Додаємо директорію для профілів браузера
    profiles_directory = 'chrome_profiles'
    os.makedirs(profiles_directory, exist_ok=True)
    
    service = Service(ChromeDriverManager().install())
    storage_directory = 'sessions'
    os.makedirs(storage_directory, exist_ok=True)

    if(with_failed):
        credentials = check_accounts(credentials)

    for i in range(login_index, len(credentials)):
        print(f"акаунт: {credentials[i]['login']} n: {i}")
        profile_path = os.path.join(profiles_directory, f'profile_{credentials[i]["login"]}')
        os.makedirs(profile_path, exist_ok=True)
        
        chrome_options.add_argument(f'--user-data-dir={profile_path}')
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get('https://www.instagram.com/')
        time.sleep(0.5)
        
        try:
            WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, '//button[div[text()="Увійти"]]'))
            ).click()
        except Exception:
            pass

        # Пробуємо знайти поля для входу
        try:
            username_field = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_field = driver.find_element(By.NAME, "password")
            
            # Якщо знайшли поля - виконуємо вхід
            username_field.send_keys(credentials[i]['login'])
            password_field.send_keys(credentials[i]['password'])
            human_like_sleep()
            password_field.submit()

            # якщо потрібно щоб аккаунт був відкритий довше то змінити тут цифру з 0 на будь-яку більшу час в секундах
            print("пауза 1")
            while True:
                if input(f"акаунт: {credentials[i]['login']} Натисніть 'y' щоб продовжити: ").lower() == 'y':
                    break
            
        except Exception:
            print("пауза 2")
            while True:
                if input(f"акаунт: {credentials[i]['login']} Натисніть 'y' щоб продовжити: ").lower() == 'y':
                    break

            # Якщо не знайшли поля - значить вже на акаунті
            print(f"Вже виконаний вхід для {credentials[i]['login']}")
            
            # Додаємо перевірку на challenge після автоматичного входу
            if "challenge" in driver.current_url:
                try:
                    WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Відхилити"]'))
                    ).click()
                    print('Dismissed label')
                except Exception:
                    print(f"Аккаунт заблоковано або треба номер: {credentials[i]['login']}")
                    results.append({credentials[i]['login']: 'failed'})
                    driver.quit()
                    continue

            # Продовжуємо зі збереженням сесії
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
           
            results.append({credentials[i]['login']: 'success'})
            driver.quit()
            continue

        if alternate_login:
            time.sleep(4)

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
                    print('Dismissed label')
                except Exception:
                    print(f"Аккаунт заблоковано або треба номер: {credentials[i]['login']}")
                    results.append({credentials[i]['login']: 'failed'})
                    driver.quit()
                    continue
    
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
        print(f"Saved session for: {credentials[i]['login']}, session: {credentials[i]['session']}\n\n")
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
