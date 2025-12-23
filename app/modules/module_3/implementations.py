import time
from .base import EmergencyUnit, Human, Structure
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

    # Araca ait kaza raporu ve protokol yönetimi
    def report_accident(self, severity_level=None):
        print("\n" + "="*45)
        print(" [DİKKAT] ARAÇ KAZA YAPTI - PROTOKOL UYGULANIYOR")
        print("="*45)

        # Kaza anında yapılması gereken standart adımlar
        protocol_steps = [
            "1. [İŞARET] Dubalarla yolu daralt, trafiği yavaşlat.",
            "2. [YARDIM] Yaralı varsa 112'ye haber ver, araçtan çıkarma.",
            "3. [TUTANAK] Kaza krokisini çiz ve tutanak tut."
        ]

        for step in protocol_steps:
            print(step)
        
        print("-" * 45)

        # Şiddetli kaza durumu (Seviye 2)
        if severity_level == 2:
            self.is_broken = True
            self.availability = False # Aracı tamamen görevlere kapatır
            print(f"[KAZA] Kritik Hasar! Araç {self.unit_id} HİZMET DIŞI.")
            print("[SİSTEM] Yedek ekip ve çekici yönlendiriliyor...")

        # Hafif kaza durumu (Seviye 1)
        elif severity_level == 1:
            self.is_broken = False 
            print(f"[KAZA] Hafif Hasar. Araç {self.unit_id} görevine devam edebilir.")
            print("[BİLGİ] Operasyon bitimi teknik kontrol gereklidir.")

        else:
            print("[HATA] Tanımsız kaza seviyesi. Lütfen (1) veya (2) giriniz.")

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

    def update_location(self, new_location):
        self.current_location = new_location

        print(f"[KONUM] Polis aracının konumu güncellendi: {self.current_location}")
    
    def open_siren(self):
        if self.is_it_on_duty:
            self.is_siren_on = True
            print("[SİREN] Sirenler açıldı")
        else:
            print("[SİREN] Araç görevde olmadığı için siren açılamaz")
    
    def report_location(self):
        print(f"[KONUM] Polis aracının konumu: {self.current_location}")

    def report_accident(self, severity_level=None):
        print("\n" + "="*45)
        print(" [DİKKAT] ARAÇ KAZA YAPTI - PROTOKOL UYGULANIYOR")
        print("="*45)

        protocol_steps = [
            "1. [İŞARET] Dubalarla yolu daralt, trafiği yavaşlat.",
            "2. [YARDIM] Yaralı varsa 112'ye haber ver, araçtan çıkarma.",
            "3. [TUTANAK] Kaza krokisini çiz ve tutanak tut."
        ]

        for step in protocol_steps:
            print(step)
        
        print("-" * 45)

        if severity_level == 2:
            self.is_broken = True
            print(f"[KAZA] Kritik Hasar! Araç {self.unit_id} HİZMET DIŞI.")
            print("[SİSTEM] Yedek ekip ve çekici yönlendiriliyor...")

        elif severity_level == 1:
            self.is_broken = False 
            print(f"[KAZA] Hafif Hasar. Araç {self.unit_id} görevine devam edebilir.")
            print("[BİLGİ] Operasyon bitimi teknik kontrol gereklidir.")

        else:
            print("[HATA] Tanımsız kaza seviyesi. Lütfen (1) veya (2) giriniz.")


    def determine_availability(self):
        if self.is_enough_staff == False or self.is_broken or self.prisoner_count > 0:
            self.availability = False
        elif self.is_it_on_duty:
            self.availability = False
        else:
            self.availability = True
        
    def call_for_backup(self, reason):
        print(f"[ACİL DURUM] {self.unit_id} kodlu ekip ACİL DESTEK istiyor!")
        print(f"             Konum: {self.current_location}")
        print(f"             Sebep: {reason}")

    def issue_traffic_ticket(self):
        plate_number = input("Plaka giriniz: ")
        type_of_punishment = input("Ceza türünü seçiniz: (Hız/Emniyet Kemeri/Ehliyet/Alkol)")

        if self.unit_specialty == "Trafik":
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

    def refill_tank(self):

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

