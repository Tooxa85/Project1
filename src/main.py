import pandas as pd

from src.reports import reports
from src.services import services
from src.utils import excel_reader
from src.views import views

filename = r"C:\Users\User\PycharmProjects\Project1\data\operations.xlsx"
operations = excel_reader(filename)
date = input("Введите дату и время в формате YYYY-MM-DD HH:MM:SS, либо нажмите Enter для использования текущей: ")


def main() -> None:
    """Основная функция, объединяющая все остальные"""
    print(views(date, operations))
    print(services(operations))
    print(reports(pd.read_excel(filename)))

    return None


if __name__ == "__main__":
    main()
