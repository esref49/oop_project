import time
from .repository import MeterRepository

def run_demo():
    """
    Modül 2'nin ana çalışma fonksiyonudur.
    Veritabanındaki tüm sayaçları listeler.
    """
    print("--- Veritabanına Bağlanılıyor... ---") # Debug için ekledim
    
    repo = MeterRepository()
    all_meters = repo.get_all()

    print("\n" + "="*60)
    print(f"   SİSTEMDE KAYITLI ABONE LİSTESİ (TOPLAM: {len(all_meters)})")
    print("="*60)

    if not all_meters:
        print("Henyüz kayıtlı veri yok. Lütfen 'seeder.py' çalıştırın.")
        return

    # Başlıkları yazdır
    print(f"{'ID':<12} {'TİP':<15} {'KONUM':<25} {'TÜKETİM':<10} {'DURUM'}")
    print("-" * 75)

    for item in all_meters:
        # Veritabanından gelen veriyi oku
        m_id = item.get("id", "N/A")
        m_type = item.get("type", "Unknown")
        location = item.get("location", "Bilinmiyor")
        usage = item.get("usage", 0)
        
        # Konum çok uzunsa kes
        if len(location) > 22:
            location = location[:22] + "..."

        print(f"{m_id:<12} {m_type:<15} {location:<25} {usage:<10.1f} Aktif")

    print("-" * 75)
    print("Listeleme tamamlandı.\n")