class FireFightingUnit(EmergencyUnit):
    def __init__(self, unit_id, fuel_level, is_enough_staff, water_level, foam_level, max_water_level, max_foam_level, max_fuel_level, ladder_length = 20,
                 unit_type = "İtfaiye", current_location = np.random.randint(20), availability = True, is_siren_on = False, is_it_on_duty = False):
        
        super().__init__(unit_id, unit_type, current_location, availability, fuel_level, is_enough_staff, is_siren_on, is_it_on_duty, max_fuel_level = 85)

        self.max_fuel_level = max_fuel_level
        self.__water_level = water_level
        self.__foam_level = foam_level
        self.__ladder_length = ladder_length
        self.__max_water_level = max_water_level
        self.__max_foam_level = max_foam_level
        self.__total_count = 0

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

    @property
    def ladder_length(self):
        return self.__ladder_length
    
    @ladder_length.setter
    def ladder_length(self, new):
        self.__ladder_length = new

    @property
    def max_water_level(self):
        return self.__max_water_level
    
    @max_water_level.setter
    def water_level(self, new):
        self.__max_water_level = new

    @property
    def max_foam_level(self):
        return self.__max_foam_level
    
    @max_foam_level.setter
    def max_foam_level(self, new):
        self.__max_foam_level = new

    @property
    def total_count(self):
        return self.__total_count
    
    @total_count.setter
    def total_count(self, new):
        self.__total_count = new

    def update_location(self, new_location):
        self.current_location = new_location
        print(f"[KONUM] Ambulansın konumu güncellendi: {self.current_location}")
    
    def open_siren(self):
        if self.is_it_on_duty:
            self.is_siren_on = True
            print("[SİREN] Sirenler açıldı")
        else:
            print("[SİREN] Araç görevde olmadığı için siren açılamaz")
    
    def report_location(self):
        print(f"[KONUM] İtfaye aracının konumu: {self.current_location}")

    # Kaza yönetimi
    def report_accident(self, severity_level=None):
        print("\n" + "="*45)
        print(" [DİKKAT] ARAÇ KAZA YAPTI - PROTOKOL UYGULANIYOR")
        print("="*45)

        protocol_steps = [
            "1. [İŞARET] Dubalarla yolu daralt, trafiği yavaşlat.",
            "2. [YARDIM] Yaralı varsa 112'ye haber ver, araçtan çıkarma.",
            "3. [TUTANAK] Kaza krokisini çiz ve tutanak tut."
        ]

        for step in protocol_steps:
            print(step)
        
        print("-" * 45)

        if severity_level == 2:
            self.is_broken = True
            print(f"[KAZA] Kritik Hasar! Araç {self.unit_id} HİZMET DIŞI.")
            print("[SİSTEM] Yedek ekip ve çekici yönlendiriliyor...")

        elif severity_level == 1:
            self.is_broken = False 
            print(f"[KAZA] Hafif Hasar. Araç {self.unit_id} görevine devam edebilir.")
            print("[BİLGİ] Operasyon bitimi teknik kontrol gereklidir.")

        else:
            print("[HATA] Tanımsız kaza seviyesi. Lütfen (1) veya (2) giriniz.")

    def determine_availability(self):
        if self.fuel_level < 20 or self.foam_level < 10 or self.water_level < 20 or self.is_enough_staff == False or self.is_broken:
            self.availability = False

        elif self.is_it_on_duty:
            self.availability = False

        else:
            self.availability = True

    def refill_tank(self):

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
        
        self.water_level = self.max_water_level
        self.foam_level = self.max_foam_level
        self.fuel_level = self.max_fuel_level
        
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
    
    @classmethod
    def show_total_vehicle_size(cls):
        return f"[SİSTEM] Şu an envanterde toplam {cls.total_fleet_count} adet itfaiye aracı kayıtlıdır"

