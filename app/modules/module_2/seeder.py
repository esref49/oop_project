import random
import time
import uuid
from .implementations import ElectricityMeter, WaterMeter, GasMeter
from .repository import MeterRepository

"""
seeder.py
-----------------------------------------------------------------------
Bu modül, Akıllı Şehir Yönetim Sistemi'nin (Module 2) test edilmesi ve
performans analizi yapılabilmesi için gereken 'Dummy Data' (Sahte Veri)
üretimini sağlar.
Manuel olarak 1000 tane veri girmek yerine, bu otomasyon script'i ile
sistemin 'Load Test' (Yük Testi) kapasitesi ölçülmüştür.

Kullanılan Algoritmalar:
- Randomizasyon: Rastgele isim, adres ve tüketim verisi üretimi.
- Factory Pattern Benzeri Yapı: Sayaç tipine göre nesne üretimi.
- Batch Processing: Verilerin veritabanına (JSON) toplu işlenmesi.
-----------------------------------------------------------------------
"""

# Rastgele veri havuzu (Veri çeşitliliği sağlamak için)
FIRST_NAMES = [
    "Ahmet", "Mehmet", "Ayse", "Fatma", "Ali", "Veli", "Hasan", "Huseyin",
    "Mustafa", "Kemal", "Zeynep", "Elif", "Burak", "Can", "Cem", "Deniz",
    "Ece", "Selin", "Pelin", "Merve", "Gamze", "Gizem", "Ozan", "Tolga",
    "Baris", "Savas", "Yigit", "Mert", "Berk", "Emre", "Kaan", "Arda",
    "Kerem", "Sinan", "Volkan", "Serkan", "Hakan", "Gokhan", "Orhan",
    "Osman", "Murat", "Fatih", "Yavuz", "Selim", "Suleyman", "Abdullah"
]

LAST_NAMES = [
    "Yilmaz", "Kaya", "Demir", "Celik", "Sahin", "Yildiz", "Yildirim",
    "Ozturk", "Aydin", "Ozdemir", "Arslan", "Dogan", "Kilic", "Aslan",
    "Cetin", "Kara", "Koc", "Kurt", "Ozkan", "Simsek", "Polat", "Acar",
    "Erdogan", "Guler", "Tekin", "Yalcin", "Avci", "Bulut", "Coskun",
    "Gunes", "Isik", "Kaplan", "Keskin", "Korkmaz", "Sonmez", "Tas",
    "Ucar", "Uysal", "Yuksel", "Zengin", "Aksoy", "Aktas", "Alkan"
]

DISTRICTS = [
    "Kadikoy", "Besiktas", "Uskudar", "Sisli", "Beyoglu", "Fatih",
    "Maltepe", "Kartal", "Pendik", "Umraniye", "Atasehir", "Bakirkoy",
    "Zeytinburnu", "Sariyer", "Beykoz", "Avcilar", "Esenyurt", "Bagcilar"
]

STREETS = [
    "Ataturk Cad.", "Cumhuriyet Cad.", "Inonu Cad.", "Bagdat Cad.",
    "Istiklal Cad.", "Baris Sok.", "Gul Sok.", "Lale Sok.", "Menekse Sok.",
    "Karanfil Sok.", "Cinar Sok.", "Papatya Sok.", "Gonca Sok."
]

def generate_random_tc():
    """Rastgele 11 haneli TC Kimlik No üretir (Algoritma simülasyonu)."""
    return str(random.randint(10000000000, 99999999999))

def generate_random_phone():
    """Rastgele 5XX'li telefon numarası üretir."""
    return f"05{random.randint(30, 55)} {random.randint(100, 999)} {random.randint(10, 99)} {random.randint(10, 99)}"

def generate_full_address():
    """Rastgele ve gerçekçi bir adres metni oluşturur."""
    district = random.choice(DISTRICTS)
    street = random.choice(STREETS)
    no = random.randint(1, 150)
    door = random.randint(1, 20)
    return f"{district}, {street} No:{no} D:{door}, Istanbul"

def create_random_meter(meter_type_choice):
    """
    Belirtilen tipe göre rastgele özelliklere sahip sayaç nesnesi üretir.
    Polimorfizm örneğidir.
    """
    customer_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    location = generate_full_address()
    
    # Unique ID oluşturma (Örn: ELEK-4A2F)
    unique_suffix = str(uuid.uuid4())[:4].upper()
    
    meter = None
    
    if meter_type_choice == 1:
        # Elektrik Sayacı Üretimi
        meter_id = f"ELK-{unique_suffix}"
        usage = random.uniform(50.0, 450.0) # Float değer
        voltage = random.choice([220, 220, 220, 380]) # Genelde 220, bazen 380 sanayi
        meter = ElectricityMeter(meter_id, usage, customer_name, voltage)
        
    elif meter_type_choice == 2:
        # Su Sayacı Üretimi
        meter_id = f"SU-{unique_suffix}"
        usage = random.uniform(5.0, 40.0)
        pipe = random.choice([0.5, 0.75, 1.0])
        meter = WaterMeter(meter_id, usage, customer_name, pipe)
        
    elif meter_type_choice == 3:
        # Doğalgaz Sayacı Üretimi
        meter_id = f"GAZ-{unique_suffix}"
        usage = random.uniform(10.0, 300.0)
        pressure = random.choice([4, 4, 4, 21]) # Bar cinsinden
        meter = GasMeter(meter_id, usage, customer_name, pressure)
        
    return meter

def run_seeder(count=100):
    """
    Ana çalıştırıcı fonksiyon.
    Varsayılan olarak 100 adet veri üretir ve veritabanına kaydeder.
    """
    print("==================================================")
    print(f"   OTOMATİK VERİ ÜRETİCİSİ (SEEDER) BAŞLATILIYOR")
    print(f"   Hedeflenen Veri Sayısı: {count}")
    print("==================================================")
    
    repo = MeterRepository()
    start_time = time.time()
    
    success_count = 0
    fail_count = 0
    
    print("\n[İşlem] Veri üretimi ve kayıt işlemi başladı...\n")
    
    for i in range(count):
        # 1 ile 3 arasında rastgele seçim yap (1:Elk, 2:Su, 3:Gaz)
        choice = random.randint(1, 3)
        
        # Nesneyi oluştur
        new_meter = create_random_meter(choice)
        
        # Veritabanına kaydet
        try:
            repo.add(new_meter)
            success_count += 1
            
            # Konsolda matrix efekti gibi akması için kısa bekleme (Opsiyonel)
            # time.sleep(0.01) 
            
            # Her 10 veride bir ekrana nokta bas (Loading bar gibi)
            if i % 10 == 0:
                print(".", end="", flush=True)
                
        except Exception as e:
            fail_count += 1
            print(f"!!! HATA DETAYI: {e}") # Hatayı ekrana bas
            continue

    end_time = time.time()
    duration = end_time - start_time
    
    print("\n\n" + "="*50)
    print(f"   SONUÇ RAPORU")
    print("="*50)
    print(f"Toplam Geçen Süre : {duration:.4f} saniye")
    print(f"Başarılı Kayıt    : {success_count}")
    print(f"Başarısız Kayıt   : {fail_count}")
    print(f"Kayıt Yeri        : /data/meters.json")
    print("="*50 + "\n")

if __name__ == "__main__":
    # Eğer bu dosya direkt çalıştırılırsa 50 tane örnek veri üret
    run_seeder(50)