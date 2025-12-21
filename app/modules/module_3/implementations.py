import time
from app.modules.module_3.base import EmergencyUnit
import numpy as np

# Ambulans Birimi
class AmbulanceUnit(EmergencyUnit):

    def __init__(self, unit_id, fuel_level, is_enough_staff, medical_supply_level, is_sterilized,
                 unit_type = "Ambulans", current_location = np.random.randint(20), availability = True, is_siren_on = False, is_it_on_duty = False):
        super().__init__(unit_id, unit_type, current_location, availability, fuel_level, is_enough_staff, is_siren_on, is_it_on_duty, max_fuel_level=80)
        
        # Ambulansa özgü özellikleri tanımlar
        self.__medical_supply_level = medical_supply_level
        self.__is_sterilized = is_sterilized

        self.is_broken = False
        self.availability = True

    @property
    def medical_supply_level(self):
        return self.__medical_supply_level
    
    @medical_supply_level.setter
    def medical_supply_level(self, new):
        self.__medical_supply_level = new

    @property
    def is_sterilized(self):
        return self.__is_sterilized

    @is_sterilized.setter
    def is_sterilized(self, new):
        self.__is_sterilized = new

    # Aracın mevcut konumunu girilen yeni konum ile günceller
    def update_location(self, new_location):
        self.current_location = new_location
        print(f"[KONUM] Ambulansın konumu güncellendi: {self.current_location}")
    
    # Ambulansın sadece görev başındaysa sirenin açılmasına izin verir
    def open_siren(self):
        if self.is_it_on_duty:
            self.is_siren_on = True
            print("[SİREN] Sirenler açıldı")
        else:
            print("[SİREN] Araç görevde olmadığı için siren açılamaz")

    # Aracın anlık konumunu verir
    def report_location(self):
        print(f"[KONUM] Ambulansın konumu: {self.current_location}")

    # Araçtaki arızaları sisteme girmeye yarar
    def report_fault(self, faulty_part=None, faulty_level=None):
        critical_parts = ["motor", "tekerlek", "gövde", "navigasyon", "tıbbi cihaz"]
        
        # Parça ismini küçük harfe çevirip kritik parça listesinde olup olmadığını ve arıza seviyesini kontrol eder
        # Eğer arıza kritik ise aracı hizmet dışına alır
        # Arıza hafif ise uyarı yapar ama aracı hizmet dışına almaz 
        if faulty_part and faulty_part.lower() in critical_parts and faulty_level == 2:
            self.is_broken = True
            print(f"[ARIZA] Kritik Arıza: {faulty_part}! Araç hizmet dışı")
        
        elif faulty_part and faulty_part.lower() in critical_parts and faulty_level == 1:
            print(f"[ARIZA] Hafif Arıza: {faulty_part}. Göreve devam edebilir")
            self.is_broken = False 

        # Herhangi bir arıza girilmemişse aracı sağlam olarak işaretler
        elif faulty_part is None and faulty_level is None:
            self.is_broken = False
            print("[ARIZA] Arıza yok araç sağlam")

        else:
            print("[ARIZA] Tanımsız arıza durumu")

    # Arıza ile birlikte diğer tüm parametreleri değerlendirerek aracın müsaitliğini belirler
    def determine_availability(self):

        # Sterilizasyon yoksa, malzeme azsa, personel eksikse veya araç bozuksa müsait değildir
        if not self.is_sterilized or self.medical_supply_level < 30 or self.is_enough_staff == False or self.is_broken:
            self.availability = False
        # Araç zaten görevdeyse müsait değildir
        elif self.is_it_on_duty:
            self.availability = False
        # Hiçbir sorun yoksa araç göreve müsaittir
        else:
            self.availability = True

    # Ambulansın benzin deposunu doldurur
    def refill_tank(self):

        # Eğer zaten doluysa işlem yapma
        if self.fuel_level == self.max_fuel_level:
            print("[BİLGİ] Depo tamamen dolu")
            return
        
        print(f"[BİLGİ] İstasyona yanaşıldı. Dolum işlemi başlıyor...")
        
        time.sleep(1)
        print("Dolum durumu: %25")
        time.sleep(1)
        print("Dolum durumu: %50")
        time.sleep(1)
        print("Dolum durumu: %75")
        time.sleep(1)
        print("Dolum durumu: %100")
        
        # Değerleri güncelle
        self.fuel_level = self.max_fuel_level
        self.availability = True 
        
        print(f"[BİLGİ] Dolum tamamlandı!")

    # Aracın tüm özelliklerini veritabanına kaydetmeden önce aracın kimlik kartını oluşturur
    def get_detailed_status(self):
        self.determine_availability()
        status_text = "EVET (MÜSAİT)" if self.availability else "HAYIR (HİZMET DIŞI)"
        
        return f"""
--------------------------------------------------
[AMBULANS KİMLİK KARTI]
Araç Id                 : {self.unit_id}
Araç Türü               : {self.unit_type}
Hizmette mi (Müsaitlik) : {status_text}
Mevcut Konum            : {self.current_location}
Benzin Seviyesi         : {self.fuel_level}
Tıbbi Malzeme           : {self.medical_supply_level}
Sterilizasyon           : {"Evet" if self.is_sterilized else "Hayır"}
Personel Durumu         : {"Yeterli" if self.is_enough_staff else "Eksik"}
Siren Durumu            : {"Açık" if self.is_siren_on else "Kapalı"}
Görevde mi              : {"Evet" if self.is_it_on_duty else "Hayır"}
--------------------------------------------------
"""


