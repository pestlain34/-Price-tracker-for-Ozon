import time
from datetime import datetime
import requests
from selenium import webdriver
import csv
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
load_dotenv()

def build_price_chart(target_name):
    df = pd.read_csv('price.csv', delimiter = ';' , quotechar='"' ,encoding = 'utf-8-sig')
    df.rename(columns = {
        "Название_вещи": "name",
        "Цена в рублях": "price",
        "Дата": "timestamp"
    } , inplace = True)
    df['timestamp'] = pd.to_datetime(df['timestamp'] ,format='%Y-%m-%dT%H:%M:%S.%f')
    filtered = df[df['name'] == target_name]
    if filtered.empty:
        print(f"⚠️ Нет данных для товара: {target_name}")
        return
    grouped = df.groupby("name")
    plt.figure(figsize=(10, 6))
    plt.plot(filtered['timestamp'], filtered['price'], label=target_name)

    plt.xlabel("Дата")
    plt.ylabel("Цена (₽)")
    plt.title(f"Изменение цены товаров: {target_name}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("price_chart.png")
    plt.close()
def send_graph_photo():
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    CHAT_ID = os.getenv('CHAT_ID')
    bot_token = TELEGRAM_TOKEN
    chat_id = CHAT_ID
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    with open('price_chart.png' , 'rb') as photo:
        payload = {
            "chat_id": chat_id,
            "caption": "📈 График изменения цен"
        }
        files = {
            "photo": photo
        }
        requests.post(url, data=payload, files=files)
def send_telegram_message(message):
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    CHAT_ID = os.getenv('CHAT_ID')
    bot_token = TELEGRAM_TOKEN
    chat_id = CHAT_ID
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url , data=payload)

def find_min_price(current_name):
    min_price = float('inf')
    with open('price.csv' , 'r' , newline = '' , encoding = 'utf-8-sig') as f:
        reader = csv.reader(f , delimiter = ';')
        next(reader)
        for row in reader:
            name , price, date = row
            priceint = int(price)
            if name == current_name:
                min_price = min(min_price , priceint)
    return min_price

def check_price():

    driver = webdriver.Chrome(service=service, options=options)
    print("Введите ссылку на товар с озона, например: https://www.ozon.ru/product/beysbolka-1725325406/ ")
    urlinput = str(input())
    driver.get(urlinput)
    driver.maximize_window()
    initial_title = driver.title
    WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-widget='webProductHeading'] h1"))
    )
    final_title = driver.title
    print(driver.title)
    print(driver.current_url)
    curprice = WebDriverWait(driver , 3).until(EC.presence_of_element_located((By.CSS_SELECTOR , "[data-widget='webPrice'] span")))
    curname = driver.find_element(By.CSS_SELECTOR, "[data-widget='webProductHeading'] h1")
    curnametext = curname.text
    curpricetext = curprice.text
    price_digits = ''.join(filter(str.isdigit, curpricetext))
    curpriceint = int(price_digits)
    with open('price.csv' , 'a', newline = '' , encoding = 'utf-8-sig') as file:
        writer = csv.writer(file, delimiter = ';' ,quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow([curnametext , curpriceint, datetime.now().isoformat()])
    min_price = find_min_price(curnametext)
    if(curpriceint < min_price):
        send_telegram_message(f"🔻 Цена упала!\n\n<b>{curnametext}</b>\nНовая цена: {curpriceint}₽ \n\nURL: <b>{driver.current_url}</b>")
    elif (curpriceint == min_price):
        send_telegram_message(f"🔻 Цена не изменилась!\n\n<b>{curnametext}</b>\nЦена: {curpriceint}₽ \n\nURL:<b>{driver.current_url}</b>")
    else:
        send_telegram_message(f"🔻 Цена выросла!\n\n<b>{curnametext}</b>\n Новая цена: {curpriceint}₽ \n\nURL:<b>{driver.current_url}</b>")
    build_price_chart(curnametext)
    send_graph_photo()
    driver.quit()

options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--remote-allow-origins=*")
options.add_argument("--disable-renderer-backgrounding")
options.add_argument("--disable-background-timer-throttling")
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
options.add_argument(f"user-agent={user_agent}")
service = Service(ChromeDriverManager().install())
while True:
    print(f"Запуск проверки: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        check_price()

    except Exception as е:
        print(f"ошибка при запуске: {е}")

    print("Ожидание следующего запуска")
    time.sleep(3600)

