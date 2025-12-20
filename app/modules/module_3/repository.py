import datetime

class EmergencyRepository():
    def __init__(self):
        self.old_cases = {}
        self.unit = {}
        self.case_counter = self.get_last_case_id()

    def get_last_case_id(self):
        file_name = "old_case_logs.txt"
        try:
            with open(file_name, "r", encoding="utf-8") as f:
                content = f.read()
                # Dosyada kaç kere 'ID: Olay-' geçtiğini sayıyoruz.
                # Mesela 5 kayıt varsa, sayaç 5 olacak. Yeni kayıt 6 diye devam edecek.
                count = content.count("ID: Olay-")
                return count
        except FileNotFoundError:
            # Dosya yoksa henüz ilk olaydır.
            return 0

    def save_case(self, case_data):
        self.case_counter += 1
        current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        
        # --- GÖRSEL DÜZENLEME ---
        # f-string içinde çok satırlı metin (multiline string) kullanıyoruz.
        # "=" ve "-" işaretleriyle güzel bir çerçeve yapıyoruz.
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
            with open("old_case_logs.txt", "a", encoding="utf-8") as file:
                file.write(log_block + "\n") # Her rapordan sonra bir boşluk bırakalım.
            
            print(f"[LOG] Olay-{self.case_counter} başarıyla dosyaya işlendi.")
            
        except Exception as e:
            print(f"[HATA] Dosyaya yazarken sorun çıktı: {e}")

    def event_history(self, message):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{now}] -> {message}"
        
        log_id = f"Log_{len(self.old_cases) + 1}"
        self.old_cases[log_id] = log_entry

        try:
            with open("old_case_logs.txt", "a", encoding="utf-8") as file:
                file.write(log_entry + "\n")
            print("[+] Vaka veritabanına kaydedildi")
        except Exception as hata:
            print(f"Log yazarken hata oluştu: {hata}")

    def unit_datas(self):
        pass