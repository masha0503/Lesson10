import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime


def create_database():
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS weather_data
                 (datetime TEXT, temperature TEXT)''')
    conn.commit()
    conn.close()


def insert_data(datetime_str, temperature):
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute("INSERT INTO weather_data (datetime, temperature) VALUES (?, ?)", (datetime_str, temperature))
    conn.commit()
    conn.close()


def get_temperature():
    url = 'https://weather.com/weather/today/l/a59084885e0fe4cd572a618fa1f01dc522c6ae0565f4c782b7b8d3a7ca3f7c0c'
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    temp_div = soup.find('span', class_='CurrentConditions--tempValue--MHmYY')
    if temp_div:
        temperature =temp_div.text
        return temperature
    else:
        raise Exception("Помилка: Неможливо отримати температуру.")


def main():
    create_database()

    try:
        temperature = get_temperature()
        datetime_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_data(datetime_str, temperature)
        print(f"Запис додана: {datetime_str}, {temperature}")
    except Exception as e:
        print(f"Помилка: {e}")


if __name__ == "__main__":
    main()
