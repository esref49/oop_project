from abc import ABC, abstractmethod
from datetime import datetime

# Enerji ve su yönetimi için temel soyut sınıf
class Utility(ABC):
    _meter_types = ["Electricity", "Water", "Gas"]

    def __init__(self, id, type, usage_amount, location):
        self._id = id
        self._type = type
        self._usage_amount = usage_amount
        self._location = location
        self._is_active = True
        self._last_reading_date = datetime.now()

    @abstractmethod
    def calculate_cost(self):
        pass

    @abstractmethod
    def get_status(self):
        pass

    @staticmethod
    def validate_usage_amount(amount):
        if amount < 0:
            return False
        return True

    @classmethod
    def get_allowed_types(cls):
        return cls._meter_types

    def get_id(self):
        return self._id

    def set_id(self, new_id):
        self._id = new_id

    def get_usage_amount(self):
        return self._usage_amount

    def set_usage_amount(self, amount):
        if self.validate_usage_amount(amount):
            self._usage_amount = amount
        else:
            print("Hata: Kullanım miktarı negatif olamaz!")

    def get_location(self):
        return self._location