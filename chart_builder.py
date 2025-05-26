import pandas as pd
import matplotlib.pyplot as plt
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