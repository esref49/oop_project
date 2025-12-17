# app/modules/module_3/implementations.py
import time
from app.modules.module_3.base import EmergencyUnit
import numpy as np

# --- Entities --- 
# --- Ambulance Sınıfı ---
class AmbulanceUnit(EmergencyUnit):

    def __init__(self, unit_id, fuel_level, is_enough_staff, medical_supply_level, is_sterilized, 
                 unit_type = "Ambulans", current_location = np.random.randint(20), availability = True, is_siren_on = False, is_it_on_duty = False):
        
        # Üst sınıfın (EmergencyUnit) özelliklerini miras alarak başlatır
        super().__init__(unit_id, unit_type, current_location, availability, fuel_level, is_enough_staff, is_siren_on, is_it_on_duty)
        
        # Ambulansa özgü (tıbbi malzeme, sterilizasyon) özellikleri tanımlar
        self.medical_supply_level = medical_supply_level
        self.is_sterilized = is_sterilized

        # Aracın teknik arıza durumu ve müsaitlik başlangıcı
        self.is_broken = False
        self.availability = True

    def update_location(self, new_location):
        # Aracın mevcut konumunu yeni gelen veriyle günceller
        self.current_location = new_location
        print(f"[+] Ambulansın konumu güncellendi: {self.current_location}")
    
    def open_siren(self):
        # Sadece araç görev başındaysa sirenin açılmasına izin verir
        if self.is_it_on_duty:
            self.is_siren_on = True
            print("[+] Sirenler açıldı")
        else:
            print("[-] Araç görevde olmadığı için siren açılamaz.")
    
    def report_location(self):
        # Aracın anlık konumunu ekrana basar
        print(f"[+] Ambulansın konumu: {self.current_location}")

    def report_fault(self, faulty_part=None, faulty_level=None):
        """
        Araçtaki arızaları değerlendirir.
        """
        critical_parts = ["motor", "tekerlek", "gövde", "navigasyon", "tıbbi cihaz"]
        
        # Parça ismini küçük harfe çevirip kritik parça listesinde olup olmadığını kontrol eder (None kontrolü eklendi)
        if faulty_part and faulty_part.lower() in critical_parts and faulty_level == 2:
            self.is_broken = True
            print(f"[-] Kritik Arıza: {faulty_part}! Araç hizmet dışı.")
        
        # Hafif arıza (seviye 1) durumunda sadece bilgilendirme yapar, aracı durdurmaz
        elif faulty_part and faulty_part.lower() in critical_parts and faulty_level == 1:
            print(f"[!] Hafif Arıza: {faulty_part}. Göreve devam edebilir.")
            self.is_broken = False 

        # Herhangi bir arıza girilmemişse aracı sağlam olarak işaretler
        elif faulty_part is None and faulty_level is None:
            self.is_broken = False
            print("[+] Arıza yok, araç sağlam.")

        else:
            print("[-] Tanımsız arıza durumu.")

    def determine_availability(self):
        """
        Aracın genel durumuna bakarak müsaitliğini belirler.
        """
        # Sterilizasyon yoksa, malzeme azsa, personel eksikse veya araç bozuksa müsait değildir
        if not self.is_sterilized or self.medical_supply_level < 30 or self.is_enough_staff == False or self.is_broken:
            self.availability = False
            print("[-] Araç operasyonel eksiklikler nedeniyle müsait değil.")
        # Araç zaten görevdeyse müsait değildir
        elif self.is_it_on_duty:
            self.availability = False
            print("[-] Araç şu an görevde.")
        # Hiçbir sorun yoksa araç göreve hazırdır
        else:
            self.availability = True
            print("[+] Araç göreve hazır.")
        

    def report_status(self):
        # Önce güncel müsaitlik durumunu hesaplar
        self.determine_availability()
        # Aracın tüm özelliklerini detaylı bir rapor halinde yazdırır
        print(f"Araç Id: {self.unit_id} - Araç Türü: {self.unit_type}" )
        print(f"Müsaitlik: {self.availability}")
        print(F"Mecvut konumu: {self.current_location}")
        print(f"Benzin Seviyesi: {self.fuel_level}")
        print(f"Tıbbi malzeme seviyesi: {self.medical_supply_level}")
        print(f"Görevde mi: {self.is_it_on_duty}")
        print(f"Siren açık mı: {self.is_siren_on}")
        print(f"Steril mi: {self.is_sterilized}")
        print(f"Yeterli personel var mı: {self.is_enough_staff}")


