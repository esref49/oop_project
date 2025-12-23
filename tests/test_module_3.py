import time
import sys

from app.modules.module_3.implementations import AmbulanceUnit, FireFightingUnit, PoliceUnit
from app.modules.module_3.repository import EmergencyRepository
from app.modules.module_3.services import EmergencyService

def main():
    print("\n[SİSTEM] Acil Durum Yönetim Sistemi Başlatılıyor...")
    time.sleep(1)

    # 1. Altyapıyı Kurma
    try:
        repo = EmergencyRepository()
        service = EmergencyService(repo)
    except NameError:
        print("[HATA] Sınıflar bulunamadı! Lütfen 'Repository' ve 'EmergencyService' sınıflarının tanımlı olduğundan emin olun.")
        return

    # 2. Başlangıç Filosunu Oluşturma
    print("[SİSTEM] Filo verileri yükleniyor...")
    filo = [
        PoliceUnit(unit_id=101, fuel_level=80, is_enough_staff=True, patrol_area="Kızılay", current_location=5),
        PoliceUnit(unit_id=102, fuel_level=40, is_enough_staff=True, patrol_area="Çankaya", current_location=12),
        AmbulanceUnit(unit_id=201, fuel_level=90, is_enough_staff=True, medical_supply_level=100, is_sterilized=True, current_location=3),
        AmbulanceUnit(unit_id=202, fuel_level=60, is_enough_staff=True, medical_supply_level=40, is_sterilized=False, current_location=18), # Bu steril değil
        FireFightingUnit(unit_id=301, fuel_level=85, is_enough_staff=True, water_level=100, foam_level=100, current_location=8)
    ]

    # 3. Başlangıç Durumunu Dosyaya Yazma (Eşitleme)
    # Program açılır açılmaz units_status.txt güncellenir.
    service.repository.save_unit_info(filo)
    print("[SİSTEM] Filo durumu 'units_status.txt' dosyasına eşitlendi.")
    time.sleep(1)

    # --- ANA MENÜ DÖNGÜSÜ ---
    while True:
        print("\n" + "█"*50)
        print("     🚨 ACİL DURUM KOMUTA MERKEZİ 🚨")
        print("█"*50)
        print("  [1] 🆘 Vaka İhbarı Gir (Operasyon Başlat)")
        print("  [2] 🔧 Filo Yönetimi (Hizmete Al/Çıkar)")
        print("  [3] ➕ Yeni Birim Ekle (Satın Alma)")
        print("  [4] 📂 Log Kayıtlarını İncele")
        print("  [5] 🚪 Sistemi Kapat")
        print("-" * 50)
        
        secim = input("👉 Komutunuz: ")

        # --- 1. VAKA OLUŞTURMA ---
        if secim == "1":
            print("\n--- VAKA TİPLERİ ---")
            print("Yangın, Trafik Kazası, Kalp Krizi, Hırsızlık, Kavga/Darp...")
            
            case_type = input("Olay Türü Giriniz: ")
            
            try:
                severity = int(input("Ciddiyet Seviyesi (1-10): "))
                # Servisi çağırıyoruz, filoyu parametre olarak veriyoruz
                service.creating_case(unit_list=filo, case_type=case_type, severity=severity)
                
                # Vaka bitince durumlar değiştiği için dosyayı tekrar güncelliyoruz
                service.repository.save_unit_info(filo)
                
            except ValueError:
                print("! Hata: Seviye sayı olmalı.")

        # --- 2. FİLO YÖNETİMİ (Hizmete Alma/Çıkarma) ---
        elif secim == "2":
            # Yazdığımız yönetim fonksiyonunu çağırıyoruz
            service.manage_unit_status(filo)

        # --- 3. YENİ BİRİM EKLEME ---
        elif secim == "3":
            print("\n--- YENİ BİRİM ALIMI ---")
            print("1. Polis | 2. Ambulans | 3. İtfaiye")
            u_type = input("Tür Seçimi: ")
            
            try:
                u_id = int(input("Yeni Araç ID: "))
                loc = int(input("Başlangıç Konumu (0-20): "))
                
                new_unit = None
                if u_type == "1":
                    new_unit = PoliceUnit(u_id, 100, True, "Genel", current_location=loc)
                elif u_type == "2":
                    new_unit = AmbulanceUnit(u_id, 100, True, 100, True, current_location=loc)
                elif u_type == "3":
                    new_unit = FireFightingUnit(u_id, 100, True, 100, 100, current_location=loc)
                
                if new_unit:
                    # Listeye ekle
                    filo.append(new_unit)
                    print(f"\n[SİSTEM] {new_unit.unit_type} (ID: {u_id}) envantere eklendi.")
                    # Dosyayı anında güncelle
                    service.repository.save_unit_info(filo)
                else:
                    print("! Geçersiz tür seçimi.")
            except ValueError:
                print("! Hatalı giriş yaptınız.")

        # --- 4. LOG PANELİ ---
        elif secim == "4":
            service.event_log_management()

        # --- 5. ÇIKIŞ ---
        elif secim == "5":
            print("\n[SİSTEM] Sistem kapatılıyor. Günlükler kaydedildi.")
            break
        
        else:
            print("\n[!] Geçersiz komut, tekrar deneyin.")
        
        input("\nDevam etmek için Enter'a basın...")

# Kodun çalıştırıldığı nokta
if __name__ == "__main__":
    main()