from src.utils import write_json


def search(data: list, to_find: str) -> list:
    """Простой поиск по строке в категории/описании"""
    transaction_list = []
    for transaction in data:
        if to_find in [transaction["Описание"], transaction["Категория"]]:
            transaction_list.append(transaction)
    if not transaction_list:
        return []
    return transaction_list


def services(data: list) -> dict:
    """Объединение функций файла services.py"""
    to_find = input("Введите поисковой запрос ")
    result = {to_find: search(data, to_find)}
    write_json("services.json", result)
    return result