# Polis Sınıfı
class PoliceUnit(EmergencyUnit):
    def __init__(self, unit_id, fuel_level, is_enough_staff, patrol_area,  prisoner_count = 0, unit_specialty = "Asayiş",
                 unit_type = "Polis", current_location = np.random.randint(20), availability = True, is_siren_on = False, is_it_on_duty = False,):
        
        super().__init__(unit_id, unit_type, current_location, availability, fuel_level, is_enough_staff, is_siren_on, is_it_on_duty, max_fuel_level=65)
   
        # Polise özgü özellikleri ayarlar
        self.__prisoner_count = prisoner_count
        self.__patrol_area = patrol_area
        self.__unit_specialty = unit_specialty
        self.max_fuel_level = 65

        self.is_broken = False
        self.availability = True
        self.gbt_check_count = 0 # GBT sayacını başlatır

    @property
    def prisoner_count(self):
        return self.__prisoner_count
    
    @prisoner_count.setter
    def prisoner_count(self, new):
        self.__prisoner_count = new

    @property
    def patrol_area(self):
        return self.__patrol_area
    
    @prisoner_count.setter
    def patrol_area(self, new):
        self.__patrol_area = new

    @property
    def unit_specialty(self):
        return self.__unit_specialty
    
    @prisoner_count.setter
    def unit_specialty(self, new):
        self.__unit_specialty = new

    # Konum güncellemesi yapar
    def update_location(self, new_location):
        self.current_location = new_location

        print(f"[KONUM] Polis aracının konumu güncellendi: {self.current_location}")
    
    # Görevdeyse sireni açar
    def open_siren(self):
        if self.is_it_on_duty:
            self.is_siren_on = True
            print("[SİREN] Sirenler açıldı")
        else:
            print("[SİREN] Araç görevde olmadığı için siren açılamaz")
    
    def report_location(self):
        # Mevcut konumu raporlar
        print(f"[KONUM] Polis aracının konumu: {self.current_location}")

    # Araçtaki arızları yönetir
    def report_fault(self, faulty_part=None, faulty_level=None):
        critical_parts = ["motor", "tekerlek", "gövde", "navigasyon", "tıbbi cihaz"]
        
        # Kritik parçalarda seviye 2 hasar varsa aracı bozuk işaretler 
        if faulty_part and faulty_part.lower() in critical_parts and faulty_level == 2:
            self.is_broken = True
            print(f"[ARIZA] Kritik Arıza: {faulty_part}! Araç hizmet dışı")
        
        # Hafif hasarda sadece bilgi verir
        elif faulty_part and faulty_part.lower() in critical_parts and faulty_level == 1:
            print(f"[ARIZA] Hafif Arıza: {faulty_part}. Göreve devam edebilir")
            self.is_broken = False

        # Arıza yoksa sağlam işaretler
        elif faulty_part is None and faulty_level is None:
            self.is_broken = False
            print("[ARIZA] Arıza yok, araç sağlam")

        else:
            print("[ARIZA] Tanımsız arıza durumu")

    # Aracın genel durumuna bakarak müsaitliğini belirler.
    # Personel, arıza, tutuklu gibi bir çok özelliği değerlendirir
    def determine_availability(self):
        if self.is_enough_staff == False or self.is_broken or self.prisoner_count > 0:
            self.availability = False
        elif self.is_it_on_duty:
            self.availability = False
        else:
            self.availability = True
        
    # Acil durumlarda destek çağrısı ve konum bilgisini diğer ekiplerle paylaşır
    def call_for_backup(self, reason):
        print(f"[ACİL DURUM] {self.unit_id} kodlu ekip ACİL DESTEK istiyor!")
        print(f"             Konum: {self.current_location}")
        print(f"             Sebep: {reason}")

    # Trafik cezası yazar
    # Sadece 'Trafik' biriminin ceza yazmasına izin verir
    def issue_traffic_ticket(self):
        plate_number = input("Plaka giriniz: ")
        type_of_punishment = input("Ceza türünü seçiniz: (Hız/Emniyet Kemeri/Ehliyet/Alkol)")

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
            print("[BİLGİ] Bu birimin trafik cezası kesme yetkisi bulunmamaktadır.")

    # GBT kontrolü yapar
    def perform_gbt_control(self):
        gbt_number = input("TC giriniz: ")
        self.gbt_check_count += 1

        # Rastgele bir şansla kişinin suçlu olup olmadığını belirler
        is_criminal = np.random.choice([0, 1, 0, 0, 1, 0])

        if is_criminal == 1:
            print("[GBT] Bu kişinin aranması mevcuttur. Hemen yakalayın!")
        else:
            print("[GBT] Kişinin herhangi bir aranması yoktur.")

    # Polisin benzin deposunu doldurur
    def refill_tank(self):

        # Eğer zaten doluysa işlem yapma
        if self.fuel_level == self.max_fuel_level:
            print("[BİLGİ] Depo tamamen dolu")
            return
        
        print(f"[BİLGİ] İstasyona yanaşıldı. Dolum işlemi başlıyor...")
        
        time.sleep(1)
        print("Dolum durumu: %25")
        time.sleep(1)
        print("Dolum durumu: %50")
        time.sleep(1)
        print("Dolum durumu: %75")
        time.sleep(1)
        print("Dolum durumu: %100")
        
        # Değerleri güncelle
        self.fuel_level = self.max_fuel_level
        self.availability = True 
        
        print(f"[BİLGİ] Dolum tamamlandı!")

    def get_detailed_status(self):
        self.determine_availability()
        status_text = "EVET (MÜSAİT)" if self.availability else "HAYIR (HİZMET DIŞI)"
        
        return f"""
--------------------------------------------------
[POLİS EKİBİ KİMLİK KARTI]
Araç Id                 : {self.unit_id}
Araç Türü               : {self.unit_type}
Hizmette mi (Müsaitlik) : {status_text}
Mevcut Konum            : {self.current_location}
Benzin Seviyesi         : {self.fuel_level}
Uzmanlık Alanı          : {self.unit_specialty}
Devriye Bölgesi         : {self.patrol_area}
Tutuklu Sayısı          : {self.prisoner_count}
GBT Sorgu Sayısı        : {self.gbt_check_count}
Personel Durumu         : {"Yeterli" if self.is_enough_staff else "Eksik"}
Görevde mi              : {"Evet" if self.is_it_on_duty else "Hayır"}
--------------------------------------------------
"""

