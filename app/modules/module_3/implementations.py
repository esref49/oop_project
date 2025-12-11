# app/modules/module_3/implementations.py
from app.modules.module_3.base import EmergencyUnit

class AmbulanceUnit(EmergencyUnit):

    def __init__(self, unit_id, unit_type, current_location, availability, fuel_level, is_enough_staff, is_siren_on, is_it_on_duty, medical_supply_level, is_sterilized):
        # Üst sınıfın (EmergencyUnit) kurucu metodunu çağırarak temel özellikleri başlatır
        super().__init__(unit_id, unit_type , current_location, availability, fuel_level, is_enough_staff, is_siren_on, is_it_on_duty)
        
        # Ambulansa özgü: Tıbbi malzeme doluluk oranı ve sterilizasyon durumu
        self.medical_supply_level = medical_supply_level
        self.is_sterilized = is_sterilized
        
        # Birim türünü kalıcı olarak 'Ambulans' olarak belirler
        self.unit_type = "Ambulans"

    def update_location(self, new_location):
        # Aracın anlık konum bilgisini günceller
        self.current_location = new_location
        print("[+] Ambulansın konumu güncellendi")
    
    def open_siren(self):
        # Sadece araç aktif görevde ise sirenlerin açılmasını sağlar
        if self.is_it_on_duty == True:
            self.is_siren_on = True
        print("[+] Sirenler açıldı")    
    
    def report_location(self):
        # Aracın güncel konumunu raporlar
        print(["[+] Ambulansın konumu: ", self.current_location])

    def report_fault(self, faulty_part = None, faulty_level = None):
        """
        Araçtaki arızaları seviyesine göre (1 veya 2) değerlendirir ve müsaitlik durumunu günceller.
        """
        # Kritik parçalarda (motor, tekerlek vb.) seviye 2 arıza varsa aracı hizmet dışı bırakır
        if faulty_part in ["motor", "tekerlek", "gövde", "nagivasyon", "tıbbi cihaz"] and faulty_level == 2:
            self.availability = False

        # Ufak arızalarda (seviye 1) araç hizmet vermeye devam edebilir (Availability=True)
        elif  faulty_part in ["motor suyu", "tekerlek", "gövde", "tıbbi cihaz"] and faulty_level == 1:
            self.availability = True

        # Herhangi bir arıza parametresi girilmediyse araç sağlam kabul edilir
        elif faulty_level == None and faulty_level == None:
            self.availability = True

        else:
            print("[-] Lütfen geçerli bir arıza parçası ve arıza seviyesi belirle")

    
    def report_status(self):
        # Aracın tüm teknik ve operasyonel durumunu detaylıca ekrana yazdırır
        print(f"Araç Id: {self.unit_id}) - Araç Türü: {self.unit_type}" )
        print(f"Müsaitlik: {self.availability}")
        print(F"Mecvut konumu: {self.current_location}")
        print(f"Benzin Seviyesi: {self.fuel_level}")
        print(f"Tıbbi malzeme seviyesi: {self.medical_supply_level}")
        print(f"Görevde mi: {self.is_it_on_duty}")
        print(f"Siren açık mı: {self.is_siren_on}")
        print(f"Steril mi: {self.is_sterilized}")
        print(f"Yeterli personel var mı: {self.is_enough_staff}")


class PoliceUnit(EmergencyUnit):
    def __init__(self, unit_id, unit_type, current_location, availability, fuel_level, is_enough_staff, is_siren_on, is_it_on_duty, detainee_count):
        super().__init__(unit_id, unit_type , current_location, availability, fuel_level, is_enough_staff, is_siren_on, is_it_on_duty)
        self.unit_type = "Polis"
        self.detainee_count = detainee_count

    def update_location(self, new_location):
        self.current_location = new_location

        print("[+] Polis konumu güncellendi")
    
    def open_siren(self):
        if self.is_it_on_duty == True:
            self.is_siren_on = True

        print("[+] Sirenler açıldı")    
    
    def report_location(self):
        print(["[+] Polis konumu: ", self.current_location])

    def report_fault(self, faulty_part = None, faulty_level = None):

        if faulty_part in ["motor", "tekerlek", "gövde", "nagivasyon"] and faulty_level == 2:
            self.availability = False

        elif  faulty_part in ["motor suyu", "tekerlek", "gövde"] and faulty_level == 1:
            self.availability = True

        elif faulty_level == None and faulty_level == None:
            self.availability = True
            
        else:
            print("[-] Lütfen geçerli bir arıza parçası ve arıza seviyesi belirle")

    
    def report_status(self):
        print(f"Araç Id: {self.unit_id}) - Araç Türü: {self.unit_type}" )
        print(f"Müsaitlik: {self.availability}")
        print(F"Mecvut konumu: {self.current_location}")
        print(f"Benzin Seviyesi: {self.fuel_level}")
        print(f"Görevde mi: {self.is_it_on_duty}")
        print(f"Siren açık mı: {self.is_siren_on}")
        print(f"Yeterli perseonel var mı: {self.is_enough_staff}")

class FireFightingUnit(EmergencyUnit):
    def method3(self):
        print(f"Sinif Attribute: {self.base3Attribute}")