import datetime

class EmergencyRepository():
    def __init__(self):
        self.save_cases = {}
        self.old_cases = {}
        self.unit = {}
        self.case_counter = 0

    def save_case(self, case_data):
        self.case_counter += 1
        time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

        log = (
            f"[{time}] | "
            f"ID: Olay-{self.case_counter} | "
            f"Tür: {case_data.get('type', 'Bilinmiyor')} | "
            f"Konum: {case_data.get('location', '-')} | "
            f"Puan: {case_data.get('severity', 0)} | "
            f"Durum: {case_data.get('status', 'Aktif')} | "
            f"Birim: {case_data.get('assigned_unit', 'Atanmadı')}"
        )

        self.save_cases[f"Olay {self.case_counter}"] = log

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