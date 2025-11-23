import requests
import pytest
from tests.conftest import BASE_URL

class TestAvitoApi:

    def test_create_item_positive(self, item_data):
        """Проверка успешного создания объявления"""
        url = f"{BASE_URL}/item"
        response = requests.post(url, json=item_data)
        
        assert response.status_code == 200
        # Проверяем, что в статусе есть подтверждение сохранения
        assert "Сохранили объявление" in response.json()['status']

    def test_create_item_negative(self, item_data):
        """Негативный кейс: передаем цену строкой"""
        url = f"{BASE_URL}/item"
        item_data['price'] = "строка вместо числа"
        
        response = requests.post(url, json=item_data)
        
        assert response.status_code == 400

    def test_get_item(self, created_item):
        """Получение объявления по ID"""
        item_id, sent_data = created_item
        url = f"{BASE_URL}/item/{item_id}"
        
        response = requests.get(url)
        assert response.status_code == 200
        
        # API возвращает список, берем первый элемент
        data = response.json()[0]
        
        assert data['id'] == item_id
        assert data['name'] == sent_data['name']
        assert data['sellerId'] == sent_data['sellerID']
        assert data['price'] == sent_data['price']

    def test_get_seller_items(self, created_item):
        """Получение объявлений по sellerID"""
        item_id, sent_data = created_item
        seller_id = sent_data['sellerID']
        
        url = f"{BASE_URL}/{seller_id}/item"
        response = requests.get(url)
        assert response.status_code == 200
        
        items = response.json()
        
        # Собираем список всех ID товаров продавца
        all_ids = [item['id'] for item in items]
        
        # Проверяем, что наш созданный товар есть в этом списке
        assert item_id in all_ids

    def test_get_statistics(self, created_item):
        """Получение статистики"""
        item_id, sent_data = created_item
        url = f"{BASE_URL}/statistic/{item_id}"
        
        response = requests.get(url)
        assert response.status_code == 200
        
        # Статистика тоже приходит в виде списка
        stats = response.json()[0]
        
        assert stats['likes'] == sent_data['statistics']['likes']
        assert stats['viewCount'] == sent_data['statistics']['viewCount']