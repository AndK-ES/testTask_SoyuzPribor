import pytest 
from main import validate_input

def test_input_success():
    data = {
        "name": "Манометр показывающий DM 02",
        "manufacturer": "Манотомь",
        "specs": {"класс": "1,5"},
        "description": "Прибор предназначен для измерения избыточного давления..."
    }
    missing_fields = validate_input(data)
    assert len(missing_fields) == 0

def test_input_missing_fields():
    data = {
        "name": "Манометр DM 02",
        "manufacturer": "",
        "specs": {},
        "description": ""
    }
    missing_fields = validate_input(data)
    assert len(missing_fields) == 3
    assert "Производитель" in missing_fields
    assert "Характеристики товара" in missing_fields
    assert "Описание / Фрагмент тех. паспорта" in missing_fields

def test_specs_parsing():
    specs_raw = "диапазон измерений = 0–1,6 МПа\nкласс точности = 1,5\nприсоединение = G1/2"
    specs = {}
    for line in specs_raw.splitlines():
        if '=' in line:
            key, value = line.split('=', 1)
            specs[key.strip()] = value.strip()
    assert specs == {
        "диапазон измерений": "0–1,6 МПа",
        "класс точности": "1,5",
        "присоединение": "G1/2"
    }