class Criminal(Human):
    most_wanted_list = []

    def __init__(self, id, name, lastname, age, blood_group, height, weight, is_alive, criminal_history, danger_level, is_caught, kill_count, injured_count):
        super().__init__(id, name, lastname, age, blood_group, height, weight, is_alive, )
        self.__criminal_history = criminal_history
        self.__danger_level = danger_level
        self.__is_caught = is_caught
        self.__kill_count = kill_count
        self.__injured_count = injured_count
        
        if danger_level > 8:
            Criminal.add_to_most_wanted(f"{name} {lastname} | Yaş:{age} | Boy:{height} Kilo:{weight} | Öldürme sayısı : {kill_count}")
    
    @property
    def criminal_history(self):
        return self.__criminal_history
    
    @criminal_history.setter
    def criminal_history(self, new):
        self.__criminal_history = new

    @property
    def danger_level(self):
        return self.__danger_level
    
    @danger_level.setter
    def danger_level(self, new):
        self.__danger_level = new

    @property
    def is_caught(self):
        return self.__is_caught
    
    @is_caught.setter
    def is_caught(self, new):
        self.__is_caught = new

    @property
    def kill_count(self):
        return self.__kill_count
    
    @kill_count.setter
    def kill_count(self, new):
        self.__kill_count = new

    @property
    def injured_count(self):
        return self.__injured_count
    
    @injured_count.setter
    def injured_count(self, new):
        self.__injured_count = new

    def report_status(self):
        status = "Yakalandı" if self.__is_caught else "Firar"
        return f"[POLİS] Suçlu Durumu: {status} | Tehlike Seviyesi: {self.__danger_level}"

    # Kişi suç durumunu açıklar
    def get_role_description(self):
        if self.__kill_count > 0:
            return f"[POLİS] Cinayet faili"
        elif self.__injured_count > 0:
            return f"[POLİS] Adam yaralama faili"
        else:
            return f"[POLİS] Yasadışı aktivitelerin faili"

    # Suçluyu en çok arananlar listesine ekler
    @classmethod
    def add_to_most_wanted(cls, full_name):
        cls.most_wanted_list.append(full_name)
        return f"[POLİS] {full_name} en çok arananlar listesine eklendi"

    # Suçlunun suç seviyesini belirler
    @staticmethod
    def analyze_crime_severity(crime_type):
        severity_map = {
            "Hırsılık": 3,
            "Darp": 6,
            "Cinayet": 10,
            "Kundaklama": 8,
            "Ağır Yaralama": 7,
        }
        return severity_map.get(crime_type, 1)
    
    # Suçlu her yeni suç işlediğinde tehliye seviyesini arttırır
    def update_danger_level(self, crime_type):
        point = self.analyze_crime_severity(crime_type)        
        current_total = self.danger_level + point
        self.danger_level = current_total
        
        print(f"[POLİS] {crime_type} işlendi. Tehlike seviyesi +{point} arttı. (Tehlike Seviyesi: {self.danger_level})")