# --- Police Sınıfı ---
class PoliceUnit(EmergencyUnit):
    def __init__(self, unit_id, fuel_level, is_enough_staff, patrol_area,  prisoner_count = 0, unit_specialty = "Asayiş",
                 unit_type = "Polis", current_location = np.random.randint(20), availability = True, is_siren_on = False, is_it_on_duty = False,):
        
        # Üst sınıf özelliklerini miras alır
        super().__init__(unit_id, unit_type, current_location, availability, fuel_level, is_enough_staff, is_siren_on, is_it_on_duty)
   
        # Polise özgü (tutuklu sayısı, devriye bölgesi, uzmanlık) özellikleri ayarlar
        self.prisoner_count = prisoner_count
        self.patrol_area = patrol_area
        self.unit_specialty = unit_specialty # Örn: "Asayiş", "Trafik"

        self.is_broken = False
        self.availability = True
        self.gbt_check_count = 0 # GBT sayacını başlatır

    def update_location(self, new_location):
        # Konum güncellemesi yapar
        self.current_location = new_location
        print(f"[+] Polis aracının konumu güncellendi: {self.current_location}")
    
    def open_siren(self):
        # Görevdeyse sireni açar
        if self.is_it_on_duty:
            self.is_siren_on = True
            print("[+] Sirenler açıldı")
        else:
            print("[-] Araç görevde olmadığı için siren açılamaz.")
    
    def report_location(self):
        # Mevcut konumu raporlar
        print(f"[+] Polis aracının konumu: {self.current_location}")

    def report_fault(self, faulty_part=None, faulty_level=None):
        """
        Araçtaki arızaları değerlendirir.
        """
        critical_parts = ["motor", "tekerlek", "gövde", "navigasyon", "tıbbi cihaz"]
        
        # Kritik parçalarda seviye 2 hasar varsa aracı bozuk işaretler (None kontrolü ile)
        if faulty_part and faulty_part.lower() in critical_parts and faulty_level == 2:
            self.is_broken = True
            print(f"[-] Kritik Arıza: {faulty_part}! Araç hizmet dışı.")
        
        # Hafif hasarda sadece bilgi verir
        elif faulty_part and faulty_part.lower() in critical_parts and faulty_level == 1:
            print(f"[!] Hafif Arıza: {faulty_part}. Göreve devam edebilir.")
            self.is_broken = False

        # Arıza yoksa sağlam işaretler
        elif faulty_part is None and faulty_level is None:
            self.is_broken = False
            print("[+] Arıza yok, araç sağlam.")

        else:
            print("[-] Tanımsız arıza durumu.")

    def determine_availability(self):
        """
        Aracın genel durumuna bakarak müsaitliğini belirler.
        """
        # Personel yoksa, araç bozuksa veya içinde tutuklu varsa müsait değildir
        if self.is_enough_staff == False or self.is_broken or self.prisoner_count > 0:
            self.availability = False
            print("[-] Araç operasyonel eksiklikler veya tutuklu nedeniyle müsait değil.")
        # Araç görevdeyse müsait değildir
        elif self.is_it_on_duty:
            self.availability = False
            print("[-] Araç şu an görevde.")
        else:
            self.availability = True
            print("[+] Araç göreve hazır.")
        
    def call_for_backup(self, reason):
        # Acil durumlarda destek çağrısı ve konum bilgisini basar
        print(f"[SOS] {self.unit_id} kodlu ekip ACİL DESTEK istiyor!")
        print(f"      Konum: {self.current_location}")
        print(f"      Sebep: {reason}")

    def issue_traffic_ticket(self):
        # Kullanıcıdan plaka ve ceza türü bilgisini alır
        plate_number = input("Plaka giriniz: ")
        type_of_punishment = input("Ceza türünü seçiniz: (Hız/Emniyet Kemeri/Ehliyet/Alkol)")

        # Sadece 'Trafik' biriminin ceza yazmasına izin verir
        if self.unit_specialty == "Trafik":
            # Ceza türüne göre tutarı belirleyip ekrana yazar
            if type_of_punishment == "Hız":
                print(f"{plate_number} plakalı araca hız aşımı gerekçesiyle 4443 TL ceza kesilmiştir.")
            elif type_of_punishment == "Eminiyet Kemeri":
                print(f"{plate_number} plakalı araca emniyet kemeri takmadığı gerekçesiyle 1367 TL ceza kesilmiştir.")
            elif type_of_punishment == "Ehliyet":
                print(f"{plate_number} plakalı araca ehliyet bulundurmadığı gerekçesiyle 6443 TL ceza kesilmiştir.")
            elif type_of_punishment == "Alkol":
                print(f"{plate_number} plakalı araca alkollü araç kullanma gerekçesiyle 9268 TL ceza kesilmiştir.")
        else:
            print("[-] Bu birimin trafik cezası kesme yetkisi bulunmamaktadır.")

    def perform_gbt_control(self):
        # Kullanıcıdan TC alır ve GBT sayacını artırır
        gbt_number = input("TC giriniz: ")
        self.gbt_check_count += 1

        # Rastgele bir şansla kişinin suçlu olup olmadığını belirler
        is_criminal = np.random.choice([0, 1, 0, 0, 1, 0])

        if is_criminal == 1:
            print(f"[!] Bu kişinin aranması mevcuttur. Hemen yakalayın!")
        else:
            print("[+] Kişinin herhangi bir aranması yoktur.")


    def report_status(self):
        # Durumu güncelle ve tüm bilgileri raporla
        self.determine_availability()
        print(f"Araç Id: {self.unit_id} - Araç Türü: {self.unit_type}" )
        print(f"Müsaitlik: {self.availability}")
        print(F"Mecvut konumu: {self.current_location}")
        print(f"Benzin Seviyesi: {self.fuel_level}")
        print(f"Araçta bulunan tutuklu sayısı: {self.prisoner_count}")
        print(f"Görevde mi: {self.is_it_on_duty}")
        print(f"Siren açık mı: {self.is_siren_on}")
        print(f"Birim Uzmanlığı: {self.unit_specialty}")
        print(f"Yeterli personel var mı: {self.is_enough_staff}")
        print(f"Görevli bulunduğu bölge: {self.patrol_area}")
        print(f"Yaptığı GBT kontrol sayısı: {self.gbt_check_count}")


