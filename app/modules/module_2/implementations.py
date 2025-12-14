from .base import Utility
import random

# -----------------------------------------------------------------------------
# SINIF 1: Elektrik Sayacı (ElectricityMeter)
# -----------------------------------------------------------------------------
class ElectricityMeter(Utility):
    """
    Elektrik tüketimini ölçen sayaç sınıfı.
    Özel Nitelik: Voltaj (voltage)
    """
    def __init__(self, id, usage_amount, location, voltage=220):
        # Base class'ın (Utility) __init__ metodunu çağırıyoruz
        super().__init__(id, "Electricity", usage_amount, location)
        self._voltage = voltage
        # Birim fiyat (TL/kWh)
        self._unit_price = 1.8 

    def calculate_cost(self):
        """
        Elektrik faturası hesaplama: Kullanım * Birim Fiyat
        """
        base_cost = self._usage_amount * self._unit_price
        
        if self._voltage > 230:
            return base_cost * 1.05  # %5 ek maliyet
        return base_cost

    def get_status(self):
        status = "AKTİF" if self._is_active else "PASİF"
        return (f"[Elektrik] ID: {self._id} | Konum: {self._location} | "
                f"Voltaj: {self._voltage}V | Durum: {status}")

    # Elektrik kesintisi simülasyonu (Ekstra Metot)
    def simulate_power_cut(self):
        self._is_active = False
        print(f"UYARI: {self._location} bölgesinde elektrik kesildi!")

# -----------------------------------------------------------------------------
# SINIF 2: Su Sayacı (WaterMeter)
# -----------------------------------------------------------------------------
class WaterMeter(Utility):
    """
    Su tüketimini ölçen sayaç sınıfı.
    Özel Nitelik: Boru Çapı (pipe_diameter)
    """
    def __init__(self, id, usage_amount, location, pipe_diameter_inches=0.5):
        super().__init__(id, "Water", usage_amount, location)
        self._pipe_diameter = pipe_diameter_inches
        self._unit_price = 5.0 # TL/m3

    def calculate_cost(self):
        """
        Su faturası hesaplama: Kademe mantığı
        10 m3 üstü kullanımda fiyat %50 artar.
        """
        if self._usage_amount > 10:
            # İlk 10 birim normal, kalanı zamlı
            normal_part = 10 * self._unit_price
            extra_part = (self._usage_amount - 10) * (self._unit_price * 1.5)
            return normal_part + extra_part
        else:
            return self._usage_amount * self._unit_price

    def get_status(self):
        return (f"[Su] ID: {self._id} | Konum: {self._location} | "
                f"Boru: {self._pipe_diameter}\" | Tüketim: {self._usage_amount} m3")

    # Su kaçağı kontrolü (Ekstra Metot)
    def check_leakage(self):
        # Rastgele kaçak tespiti
        if random.choice([True, False]):
            print(f"ALARM: {self._id} numaralı su sayacında kaçak şüphesi!")
            return True
        return False

# -----------------------------------------------------------------------------
# SINIF 3: Doğalgaz Sayacı (GasMeter)
# -----------------------------------------------------------------------------
class GasMeter(Utility):
    """
    Doğalgaz tüketimini ölçen sayaç sınıfı.
    Özel Nitelik: Basınç (pressure_bar)
    """
    def __init__(self, id, usage_amount, location, pressure_bar=4):
        super().__init__(id, "Gas", usage_amount, location)
        self._pressure_bar = pressure_bar
        self._unit_price = 4.5 # TL/m3

    def calculate_cost(self):
        """
        Doğalgaz maliyeti: Basınç faktörü ile çarpılarak hesaplanır.
        """
        pressure_factor = 1.0
        if self._pressure_bar > 5:
            pressure_factor = 1.1  # Yüksek basınçta birim maliyet artar
            
        return self._usage_amount * self._unit_price * pressure_factor

    def get_status(self):
        return (f"[Doğalgaz] ID: {self._id} | Konum: {self._location} | "
                f"Basınç: {self._pressure_bar} Bar")