# Kurban
class Victim(Human):
    all_victims_registry = []

    def __init__(self, id, name, lastname, age, blood_group, height, weight, is_alive, degree_of_injury, the_person_who_injured, cause_of_injury, ):
        super().__init__(id, name, lastname, age, blood_group, height, weight, is_alive)
        self.__degree_of_injury = degree_of_injury
        self.__the_person_who_injured = the_person_who_injured
        self.__cause_of_injury = cause_of_injury

    @property
    def degree_of_injury(self):
        return self.__degree_of_injury
    
    @degree_of_injury.setter
    def degree_of_injury(self, new):
        self.__degree_of_injury = new

    @property
    def the_person_who_injured(self):
        return self.__the_person_who_injured
    
    @the_person_who_injured.setter
    def the_person_who_injured(self, new):
        self.__the_person_who_injured = new

    @property
    def cause_of_injury(self):
        return self.__cause_of_injury
    
    @cause_of_injury.setter
    def cause_of_injury(self, new): 
        self.__cause_of_injury = new

    # Kurban durumu
    def report_status(self):
        return f"[AMBULANS][YARALI DURUMU] Yaralanma Seviyesi: {self.__degree_of_injury}/10 | Neden: {self.__cause_of_injury}"

    # Kurban hakkında açıklama
    def get_role_description(self):
        return f"Kurban {self.__cause_of_injury} sebebiyle yaralı"

    # Kurbanın ailesine haber veriyoruz
    def notify_family(self, hospital_name):
        if not self.is_alive:
            message = f"[HASTAHANE] Başınız Sağolsun: {self.name} {self.lastname} isimli yakınınızı kaybettik. Lütfen {hospital_name} morguna geliniz."
        elif self.__degree_of_injury > 7:
            message = f"[HASTAHANE] Yakınınız {self.name}, {hospital_name} hastanesine kaldırıldı. Durumu KRİTİK. Acilen gelmeniz gerekiyor."
        else:
            message = f"[HASTAHANE] Yakınınız {self.name}, {hospital_name} hastanesinde müşahade altında. Durumu iyi, endişelenmeyin."
        
        # Durumu mesaj olarak hasta yakınlarına gönderir
        print(f"📨 [SMS GÖNDERİLDİ] -> {self.__family_contact}: {message}")
        return True
    
    # Sadece yaralı olan ve belli bir seviyenin üstündeki hastaların yakınlarına bilgilendirme yapar
    @classmethod
    def mass_notify_families(cls, min_severity=1):
        count = 0
        
        for victim in cls.all_victims_registry:
            if victim.is_alive and victim.degree_of_injury >= min_severity:
                victim.notify_family("Merkez Şehir Hastanesi")
                count += 1
        
        return f"[HASTAHANE] Toplam {count} ailenin telefonuna bilgilendirme mesajı gönderildi."

    # Yaralının yaşına ve yaralanma derecesine göre öncelik belirler
    @staticmethod
    def prioritize(degree_of_injury, age):
        score = degree_of_injury
        if age > 70 or age < 10:
            score += 2
        return score
    
class Hospital(Structure):
    pandemic_mode = False

    def __init__(self, structure_id, name, address, capacity, current_occupancy, location, number_of_doctors, number_of_ambulances, specialized_units):
        super().__init__(structure_id, name, address, capacity, current_occupancy, location)
        self.__number_of_doctors = number_of_doctors
        self.__number_of_ambulances = number_of_ambulances
        self.__specialized_units = specialized_units
        self.__patients_list = []

    @property
    def number_of_doctors(self):
        return self.__number_of_doctors
    
    @number_of_doctors.setter
    def number_of_doctors(self, count):
        self.__number_of_doctors = count

    @property
    def number_of_ambulances(self):
        return self.__number_of_ambulances
    
    @number_of_ambulances.setter
    def number_of_ambulances(self, count):
        self.__number_of_ambulances = count

    @property
    def specialized_units(self):
        return self.__specialized_units
    
    @specialized_units.setter
    def specialized_units(self, units):
        self.__specialized_units = units

    @property
    def patients_list(self):
        return self.__patients_list

    # Hasta ekleme
    def add_patient(self, victim):
        if self.current_occupancy < self.capacity:
            self.__patients_list.append(victim)
            self.current_occupancy += 1
            return True
        return False

    # Hastahane bakım maliyetini hesaplar
    def calculate_maintenance_cost(self):
        base_cost = 5000
        doctor_cost = self.__number_of_doctors * 200
        return base_cost + doctor_cost

    @classmethod
    def set_pandemic_mode(cls, status):
        cls.pandemic_mode = status
        return f"[HASTAHANE] Pandemi durumu: {status}"

    # Kan grubu uyumunu kontrol eder
    @staticmethod
    def check_blood_compatibility(donor_type, recipient_type):
        if donor_type == "O Rh-":
            return True
        elif donor_type == recipient_type:
            return True
        return False

