from unittest.mock import patch

import pandas as pd

from src.utils import excel_reader


def test_excel_reader() -> None:
    """Тест чтения excel-файла"""
    with patch("pandas.read_excel") as mock_excel:
        mock_excel.return_value = pd.DataFrame(
            [
                {
                    "Дата операции": "15.07.2025 20:16:35",
                    "Номер карты": "*4328",
                    "Категория": "Супермаркеты",
                    "Сумма платежа": "-243.43",
                }
            ]
        )
        data = excel_reader("data/transactions.excel.xlsx")
        assert data == [
            {
                "Дата операции": "15.07.2025 20:16:35",
                "Номер карты": "*4328",
                "Категория": "Супермаркеты",
                "Сумма платежа": "-243.43",
            }
        ]
