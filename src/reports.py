from datetime import datetime as dt
from typing import Any, Optional

import pandas as pd

from src.logger import log_setup

logger = log_setup()


def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[Any] = None
) -> Optional[pd.DataFrame]:
    """Отчёт трат по категориям за 3 месяца до указанной даты"""
    if category not in transactions["Категория"].values:
        return None
    data = transactions[transactions["Категория"].str.contains(category, case=False, na=False)]
    data["Дата платежа"] = pd.to_datetime(data["Дата платежа"], dayfirst=True)
    if date is None:
        date = dt.now()
    start_date = pd.to_datetime(date, format="%d.%m.%Y") - pd.offsets.MonthEnd(3)
    filtered_data = data[
        data["Дата платежа"].notnull()
        & data["Дата платежа"].between(start_date, pd.to_datetime(date, format="%d.%m.%Y"))
    ]
    logger.info(filtered_data)
    if filtered_data.empty:
        return None
    return filtered_data


def reports(data: pd.DataFrame) -> Optional[pd.DataFrame]:
    """Объединение функций файла reports.py"""
    category = input("По какой категории вы хотите произвести поиск? ")
    date = input("Введите дату окончания поиска: ")
    return spending_by_category(data, category, date)
