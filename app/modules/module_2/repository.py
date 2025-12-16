import json
import os
from datetime import datetime

class UtilityRepository:
    """
    Veri erişim katmanı (Data Access Layer).
    Sayaç verilerini yönetir, filtreler ve (simüle edilmiş) veritabanı işlemlerini yapar.
    """

    def __init__(self):
        # Bellek içi (In-Memory) veritabanı
        self._storage = []
        # Yedekleme dosyasının adı
        self._db_file = "utilities_backup.json"

    def add(self, utility_obj):
        """Yeni bir sayaç nesnesini depoya ekler."""
        # Aynı ID'ye sahip sayaç var mı kontrol et
        if self.get_by_id(utility_obj.get_id()):
            print(f"HATA: {utility_obj.get_id()} ID'li sayaç zaten kayıtlı!")
            return False
        
        self._storage.append(utility_obj)
        print(f"[Repo] {utility_obj.get_id()} başarıyla kaydedildi.")
        return True

    def get_by_id(self, id):
        """ID bilgisine göre sayaç arar."""
        for item in self._storage:
            if item.get_id() == id:
                return item
        return None

    def get_all(self):
        """Tüm kayıtlı sayaçları döndürür."""
        return self._storage

    def delete(self, id):
        """ID bilgisine göre sayacı sistemden siler."""
        meter = self.get_by_id(id)
        if meter:
            self._storage.remove(meter)
            print(f"[Repo] {id} silindi.")
            return True
        print(f"[Repo] Hata: Silinecek {id} bulunamadı.")
        return False

    def filter_by_type(self, meter_type):
        """Belirli bir türdeki (örn: Electricity) sayaçları listeler."""
        result = [m for m in self._storage if m._type == meter_type]
        return result

    def filter_by_status(self, is_active=True):
        """Aktif veya Pasif durumdaki sayaçları filtreler."""
        # _is_active özelliği base class'tan gelir
        result = [m for m in self._storage if getattr(m, '_is_active', False) == is_active]
        return result

    def save_to_json(self):
        """
        Mevcut verileri bir JSON dosyasına yedekler.
        (Dosya tabanlı veritabanı simülasyonu)
        """
        data_export = []
        for meter in self._storage:
            # Nesneyi sözlüğe (dict) çeviriyoruz
            data_export.append({
                "id": meter.get_id(),
                "type": meter._type,
                "location": meter.get_location(),
                "usage": meter.get_usage_amount(),
                "backup_date": str(datetime.now())
            })
        
        try:
            with open(self._db_file, 'w', encoding='utf-8') as f:
                json.dump(data_export, f, ensure_ascii=False, indent=4)
            print(f"[Repo] Veriler '{self._db_file}' dosyasına yedeklendi.")
            return True
        except Exception as e:
            print(f"[Repo] Yedekleme hatası: {e}")
            return False

    def load_from_json(self):
        """
        JSON dosyasından verileri okuma simülasyonu.
        Gerçek bir projede nesneleri burada tekrar oluştururuz.
        """
        if not os.path.exists(self._db_file):
            print("[Repo] Yedek dosyası bulunamadı.")
            return []

        try:
            with open(self._db_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"[Repo] {len(data)} adet kayıt dosyadan okundu.")
            return data
        except Exception as e:
            print(f"[Repo] Okuma hatası: {e}")
            return []

    def count_total_usage(self):
        """Depodaki tüm sayaçların toplam kullanım miktarını hesaplar."""
        total = 0
        for meter in self._storage:
            total += meter.get_usage_amount()
        return total