# --- İtfaye Sınıfı ---
class FireFightingUnit(EmergencyUnit):
    def __init__(self, unit_id, fuel_level, is_enough_staff, water_level, foam_level, ladder_length = 20,
                 unit_type = "İtfaye", current_location = np.random.randint(20), availability = True, is_siren_on = False, is_it_on_duty = False):
        
        # Üst sınıfın (EmergencyUnit) özelliklerini miras alarak başlatır
        super().__init__(unit_id, unit_type, current_location, availability, fuel_level, is_enough_staff, is_siren_on, is_it_on_duty)

        self.water_level = water_level
        self.foam_level = foam_level
        self.ladder_length = ladder_length

        # Aracın teknik arıza durumu ve müsaitlik başlangıcı
        self.is_broken = False
        self.availability = True

    def update_location(self, new_location):
        # Aracın mevcut konumunu yeni gelen veriyle günceller
        self.current_location = new_location
        print(f"[+] Ambulansın konumu güncellendi: {self.current_location}")
    
    def open_siren(self):
        # Sadece araç görev başındaysa sirenin açılmasına izin verir
        if self.is_it_on_duty:
            self.is_siren_on = True
            print("[+] Sirenler açıldı")
        else:
            print("[-] Araç görevde olmadığı için siren açılamaz.")
    
    def report_location(self):
        # Aracın anlık konumunu ekrana basar
        print(f"[+] İtfaye aracının konumu: {self.current_location}")

    def report_fault(self, faulty_part=None, faulty_level=None):
        """
        Araçtaki arızaları değerlendirir.
        """
        critical_parts = ["motor", "tekerlek", "gövde", "navigasyon", "merdiven", "pompa"]
        
        # Parça ismini küçük harfe çevirip kritik parça listesinde olup olmadığını kontrol eder (None kontrolü eklendi)
        if faulty_part and faulty_part.lower() in critical_parts and faulty_level == 2:
            self.is_broken = True
            print(f"[-] Kritik Arıza: {faulty_part}! Araç hizmet dışı.")
        
        # Hafif arıza (seviye 1) durumunda sadece bilgilendirme yapar, aracı durdurmaz
        elif faulty_part and faulty_part.lower() in critical_parts and faulty_level == 1:
            print(f"[!] Hafif Arıza: {faulty_part}. Göreve devam edebilir.")
            self.is_broken = False 

        # Herhangi bir arıza girilmemişse aracı sağlam olarak işaretler
        elif faulty_part is None and faulty_level is None:
            self.is_broken = False
            print("[+] Arıza yok, araç sağlam.")

        else:
            print("[-] Tanımsız arıza durumu.")

    def determine_availability(self):
        """
        Aracın genel durumuna bakarak müsaitliğini belirler.
        """
        # Sterilizasyon yoksa, malzeme azsa, personel eksikse veya araç bozuksa müsait değildir
        if self.fuel_level < 20 or self.foam_level < 10 or self.water_level < 20 or self.is_enough_staff == False or self.is_broken:
            self.availability = False
            print("[-] Araç operasyonel eksiklikler nedeniyle müsait değil.")
        # Araç zaten görevdeyse müsait değildir
        elif self.is_it_on_duty:
            self.availability = False
            print("[-] Araç şu an görevde.")
        # Hiçbir sorun yoksa araç göreve hazırdır
        else:
            self.availability = True
            print("[+] Araç göreve hazır.")

    def refill_tank(self):
        max_water = 100
        max_foam = 100

        # Eğer zaten doluysa işlem yapma
        if self.water_level == max_water and self.foam_level == max_foam:
            print("[!] Depolar zaten tamamen dolu.")
            return

        print(f"[+] İstasyona yanaşıldı. Dolum işlemi başlıyor... (Şu anki Su: {self.water_level} lt)")
        
        time.sleep(1)
        print("Dolum durumu: %25")
        time.sleep(1)
        print("Dolum durumu: %50")
        time.sleep(1)
        print("Dolum durumu: %75")
        time.sleep(1)
        print("Dolum durumu: %100")
        
        # Değerleri güncelle
        self.water_level = max_water
        self.foam_level = max_foam
        self.availability = True # Eğer su bittiği için False olduysa, şimdi True yap
        
        print(f"[+] Dolum tamamlandı! (Su: {self.water_level} lt - Köpük: {self.foam_level} lt)")

    def report_status(self):
        # Önce güncel müsaitlik durumunu hesaplar
        self.determine_availability()
        # Aracın tüm özelliklerini detaylı bir rapor halinde yazdırır
        print(f"Araç Id: {self.unit_id} - Araç Türü: {self.unit_type}" )
        print(f"Müsaitlik: {self.availability}")
        print(F"Mecvut konumu: {self.current_location}")
        print(f"Benzin Seviyesi: {self.fuel_level}")
        print(f"Depodaki su seviyesi: {self.water_level}")
        print(f"Depodaki köğük seviyesi: {self.foam_level}")
        print(f"Depodaki su seviyesi: {self.water_level}")
        print(f"Aracın merdiven uzunluğu: {self.ladder_length}")
        print(f"Görevde mi: {self.is_it_on_duty}")
        print(f"Siren açık mı: {self.is_siren_on}")
        print(f"Yeterli personel var mı: {self.is_enough_staff}")