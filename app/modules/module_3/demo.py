import os
import time
from turtle import clearscreen
from app.modules.module_3.repository import EmergencyRepository
from app.modules.module_3.services import EmergencyService
from app.modules.module_3.implementations import AmbulanceUnit, PoliceUnit, FireFightingUnit

def main():
    
    print("="*50)
    print("[SİSTEM] Sistem başlatılıyor...")
    print("[SİSTEM] Veritabanı bağlantısı kontrol ediliyor...")
    time.sleep(2)
    repository = EmergencyRepository()
    service = EmergencyService(repository)
    print("[SİSTEM] Veritabanı başarılı bir şekilde bağlandı\n")
    print("[SİSTEM] Araçlar hizmete alınıyor...")
    time.sleep(2)

    repo = EmergencyRepository()

    ambulance1 = AmbulanceUnit(unit_id = 101, fuel_level = 79, is_enough_staff = False, medical_supply_level = 45, is_sterilized = True)
    ambulance2 = AmbulanceUnit(unit_id = 102, fuel_level = 33, is_enough_staff = True, medical_supply_level = 88, is_sterilized = False)
    ambulance3 = AmbulanceUnit(unit_id = 103, fuel_level = 47, is_enough_staff = True, medical_supply_level = 93, is_sterilized = True)
    ambulance4 = AmbulanceUnit(unit_id = 104, fuel_level = 63, is_enough_staff = True, medical_supply_level = 100, is_sterilized = True)

    police1 = PoliceUnit(unit_id = 201, fuel_level = 55, is_enough_staff = True, patrol_area=[0,5], unit_specialty="Asayiş")
    police2 = PoliceUnit(unit_id = 202, fuel_level = 56, is_enough_staff = True, patrol_area=[5,10], unit_specialty="PÖH")
    police3 = PoliceUnit(unit_id = 203, fuel_level = 43, is_enough_staff = True, patrol_area=[10,15], unit_specialty="Trafik")
    police4 = PoliceUnit(unit_id = 204, fuel_level = 12, is_enough_staff = True, patrol_area=[15,20], unit_specialty="Çelik Kuvvet")

    fire_fighting1 = FireFightingUnit(unit_id = 301, fuel_level = 83, is_enough_staff = True, water_level=780, foam_level = 239, max_water_level=3000, max_foam_level = 600, max_fuel_level=100, ladder_length = 45)
    fire_fighting2 = FireFightingUnit(unit_id = 302, fuel_level = 95, is_enough_staff = True, water_level=330, foam_level = 112, max_water_level=1000, max_foam_level = 500, max_fuel_level=100, ladder_length = 40)
    fire_fighting3 = FireFightingUnit(unit_id = 303, fuel_level = 63, is_enough_staff = False, water_level=678, foam_level = 569, max_water_level=2000, max_foam_level = 600, max_fuel_level=100, ladder_length = 45)
    fire_fighting4 = FireFightingUnit(unit_id = 304, fuel_level = 58, is_enough_staff = True, water_level=450, foam_level = 92, max_water_level=1500, max_foam_level = 400, max_fuel_level=100, ladder_length = 30)

    units = [ambulance1, ambulance2, ambulance3, ambulance4, police1, police2, police3, police4, fire_fighting1, fire_fighting2, fire_fighting3, fire_fighting4]

    print("[SİSTEM] Araçlar hizmete alındı")
    print("="*50 + "\n")

    while True:
        clearscreen()
        print(f"Aktif Araç Sayısı: {len(units)} | Son Vaka ID: {repo.get_last_case_id()}")
        print("-" * 40)
        print(" [1] 🆘 ACİL İHBAR GİRİŞİ (Vaka Oluştur)")
        print(" [2] 🚓 CANLI FİLO DURUMU (Listele)")
        print(" [3] 🛠️ ARAÇ YÖNETİMİ (Bakım/Statü Değiştir)")
        print(" [4] ➕ YENİ EKİP EKLE (Envantere Kayıt)")
        print(" [5] 🗑️ ARAÇ SİL (Envanterden Düş)")
        print(" [6] 📂 SİSTEM LOGLARINI OKU")
        print(" [Q] ❌ ÇIKIŞ")
        print("-" * 40)
        
        secim = input("👉 İşlem Seçiniz: ").upper()
        
        # --- SEÇENEK 1: VAKA OLUŞTURMA ---
        if secim == "1":
            print("\n--- 🆘 YENİ VAKA GİRİŞİ ---")
            print("Vaka Türleri: Yangın, Trafik Kazası, Kalp Krizi, Hırsızlık, Sel/Su Baskını")
            v_tur = input("Olay Türü: ")
            
            try:
                v_sev = int(input("Ciddiyet Seviyesi (1-10): "))
                # Servis katmanını çağırıyoruz
                service.creating_case(v_tur, v_sev, units)
                
                # İşlemi kaydediyoruz
                repo.save_unit_info(units) 
                
            except ValueError:
                print("! Hata: Seviye sayı olmalı.")
            
            input("\nDevam etmek için Enter'a basın...")

        # --- SEÇENEK 2: FİLO LİSTELEME ---
        elif secim == "2":
            print("\n--- 🚓 FİLO DURUM RAPORU ---")
            print(f"{'ID':<10} {'TÜR':<15} {'KONUM':<10} {'DURUM'}")
            print("-" * 50)
            for u in units:
                durum = "MÜSAİT" if u.availability else "MEŞGUL/HİZMET DIŞI"
                print(f"{u.unit_id:<10} {u.unit_type:<15} {u.current_location:<10} {durum}")
            
            input("\nDevam etmek için Enter'a basın...")

        # --- SEÇENEK 3: BAKIM / STATÜ ---
        elif secim == "3":
            # Senin yazdığın 'manage_unit_status' fonksiyonunu kullanıyoruz
            service.manage_unit_status(units)
            repo.save_unit_info(units)
            input("\nDevam etmek için Enter'a basın...")

        # --- SEÇENEK 4: YENİ ARAÇ EKLEME ---
        elif secim == "4":
            print("\n--- ➕ YENİ EKİP EKLEME ---")
            tur = input("Araç Türü (A: Ambulans / P: Polis / I: İtfaiye): ").upper()
            try:
                u_id = int(input("Araç ID (Örn: 101): "))
                loc = int(input("Başlangıç Konumu (0-20): "))
                
                yeni_arac = None
                if tur == "A":
                    yeni_arac = AmbulanceUnit(u_id, 100, True, 100, True, current_location=loc)
                elif tur == "P":
                    yeni_arac = PoliceUnit(u_id, 100, True, "Merkez", current_location=loc)
                elif tur == "I":
                    yeni_arac = FireFightingUnit(u_id, 100, True, 100, 100, current_location=loc)
                else:
                    print("! Geçersiz tür.")
                
                if yeni_arac:
                    units.append(yeni_arac)
                    repo.save_unit_info(units)
                    print(f"✅ {u_id} numaralı araç filoya eklendi.")
                    
            except ValueError:
                print("! Hata: ID ve Konum sayı olmalı.")
            
            input("\nDevam etmek için Enter'a basın...")

        # --- SEÇENEK 5: ARAÇ SİLME ---
        elif secim == "5":
            try:
                silinecek_id = int(input("Silinecek Araç ID: "))
                # Listeden bul ve sil (List Comprehension yöntemi)
                eski_len = len(units)
                units = [u for u in units if u.unit_id != silinecek_id]
                
                if len(units) < eski_len:
                    print(f"✅ {silinecek_id} silindi.")
                    # Veritabanını güncelle
                    repo.save_unit_info(units)
                    # Log dosyasından da temizle (Senin yazdığın fonksiyon)
                    repo.delete_unit_from_file(silinecek_id)
                else:
                    print("! Araç bulunamadı.")
            except ValueError:
                print("! Hata: Sayı giriniz.")
            
            input("\nDevam etmek için Enter'a basın...")

        # --- SEÇENEK 6: LOG OKUMA ---
        elif secim == "6":
            # Senin service.event_log_management fonksiyonunu çağırabiliriz
            # Ama basitlik olsun diye burada okuyalım
            if os.path.exists(repo.file_name):
                print("\n--- 📂 SON 10 VAKA KAYDI ---")
                with open(repo.file_name, "r", encoding="utf-8") as f:
                    # Son satırları göster
                    print(f.read())
            else:
                print("Henüz kayıt yok.")
            input("\nDevam etmek için Enter'a basın...")

        # --- ÇIKIŞ ---
        elif secim == "Q":
            print("Sistem kapatılıyor... İyi nöbetler.")
            break
        
        else:
            print("! Geçersiz seçim.")
            time.sleep(1)
            
if __name__ == "__main__":
    main()