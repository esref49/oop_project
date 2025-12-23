import time

from app.modules.module_2.implementations import (
     ElectricityMeter, WaterMeter, GasMeter
)


from app.modules.module_3.implementations import (
    AmbulanceUnit, PoliceUnit, FireFightingUnit,
    Criminal, Victim,
    Hospital, PoliceStation, FireStation
)

from app.modules.module_4.implementations import (
    GidaYardimi, BarinmaDestegi, EgitimDestegi
)


def run_demo():
    while True:
        print("\n" + "="*60)
        print("🚨 AKILLI ACİL DURUM YÖNETİM SİSTEMİ - ANA MENÜ")
        print("="*60)
        print("📚 PROJE MODÜL SEÇİCİ")
        print("-"*60)
        
        print("\n📦 MEVCUT MODÜLLER:")
        print(" [2] 🏙️ Modül 2 - Akıllı Şehir Altyapı Sistemi")
        print(" [3] 🚨 Modül 3 - Akıllı Acil Durum Yönetim Sistemi")
        print(" [4] 📈 Modül 4 - Sosyal Hizmetler Modülü")
        print(" [Q] ❌ Çıkış")
        print("-"*60)
        
        choice = input("👉 Seçiminiz (1-4, Q): ").upper()

        #Modül 2           
        if choice == "2":
            print("\n" + "="*40)
            print("🏙️ MODÜL 2 - AKILLI ŞEHİR ALTYAPI SİSTEMİ")
            print("="*40)
            
            try:
                from app.modules.module_2.demo import run_demo as run_module_2_demo
                run_module_2_demo()
            except ImportError as e:
                print(f"[HATA] Modül 2 demo'su yüklenemedi: {e}")
            
            input("\nDevam etmek için Enter'a basın...")

        # Modül 3   
        elif choice == "3":
            print("\n" + "="*40)
            print("🚨 MODÜL 3 - AKILLI ACİL DURUM YÖNETİM SİSTEMİ")
            print("="*40)
                        
            try:
                from app.modules.module_3.demo import main as run_module_3_demo
                run_module_3_demo()
            except ImportError as e:
                print(f"[HATA] Modül 3 demo'su yüklenemedi: {e}")

        # Modül 4     
        elif choice == "4":
            print("\n" + "="*40)
            print("📈 MODÜL 4 - ÖĞRENCİ 4 PROJESİ")
            print("="*40)
            
            try:
                from app.modules.module_4.demo import main as run_module_4_demo
                run_module_4_demo()
            except ImportError as e:
                print(f"[HATA] Modül 4 demo'su yüklenemedi: {e}")

            input("\nDevam etmek için Enter'a basın...")        
            
        elif choice == "Q":
            print("\n" + "="*40)
            print("👋 Sistemden çıkılıyor...")
            print("İyi çalışmalar!")
            print("="*40)
            break
            
        else:
            print("[HATA] Geçersiz seçim! Lütfen 1-4 arası bir sayı veya Q girin.")
            time.sleep(1)

if __name__ == "__main__":
    run_demo()