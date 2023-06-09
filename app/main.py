import auth as settings

import re
import logging
import time

from selenium import webdriver
from selenium.common import NoSuchElementException, ElementNotInteractableException, WebDriverException, \
    TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# Настройки драйвера
chrome_options = Options()
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument('--ignore-ssl-errors=yes')
# chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.set_capability("browserVersion", "111.0")
# driver = webdriver.Remote(
#     command_executor='http://localhost:4444/wd/hub',
#     options=chrome_options
# )
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)


def auth():
    # Переходим на страницу авторизации
    driver.get('https://hh.ru/account/login')
    # Нажимаем кнопку войти через hh
    form = driver.find_element(By.CLASS_NAME, 'account-login-tile')
    form.find_elements(By.CLASS_NAME, 'bloko-link')[1].click()

    # wait until the page is loaded
    WebDriverWait(driver, 3).until(ec.presence_of_element_located((By.CLASS_NAME, 'bloko-input-text')))

    # Вводим логин и пароль
    input = form.find_elements(By.CLASS_NAME, 'bloko-input-text')
    input[0].send_keys(settings.HH_USER)
    input[1].send_keys(settings.HH_PASSWORD)

    # Нажимаем кнопку войти
    form.find_element(By.CLASS_NAME, 'bloko-button_kind-primary').click()


def get_data():
    salary = 40000
    only_with_salary = 'false'

    for index in range(10):
        driver.get(
            f'https://hh.ru/search/vacancy?salary={salary}&only_with_salary={only_with_salary}&page={index}&area=113&schedule=remote')
        vac = driver.find_elements(By.CLASS_NAME, 'serp-item')
        for i, el in enumerate(vac):
            logging.info(el.find_element(By.CLASS_NAME, 'serp-item__title').text,
                         el.find_element(By.CLASS_NAME, 'serp-item__title').get_attribute('href'))


auth()
