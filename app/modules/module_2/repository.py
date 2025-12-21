import json
import os
from .implementations import ElectricityMeter, WaterMeter, GasMeter

class MeterRepository:
    """
    Veritabanı İşlemleri Sınıfı (Repository Pattern).
    -------------------------------------------------------------------------
    Sayaç verilerinin kalıcı olarak saklanmasını (Persistence) ve
    yönetilmesini sağlar. Veriler JSON formatında tutulur.
    """

    def __init__(self):
        # Dosya yolunu dinamik olarak belirle
        # Bu dosyanın olduğu klasörün içine 'data' klasörü oluşturacağız
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.base_dir, "data")
        self.file_path = os.path.join(self.data_dir, "meters.json")
        
        # Data klasörü yoksa oluştur
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
        # JSON dosyası yoksa boş bir liste ile başlat
        if not os.path.exists(self.file_path):
            self._save_to_file([])

    def _save_to_file(self, data):
        """Verileri JSON dosyasına yazar."""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def _load_from_file(self):
        """Verileri JSON dosyasından okur."""
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def add(self, meter):
        """
        Yeni bir sayaç nesnesini veritabanına ekler.
        """
        current_data = self._load_from_file()
        
        # 1. ADIM: Verileri senin base.py yapına (Getter Metotlarına) göre çekiyoruz
        # 'get_id' metodunu kullanıyoruz, çünkü değişkene direkt erişim kapalı (_id)
        
        # ID Çekme
        if hasattr(meter, "get_id"):
            m_id = meter.get_id()
        else:
            # Yedek plan: Direkt _id'ye eriş
            m_id = getattr(meter, "_id", "Unknown-ID")

        # Tip Çekme (base.py'de get_type yok, o yüzden _type özelliğine bakıyoruz)
        m_type = getattr(meter, "_type", "Unknown-Type")

        # Tüketim Çekme (get_usage_amount metodu var)
        if hasattr(meter, "get_usage_amount"):
            m_usage = meter.get_usage_amount()
        else:
            m_usage = getattr(meter, "_usage_amount", 0.0)

        # Konum Çekme (get_location metodu var)
        if hasattr(meter, "get_location"):
            m_location = meter.get_location()
        else:
            m_location = getattr(meter, "_location", "Unknown-Location")

        meter_dict = {
            "type": m_type, 
            "id": m_id,
            "usage": m_usage,
            "location": m_location,
            "status": "Active"
        }

        # 2. ADIM: Türe özel alanları ekle (Voltaj, Basınç vb.)
        # Bu özellikler implementations.py içinde tanımlı olduğu için genellikle public'tir (self.voltage)
        if "Electricity" in m_type:
            meter_dict["voltage"] = getattr(meter, "voltage", 220)
            
        elif "Water" in m_type:
            meter_dict["pipe_diameter"] = getattr(meter, "pipe_diameter", 0.5)
            
        elif "Gas" in m_type:
            meter_dict["pressure"] = getattr(meter, "pressure", 4)

        current_data.append(meter_dict)
        self._save_to_file(current_data)
        
        print(f"[Repo] {m_id} başarıyla kaydedildi.")
        
    def get_all(self):
        """Tüm kayıtlı sayaçları getirir."""
        return self._load_from_file()

    def get_by_id(self, meter_id):
        """ID'ye göre sayaç arar."""
        data = self._load_from_file()
        for item in data:
            if item.get("id") == meter_id:
                return item
        return None