# İtfaiye Sınıfı
class FireFightingUnit(EmergencyUnit):
    def __init__(self, unit_id, fuel_level, is_enough_staff, water_level, foam_level, max_water_level, max_foam_level, max_fuel_level, ladder_length = 20,
                 unit_type = "İtfaiye", current_location = np.random.randint(20), availability = True, is_siren_on = False, is_it_on_duty = False):
        
        super().__init__(unit_id, unit_type, current_location, availability, fuel_level, is_enough_staff, is_siren_on, is_it_on_duty, max_fuel_level = 85)

        self.__water_level = water_level
        self.__foam_level = foam_level
        self.ladder_length = ladder_length
        self.max_fuel_level = max_fuel_level
        self.max_water_level = max_water_level
        self.max_foam_level = max_foam_level

        self.is_broken = False
        self.availability = True

    @property
    def water_level(self):
        return self.__water_level
    
    @water_level.setter
    def water_level(self, new):
        self.__water_level = new

    @property
    def foam_level(self):
        return self.__foam_level
    
    @foam_level.setter
    def water_level(self, new):
        self.__foam_level = new


    def update_location(self, new_location):
        self.current_location = new_location
        print(f"[KONUM] Ambulansın konumu güncellendi: {self.current_location}")
    
    def open_siren(self):
        if self.is_it_on_duty:
            self.is_siren_on = True
            print("[SİREN] Sirenler açıldı")
        else:
            print("[SİREN] Araç görevde olmadığı için siren açılamaz")
    
    # Aracın alık konumunu verir
    def report_location(self):
        print(f"[KONUM] İtfaye aracının konumu: {self.current_location}")

    def report_fault(self, faulty_part=None, faulty_level=None):
        critical_parts = ["motor", "tekerlek", "gövde", "navigasyon", "merdiven", "pompa"]
        
        # Parça ismini küçük harfe çevirip kritik parça listesinde olup olmadığını kontrol eder
        if faulty_part and faulty_part.lower() in critical_parts and faulty_level == 2:
            self.is_broken = True
            print(f"[ARIZA] Kritik Arıza: {faulty_part}! Araç hizmet dışı")
        
        # Hafif arıza (seviye 1) durumunda sadece bilgilendirme yapar, aracı durdurmaz
        elif faulty_part and faulty_part.lower() in critical_parts and faulty_level == 1:
            print(f"[ARIZA] Hafif Arıza: {faulty_part}. Göreve devam edebilir")
            self.is_broken = False 

        # Herhangi bir arıza girilmemişse aracı sağlam olarak işaretler
        elif faulty_part is None and faulty_level is None:
            self.is_broken = False
            print("[ARIZA] Arıza yok, araç sağlam")

        else:
            print("[ARIZA] Tanımsız arıza durumu")

    # Birçok parametreyi değerlendirerek aracın müsaitliğini belirler.
    def determine_availability(self):
        if self.fuel_level < 20 or self.foam_level < 10 or self.water_level < 20 or self.is_enough_staff == False or self.is_broken:
            self.availability = False

        elif self.is_it_on_duty:
            self.availability = False

        else:
            self.availability = True

    # İtfaiyenin su ve köpük depolarını doldurmaya yarar
    def refill_tank(self):

        # Eğer zaten doluysa işlem yapma
        if self.water_level == self.max_water_level and self.foam_level == self.max_foam_level and self.fuel_level == self.max_fuel_level:
            print("[BİLGİ] Depolar zaten tamamen dolu")
            return

        text = input("Hangi depoda dolum yapmak istiyorsunuz: (1-SU/2-KÖPÜK/3-SU VE KÖPÜK/4-BENZİN)")

        print(f"[BİLGİ] İstasyona yanaşıldı. Dolum işlemi başlıyor...")
        
        time.sleep(1)
        print("Dolum durumu: %25")
        time.sleep(1)
        print("Dolum durumu: %50")
        time.sleep(1)
        print("Dolum durumu: %75")
        time.sleep(1)
        print("Dolum durumu: %100")
        
        # Değerleri güncelle
        self.water_level = self.max_water_level
        self.foam_level = self.max_foam_level
        self.fuel_level = self.max_fuel_level
        self.availability = True # Eğer köpük veya su bittiği için False olduysa, şimdi True yap
        
        print(f"[BİLGİ] Dolum tamamlandı!")

    def get_detailed_status(self):
        self.determine_availability()
        status_text = "EVET (MÜSAİT)" if self.availability else "HAYIR (HİZMET DIŞI)"
        
        return f"""
--------------------------------------------------
[İTFAİYE ARACI KİMLİK KARTI]
Araç Id                 : {self.unit_id}
Araç Türü               : {self.unit_type}
Hizmette mi (Müsaitlik) : {status_text}
Mevcut Konum            : {self.current_location}
Benzin Seviyesi         : {self.fuel_level} lt
Depodaki Su Seviyesi    : {self.water_level} lt
Depodaki Köpük Seviyesi : {self.foam_level} lt
Merdiven Uzunluğu       : {self.ladder_length} m
Personel Durumu         : {"Yeterli" if self.is_enough_staff else "Eksik"}
Siren Durumu            : {"Açık" if self.is_siren_on else "Kapalı"}
Görevde mi              : {"Evet" if self.is_it_on_duty else "Hayır"}
--------------------------------------------------
"""