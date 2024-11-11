import os
from datetime import datetime as dt

import requests
from dotenv import load_dotenv

from src.logger import log_setup
from src.utils import read_json, write_json

log = log_setup()
load_dotenv()
apikey = os.getenv("api_key")
stock_apikey = os.getenv("stock_api")


def greeting(dt_: str) -> str:
    """Приветствие программы в зависимости от времени"""
    if dt_ == "":
        formated_date = dt.strptime(str(dt.now()), "%Y-%m-%d %H:%M:%S.%f")
    else:
        formated_date = dt.strptime(dt_, "%Y-%m-%d %H:%M:%S")
    hour = int(formated_date.strftime("%H"))
    if hour < 7:
        greet = "Доброй ночи"
    elif 6 < hour < 13:
        greet = "Доброе утро"
    elif 12 < hour < 19:
        greet = "Добрый день"
    else:
        greet = "Добрый вечер"
    log.info(f"Приветствие будет {greet}")
    return greet


def card_info(data: list) -> list:
    """Информация по каждой карте в формате словаря"""
    card_info_list = []
    unique_cards_set = set()
    for operation in data:
        card = operation["Номер карты"]
        if str(card)[0] == "*" and str(card)[1:] not in unique_cards_set:
            unique_cards_set.add(str(card)[1:])
            last_digits = str(card)[1:]
            total_spent = 0.0
            total_spent += operation["Сумма платежа"]
            cashback = total_spent % 100
            info = {
                "last_digits": last_digits,
                "total_spent": round(abs(total_spent), 2),
                "cashback": int(cashback),
            }
            card_info_list.append(info)
    return sorted(card_info_list, key=lambda x: int(x["last_digits"]))


def top_transactions(data: list) -> list:
    """Выводит топ-5 транзакций в формате словаря"""
    transactions = sorted(data, key=lambda x: abs(x["Сумма платежа"]))
    top = []
    for transaction in transactions[-5:]:
        top.append(
            {
                "date": transaction["Дата операции"][:10],
                "amount": abs(transaction["Сумма операции"]),
                "category": transaction["Категория"],
                "description": transaction["Описание"],
            }
        )
    return top


def currency_rates(currencies: list) -> list:
    """Выводит курс валют из переданного списка"""
    rates = []
    for currency in currencies:
        url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency}"
        response = requests.get(url, headers={"apikey": apikey}, timeout=40)
        data = round(response.json()["rates"]["RUB"], 2)
        rates.append({"currency": currency, "rate": data})
    return rates


def stock_rates(stocks: list) -> list:
    """Выводит актуальную стоимость акций из S&P 500"""
    rates = []
    for stock in stocks:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={stock_apikey}"
        response = requests.get(url, timeout=30)
        data = round(float(response.json()["Global Quote"]["02. open"]), 2)
        rates.append({"stock": stock, "rate": data})
    return rates


def views(date: str, data: list) -> dict:
    """Объединение функций файла views.py"""
    try:
        currency = currency_rates(read_json("user_settings.json")[0]["user_currencies"])
    except IndexError:
        currency = "Бесплатные api-запросы закончились"
    try:
        stock = stock_rates(read_json("user_settings.json")[0]["user_stocks"])
    except IndexError:
        stock = "Бесплатные api-запросы закончились"
    result = {
        "greeting": greeting(date),
        "cards": card_info(data),
        "top transactions": top_transactions(data),
        "currency rates": currency,
        "stock rates": stock,
    }
    write_json("views.json", result)
    return result
