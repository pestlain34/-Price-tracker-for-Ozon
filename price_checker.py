import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telegram_bot import send_telegram_message, send_graph_photo
from chart_builder import build_price_chart
from config import get_selenium_options, get_chrome_service
options = get_selenium_options()
service = get_chrome_service()
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