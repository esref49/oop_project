import os
from datetime import datetime

class SystemLogger:
    """
    Sistem Olay Günlüğü (Logging) Yöneticisi.
    -------------------------------------------------------------------------
    Bu sınıf, sistemde meydana gelen kritik olayları, hataları ve uyarıları
    hem konsola yazar hem de kalıcı olarak bir .log dosyasına kaydeder.
    
    Kullanım Amacı:
    - Hata ayıklamayı (Debugging) kolaylaştırmak.
    - Sistem geçmişini denetlenebilir (Auditable) hale getirmek.
    """

    def __init__(self, log_file_name="system_logs.txt"):
        """
        Logger başlatıcı.
        
            log_file_name (str): Logların tutulacağı dosya adı.
        """
        self.module_dir = os.path.dirname(os.path.abspath(__file__))
        self.log_dir = os.path.join(self.module_dir, "logs")
        self.log_file = os.path.join(self.log_dir, log_file_name)
        
        # Log klasörü yoksa oluştur
        self._ensure_log_dir_exists()

    def _ensure_log_dir_exists(self):
        """Log klasörünün varlığını kontrol eder, yoksa oluşturur."""
        if not os.path.exists(self.log_dir):
            try:
                os.makedirs(self.log_dir)
            except OSError as e:
                print(f"[CRITICAL] Log klasörü oluşturulamadı: {e}")

    def _get_timestamp(self):
        """Şu anki zamanı formatlı string olarak döndürür."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _write_to_file(self, level, message):
        """Mesajı dosyaya append (ekleme) modunda yazar."""
        timestamp = self._get_timestamp()
        formatted_message = f"[{timestamp}] [{level}] {message}\n"
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(formatted_message)
        except Exception as e:
            # Log yazarken hata olursa konsola bas ama programı durdurma
            print(f"Log yazma hatası: {e}")

    def log_info(self, message):
        """
        Bilgilendirme mesajı kaydeder.
        Örnek: "Yeni müşteri eklendi."
        """
        self._write_to_file("INFO", message)
        # İsteğe bağlı: Konsola da basılabilir
        # print(f"[INFO] {message}")

    def log_warning(self, message):
        """
        Uyarı mesajı kaydeder.
        Örnek: "Stok azaldı."
        """
        self._write_to_file("WARNING", message)
        print(f"[UYARI] {message}")

    def log_error(self, message):
        """
        Hata mesajı kaydeder.
        Örnek: "Veritabanı bağlantısı koptu."
        """
        self._write_to_file("ERROR", message)
        print(f"[HATA] {message}")

    def log_critical(self, message):
        """
        Kritik hata mesajı kaydeder.
        Örnek: "Sistem çöküyor!"
        """
        self._write_to_file("CRITICAL", message)
        print(f"!!! [KRİTİK HATA] {message} !!!")

    def read_logs(self, limit=10):
        """
        Son kaydedilen logları okur.
        
        Args:
            limit (int): Okunacak son satır sayısı.
        """
        if not os.path.exists(self.log_file):
            return ["Henüz log kaydı yok."]
            
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                return lines[-limit:]
        except Exception:
            return ["Log dosyası okunamadı."]

    def clear_logs(self):
        """Log dosyasını temizler."""
        try:
            open(self.log_file, 'w').close()
            print("Log dosyası temizlendi.")
        except Exception as e:
            print(f"Temizleme hatası: {e}")

# Test Bloğu
if __name__ == "__main__":
    logger = SystemLogger()
    logger.log_info("Logger sistemi başlatıldı.")
    logger.log_warning("Disk alanı azalıyor.")
    logger.log_error("Test hatası denemesi.")