class PoliceStation(Structure):
    # Tüm birimlerin ciddiyet seviyesi
    severity = 3

    def __init__(self, structure_id, name, address, capacity, current_occupancy, location, cell_count, number_of_officers, patrol_cars_count):
        super().__init__(structure_id, name, address, capacity, current_occupancy, location)
        self.__cell_count = cell_count
        self.__number_of_officers = number_of_officers
        self.__patrol_cars_count = patrol_cars_count
        self.__criminals_in_custody = []

    @property
    def cell_count(self):
        return self.__cell_count
    
    @cell_count.setter
    def cell_count(self, count):
        self.__cell_count = count

    @property
    def number_of_officers(self):
        return self.__number_of_officers
    
    @number_of_officers.setter
    def number_of_officers(self, count):
        self.__number_of_officers = count

    @property
    def patrol_cars_count(self):
        return self.__patrol_cars_count
    
    @patrol_cars_count.setter
    def patrol_cars_count(self, count):
        self.__patrol_cars_count = count

    @property
    def criminals_in_custody(self):
        return self.__criminals_in_custody

    def book_criminal(self, criminal):
        if len(self.__criminals_in_custody) < self.__cell_count:
            self.__criminals_in_custody.append(criminal)
            self.current_occupancy += 1
            return True
        return False

    # Bina bakım maliyetini hesaplar
    def calculate_maintenance_cost(self):
        return (self.__number_of_officers * 100) + (self.__patrol_cars_count * 50)

    # Ülke genelinde polis birimlerinin ciddiyet seviyesini belirler
    @classmethod
    def change_severity_level(cls, level):
        if 1 <= level <= 5:
            cls.severity = level
            return f"[SİSTEM] Ülke genelinde tüm birimlerin ciddiyet seviyesi güncellendi: {level}"
        return "[SİSTEM] Geçerli bir seviye girin"
 
    # Kişinin serbest bırakılması için gerekli olan kefalet miktarını belirle
    @staticmethod
    def calculate_bail_amount(danger_level, crime_count):
        base_bail = 1000
        return base_bail * danger_level * (crime_count + 1)

class FireStation(Structure):
    # Binalarda olması gereken min su seviyesi (lt türünden)
    water_reserve_standard = 100000

    def __init__(self, structure_id, name, address, capacity, current_occupancy, location, number_of_engines, water_tank_capacity, foam_reserve):
        super().__init__(structure_id, name, address, capacity, current_occupancy, location)
        self.__number_of_engines = number_of_engines
        self.__water_tank_capacity = water_tank_capacity
        self.__foam_reserve = foam_reserve

    @property
    def number_of_engines(self):
        return self.__number_of_engines
    
    @number_of_engines.setter
    def number_of_engines(self, count):
        self.__number_of_engines = count

    @property
    def water_tank_capacity(self):
        return self.__water_tank_capacity
    
    @water_tank_capacity.setter
    def water_tank_capacity(self, capacity):
        self.__water_tank_capacity = capacity

    @property
    def foam_reserve(self):
        return self.__foam_reserve
    
    @foam_reserve.setter
    def foam_reserve(self, reserve):
        self.__foam_reserve = reserve

    # Binanın işleyiş maliyetini hesaplar
    def calculate_maintenance_cost(self):
        return (self.__number_of_engines * 300) + (self.__water_tank_capacity * 0.1) + (self.__foam_reserve * 0.4)

    # Olması gerekn min su seviyesini günceller
    @classmethod
    def update_water_standard(cls, new_standard):
        cls.water_reserve_standard = new_standard
        return f"[SİSTEM] Ülke geenelindeki itfaiye binlarında olması gereken su miktarı güncellendi: {new_standard}"

    # Suyun yangın yerine ulaşması için gereken pompa gücünü hesaplar
    @staticmethod
    def calculate_needed_pressure(height):
        return 2 + (height * 0.43)