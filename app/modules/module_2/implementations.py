from .base import Utility

# =============================================================================
# MODÜL 2: SAYAÇ İMPLEMENTASYONLARI
# =============================================================================
# Bu modül, 'base.py' içerisinde tanımlanan soyut (Abstract) 'Utility' sınıfını
# temel alarak, özelleştirilmiş sayaç sınıflarını (Elektrik, Su, Gaz) içerir.
#
# OOP Prensipleri:
# 1. Inheritance (Kalıtım): Tüm sınıflar Utility sınıfından türetilmiştir.
# 2. Polymorphism (Çok Biçimlilik): calculate_cost ve get_status metodları
#    her sınıf için farklı davranışlar sergiler.
# 3. Encapsulation (Kapsülleme): Veri bütünlüğü korunur.
# =============================================================================

class ElectricityMeter(Utility):
    """
    Elektrik Enerjisi Tüketim Sayacı Sınıfı.
    -------------------------------------------------------------------------
    Şehir şebekesindeki aktif elektrik abonelerinin tüketim verilerini ve
    teknik özelliklerini simüle eder.

    Attributes:
        voltage (int): Şebeke gerilim seviyesi (Örn: 220V Ev, 380V Sanayi).
        
    Business Logic (İş Mantığı):
        - Elektrik birim fiyatı diğer enerji türlerine göre daha değişkendir.
        - Voltaj değeri, güvenlik kontrolleri için saklanır.
    """

    def __init__(self, meter_id, usage, location, voltage=220):
        """
        Yeni bir Elektrik Sayacı nesnesi başlatır (Constructor).
        """
        # Base sınıfın (Utility) yapıcısını çağırarak temel özellikleri set ediyoruz.
        # "Electricity" tipi otomatik olarak atanır.
        super().__init__(meter_id, "Electricity", usage, location)
        
        # Ekstra validasyon katmanı
        if voltage < 0:
            raise ValueError("Voltaj değeri negatif olamaz! Fizik kurallarına aykırı.")
            
        self.voltage = voltage

    def calculate_cost(self):
        """
        Fatura Hesaplama Motoru (Polimorfik Metot).
        
        Bu metot, Utility sınıfındaki soyut metodu ezer (Override).
        Elektrik piyasası birim fiyatlarına göre borç hesaplar.

        Formül:
            Toplam Tutar = Tüketim (kWh) * Birim Fiyat (TL)
        
        Returns:
            float: Hesaplanan toplam fatura tutarı.
        """
        # 2025 Enerji Piyasası Düzenleme Kurumu (EPDK) simülasyon fiyatı
        unit_price = 1.5         
        return self.get_usage_amount() * unit_price

    def get_status(self):
        """
        Cihaz Durum Raporu (Polimorfik Metot).
        
        Sistemin izleme ekranlarında (Dashboard) gösterilecek detaylı bilgiyi üretir.
        Elektrik sayacına özel 'Voltaj' bilgisini rapora ekler.

        Returns:
            str: Okunabilir formatta durum metni.
        """
        status_msg = (
            f"[Elektrik Sayacı] ID: {self.get_id()} | "
            f"Konum: {self.get_location()} | "
            f"Tüketim: {self.get_usage_amount()} kWh | "
            f"Voltaj: {self.voltage}V | "
            f"Durum: {'Aktif' if self._is_active else 'Pasif'}"
        )
        return status_msg


class WaterMeter(Utility):
    """
    Su Şebekesi Yönetim Sınıfı.
    -------------------------------------------------------------------------
    İSKİ vb. kurumların su sayaçlarını temsil eder.
    
    Özellikler:
        - Boru çapı bilgisi (pipe_diameter) ile basınç analizi imkanı sağlar.
        - Metreküp (m3) cinsinden hesaplama yapar.
    """

    def __init__(self, meter_id, usage, location, pipe_diameter=0.5):
        """
        Su Sayacı Kurulumu.
        """
        super().__init__(meter_id, "Water", usage, location)
        self.pipe_diameter = pipe_diameter

    def calculate_cost(self):
        """
        Su Faturası Hesaplama.
        
        Not: Su birim fiyatlarına atık su bedeli dahildir.

        """
        unit_price = 4.0  # Birim Fiyat (TL/m3)
        return self.get_usage_amount() * unit_price

    def get_status(self):
        """
        Su sayacı durumunu raporlar.
        Boru çapı bilgisi eklenmiştir.
        """
        status_msg = (
            f"[Su Sayacı] ID: {self.get_id()} | "
            f"Konum: {self.get_location()} | "
            f"Tüketim: {self.get_usage_amount()} m3 | "
            f"Boru Çapı: {self.pipe_diameter}\" "
        )
        return status_msg


class GasMeter(Utility):
    """
    Doğalgaz Dağıtım ve Ölçüm Sınıfı.
    -------------------------------------------------------------------------
    Isınma ve sanayi tipi doğalgaz abonelerini yönetir.
    Güvenlik kritik bir parametre olduğu için 'Basınç' (Pressure) takibi yapar.
    """

    def __init__(self, meter_id, usage, location, pressure=4):
        """
        Doğalgaz Sayacı Başlatıcı.
        
            meter_id (str): Sayaç ID.
            usage (float): m3 cinsinden gaz tüketimi.
            location (str): Tesisat adresi.
            pressure (int, optional): Gaz basıncı (Bar). Standart: 4 Bar.
        """
        super().__init__(meter_id, "Gas", usage, location)
        self.pressure = pressure

    def calculate_cost(self):
        """
        Doğalgaz Faturası Hesaplama.
        
        Kış tarifesi ve KDV dahil fiyatlandırma simülasyonudur.
        
        Returns:
            float: Tutar.
        """
        unit_price = 5.0  # TL/m3
        return self.get_usage_amount() * unit_price

    def get_status(self):
        """
        Gaz sayacı için güvenlik odaklı durum raporu.
        Basınç değerini içerir.
        """
        status_msg = (
            f"[Doğalgaz] ID: {self.get_id()} | "
            f"Konum: {self.get_location()} | "
            f"Tüketim: {self.get_usage_amount()} m3 | "
            f"Basınç: {self.pressure} Bar"
        )
        return status_msg