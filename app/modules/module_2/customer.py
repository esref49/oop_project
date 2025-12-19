from .implementations import ElectricityMeter, WaterMeter, GasMeter

class Customer:
    """
    Sistemdeki müşterileri temsil eden sınıf.
    OOP İlişkisi: Aggregation (Müşteri -> Sayaçlar)
    Bir müşterinin birden fazla sayacı olabilir.
    """
    def __init__(self, tc_no, full_name, phone=""):
        # Kapsülleme (Encapsulation) için protected değişkenler
        self._tc_no = tc_no
        self._full_name = full_name
        self._phone = phone
        # Müşteriye ait sayaçları tutan liste
        self._meters = []

    def add_meter(self, meter_obj):
        """Müşteriye yeni bir sayaç (Elektrik/Su/Gaz) tanımlar."""
        # Basit bir kontrol: Gelen nesne gerçekten bir sayaç mı?
        if hasattr(meter_obj, 'calculate_cost'):
            self._meters.append(meter_obj)
            print(f"[Müşteri] {self._full_name} kişisine {meter_obj.get_id()} eklendi.")
        else:
            print("[Hata] Geçersiz sayaç nesnesi!")

    def remove_meter(self, meter_id):
        """Müşterinin üzerine kayıtlı bir sayacı siler."""
        for meter in self._meters:
            if meter.get_id() == meter_id:
                self._meters.remove(meter)
                print(f"[Bilgi] {meter_id} sayacı {self._full_name} portföyünden çıkarıldı.")
                return True
        return False

    def get_total_debt(self):
        """
        Müşterinin sahip olduğu TÜM sayaçlardaki toplam fatura tutarını hesaplar.
        """
        total = 0.0
        print(f"\n--- Sn. {self._full_name} FATURA DÖKÜMÜ ---")
        for meter in self._meters:
            cost = meter.calculate_cost()
            print(f"- {meter.get_status()} => {cost:.2f} TL")
            total += cost
        print(f"TOPLAM ÖDENECEK: {total:.2f} TL\n")
        return total

    def __str__(self):
        """Sınıfın okunabilir (string) temsili."""
        return f"Müşteri: {self._full_name} (TC: {self._tc_no}) | Abone Sayısı: {len(self._meters)}"

# --- Modül Test Bloğu ---
if __name__ == "__main__":
    # Bu dosya tek başına çalıştırılırsa bu test kodu devreye girer
    print("--- Customer Modülü Testi Başlıyor ---")
    
    # Örnek Müşteri
    musteri = Customer("12345678901", "Bilal Emir")
    
    # Örnek Sayaçlar
    e_meter = ElectricityMeter("E-101", 150, "Ev")
    w_meter = WaterMeter("W-202", 15, "Ev")
    
    # İlişkilendirme (Aggregation)
    musteri.add_meter(e_meter)
    musteri.add_meter(w_meter)
    
    # Müşteri Bilgisi ve Borç Sorgulama
    print(musteri)
    musteri.get_total_debt()