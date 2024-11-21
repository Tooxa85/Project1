import json
from typing import Any

import numpy as np
import pandas as pd

from src.logger import log_setup

log = log_setup()


def excel_reader(filename: str) -> list:
    """Читает xlsx файл по переданному пути"""
    if filename.endswith(".xlsx"):
        try:
            data = pd.read_excel(filename)
            data = data.replace(np.nan, None)
            log.info("Файл успешно прочитан")
            return data.to_dict("records")
        except FileNotFoundError:
            log.info("Файл с данным названием не был найден")
            return []
    else:
        log.info("Данный файл имеет некорректный формат")
        return []


def read_json(filename: str) -> list:
    """Читает json-файл по переданному пути"""
    try:
        with open(filename, encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                log.info("Применена функция read_json")
                return data
            else:
                log.error("В файле находится не список")
                return []
    except (FileNotFoundError, json.JSONDecodeError):
        log.error("Что-то координально пошло не так")
        return []


def write_json(filename: str, data: Any) -> None:
    """Записывает данные в переданный файл"""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file)
        log.info("Данные успешно записаны")
        return None
