import pytest
import requests
import random
from faker import Faker

fake = Faker()
BASE_URL = "https://qa-internship.avito.com/api/1"

@pytest.fixture
def item_data():
    """
    Генерируем данные для нового объявления.
    Используем random для sellerID, чтобы данные не пересекались
    с другими кандидатами.
    """
    return {
        "sellerID": random.randint(111111, 999999),
        "name": fake.job(),
        "price": random.randint(100, 50000),
        "statistics": {
            "likes": random.randint(0, 100),
            "viewCount": random.randint(100, 500),
            "contacts": random.randint(0, 10)
        }
    }

@pytest.fixture
def created_item(item_data):
    """
    Фикстура, которая создает объявление перед тестом
    и возвращает его ID и данные.
    """
    response = requests.post(f"{BASE_URL}/item", json=item_data)
    assert response.status_code == 200, "Не удалось создать объявление для теста"
    
    # Получаем данные из ответа
    response_data = response.json()
    
    # В документации указано, что ответ может содержать статус строкой
    # вида "Сохранили объявление - <ID>"
    status_msg = response_data.get('status', '')
    item_id = status_msg.split(' - ')[-1]
    
    return item_id, item_data