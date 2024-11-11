from unittest.mock import patch

import pytest

from src.utils import excel_reader
from src.views import card_info, currency_rates, greeting, stock_rates, top_transactions


@pytest.mark.parametrize(
    "date, expected",
    [
        ("2024-06-06 08:00:00", "Доброе утро"),
        ("2024-06-06 14:00:00", "Добрый день"),
        ("2024-06-06 20:00:00", "Добрый вечер"),
        ("2024-06-06 03:00:00", "Доброй ночи"),
    ],
)
def test_greeting(date: str, expected: str) -> None:
    """Тест приветствия в зависимости от времени"""
    assert greeting(date) == expected


def test_card_info() -> None:
    """Тест вывода информации по карте"""
    assert card_info(excel_reader(r"C:\Users\User\PycharmProjects\Project1\data\operations.xlsx"))[0] == {
        "last_digits": "1112",
        "total_spent": 1000.0,
        "cashback": 0,
    }


def test_top_transactions() -> None:
    """Тест вывода топа транзакций по сумме"""
    assert top_transactions(excel_reader(r"C:\Users\User\PycharmProjects\Project1\data\operations.xlsx"))[0] == {
        "date": "28.07.2018",
        "amount": 179571.56,
        "category": None,
        "description": "Перевод средств с брокерского счета",
    }


def test_currency_rate() -> None:
    """Тест вывода курса валют"""
    with patch("requests.get") as mock_get:
        mock_response = {
            "success": True,
            "timestamp": 1719475383,
            "base": "EUR",
            "date": "2024-06-27",
            "rates": {"RUB": 90.0},
        }
        mock_get.return_value.json.return_value = mock_response
        assert currency_rates(["EUR"]) == [{"currency": "EUR", "rate": 90.0}]


def test_stock_rates() -> None:
    """Тест вывода курса акций"""
    with patch("requests.get") as mock_get:
        mock_response = {"Global Quote": {"01. symbol": "GOOGL", "02. open": "180.0"}}
        mock_get.return_value.json.return_value = mock_response
        assert stock_rates(["GOOGL"]) == [{"rate": 180.0, "stock": "GOOGL"}]
