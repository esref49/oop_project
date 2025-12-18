import unittest
from .implementations import ElectricityMeter, WaterMeter, GasMeter
from .repository import UtilityRepository
from .services import MeterService

class TestUtilitySystem(unittest.TestCase):
    """
    Enerji ve Su Yönetim Sistemi için Birim Testleri (Unit Tests).
    Proje gereksinimlerinde belirtilen senaryoları test eder.
    """

    def setUp(self):
        """Her testten önce çalışır, temiz bir ortam hazırlar."""
        self.repo = UtilityRepository()
        self.service = MeterService()
        # Test verileri
        self.elec_meter = ElectricityMeter("TEST-E1", 100, "Test Location", voltage=220)
        self.water_meter = WaterMeter("TEST-W1", 5, "Test Location", pipe_diameter_inches=0.5)

    def test_electricity_cost_calculation(self):
        """Elektrik faturası hesaplama testi."""
        # 100 birim * 1.8 birim fiyat = 180 TL olmalı
        expected_cost = 100 * 1.8
        self.assertEqual(self.elec_meter.calculate_cost(), expected_cost)

    def test_water_tier_pricing(self):
        """Su faturası kademeli fiyatlandırma testi (Limit aşım testi)."""
        # 10 m3 altı kullanım (Normal tarife)
        meter_low = WaterMeter("W-LOW", 8, "Loc") # 8 m3
        cost_low = 8 * 5.0
        self.assertEqual(meter_low.calculate_cost(), cost_low)

        # 10 m3 üstü kullanım (Zamlı tarife)
        meter_high = WaterMeter("W-HIGH", 12, "Loc") # 12 m3 (10 normal + 2 zamlı)
        expected_high = (10 * 5.0) + (2 * (5.0 * 1.5))
        self.assertEqual(meter_high.calculate_cost(), expected_high)

    def test_repository_add_and_get(self):
        """Repository ekleme ve getirme testi."""
        self.repo.add(self.elec_meter)
        retrieved = self.repo.get_by_id("TEST-E1")
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.get_location(), "Test Location")

    def test_repository_duplicate_prevention(self):
        """Aynı ID ile iki kere kayıt eklenememesi testi."""
        self.repo.add(self.elec_meter)
        # Aynı sayacı tekrar eklemeye çalışıyoruz
        result = self.repo.add(self.elec_meter)
        # False dönmeli çünkü zaten var
        self.assertFalse(result)

    def test_negative_usage_validation(self):
        """Negatif kullanım girilmesini engelleme testi."""
        # Base class'taki validasyon kontrolü
        self.elec_meter.set_usage_amount(-50)
        # Değer değişmemeli, eski değer (100) kalmalı
        self.assertEqual(self.elec_meter.get_usage_amount(), 100)

    def test_service_meter_creation(self):
        """Servis üzerinden sayaç oluşturma testi."""
        new_meter = self.service.register_meter("Gas", 50, "Sanayi")
        self.assertIsInstance(new_meter, GasMeter)
        self.assertEqual(new_meter.get_usage_amount(), 50)

if __name__ == '__main__':
    unittest.main()