import os
import time
from turtle import clearscreen
from app.modules.module_3.repository import EmergencyRepository
from app.modules.module_3.services import EmergencyService
from app.modules.module_3.implementations import AmbulanceUnit, PoliceUnit, FireFightingUnit

def main():
    
    print("\n"+"="*50)
    print("[SİSTEM] Sistem başlatılıyor...")
    print("[SİSTEM] Veritabanı bağlantısı kontrol ediliyor...")
    time.sleep(2)
    repository = EmergencyRepository()
    service = EmergencyService(repository)
    print("[SİSTEM] Veritabanı başarılı bir şekilde bağlandı")
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
        print(f"Aktif Araç Sayısı: {len(units)}")
        print("-" * 40)
        print(" [1] 🆘  ACİL İHBAR GİRİŞİ (Vaka Oluştur)")
        print(" [2] 🚓  CANLI FİLO DURUMU (Listele)")
        print(" [3] 🛠️  ARAÇ YÖNETİMİ (Bakım/Statü Değiştir)")
        print(" [4] ➕  YENİ EKİP EKLE (Envantere Kayıt)")
        print(" [5] 🗑️  ARAÇ SİL (Envanterden Düş)")
        print(" [6] 📂  LOG PANELİ")
        print(" [Q] ❌  ÇIKIŞ")
        print("-" * 40)
        
        text = input("👉 İşlem Seçiniz: ").upper()
        
        # Vaka Oluşturma
        if text == "1":
            print("\n--- 🆘 YENİ VAKA GİRİŞİ ---")
            print("Vaka Türleri: Yangın, Trafik Kazası, Kalp Krizi, Hırsızlık, Sel/Su Baskını")
            case_type = input("Olay Türü: ")
            
            try:
                severity = int(input("Ciddiyet Seviyesi (1-10): "))
                # Servis katmanını çağırır
                service.creating_case(case_type, severity, units)
                
                # İşlemi kaydeder
                repo.save_unit_info(units) 
                
            except ValueError:
                print("[HATA] Seviye sayı olmalı.")
            
            input("\nDevam etmek için Enter'a basın...")

        # Sistemdeki tüm araçları gösterir
        elif text == "2":
            print("\n--- 🚓 FİLO DURUM RAPORU ---")
            print(f"{'ID':<10} {'TÜR':<15} {'KONUM':<10} {'DURUM'}")
            print("-" * 50)
            for u in units:
                durum = "MÜSAİT" if u.availability else "MEŞGUL/HİZMET DIŞI"
                print(f"{u.unit_id:<10} {u.unit_type:<15} {u.current_location:<10} {durum}")
            
            input("\nDevam etmek için Enter'a basın...")

        # Sistemdeki araçları yönetir
        elif text == "3":
            service.manage_unit_status(units)
            repo.save_unit_info(units)
            input("\nDevam etmek için Enter'a basın...")

        # Sisteme yeni araç ekler
        elif text == "4":
            print("\n--- ➕ YENİ EKİP EKLEME ---")
            unit_type = input("Araç Türü (A: Ambulans / P: Polis / I: İtfaiye): ").upper()
            try:
                u_id = int(input("Araç ID (Örn: 101): "))
                location = int(input("Başlangıç Konumu (0-20): "))
                
                new_unit = None
                if unit_type == "A":
                    new_unit = AmbulanceUnit(u_id, 100, True, 100, True, current_location=location)
                elif unit_type == "P":
                    new_unit = PoliceUnit(u_id, 100, True, "Merkez", current_location=location)
                elif unit_type == "I":
                    new_unit = FireFightingUnit(u_id, 100, True, 100, 100, current_location=location)
                else:
                    print("[HATA] Geçersiz tür")
                
                if new_unit:
                    units.append(new_unit)
                    repo.save_unit_info(units)
                    print(f"✅ {u_id} numaralı araç filoya eklendi.")
                    
            except ValueError:
                print("[HATA] ID ve Konum sayı olmalı.")
            
            input("\nDevam etmek için Enter'a basın...")

        # Sistemden araç siler
        elif text == "5":
            try:
                deleted_id = int(input("Silinecek Araç ID: "))
                # Listeden bulur ve siler
                all_units_len = len(units)
                # Listedeki tüm araçları tarar ve silinmek istenen ID'ye sahip araç hariç diğerlerini yeni bir listeye aktararak o aracı listeden çıkarır
                units = [u for u in units if u.unit_id != deleted_id]
                
                if len(units) < all_units_len:
                    print(f"✅ {deleted_id} silindi.")
                    # Veritabanını günceller
                    repo.save_unit_info(units)
                    # Log dosyasından da temizler
                    repo.delete_unit_from_file(deleted_id)
                else:
                    print("[HATA] Araç bulunamadı")
            except ValueError:
                print("[HATA] Sayı giriniz.")
            
            input("\nDevam etmek için Enter'a basın...")

        # Sistem loglarını okuma
        elif text == "6":
            service.event_log_management()

        # Çıkış
        elif text == "Q":
            print("[SİSTEM] Sistem kapatılıyor... İyi nöbetler")
            break
        
        else:
            print("[HATA] Geçersiz seçim")
            time.sleep(1)
            
if __name__ == "__main__":
    main()