import datetime
from .implementations import Criminal, Victim, Hospital, PoliceStation, FireStation

class EmergencyRepository():
    def __init__(self):
        self.status_file = "units_log.txt"
        self.file_name = "case_log.txt"
        self.event_history_file = "event_history_log.txt"
        self.criminal_file = "criminal_registry.txt"
        self.victim_file = "victim_registry.txt"
        self.structure_file = "structure_registry.txt"
        self.case_counter = self.get_last_case_id()

    @property
    def status_file(self):
        return self.__status_file
    
    @status_file.setter
    def status_file(self, new):
        self.__status_file = new

    @property
    def file_name(self):
        return self.__file_name
    
    @file_name.setter
    def file_name(self, new):
        self.__file_name = new

    @property
    def event_history_file(self):
        return self.__event_history_file
    
    @event_history_file.setter
    def event_history_file(self, new):
        self.__event_history_file = new

    @property
    def criminal_file(self):
        return self.__criminal_file
    
    @criminal_file.setter
    def criminal_file(self, new):
        self.__criminal_file = new

    @property
    def victim_file(self):
        return self.__victim_file
    
    @victim_file.setter
    def victim_file(self, new):
        self.__victim_file = new

    @property
    def structure_file(self):
        return self.__structure_file
    
    @structure_file.setter
    def structure_file(self, new):
        self.__structure_file = new

    @property
    def case_counter(self):
        return self.__case_counter
    
    @case_counter.setter
    def case_counter(self, new):
        self.__case_counter = new
    
    def get_last_case_id(self):
        try:
            with open(self.file_name, "r", encoding="utf-8") as f:
                content = f.read()
                count = content.count("ID: Olay-")
                return count
        except FileNotFoundError:
            return 0

    def save_case(self, case_data):
        self.case_counter += 1
        current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    
        assigned_unit_info = "Atama Yapılamadı"
        if case_data.get('assigned_unit_id'):
            unit_type = case_data.get('assigned_unit', 'Bilinmeyen')
            unit_id = case_data.get('assigned_unit_id')
            assigned_unit_info = f"{unit_type} (ID: {unit_id})"
    
        log_block = f"""
==================================================
[VAKA KAYIT RAPORU] - ID: Olay-{self.case_counter}
==================================================
Tarih             : {current_time}
Olay Türü         : {case_data.get('type', 'Belirtilmedi')}
Olay Konumu       : {case_data.get('location', 'Bilinmiyor')}
--------------------------------------------------
Ciddiyet Seviyesi : {case_data.get('severity', 0)} / 10
Kritik Durum      : {case_data.get('critical_status', '-')}
Gereken Ekipler   : {case_data.get('needed_unit_types', [])}
--------------------------------------------------
Atanan Birimler   : {assigned_unit_info}
Vaka Durumu       : {case_data.get('status', 'Aktif')}
==================================================
"""

        try:
            with open(self.file_name, "a", encoding="utf-8") as file:
                file.write(log_block + "\n")
        
            print(f"[LOG] Olay-{self.case_counter} başarıyla dosyaya işlendi")
        
        except Exception as e:
            print(f"[HATA] Dosyaya yazarken sorun çıktı: {e}")

            
    def save_unit_info(self, all_units):
        current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
        try:
            with open(self.status_file, "w", encoding="utf-8") as f:
                main_header = f"""
==================================================
         CANLI FİLO TAKİP SİSTEMİ
         Rapor Saati : {current_time}
         Araç Sayısı : {len(all_units)}
==================================================
"""
                f.write(main_header + "\n")
                
                if all_units:
                    for unit in all_units:
                        f.write(unit.get_detailed_status())
                        f.write("\n")
                else:
                    f.write("\n[HATA] SİSTEMDE KAYITLI ARAÇ BULUNAMADI\n")
                    
        except Exception as e:
            print(f"[HATA] Filo dosyası güncellenemedi: {e}")

    def delete_unit_from_file(self, unit_id):
        target_str = f"Araç Id                 : {unit_id}"
        separator = "--------------------------------------------------"
        
        try:
            with open(self.status_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            new_lines = []
            deleted = False
            
            target_index = -1
            for i, line in enumerate(lines):
                if target_str in line:
                    target_index = i
                    break
            
            if target_index == -1:
                print(f"[UYARI] Dosyada {unit_id} ID'li araç bulunamadı")
                return
            
            start_delete_index = target_index - 1
            end_delete_index = -1
            
            for i in range(target_index, len(lines)):
                if separator in lines[i].strip():
                    end_delete_index = i
                    break
            
            for i in range(len(lines)):
                if start_delete_index <= i <= end_delete_index:
                    deleted = True
                    continue
                new_lines.append(lines[i])

            if deleted:
                with open(self.status_file, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
                print(f"[BİLGİ] {unit_id} ID'li araç dosyadan başarıyla silindi")
                
        except Exception as e:
            print(f"[HATA] Dosyadan silme işlemi başarısız: {e}")

    def save_event_history(self, message):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        
        try:
            with open(self.event_history_file, "a", encoding="utf-8") as f:
                f.write(f"[{current_time}] {message}\n")
        except Exception as e:
            print(f"[HATA] Müdahale kaydı yapılamadı: {e}")

    def save_human_registry(self, human):
        # Vakanın sırasını belirliyoruz
        self.case_counter += 1
        current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

        if isinstance(human, Criminal()):
            is_criminal = True
        
        log_block = f"""
==================================================
[İnsan] - SIRA: {self.case_counter}
==================================================
Ad Soyad          : {human.name} {human.lastname}
TC                : {human.id}
Yaş               : {human.age}
Kilo - Boy        : {human.weight} kg - {human.height} cm
Kan Grubu         : {human.blood_group}
Doğum Tarihi      : {current_time}
--------------------------------------------------
Hayatta mı        : {human.is_alive}
Suç kaydı var mı  : {is_criminal}
==================================================
"""
        
        try:
            with open(self.human_population, "a", encoding="utf-8") as file:
                file.write(log_block + "\n") # Her rapordan sonra bir boşluk bırakır
            
            print(f"Kişi-{self.case_counter} başarıyla dosyaya işlendi")
            
        except Exception as e:
            print(f"[HATA] Dosyaya yazarken sorun çıktı: {e}")



    def save_criminal_record(self, criminal):
        current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        
        crime_status = "AKTİF" if not criminal.is_caught else "GÖZALTINDA"
        threat_level = "YÜKSEK RİSK" if criminal.danger_level > 7 else "ORTA RİSK" if criminal.danger_level > 4 else "DÜŞÜK RİSK"
        
        log_block = f"""
==================================================
[SUÇLU KAYIT RAPORU] - TC: {criminal.id}
==================================================
Kayıt Tarihi            : {current_time}
Ad Soyad                : {criminal.name} {criminal.lastname}
Yaş                     : {criminal.age}
Kan Grubu               : {criminal.blood_group}
Boy / Kilo              : {criminal.height} cm / {criminal.weight} kg
--------------------------------------------------
SUÇ BİLGİLERİ
--------------------------------------------------
Tehlike Seviyesi        : {criminal.danger_level}/10 ({threat_level})
Suç Durumu              : {crime_status}
Öldürme Sayısı          : {criminal.kill_count}
Yaralama Sayısı         : {criminal.injured_count}
Suç Geçmişi             : {criminal.criminal_history}
Hayatta mı              : {"EVET" if criminal.is_alive else "HAYIR"}
--------------------------------------------------
DURUM                   : {"🔴 FİRARDA - ACİL ARANMAKTADIR" if not criminal.is_caught else "🟢 GÖZALTINDA"}
==================================================
"""

        try:
            with open(self.criminal_file, "a", encoding="utf-8") as file:
                file.write(log_block + "\n")
            
            print(f"[KAYIT] {criminal.name} {criminal.lastname} suçlu veritabanına eklendi")
            
        except Exception as e:
            print(f"[HATA] Suçlu kaydı yapılamadı: {e}")

    def save_victim_record(self, victim):
        current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        
        severity_status = "KRİTİK DURUM" if victim.degree_of_injury > 7 else "CİDDİ" if victim.degree_of_injury > 4 else "HAFİF"
        
        log_block = f"""
==================================================
[MAĞDUR KAYIT RAPORU] - TC: {victim.id}
==================================================
Kayıt Tarihi            : {current_time}
Ad Soyad                : {victim.name} {victim.lastname}
Yaş                     : {victim.age}
Kan Grubu               : {victim.blood_group}
Boy / Kilo              : {victim.height} cm / {victim.weight} kg
--------------------------------------------------
YARALANMA BİLGİLERİ
--------------------------------------------------
Yaralanma Derecesi      : {victim.degree_of_injury}/10 ({severity_status})
Yaralayan Kişi          : {victim.the_person_who_injured}
Yaralanma Sebebi        : {victim.cause_of_injury}
Hayatta mı              : {"EVET" if victim.is_alive else "HAYIR"}
--------------------------------------------------
DURUM                   : {"🔴 ACİL MÜDAHALE GEREKLİ" if victim.degree_of_injury > 7 else "🟡 TAKİP ALTINDA" if victim.degree_of_injury > 4 else "🟢 STABIL"}
==================================================
"""

        try:
            with open(self.victim_file, "a", encoding="utf-8") as file:
                file.write(log_block + "\n")
            
            print(f"[KAYIT] {victim.name} {victim.lastname} mağdur veritabanına eklendi")
            
        except Exception as e:
            print(f"[HATA] Mağdur kaydı yapılamadı: {e}")

    def update_criminal_status(self, criminal_id, new_caught_status):
        try:
            with open(self.criminal_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            target_block_start = f"[SUÇLU KAYIT RAPORU] - TC: {criminal_id}"
            
            if target_block_start not in content:
                print(f"[HATA] {criminal_id} TC'li suçlu veritabanında bulunamadı")
                return False
            
            blocks = content.split("==================================================")
            updated_blocks = []
            
            for block in blocks:
                if target_block_start in block:
                    if new_caught_status:
                        block = block.replace("Suç Durumu              : AKTİF", "Suç Durumu              : GÖZALTINDA")
                        block = block.replace("DURUM                   : 🔴 FİRARDA - ACİL ARANMAKTADIR", "DURUM                   : 🟢 GÖZALTINDA")
                    else:
                        block = block.replace("Suç Durumu              : GÖZALTINDA", "Suç Durumu              : AKTİF")
                        block = block.replace("DURUM                   : 🟢 GÖZALTINDA", "DURUM                   : 🔴 FİRARDA - ACİL ARANMAKTADIR")
                    
                updated_blocks.append(block)
            
            with open(self.criminal_file, "w", encoding="utf-8") as f:
                f.write("==================================================".join(updated_blocks))
            
            status_text = "GÖZALTINA ALINDI" if new_caught_status else "FİRAR ETTİ"
            print(f"[GÜNCELLEME] {criminal_id} TC'li suçlunun durumu güncellendi: {status_text}")
            return True
            
        except Exception as e:
            print(f"[HATA] Durum güncellenemedi: {e}")
            return False

    def save_structure_registry(self, all_structures):
        current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
        try:
            with open(self.structure_file, "w", encoding="utf-8") as f:
                main_header = f"""
==================================================
         ALTYAPI KAYIT SİSTEMİ
         Rapor Saati : {current_time}
         Toplam Yapı : {len(all_structures)}
==================================================
"""
                f.write(main_header + "\n")
                
                if all_structures:
                    for structure in all_structures:
                        maintenance = structure.calculate_maintenance_cost()
                        
                        if isinstance(structure, Hospital):
                            block = f"""
--------------------------------------------------
[HASTAHANE KAYDI]
ID                      : {structure.structure_id}
İsim                    : {structure.name}
Adres                   : {structure.address}
Kapasite                : {structure.capacity}
Doluluk                 : {structure.current_occupancy}
Konum                   : {structure.location}
--------------------------------------------------
Doktor Sayısı           : {structure.number_of_doctors}
Ambulans Sayısı         : {structure.number_of_ambulances}
Uzman Birimler          : {structure.specialized_units}
Bakım Maliyeti          : {maintenance} TL
--------------------------------------------------
"""
                        elif isinstance(structure, PoliceStation):
                            block = f"""
--------------------------------------------------
[POLİS KARAKOLU KAYDI]
ID                      : {structure.structure_id}
İsim                    : {structure.name}
Adres                   : {structure.address}
Kapasite                : {structure.capacity}
Doluluk                 : {structure.current_occupancy}
Konum                   : {structure.location}
--------------------------------------------------
Hücre Sayısı            : {structure.cell_count}
Memur Sayısı            : {structure.number_of_officers}
Devriye Araç Sayısı     : {structure.patrol_cars_count}
Bakım Maliyeti          : {maintenance} TL
--------------------------------------------------
"""
                        elif isinstance(structure, FireStation):
                            block = f"""
--------------------------------------------------
[İTFAİYE İSTASYONU KAYDI]
ID                      : {structure.structure_id}
İsim                    : {structure.name}
Adres                   : {structure.address}
Kapasite                : {structure.capacity}
Doluluk                 : {structure.current_occupancy}
Konum                   : {structure.location}
--------------------------------------------------
İtfaiye Aracı Sayısı    : {structure.number_of_engines}
Su Tank Kapasitesi      : {structure.water_tank_capacity} lt
Köpük Rezervi           : {structure.foam_reserve} lt
Bakım Maliyeti          : {maintenance} TL
--------------------------------------------------
"""
                        else:
                            block = f"""
--------------------------------------------------
[GENEL YAPI KAYDI]
ID                      : {structure.structure_id}
İsim                    : {structure.name}
Adres                   : {structure.address}
Kapasite                : {structure.capacity}
Doluluk                 : {structure.current_occupancy}
Konum                   : {structure.location}
Bakım Maliyeti          : {maintenance} TL
--------------------------------------------------
"""
                        f.write(block + "\n")
                else:
                    f.write("\n[HATA] SİSTEMDE KAYITLI YAPI BULUNAMADI\n")
                    
        except Exception as e:
            print(f"[HATA] Altyapı dosyası güncellenemedi: {e}")

    def delete_criminal_from_file(self, criminal_id):
        target_str = f"[SUÇLU KAYIT RAPORU] - TC: {criminal_id}"
        
        try:
            with open(self.criminal_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            if target_str not in content:
                print(f"[UYARI] Dosyada {criminal_id} TC'li suçlu bulunamadı")
                return
            
            blocks = content.split("==================================================")
            filtered_blocks = [block for block in blocks if target_str not in block]
            
            with open(self.criminal_file, "w", encoding="utf-8") as f:
                f.write("==================================================".join(filtered_blocks))
            
            print(f"[BİLGİ] {criminal_id} TC'li suçlu dosyadan başarıyla silindi")
                
        except Exception as e:
            print(f"[HATA] Dosyadan silme işlemi başarısız: {e}")

    def delete_victim_from_file(self, victim_id):
        target_str = f"[MAĞDUR KAYIT RAPORU] - TC: {victim_id}"
        
        try:
            with open(self.victim_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            if target_str not in content:
                print(f"[UYARI] Dosyada {victim_id} TC'li mağdur bulunamadı")
                return
            
            blocks = content.split("==================================================")
            filtered_blocks = [block for block in blocks if target_str not in block]
            
            with open(self.victim_file, "w", encoding="utf-8") as f:
                f.write("==================================================".join(filtered_blocks))
            
            print(f"[BİLGİ] {victim_id} TC'li mağdur dosyadan başarıyla silindi")
                
        except Exception as e:
            print(f"[HATA] Dosyadan silme işlemi başarısız: {e}")

    def delete_structure_from_file(self, structure_id):
        target_str = f"ID                      : {structure_id}"
        separator = "--------------------------------------------------"
        
        try:
            with open(self.structure_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            new_lines = []
            deleted = False
            
            target_index = -1
            for i, line in enumerate(lines):
                if target_str in line:
                    target_index = i
                    break
            
            if target_index == -1:
                print(f"[UYARI] Dosyada {structure_id} ID'li yapı bulunamadı")
                return
            
            start_delete_index = target_index - 1
            end_delete_index = -1
            
            for i in range(target_index, len(lines)):
                if separator in lines[i].strip() and i > target_index:
                    end_delete_index = i
                    break
            
            for i in range(len(lines)):
                if start_delete_index <= i <= end_delete_index:
                    deleted = True
                    continue
                new_lines.append(lines[i])

            if deleted:
                with open(self.structure_file, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
                print(f"[BİLGİ] {structure_id} ID'li yapı dosyadan başarıyla silindi")
                
        except Exception as e:
            print(f"[HATA] Dosyadan silme işlemi başarısız: {e}")
