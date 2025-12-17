from .services import MeterService
from .repository import UtilityRepository
import random
import time

def run_demo():
    """
    Projenin tüm özelliklerini sergileyen ana senaryo fonksiyonu.
    """
    print("--- AKILLI SEHIR: ENERJI VE SU YONETIM SISTEMI DEMO BASLATIYOR ---")
    
    # 1. Servis ve Depo (Repository) Kurulumu başlatılıyor
    service = MeterService()
    repo = UtilityRepository()
    
    print("\n[ADIM 1] SAYAÇLAR SİSTEME KAYDEDİLİYOR...")
    
    # Farklı tiplerde sayaçlar oluşturarak Polimorfizm (Çok Biçimlilik) hazırlığı
    # Servis katmanı kullanılarak nesneler üretiliyor
    m1 = service.register_meter("Electricity", 100, "Kizilay Mah. Apt:5")
    m2 = service.register_meter("Water", 45, "Cankaya Kosk Yolu")
    m3 = service.register_meter("Gas", 300, "Ulus Sanayi Sitesi")
    m4 = service.register_meter("Electricity", 50, "Batikent Metro Yandi")
    m5 = service.register_meter("Water", 12, "Kizilay AVM")
    
    # Oluşturulan sayaçları Repository'e (Veritabanına) ekliyoruz
    # Repo katmanı burada "Kalıcılık" (Persistence) görevini üstleniyor
    repo.add(m1)
    repo.add(m2)
    repo.add(m3)
    repo.add(m4)
    repo.add(m5)
    
    print(f"   -> Toplam {len(repo.get_all())} adet sayaç başarıyla veritabanına işlendi.")

    # 2. Kullanım Simülasyonu
    print("\n[ADIM 2] GÜNLÜK TÜKETİM VERİLERİ SİMÜLE EDİLİYOR...")
    # Döngü ile tüm sayaçları gezip rastgele kullanım ekliyoruz
    for meter in repo.get_all():
        # 10 ile 50 birim arası rastgele tüketim
        delta = random.randint(10, 50)
        # Servis katmanı üzerinden iş mantığı işletiliyor
        log_message = service.record_usage(meter.get_id(), delta)
        print(f"   -> {log_message}")
        
    # 3. Raporlama ve Fatura Hesaplama
    print("\n[ADIM 3] FATURALAR VE DURUM RAPORU HAZIRLANIYOR...")
    # Burada her nesne kendi 'calculate_cost' metodunu kullanır (POLİMORFİZM)
    # Elektrik sayacı voltaja göre, Su sayacı kademeye göre hesap yapar.
    full_report = service.generate_report()
    print(full_report)

    # 4. Arıza ve Kesinti Simülasyonu
    print("\n[ADIM 4] ACİL DURUM VE KESİNTİ SİMÜLASYONU...")
    # 'Kizilay' bölgesindeki 'Electricity' (Elektrik) sayaçlarını sabote ediyoruz
    print("   -> Uyarı: Kizilay bölgesinde trafo patlaması simüle ediliyor...")
    failure_log = service.simulate_failure("Electricity", "Kizilay")
    print(f"   -> SİSTEM YANITI: {failure_log}")

    # 5. Verileri Yedekleme (Dosya İşlemleri)
    print("\n[ADIM 5] GÜN SONU YEDEĞİ ALINIYOR (JSON)...")
    if repo.save_to_json():
        print("   -> Veriler 'utilities_backup.json' dosyasına güvenle kaydedildi.")
    else:
        print("   -> Hata: Yedekleme başarısız.")
    
    print("\n--- DEMO SENARYOSU BAŞARIYLA TAMAMLANDI ---")

# Bu dosya modül olarak çağrıldığında çalışması için fonksiyonu dışarı açıyoruz
if __name__ == "__main__":
    run_demo()