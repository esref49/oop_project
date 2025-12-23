import os
import random
import time
import numpy as np
from app.modules.module_3.base import Human
from app.modules.module_3.repository import EmergencyRepository
from app.modules.module_3.services import EmergencyService, HumanService, StructureService
from app.modules.module_3.implementations import (
    AmbulanceUnit, PoliceUnit, FireFightingUnit,
    Criminal, Victim,
    Hospital, PoliceStation, FireStation
)

def main():
    emergency_service = None
    human_service = None
    structure_service = None
    repository = None
    units = []
    people = []
    structures = []
    
    print("\n" + "="*60)
    print("🚨 AKILLI ACİL DURUM YÖNETİM SİSTEMİ 🚨")
    print("="*60)
    print("[SİSTEM] Sistem başlatılıyor...")
    time.sleep(1)
    
    # Repository oluştur
    repository = EmergencyRepository()
    print("[SİSTEM] Veritabanı bağlantısı başarılı")
    
    # Servisleri oluştur
    emergency_service = EmergencyService(repository)
    human_service = HumanService(repository)
    structure_service = StructureService(repository)
    
    print("[SİSTEM] Tüm servisler hazır")
    time.sleep(1)
    
    # Örnek veriler oluştur
    
    # Acil durum araçları
    units = [
        AmbulanceUnit(unit_id=101, fuel_level=79, is_enough_staff=True, medical_supply_level=45, is_sterilized=True),
        AmbulanceUnit(unit_id=102, fuel_level=33, is_enough_staff=True, medical_supply_level=88, is_sterilized=False),
        AmbulanceUnit(unit_id=103, fuel_level=47, is_enough_staff=True, medical_supply_level=93, is_sterilized=True),
        PoliceUnit(unit_id=201, fuel_level=55, is_enough_staff=True, patrol_area=[0,5], unit_specialty="Asayiş"),
        PoliceUnit(unit_id=202, fuel_level=56, is_enough_staff=True, patrol_area=[5,10], unit_specialty="PÖH"),
        PoliceUnit(unit_id=203, fuel_level=43, is_enough_staff=True, patrol_area=[10,15], unit_specialty="Trafik"),
        FireFightingUnit(unit_id=301, fuel_level=83, is_enough_staff=True, water_level=780, foam_level=239, max_water_level=3000, max_foam_level=600, max_fuel_level=100, ladder_length=45),
        FireFightingUnit(unit_id=302, fuel_level=95, is_enough_staff=True, water_level=330, foam_level=112, max_water_level=1000, max_foam_level=500, max_fuel_level=100, ladder_length=40)
    ]
    
    # İnsanlar
    people = [
        Criminal(id=12345678901, name="Ahmet", lastname="Yılmaz", age=35, blood_group="A Rh+", height=175, weight=80,is_alive=True, criminal_history=["Hırsızlık"], danger_level=7, is_caught=False, kill_count=0, injured_count=2),
        Criminal(id=23456789012, name="Mehmet", lastname="Kaya", age=42, blood_group="B Rh+", height=180, weight=85,is_alive=True, criminal_history=["Darp"], danger_level=5, is_caught=True, kill_count=0, injured_count=1),
        Victim(id=34567890123, name="Ayşe", lastname="Demir", age=28, blood_group="0 Rh+", height=165, weight=60,is_alive=True, degree_of_injury=8, the_person_who_injured="Bilinmiyor", cause_of_injury="Trafik Kazası"),
        Victim(id=45678901234, name="Fatma", lastname="Çelik", age=45, blood_group="AB Rh-", height=170, weight=65,is_alive=True, degree_of_injury=3, the_person_who_injured="Bilinmiyor", cause_of_injury="Kavga")
    ]
    
    # Yapılar
    structures = [
        Hospital(structure_id=1, name="Şehir Hastanesi", address="Merkez Mah.", capacity=100, current_occupancy=75,location=15, number_of_doctors=25, number_of_ambulances=8, specialized_units=["Acil", "KVC", "Travma"]),
        Hospital(structure_id=2, name="Acil Üniversite Hastanesi", address="Üniversite Cad.", capacity=50, current_occupancy=45,location=25, number_of_doctors=15, number_of_ambulances=5, specialized_units=["Acil", "Çocuk", "Nöroloji"]),
        PoliceStation(structure_id=3, name="Merkez Karakol", address="Merkez Sokak", capacity=30, current_occupancy=12,location=10, cell_count=20, number_of_officers=35, patrol_cars_count=8),
        PoliceStation(structure_id=4, name="İlçe Emniyet", address="İlçe Meydanı", capacity=20, current_occupancy=8,location=35, cell_count=15, number_of_officers=25, patrol_cars_count=5),
        FireStation(structure_id=5, name="Merkez İtfaiye", address="Ana Cad.", capacity=15, current_occupancy=10,location=5, number_of_engines=6, water_tank_capacity=50000, foam_reserve=10000),
        FireStation(structure_id=6, name="İlçe İtfaiye", address="Yan Sokak", capacity=10, current_occupancy=4,location=40, number_of_engines=4, water_tank_capacity=30000, foam_reserve=5000)
    ]
    
    # Yapıları veritabanına kaydeder
    for structure in structures:
        structure_service.register_structure(structure)
    
    # İnsanları veritabanına kaydeder
    for person in people:
        if isinstance(person, Criminal):
            human_service.register_criminal(person)
        elif isinstance(person, Victim):
            human_service.register_victim(person)
    
    print("[SİSTEM] Örnek veriler oluşturuldu")
    print(f"[SİSTEM] Araç Sayısı: {len(units)}")
    print(f"[SİSTEM] Kişi Sayısı: {len(people)}")
    print(f"[SİSTEM] Yapı Sayısı: {len(structures)}")
    print("="*60)
    time.sleep(1)
    
    while True:
        print("\n" + "="*60)
        print("🏢 ANA MENÜ - AKILLI ACİL DURUM YÖNETİM SİSTEMİ")
        print("="*60)
        print(" [1] 🆘  ACİL DURUM YÖNETİMİ (Vaka Oluştur)")
        print(" [2] 👤  İNSAN KAYIT YÖNETİMİ")
        print(" [3] 🏥  YAPI VE KAPASİTE YÖNETİMİ")
        print(" [4] 🚗  FİLO VE ARAÇ YÖNETİMİ")
        print(" [5] 📊  SİSTEM RAPORLARI VE İSTATİSTİKLER")
        print(" [6] 📂  LOG VE KAYIT YÖNETİMİ")
        print(" [Q] ❌  ÇIKIŞ")
        print("="*60)
        
        choice = input("👉 Seçiminiz: ").upper()
        
        # acil durum yönetimi
        if choice == "1":
            while True:
                print("\n" + "="*50)
                print("🚨 ACİL DURUM YÖNETİMİ")
                print("="*50)
                print(" [1] 🆘 Yeni Vaka Oluştur")
                print(" [2] 📍 En Yakın Birimi Bul")
                print(" [3] 🔙 Ana Menüye Dön")
                
                text = input("👉 Seçiminiz: ")
                
                if text == "1":
                    print("\n--- YENİ VAKA GİRİŞİ ---")
                    print("Vaka Türleri: Yangın, Trafik Kazası, Kalp Krizi, Hırsızlık, Sel/Su Baskını")
                    print("Rehine Krizi, Doğum, Bayılma, Kavga/Darp, Şüpheli Paket")
                    print("Kimyasal Sızıntı, Mahsur Kalma, Yaralanma, Zehirlenme")
                    
                    case_type = input("Olay Türü: ")
                    
                    try:
                        severity = int(input("Ciddiyet Seviyesi (1-10): "))
                        if severity < 1 or severity > 10:
                            print("[HATA] Ciddiyet 1-10 arasında olmalı!")
                            continue
                        
                        case_location = int(input("Olay Konumu (0-100): "))
                        if case_location < 0 or case_location > 100:
                            print("[HATA] Konum 0-100 arasında olmalı!")
                            continue
                        
                        print("\n" + "="*40)
                        print("Vaka bilgileri işleniyor...")
                        time.sleep(1)
                        
                        # vaka oluştur
                        emergency_service.creating_case(case_type, severity, units, case_location)
                        
                        # Veritabanına kaydet
                        repository.save_unit_info(units)
                        
                    except ValueError:
                        print("[HATA] Geçerli bir sayı girin!")
                    except Exception as e:
                        print(f"[HATA] Vaka oluşturulamadı: {e}")
                    
                    input("\nDevam etmek için Enter'a basın...")
                
                elif text == "2":
                    print("\n--- EN YAKIN BİRİM BULMA ---")
                    
                    try:
                        incident_location = int(input("Olay Konumu (0-100): "))
                        print("\nBirim Türleri: Ambulans, Polis, İtfaiye")
                        unit_type_input = input("İhtiyaç Duyulan Birim Türü: ")

                        # Tür dönüşümü
                        unit_type_map = {
                            "ambulans": "Ambulans",
                            "polis": "Polis", 
                            "itfaiye": "İtfaiye"
                        }
                        
                        unit_type = unit_type_map.get(unit_type_input.lower(), unit_type_input)
                        
                        # incident_location parametresini ekleyerek çağır
                        nearest = emergency_service.finding_the_nearest_unit(units, unit_type, incident_location)
                        if nearest:
                            print(f"\n✅ En yakın birim: {nearest.unit_id} - {nearest.unit_type}")
                            print(f"   Konum: {nearest.current_location} km")
                        else:
                            print(f"\n❌ {unit_type} türünde müsait birim bulunamadı!")

                    except ValueError as ve:
                        print(f"[HATA] Konum için geçerli bir sayı girin! {ve}")
                    except Exception as e:
                        print(f"[HATA] İşlem sırasında beklenmeyen bir hata oluştu: {e}")
                    
                    input("\nDevam etmek için Enter'a basın...")
                
                elif text == "3":
                    break
                else:
                    print("[HATA] Geçersiz seçim!")
        
        # kayı yönetimi
        elif choice == "2":
            while True:
                print("\n" + "="*50)
                print("👤 İNSAN KAYIT YÖNETİMİ")
                print("="*50)
                print(" [1] 👤 Vatandaş kaydet")
                print(" [2] 🚨 Suçlu Kaydı Oluştur")
                print(" [3] 🚑 Mağdur Kaydı Oluştur")
                print(" [4] 📋 Tüm Suçluları Listele")
                print(" [5] 📋 Tüm Mağdurları Listele")
                print(" [6] 🔍 TC ile Kişi Ara")
                print(" [7] ⚠️ Kritik Mağdurları Listele")
                print(" [8] 🔄 Suçlu Durumunu Güncelle")
                print(" [9] 📊 Kayıt İstatistikleri")
                print(" [Q] 🔙 Ana Menüye Dön")
                
                text = input("👉 Seçiminiz: ")
                
                if text == "1":
                    print("\n--- VATANDAŞ KAYDI ---")
                    try:
                        tc = input("TC Kimlik No (11 haneli): ")
                        if len(tc) != 11:
                            print("[HATA] TC 11 haneli olmalı!")
                            continue
                        else:
                            name = input("Ad: ")
                            lastname = input("Soyad: ")
                            age = int(input("Yaş: "))
                            blood_group = input("Kan Grubu: ")
                            height = int(input("Boy (cm): "))
                            weight = int(input("Kilo (kg): "))

                            human = Human(id=tc, name=name, lastname=lastname, age=age, blood_group=blood_group,
                                          height=height, weight=weight, is_alive=True)

                            if human_service.register_human(criminal):
                                people.append(human)
                                print(f"\n✅ {name} {lastname} başarıyla kaydedildi!")

                    except ValueError:
                        print("[HATA] Geçerli değerler girin!")
                    except Exception as e:
                        print(f"[HATA] Kayıt oluşturulamadı: {e}")
                    
                    input("\nDevam etmek için Enter'a basın...")

                elif text == "2":
                    print("\n--- YENİ SUÇLU KAYDI ---")
                    
                    try:
                        tc = input("TC Kimlik No (11 haneli): ")
                        if len(tc) != 11:
                            print("[HATA] TC 11 haneli olmalı!")
                            continue
                        
                        else:
                            name = input("Ad: ")
                            lastname = input("Soyad: ")
                            age = int(input("Yaş: "))
                            blood_group = input("Kan Grubu: ")
                            height = int(input("Boy (cm): "))
                            weight = int(input("Kilo (kg): "))
                            crime_type = input("Suç Türü: ")
                            danger_level = int(input("Tehlike Seviyesi (1-10): "))
                        
                            criminal = Criminal(id=tc, name=name, lastname=lastname, age=age, blood_group=blood_group,
                                          height=height, weight=weight, is_alive=True, criminal_history=[crime_type],
                                          danger_level=danger_level, is_caught=False, kill_count=0, injured_count=0)
                        
                            if human_service.register_criminal(criminal):
                                people.append(criminal)
                                print(f"\n✅ {name} {lastname} başarıyla kaydedildi!")
                        
                    except ValueError:
                        print("[HATA] Geçerli değerler girin!")
                    except Exception as e:
                        print(f"[HATA] Kayıt oluşturulamadı: {e}")
                    
                    input("\nDevam etmek için Enter'a basın...")
                
                elif text == "3":
                    print("\n--- YENİ MAĞDUR KAYDI ---")
                    
                    try:
                        tc = int(input("TC Kimlik No (11 haneli): "))
                        if len(str(tc)) != 11:
                            print("[HATA] TC 11 haneli olmalı!")
                            continue
                        
                        name = input("Ad: ")
                        lastname = input("Soyad: ")
                        age = int(input("Yaş: "))
                        blood_group = input("Kan Grubu: ")
                        height = int(input("Boy (cm): "))
                        weight = int(input("Kilo (kg): "))
                        degree_of_injury = int(input("Yaralanma Derecesi (1-10): "))
                        cause = input("Olay Nedeni: ")
                        who_injured = input("Yaralayan Kişi: ")
                        
                        victim = Victim(id=tc, name=name, lastname=lastname, age=age, blood_group=blood_group,
                                      height=height, weight=weight, is_alive=True, degree_of_injury=degree_of_injury,
                                      the_person_who_injured=who_injured, cause_of_injury=cause)
                        
                        if human_service.register_victim(victim):
                            people.append(victim)
                            print(f"\n✅ {name} {lastname} başarıyla kaydedildi!")
                        
                    except ValueError:
                        print("[HATA] Geçerli değerler girin!")
                    except Exception as e:
                        print(f"[HATA] Kayıt oluşturulamadı: {e}")
                    
                    input("\nDevam etmek için Enter'a basın...")
                
                elif text == "4":
                    human_service.list_all_criminals()
                    input("\nDevam etmek için Enter'a basın...")
                
                elif text == "5":
                    human_service.list_all_victims()
                    input("\nDevam etmek için Enter'a basın...")
                
                elif text == "6":
                    try:
                        tc = int(input("Aranacak TC Kimlik No: "))
                        person = human_service.find_person_by_id(tc)
                        
                        if person:
                            print(f"\n✅ Kişi bulundu:")
                            print(f"   Ad Soyad: {person.name} {person.lastname}")
                            
                            if isinstance(person, Criminal):
                                print(f"   Tür: Suçlu")
                                print(f"   Suç: {person.crime_type}")
                                print(f"   Tehlike: {person.danger_level}/10")
                                print(f"   Yakalandı mı: {'Evet' if person.is_caught else 'Hayır'}")
                            elif isinstance(person, Victim):
                                print(f"   Tür: Mağdur")
                                print(f"   Yaralanma: {person.degree_of_injury}/10")
                                print(f"   Hayatta mı: {'Evet' if person.is_alive else 'Hayır'}")
                                print(f"   Olay Nedeni: {person.cause_of_injury}")
                        
                    except ValueError:
                        print("[HATA] Geçerli TC girin!")
                    
                    input("\nDevam etmek için Enter'a basın...")
                
                elif text == "7":
                    print("\n--- KRİTİK MAĞDURLAR ---")
                    try:
                        min_severity = int(input("Minimum Yaralanma Derecesi (varsayılan: 5): ") or "5")
                        critical = human_service.filter_critical_victims(min_severity)
                        
                        if critical:
                            print(f"\n📋 {len(critical)} kritik mağdur bulundu:")
                            for victim in critical:
                                print(f"   {victim.name} {victim.lastname} - Derece: {victim.degree_of_injury}/10")
                        else:
                            print("\nℹ️ Kritik mağdur bulunamadı.")
                            
                    except ValueError:
                        print("[HATA] Geçerli sayı girin!")
                    
                    input("\nDevam etmek için Enter'a basın...")
                
                elif text == "8":
                    print("\n--- SUÇLU DURUM GÜNCELLEME ---")
                    
                    try:
                        tc = int(input("Suçlu TC Kimlik No: "))
                        is_caught_input = input("Yakalandı mı? (E/H): ").upper()
                        is_caught = True if is_caught_input == "E" else False
                        
                        if human_service.update_criminal_status(tc, is_caught):
                            print(f"\n✅ {tc} TC'li suçlu durumu güncellendi!")
                            print(f"   Yeni durum: {'Yakalandı' if is_caught else 'Firarda'}")
                        else:
                            print(f"\n❌ {tc} TC'li suçlu bulunamadı!")
                            
                    except ValueError:
                        print("[HATA] Geçerli TC girin!")
                    
                    input("\nDevam etmek için Enter'a basın...")
                
                elif text == "9":
                    print("\n--- KAYIT İSTATİSTİKLERİ ---")
                    total = human_service.get_registry_count()
                    
                    criminals = sum(1 for p in people if isinstance(p, Criminal))
                    victims = sum(1 for p in people if isinstance(p, Victim))
                    
                    caught_criminals = sum(1 for p in people if isinstance(p, Criminal) and p.is_caught)
                    critical_victims = sum(1 for p in people if isinstance(p, Victim) and p.degree_of_injury >= 5)
                    
                    print(f"📊 Toplam Kayıt: {total}")
                    print(f"🚨 Suçlu Sayısı: {criminals} (Yakalanan: {caught_criminals})")
                    print(f"🚑 Mağdur Sayısı: {victims} (Kritik: {critical_victims})")
                    print(f"👥 Sistemdeki Toplam Kişi: {len(people)}")
                    
                    input("\nDevam etmek için Enter'a basın...")
                
                elif text == "Q":
                    break
                else:
                    print("[HATA] Geçersiz seçim!")
        
        # yapı yönetimi
        elif choice == "3":
            while True:
                print("\n" + "="*50)
                print("🏥 YAPI VE KAPASİTE YÖNETİMİ")
                print("="*50)
                print(" [1] 📋 Tüm Yapıları Listele")
                print(" [2] 📊 Kapasite İstatistikleri")
                print(" [3] 🔧 Kapasite Yönetimi")
                print(" [4] 🚑 En Yakın Hastane Bul")
                print(" [5] 🚓 En Yakın Karakol Bul")
                print(" [6] 🚒 En Yakın İtfaiye Bul")
                print(" [7] 🔙 Ana Menüye Dön")
                
                text= input("👉 Seçiminiz: ")
                
                if text == "1":
                    structure_service.list_all_structures()
                    input("\nDevam etmek için Enter'a basın...")
                
                elif text == "2":
                    structure_service.show_statistics()
                    input("\nDevam etmek için Enter'a basın...")
                
                elif text == "3":
                    structure_service.manage_structure_capacity()
                    input("\nDevam etmek için Enter'a basın...")
                
                elif text == "4":
                    print("\n--- EN YAKIN HASTANE BULMA ---")
                    
                    try:
                        location = int(input("Hasta Konumu (0-100): "))
                        nearest = structure_service.dispatch_nearest_unit(location, Hospital)
                        
                        if nearest:
                            print(f"\n✅ En yakın hastane: {nearest.name}")
                            print(f"   Konum: {nearest.location} km")
                            print(f"   Boş yatak: {nearest.capacity - nearest.current_occupancy}")
                        else:
                            print("\n❌ Uygun hastane bulunamadı!")
                            
                    except ValueError:
                        print("[HATA] Geçerli konum girin!")
                    
                    input("\nDevam etmek için Enter'a basın...")
                
                elif text == "5":
                    print("\n--- EN YAKIN KARAKOL BULMA ---")
                    
                    try:
                        location = int(input("Olay Konumu (0-100): "))
                        nearest = structure_service.dispatch_nearest_unit(location, PoliceStation)
                        
                        if nearest:
                            print(f"\n✅ En yakın karakol: {nearest.name}")
                            print(f"   Konum: {nearest.location} km")
                            print(f"   Boş kapasite: {nearest.capacity - nearest.current_occupancy}")
                        else:
                            print("\n❌ Uygun karakol bulunamadı!")
                            
                    except ValueError:
                        print("[HATA] Geçerli konum girin!")
                    
                    input("\nDevam etmek için Enter'a basın...")
                
                elif text == "6":
                    print("\n--- EN YAKIN İTFAİYE BULMA ---")
                    
                    try:
                        location = int(input("Yangın Konumu (0-100): "))
                        nearest = structure_service.dispatch_nearest_unit(location, FireStation)
                        
                        if nearest:
                            print(f"\n✅ En yakın itfaiye: {nearest.name}")
                            print(f"   Konum: {nearest.location} km")
                            print(f"   Boş kapasite: {nearest.capacity - nearest.current_occupancy}")
                        else:
                            print("\n❌ Uygun itfaiye bulunamadı!")
                            
                    except ValueError:
                        print("[HATA] Geçerli konum girin!")
                    
                    input("\nDevam etmek için Enter'a basın...")
                
                elif text == "7":
                    break
                else:
                    print("[HATA] Geçersiz seçim!")
        
        # araç yönetimi
        elif choice == "4":
            while True:
                print("\n" + "="*50)
                print("🚗 FİLO VE ARAÇ YÖNETİMİ")
                print("="*50)
                print(" [1] 📋 Tüm Araçları Listele")
                print(" [2] 🔧 Araç Statü Yönetimi")
                print(" [3] ⛽ Yakıt Doldur")
                print(" [4] 🆕 Yeni Araç Ekle")
                print(" [5] 🗑️  Araç Sil")
                print(" [6] 🚨 Araç Kazası Bildir")
                print(" [7] 🔙 Ana Menüye Dön")
                
                text = input("👉 Seçiminiz: ")
                
                if text == "1":
                    print("\n--- TÜM ARAÇLAR ---")
                    print(f"{'ID':<8} {'TÜR':<15} {'KONUM':<10} {'DURUM':<15} {'YAKIT':<10}")
                    print("-" * 60)
                    
                    for unit in units:
                        status = "🟢 MÜSAİT" if unit.availability else "🔴 MEŞGUL"
                        fuel_status = f"{unit.fuel_level}%"
                        
                        print(f"{unit.unit_id:<8} {unit.unit_type:<15} {unit.current_location:<10} {status:<15} {fuel_status:<10}")
                    
                    print(f"\nToplam araç sayısı: {len(units)}")
                    
                    input("\nDevam etmek için Enter'a basın...")
                
                elif text == "2":
                    emergency_service.manage_unit_status(units)
                    repository.save_unit_info(units)
                    input("\nDevam etmek için Enter'a basın...")
                
                elif text == "3":
                    print("\n--- YAKIT DOLDURMA ---")
                    
                    try:
                        unit_id = int(input("Araç ID: "))
                        unit = next((u for u in units if u.unit_id == unit_id), None)
                        
                        if unit:
                            unit.refill_tank()
                            repository.save_unit_info(units)
                            print(f"\n✅ {unit_id} ID'li aracın yakıtı dolduruldu!")
                        else:
                            print(f"\n❌ {unit_id} ID'li araç bulunamadı!")
                            
                    except ValueError:
                        print("[HATA] Geçerli ID girin!")
                    
                    input("\nDevam etmek için Enter'a basın...")
                
                elif text == "4":
                    print("\n--- YENİ ARAÇ EKLEME ---")
                    
                    print("Araç Türleri:")
                    print(" 1) Ambulans")
                    print(" 2) Polis Aracı")
                    print(" 3) İtfaiye Aracı")
                    
                    try:
                        type_choice = input("Araç Türü Seçin (1-3): ")
                        unit_id = int(input("Araç ID: "))
                        
                        # ID kontrolü
                        if any(u.unit_id == unit_id for u in units):
                            print(f"\n❌ {unit_id} ID'li araç zaten var!")
                            input("\nDevam etmek için Enter'a basın...")
                            continue
                        
                        location = int(input("Başlangıç Konumu (0-100): "))
                        
                        new_unit = None
                        if type_choice == "1":
                            new_unit = AmbulanceUnit(unit_id=unit_id, fuel_level=100, is_enough_staff=True, 
                                                    medical_supply_level=100, is_sterilized=True, current_location=location)
                        elif type_choice == "2":
                            new_unit = PoliceUnit(unit_id=unit_id, fuel_level=100, is_enough_staff=True,
                                                 patrol_area=[0, 20], unit_specialty="Genel", current_location=location)
                        elif type_choice == "3":
                            new_unit = FireFightingUnit(unit_id=unit_id, fuel_level=100, is_enough_staff=True,
                                                       water_level=1000, foam_level=500, max_water_level=2000,
                                                       max_foam_level=1000, max_fuel_level=100, ladder_length=30,
                                                       current_location=location)
                        else:
                            print("\n❌ Geçersiz araç türü!")
                            input("\nDevam etmek için Enter'a basın...")
                            continue
                        
                        units.append(new_unit)
                        repository.save_unit_info(units)
                        print(f"\n✅ {unit_id} ID'li yeni araç başarıyla eklendi!")
                        
                    except ValueError:
                        print("[HATA] Geçerli değerler girin!")
                    
                    input("\nDevam etmek için Enter'a basın...")
                
                elif text == "5":
                    print("\n--- ARAÇ SİLME ---")
                    
                    try:
                        unit_id = int(input("Silinecek Araç ID: "))
                        initial_count = len(units)
                        
                        # Araçları filtrele
                        units = [u for u in units if u.unit_id != unit_id]
                        
                        if len(units) < initial_count:
                            repository.save_unit_info(units)
                            print(f"\n✅ {unit_id} ID'li araç başarıyla silindi!")
                        else:
                            print(f"\n❌ {unit_id} ID'li araç bulunamadı!")
                            
                    except ValueError:
                        print("[HATA] Geçerli ID girin!")
                    
                    input("\nDevam etmek için Enter'a basın...")
                elif text == "6":
                    print("\n--- ARAÇ KAZASI BİLDİRİMİ ---")

                    try:
                        unit_id = int(input("Kazaya Karışan Araç ID: "))
                        unit = next((u for u in units if u.unit_id == unit_id), None)
                        
                        if unit:
                            print("\nKaza Şiddeti:")
                            print(" 1) Hafif Hasar (Göreve devam edebilir)")
                            print(" 2) Ağır Hasar (Hizmet dışı)")
                            
                            # Kullanıcıdan geçerli bir giriş alana kadar döngü
                            severity = None
                            while True:
                                try:
                                    severity_input = input("Şiddet Seviyesi (1-2): ")
                                    severity = int(severity_input)
                                    
                                    if severity == 1 or severity == 2:
                                        unit.report_accident(severity_level=severity)
                                        repository.save_unit_info(units)
                                        print(f"\n✅ {unit_id} ID'li aracın kaza raporu sisteme işlendi!")
                                        break  # Geçerli giriş, döngüden çık
                                    else:
                                        print("[HATA] Lütfen sadece 1 veya 2 giriniz!")
                                        # Geçersiz seçimde report_accident çağırma ve kayıt yapma
                                except ValueError:
                                    print("[HATA] Geçerli bir sayı giriniz! (1 veya 2)")
                                    # Geçersiz girişte report_accident çağırma ve kayıt yapma
                        else:
                            print(f"\n❌ {unit_id} ID'li araç bulunamadı!")
                            
                    except ValueError:
                        print("[HATA] Araç ID için geçerli bir sayı girin!")

                    input("\nDevam etmek için Enter'a basın...")
                
                elif text == "7":
                    break
                else:
                    print("[HATA] Geçersiz seçim!")
        
        # sitemin istatistikleri
        elif choice == "5":
            print("\n" + "="*50)
            print("📊 SİSTEM RAPORLARI VE İSTATİSTİKLER")
            print("="*50)
            
            print(f"🚗 TOPLAM ARAÇ SAYISI: {len(units)}")
            ambulances = sum(1 for u in units if isinstance(u, AmbulanceUnit))
            police = sum(1 for u in units if isinstance(u, PoliceUnit))
            fire = sum(1 for u in units if isinstance(u, FireFightingUnit))
            print(f"   🚑 Ambulans: {ambulances}")
            print(f"   🚓 Polis: {police}")
            print(f"   🚒 İtfaiye: {fire}")
            
            available = sum(1 for u in units if u.availability)
            busy = len(units) - available
            print(f"   ✅ Müsait: {available}")
            print(f"   ❌ Meşgul/Hizmet Dışı: {busy}")
            
            print(f"\n👥 TOPLAM KİŞİ SAYISI: {len(people)}")
            criminals = sum(1 for p in people if isinstance(p, Criminal))
            victims = sum(1 for p in people if isinstance(p, Victim))
            print(f"   🚨 Suçlu: {criminals}")
            print(f"   🚑 Mağdur: {victims}")
            
            print(f"\n🏢 TOPLAM YAPI SAYISI: {len(structures)}")
            hospitals = sum(1 for s in structures if isinstance(s, Hospital))
            police_stations = sum(1 for s in structures if isinstance(s, PoliceStation))
            fire_stations = sum(1 for s in structures if isinstance(s, FireStation))
            print(f"   🏥 Hastane: {hospitals}")
            print(f"   🚓 Karakol: {police_stations}")
            print(f"   🚒 İtfaiye: {fire_stations}")
            
            total_capacity = sum(s.capacity for s in structures)
            total_occupancy = sum(s.current_occupancy for s in structures)
            occupancy_rate = (total_occupancy / total_capacity * 100) if total_capacity > 0 else 0
            print(f"\n📈 KAPASİTE DURUMU:")
            print(f"   Toplam Kapasite: {total_capacity}")
            print(f"   Toplam Doluluk: {total_occupancy}")
            print(f"   Doluluk Oranı: %{occupancy_rate:.1f}")
            
            if occupancy_rate > 80:
                print("[UYARI] Sistem kapasitesi kritik seviyede!")
            
            input("\nDevam etmek için Enter'a basın...")
        
        # veritabanı yönetimi
        elif choice == "6":
            emergency_service.event_log_management()
        
        # çık
        elif choice == "Q":
            print("\n" + "="*60)
            print("[SİSTEM] Sistem kapatılıyor...")
            print("[SİSTEM] Tüm kayıtlar kaydediliyor...")
            time.sleep(1)
            repository.save_unit_info(units)
            print("[SİSTEM] İyi nöbetler! 👮‍♂️🚑🚒")
            print("="*60)
            break
        
        else:
            print("[HATA] Geçersiz seçim!")
            time.sleep(1)

if __name__ == "__main__":
    main()