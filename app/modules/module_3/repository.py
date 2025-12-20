import datetime

class EmergencyRepository():
    def __init__(self):
        self.old_cases = {}
        self.status_file = "units_log.txt"
        self.file_name = "case_log.txt"
        self.event_history_file = "event_history_log.txt"
        self.case_counter = self.get_last_case_id()

    # Loglara bakarak olayın kaçıncı olay olduğunu belirler
    def get_last_case_id(self):
        try:
            with open(self.file_name, "r", encoding="utf-8") as f:
                content = f.read()
                # Dosyada kaç kere 'ID: Olay-' geçtiğini sayıyoruz
                # Mesela 5 kayıt varsa, sayaç 5 olacak. Yeni kayıt 6 diye devam edecek
                count = content.count("ID: Olay-")
                return count
        except FileNotFoundError:
            # Dosya yoksa henüz ilk olaydır.
            return 0

    def save_case(self, case_data):
        self.case_counter += 1
        current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        
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
Atanan Birimler   : {case_data.get('assigned_unit_ids', 'Atama Yapılamadı')}
Vaka Durumu       : {case_data.get('status', 'Aktif')}
==================================================
"""

        try:
            with open(self.file_name, "a", encoding="utf-8") as file:
                file.write(log_block + "\n") # Her rapordan sonra bir boşluk bırakır
            
            print(f"[LOG] Olay-{self.case_counter} başarıyla dosyaya işlendi")
            
        except Exception as e:
            print(f"[HATA] Dosyaya yazarken sorun çıktı: {e}")

    # Filodaki tüm araçların durumunu 'save_case' benzeri şık bir formatta units_log.txt dosyasına yazar
    def save_unit_info(self, all_units):
        
        current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
        try:
            # "w" write modu ile dosyayı açıyoruz
            with open(self.status_file, "w", encoding="utf-8") as f:
                
                main_header = f"""
==================================================
         CANLI FİLO TAKİP SİSTEMİ
         Rapor Saati : {current_time}
         Araç Sayısı : {len(all_units)}
==================================================
"""
                f.write(main_header + "\n")
                
                # Araçları limlik kartlarını tek tek dosyaya yazdırır
                if all_units:
                    for unit in all_units:
                        # Her birimin kendi süslü raporunu alıp yazıyoruz
                        f.write(unit.get_detailed_status())
                        f.write("\n") # Bloklar birbirine yapışmasın
                else:
                    f.write("\n[HATA] SİSTEMDE KAYITLI ARAÇ BULUNAMADI\n")
                    
        except Exception as e:
            print(f"[HATA] Filo dosyası güncellenemedi: {e}")

    # ID ye göre istediğimiz aracı veritabanından silmeye yarar
    def delete_unit_from_file(self, unit_id):
        target_str = f"[ARAÇ DURUM KARTI] - ID: {unit_id}"
        separator = "=================================================="
        
        try:
            # Dosyadaki tüm satırları okuyup bir listeye alır
            with open(self.status_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            new_lines = []
            deleted = False
            
            # Satırları gezerek silinecek aracın ID'sinin bulunduğu satır numarasını tespit eder
            target_index = -1
            for i, line in enumerate(lines):
                if target_str in line:
                    target_index = i
                    break
            
            # Eğer ID dosyada yoksa işlemi durdurur
            if target_index == -1:
                print(f"[UYARI] Dosyada {unit_id} ID'li araç bulunamadı")
                return
            
            # Silinecek bloğun üst sınır çizgisini (başlangıç noktasını) belirler
            start_delete_index = target_index - 1 
            end_delete_index = -1
            
            # Hedef satırdan aşağı doğru inerek bloğun bittiği alt çizgi satırını belirler
            for i in range(target_index, len(lines)):
                if separator in lines[i].strip():
                    end_delete_index = i
                    break
            
            # Belirlenen aralıkta kalan satırları atlayıp diğerlerini yeni listeye ekler
            for i in range(len(lines)):
                if start_delete_index <= i <= end_delete_index:
                    deleted = True
                    continue
                
                new_lines.append(lines[i])

            # Silme işlemi yapıldıysa güncel listeyi dosyaya tekrar yazar
            if deleted:
                with open(self.status_file, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
                print(f"[BİLGİ] {unit_id} ID'li araç dosyadan başarıyla silindi")
                
        except Exception as e:
            print(f"[HATA] Dosyadan silme işlemi başarısız: {e}")

    # Vaka sırasında gerçekleşen adımları ayrı bir veritabanına kaydeder 
    def save_event_history(self, message):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        
        try:
            # Dosyayı "a" (append) moduyla açar ve adımları alt alta ekler
            with open(self.event_history_file, "a", encoding="utf-8") as f:
                f.write(f"[{current_time}] {message}\n")
        except Exception as e:
            print(f"[HATA] Müdahale kaydı yapılamadı: {e}")