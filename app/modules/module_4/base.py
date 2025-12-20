from abc import ABC, abstractmethod
from datetime import datetime

# Sosyal hizmetler için temel abstract sınıf
class SocialService(ABC):
    # Tüm hizmetler için ortak sayaç
    _toplam_hizmet_sayisi = 0
    
    # Constructor metodu - her hizmet için temel özellikleri tanımlar
    def __init__(self, service_id, name, target_group):
        self._service_id = service_id
        self._name = name
        self._target_group = target_group
        self._status = "pasif"
        self._olusturma_tarihi = datetime.now()
        self._basvuru_sayisi = 0
        self._toplam_destek_miktari = 0
        self._oncelik_seviyesi = 1
        SocialService._toplam_hizmet_sayisi += 1
    
    # Hizmet ID'sini döndüren getter metodu
    @property
    def service_id(self):
        return self._service_id
    
    # Hizmet adını döndüren getter metodu
    @property
    def name(self):
        return self._name
    
    # Hedef grubu döndüren getter metodu
    @property
    def target_group(self):
        return self._target_group
    
    # Hizmet durumunu döndüren getter metodu
    @property
    def status(self):
        return self._status
    
    # Hizmet durumunu değiştiren setter metodu
    @status.setter
    def status(self, value):
        if value in ["aktif", "pasif", "beklemede"]:
            self._status = value
        else:
            raise ValueError("Geçersiz durum değeri")
    
    # Başvuru sayısını döndüren getter metodu
    @property
    def basvuru_sayisi(self):
        return self._basvuru_sayisi
    
    # Öncelik seviyesini döndüren getter metodu
    @property
    def oncelik_seviyesi(self):
        return self._oncelik_seviyesi
    
    # Öncelik seviyesini değiştiren setter metodu
    @oncelik_seviyesi.setter
    def oncelik_seviyesi(self, value):
        if 1 <= value <= 5:
            self._oncelik_seviyesi = value
        else:
            raise ValueError("Öncelik seviyesi 1-5 arasında olmalıdır")
    
    # Vatandaşın hizmete uygunluğunu kontrol eden abstract metod
    @abstractmethod
    def uygunluk_kontrolu(self, vatandas):
        pass
    
    # Destek miktarını hesaplayan abstract metod
    @abstractmethod
    def destek_hesapla(self):
        pass
    
    # Hizmeti aktif duruma getiren metod
    def aktif_et(self):
        self._status = "aktif"
        return f"{self._name} hizmeti aktif edildi"
    
    # Hizmeti pasif duruma getiren metod
    def pasif_et(self):
        self._status = "pasif"
        return f"{self._name} hizmeti pasif edildi"
    
    # Başvuru sayısını artıran metod
    def basvuru_ekle(self):
        self._basvuru_sayisi += 1
        return self._basvuru_sayisi
    
    # Toplam destek miktarını güncelleyen metod
    def destek_miktari_guncelle(self, miktar):
        self._toplam_destek_miktari += miktar
        return self._toplam_destek_miktari
    
    # Ortalama destek miktarını hesaplayan metod
    def ortalama_destek_hesapla(self):
        if self._basvuru_sayisi == 0:
            return 0
        return self._toplam_destek_miktari / self._basvuru_sayisi
    
    # Hizmetin bilgilerini string olarak döndüren metod
    def hizmet_bilgisi(self):
        return f"Hizmet: {self._name}, Hedef: {self._target_group}, Durum: {self._status}"
    
    # Hizmetin istatistiklerini döndüren metod
    def istatistik_getir(self):
        return {
            "hizmet_adi": self._name,
            "basvuru_sayisi": self._basvuru_sayisi,
            "toplam_destek": self._toplam_destek_miktari,
            "ortalama_destek": self.ortalama_destek_hesapla(),
            "durum": self._status
        }
    
    # String temsilini döndüren magic metod
    def __str__(self):
        return f"SocialService({self._name}, {self._target_group}, {self._status})"
    
    # Hizmet servis tipini 
    @classmethod
    def servis_tipi(cls):
        return cls.__name__
    
    # Toplam hizmet sayısın
    @classmethod
    def toplam_hizmet_sayisi(cls):
        return cls._toplam_hizmet_sayisi
    
    # Hizmet sayısını 
    @classmethod
    def hizmet_sayisini_sifirla(cls):
        cls._toplam_hizmet_sayisi = 0
        return "Hizmet sayısı sıfırlandı"
    
    # Belediye politikasını 
    @staticmethod
    def belediye_politikasi():
        return "Sosyal adalet ve eşit destek"
    
    # Hizmet öncelik 
    @staticmethod
    def oncelik_kategorileri():
        return {
            1: "Düşük",
            2: "Normal",
            3: "Orta",
            4: "Yüksek",
            5: "Acil"
        }
    
    # Minimum destek
    @staticmethod
    def minimum_destek_tutari():
        return 500
    
    # Maksimum destek 
    @staticmethod
    def maksimum_destek_tutari():
        return 10000
