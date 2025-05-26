import time
from price_checker import *
from dotenv import load_dotenv
load_dotenv()
while True:
    print(f"Запуск проверки: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        check_price()

    except Exception as е:
        print(f"ошибка при запуске: {е}")

    print("Ожидание следующего запуска")
    time.sleep(3600)

