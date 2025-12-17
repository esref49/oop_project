from datetime import datetime

# Sosyal hizmet ve başvuru verilerini yöneten repository sınıfı
class SosyalHizmetRepository:
    # Tüm repository instance'ları için sayaç
    _instance_sayisi = 0
    
    # Constructor - veri yapılarını başlatır
    def __init__(self):
        self._hizmetler = []
        self._basvurular = []
        self._vatandaslar = []
        self._log_kayitlari = []
        self._basvuru_id_sayac = 1
        self._hizmet_istatistikleri = {}
        SosyalHizmetRepository._instance_sayisi += 1
    
    # Hizmetler listesini döndüren getter metodu
    @property
    def hizmetler(self):
        return self._hizmetler
    
    # Başvurular listesini döndüren getter metodu
    @property
    def basvurular(self):
        return self._basvurular
    
    # Vatandaşlar listesini döndüren getter metodu
    @property
    def vatandaslar(self):
        return self._vatandaslar
    
    # Yeni hizmet ekleyen metod
    def hizmet_ekle(self, hizmet):
        if hizmet not in self._hizmetler:
            self._hizmetler.append(hizmet)
            self._log_ekle(f"Yeni hizmet eklendi: {hizmet.name}")
            return f"{hizmet.name} başarıyla eklendi"
        return "Hizmet zaten mevcut"
    
    # Tüm hizmetleri döndüren metod
    def hizmetleri_getir(self):
        return self._hizmetler
    
    # ID'ye göre hizmet bulan metod
    def hizmet_bul(self, service_id):
        for hizmet in self._hizmetler:
            if hizmet.service_id == service_id:
                return hizmet
        return None
    
    # Duruma göre hizmetleri filtreleyen metod
    def hizmetleri_duruma_gore_getir(self, durum):
        return [h for h in self._hizmetler if h.status == durum]
    
    # Hedef gruba göre hizmetleri filtreleyen metod
    def hedef_gruba_gore_hizmetler(self, hedef_grup):
        return [h for h in self._hizmetler if h.target_group == hedef_grup]
    
    # Hizmet silen metod
    def hizmet_sil(self, service_id):
        for hizmet in self._hizmetler:
            if hizmet.service_id == service_id:
                self._hizmetler.remove(hizmet)
                self._log_ekle(f"Hizmet silindi: {hizmet.name}")
                return f"{hizmet.name} silindi"
        return "Hizmet bulunamadı"
    
    # Yeni başvuru ekleyen metod
    def basvuru_ekle(self, basvuru):
        basvuru["id"] = self._basvuru_id_sayac
        basvuru["tarih"] = datetime.now()
        self._basvurular.append(basvuru)
        self._basvuru_id_sayac += 1
        self._log_ekle(f"Yeni başvuru: {basvuru.get('vatandas', 'Bilinmeyen')}")
        return basvuru["id"]
    
    # Tüm başvuruları döndüren metod
    def basvurulari_getir(self):
        return self._basvurular
    
    # ID'ye göre başvuru bulan metod
    def basvuru_bul(self, basvuru_id):
        for basvuru in self._basvurular:
            if basvuru.get("id") == basvuru_id:
                return basvuru
        return None
    
    # Duruma göre başvuruları filtreleyen metod
    def basvurulari_duruma_gore_getir(self, durum):
        return [b for b in self._basvurular if b.get("durum") == durum]
    
    # Hizmete göre başvuruları filtreleyen metod
    def hizmete_gore_basvurular(self, hizmet_adi):
        return [b for b in self._basvurular if b.get("hizmet") == hizmet_adi]
    
    # Vatandaşa göre başvuruları filtreleyen metod
    def vatandasa_gore_basvurular(self, vatandas_adi):
        return [b for b in self._basvurular if b.get("vatandas") == vatandas_adi]
    
    # Başvuru durumunu güncelleyen metod
    def basvuru_durumu_guncelle(self, basvuru_id, yeni_durum):
        basvuru = self.basvuru_bul(basvuru_id)
        if basvuru:
            basvuru["durum"] = yeni_durum
            basvuru["guncelleme_tarihi"] = datetime.now()
            self._log_ekle(f"Başvuru {basvuru_id} durumu güncellendi: {yeni_durum}")
            return True
        return False
    
    # Başvuru silen metod
    def basvuru_sil(self, basvuru_id):
        basvuru = self.basvuru_bul(basvuru_id)
        if basvuru:
            self._basvurular.remove(basvuru)
            self._log_ekle(f"Başvuru silindi: {basvuru_id}")
            return True
        return False
    
    # Yeni vatandaş ekleyen metod
    def vatandas_ekle(self, vatandas):
        if vatandas not in self._vatandaslar:
            self._vatandaslar.append(vatandas)
            self._log_ekle(f"Yeni vatandaş: {vatandas.get('ad', 'Bilinmeyen')}")
            return True
        return False
    
    # Tüm vatandaşları döndüren metod
    def vatandaslari_getir(self):
        return self._vatandaslar
    
    # Vatandaş bulan metod
    def vatandas_bul(self, ad):
        for vatandas in self._vatandaslar:
            if vatandas.get("ad") == ad:
                return vatandas
        return None
    
    # Gelir aralığına göre vatandaşları filtreleyen metod
    def gelir_araligina_gore_vatandaslar(self, min_gelir, max_gelir):
        return [v for v in self._vatandaslar if min_gelir <= v.get("gelir", 0) <= max_gelir]
    
    # Log kaydı ekleyen metod
    def _log_ekle(self, mesaj):
        log = {
            "tarih": datetime.now(),
            "mesaj": mesaj
        }
        self._log_kayitlari.append(log)
    
    # Log kayıtlarını döndüren metod
    def loglari_getir(self):
        return self._log_kayitlari
    
    # Son N log kaydını döndüren metod
    def son_loglari_getir(self, n=10):
        return self._log_kayitlari[-n:]
    
    # Hizmet istatistiklerini hesaplayan metod
    def hizmet_istatistikleri_hesapla(self):
        istatistikler = {}
        for hizmet in self._hizmetler:
            hizmet_adi = hizmet.name
            basvurular = self.hizmete_gore_basvurular(hizmet_adi)
            istatistikler[hizmet_adi] = {
                "toplam_basvuru": len(basvurular),
                "onaylanan": len([b for b in basvurular if b.get("durum") == "onaylandi"]),
                "reddedilen": len([b for b in basvurular if b.get("durum") == "reddedildi"]),
                "bekleyen": len([b for b in basvurular if b.get("durum") == "beklemede"])
            }
        return istatistikler
    
    # Toplam başvuru sayısını döndüren metod
    def toplam_basvuru_sayisi(self):
        return len(self._basvurular)
    
    # Onaylanan başvuru sayısını döndüren metod
    def onaylanan_basvuru_sayisi(self):
        return len(self.basvurulari_duruma_gore_getir("onaylandi"))
    
    # Reddedilen başvuru sayısını döndüren metod
    def reddedilen_basvuru_sayisi(self):
        return len(self.basvurulari_duruma_gore_getir("reddedildi"))
    
    # Bekleyen başvuru sayısını döndüren metod
    def bekleyen_basvuru_sayisi(self):
        return len(self.basvurulari_duruma_gore_getir("beklemede"))
    
    # Toplam destek tutarını hesaplayan metod
    def toplam_destek_tutari(self):
        toplam = 0
        for basvuru in self._basvurular:
            if basvuru.get("durum") == "onaylandi":
                toplam += basvuru.get("miktar", 0)
        return toplam
    
    # Ortalama destek tutarını hesaplayan metod
    def ortalama_destek_tutari(self):
        onaylanan = self.onaylanan_basvuru_sayisi()
        if onaylanan > 0:
            return self.toplam_destek_tutari() / onaylanan
        return 0
    
    # Tarih aralığına göre başvuruları filtreleyen metod
    def tarih_araligina_gore_basvurular(self, baslangic, bitis):
        return [b for b in self._basvurular 
                if baslangic <= b.get("tarih", datetime.min) <= bitis]
    
    # En çok başvuru yapan vatandaşları bulan metod
    def en_cok_basvuru_yapanlar(self, limit=5):
        vatandas_sayaci = {}
        for basvuru in self._basvurular:
            vatandas = basvuru.get("vatandas")
            vatandas_sayaci[vatandas] = vatandas_sayaci.get(vatandas, 0) + 1
        sirali = sorted(vatandas_sayaci.items(), key=lambda x: x[1], reverse=True)
        return sirali[:limit]
    
    # En popüler hizmeti bulan metod
    def en_populer_hizmet(self):
        hizmet_sayaci = {}
        for basvuru in self._basvurular:
            hizmet = basvuru.get("hizmet")
            hizmet_sayaci[hizmet] = hizmet_sayaci.get(hizmet, 0) + 1
        if hizmet_sayaci:
            return max(hizmet_sayaci.items(), key=lambda x: x[1])
        return None
    
    # Veritabanını temizleyen metod
    def veritabanini_temizle(self):
        self._hizmetler.clear()
        self._basvurular.clear()
        self._vatandaslar.clear()
        self._log_kayitlari.clear()
        self._basvuru_id_sayac = 1
        self._log_ekle("Veritabanı temizlendi")
        return "Tüm veriler temizlendi"
    
    # Yedekleme işlemi yapan metod
    def yedekle(self):
        yedek = {
            "hizmetler": self._hizmetler.copy(),
            "basvurular": self._basvurular.copy(),
            "vatandaslar": self._vatandaslar.copy(),
            "tarih": datetime.now()
        }
        return yedek
    
    # Özet rapor oluşturan metod
    def ozet_rapor(self):
        return {
            "toplam_hizmet": len(self._hizmetler),
            "toplam_basvuru": self.toplam_basvuru_sayisi(),
            "onaylanan": self.onaylanan_basvuru_sayisi(),
            "reddedilen": self.reddedilen_basvuru_sayisi(),
            "bekleyen": self.bekleyen_basvuru_sayisi(),
            "toplam_destek": self.toplam_destek_tutari(),
            "ortalama_destek": self.ortalama_destek_tutari(),
            "toplam_vatandas": len(self._vatandaslar)
        }
    
    # String temsilini döndüren metod
    def __str__(self):
        return f"Repository(hizmetler={len(self._hizmetler)}, basvurular={len(self._basvurular)})"
    
    # Toplam instance sayısını döndüren class metodu
    @classmethod
    def instance_sayisi(cls):
        return cls._instance_sayisi
    
    # Yeni repository oluşturan class metodu
    @classmethod
    def yeni_repository_olustur(cls):
        return cls()
    
    # Repository sıfırlayan class metodu
    @classmethod
    def instance_sayisini_sifirla(cls):
        cls._instance_sayisi = 0
        return "Instance sayısı sıfırlandı"
    
    # Desteklenen başvuru durumlarını döndüren static metod
    @staticmethod
    def desteklenen_durumlar():
        return ["beklemede", "onaylandi", "reddedildi", "iptal"]
    
    # Maksimum başvuru limitini döndüren static metod
    @staticmethod
    def maksimum_basvuru_limiti():
        return 1000
    
    # Veri doğrulama kurallarını döndüren static metod
    @staticmethod
    def veri_dogrulama_kurallari():
        return {
            "min_gelir": 0,
            "max_gelir": 100000,
            "min_yaş": 0,
            "max_yaş": 120
        }
