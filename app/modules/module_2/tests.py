import unittest
import os
import json
from .implementations import ElectricityMeter, WaterMeter, GasMeter
from .repository import MeterRepository
from .services import MeterService
from .customer import Customer

class TestElectricityMeter(unittest.TestCase):
    """Elektrik Sayacı Sınıfı Testleri"""

    def setUp(self):
        self.meter = ElectricityMeter("TEST-E1", 100.0, "Istanbul", voltage=220)

    def test_initialization(self):
        """Başlangıç değerlerinin doğru atanması"""
        self.assertEqual(self.meter.get_id(), "TEST-E1")
        self.assertEqual(self.meter.get_usage_amount(), 100.0)
        self.assertEqual(self.meter.voltage, 220)
        self.assertEqual(self.meter._type, "Electricity")

    def test_negative_voltage_error(self):
        """Negatif voltaj girildiğinde hata vermeli"""
        with self.assertRaises(ValueError):
            ElectricityMeter("ERR", 100, "Loc", voltage=-50)

    def test_cost_calculation(self):
        """Fatura hesaplama doğruluğu (100 * 1.5 = 150)"""
        expected = 100.0 * 1.5
        self.assertEqual(self.meter.calculate_cost(), expected)

    def test_status_message(self):
        """Durum mesajının formatı"""
        status = self.meter.get_status()
        self.assertIn("220V", status)
        self.assertIn("TEST-E1", status)


class TestWaterMeter(unittest.TestCase):
    """Su Sayacı Sınıfı Testleri"""

    def setUp(self):
        self.meter = WaterMeter("TEST-W1", 10.0, "Ankara", pipe_diameter=0.75)

    def test_initialization(self):
        self.assertEqual(self.meter.pipe_diameter, 0.75)
        self.assertEqual(self.meter._type, "Water")

    def test_cost_calculation(self):
        """Su faturası: 10 * 4.0 = 40.0"""
        self.assertEqual(self.meter.calculate_cost(), 40.0)

    def test_usage_update(self):
        """Kullanım miktarı güncelleme"""
        self.meter.set_usage_amount(20.0)
        self.assertEqual(self.meter.get_usage_amount(), 20.0)


class TestGasMeter(unittest.TestCase):
    """Doğalgaz Sayacı Sınıfı Testleri"""

    def setUp(self):
        self.meter = GasMeter("TEST-G1", 50.0, "Izmir", pressure=4)

    def test_pressure_assignment(self):
        self.assertEqual(self.meter.pressure, 4)

    def test_cost_calculation(self):
        """Gaz faturası: 50 * 5.0 = 250.0"""
        self.assertEqual(self.meter.calculate_cost(), 250.0)


class TestMeterRepository(unittest.TestCase):
    """Veritabanı (Repository) Testleri"""

    def setUp(self):
        # Test için geçici bir repo oluştur
        self.repo = MeterRepository()
        # Test verisi ekle
        self.e_meter = ElectricityMeter("REPO-TEST-1", 50, "TestLoc")

    def test_add_and_retrieve(self):
        """Kayıt ekleme ve geri okuma"""
        self.repo.add(self.e_meter)
        data = self.repo.get_all()
        
        found = False
        for item in data:
            if item.get("id") == "REPO-TEST-1":
                found = True
                break
        self.assertTrue(found, "Eklenen kayıt veritabanında bulunamadı!")

    def test_get_by_id(self):
        """ID ile arama testi"""
        self.repo.add(self.e_meter)
        item = self.repo.get_by_id("REPO-TEST-1")
        self.assertIsNotNone(item)
        self.assertEqual(item.get("type"), "Electricity")

    def test_non_existent_id(self):
        """Olmayan kayıt aranırsa None dönmeli"""
        item = self.repo.get_by_id("X-9999")
        self.assertIsNone(item)


class TestServices(unittest.TestCase):
    """Servis Katmanı Testleri"""

    def setUp(self):
        self.service = MeterService()

    def test_unique_id_generation(self):
        """ID üretim testi"""
        id1 = self.service.generate_unique_id("E")
        id2 = self.service.generate_unique_id("E")
        self.assertNotEqual(id1, id2)
        self.assertTrue(id1.startswith("E-"))

    def test_register_meter(self):
        """Servis üzerinden kayıt"""
        meter = self.service.register_meter("Electricity", 100, "ServiceLoc")
        self.assertIsInstance(meter, ElectricityMeter)
        self.assertEqual(meter.get_usage_amount(), 100)

    def test_invalid_type_registration(self):
        """Hatalı tip gönderimi"""
        with self.assertRaises(ValueError):
            self.service.register_meter("Nuclear", 100, "Loc")


class TestCustomer(unittest.TestCase):
    """Müşteri Sınıfı Testleri"""

    def setUp(self):
        self.customer = Customer("11111111111", "Test User")
        self.e_meter = ElectricityMeter("CUST-E1", 100, "Home")
        self.w_meter = WaterMeter("CUST-W1", 20, "Home")

    def test_add_meter(self):
        """Müşteriye sayaç ekleme"""
        self.customer.add_meter(self.e_meter)
        self.assertIn(f"Abone Sayısı: 1", str(self.customer))

    def test_remove_meter(self):
        """Sayaç silme"""
        self.customer.add_meter(self.e_meter)
        result = self.customer.remove_meter("CUST-E1")
        self.assertTrue(result)
        self.assertIn(f"Abone Sayısı: 0", str(self.customer))

    def test_total_debt(self):
        """Toplam borç hesaplama"""
        self.customer.add_meter(self.e_meter) # 150 TL
        self.customer.add_meter(self.w_meter) # 80 TL
        total = self.customer.get_total_debt()
        self.assertEqual(total, 230.0)


if __name__ == "__main__":
    unittest.main()