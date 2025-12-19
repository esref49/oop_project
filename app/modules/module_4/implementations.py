from .base import SocialService
from datetime import datetime

# Düşük gelirli vatandaşlara gıda yardımı sağlayan sınıf
class GidaYardimi(SocialService):
    # Gıda yardımı için özel sayaç
    _gida_yardimi_sayisi = 0
    
    # Constructor - gıda yardımı için gerekli parametreleri alır
    def __init__(self, service_id, aylik_tutar, ekstra_cocuk_yuzdesi=10):
        super().__init__(service_id, "Gıda Yardımı", "Düşük Gelir")
        self._aylik_tutar = aylik_tutar
        self._ekstra_cocuk_yuzdesi = ekstra_cocuk_yuzdesi
        self._dagitim_sayisi = 0
        self._son_dagitim_tarihi = None
        self._yararlanicilar = []
        GidaYardimi._gida_yardimi_sayisi += 1
    
    # Aylık tutarı döndüren getter metodu
    @property
    def aylik_tutar(self):
        return self._aylik_tutar
    
    # Aylık tutarı değiştiren setter metodu
    @aylik_tutar.setter
    def aylik_tutar(self, value):
        if value > 0:
            self._aylik_tutar = value
        else:
            raise ValueError("Aylık tutar pozitif olmalıdır")
    
    # Yararlanıcıları döndüren getter metodu
    @property
    def yararlanicilar(self):
        return self._yararlanicilar
    
    # Vatandaşın gıda yardımına uygun olup olmadığını kontrol eden metod
    def uygunluk_kontrolu(self, vatandas):
        gelir_limiti = 10000
        if "gelir" in vatandas and vatandas["gelir"] < gelir_limiti:
            return True
        return False
    
    # Vatandaş için destek miktarını hesaplayan metod
    def destek_hesapla(self):
        return self._aylik_tutar
    
    # Çocuk sayısına göre ekstra destek hesaplayan metod
    def cocuk_destegi_hesapla(self, cocuk_sayisi):
        ekstra = self._aylik_tutar * (self._ekstra_cocuk_yuzdesi / 100) * cocuk_sayisi
        return self._aylik_tutar + ekstra
    
    # Gelire göre özel destek hesaplayan metod
    def gelire_gore_destek(self, gelir):
        if gelir < 5000:
            return self._aylik_tutar * 1.5
        elif gelir < 7500:
            return self._aylik_tutar * 1.25
        else:
            return self._aylik_tutar
    
    # Yararlanıcı ekleyen metod
    def yararlanici_ekle(self, vatandas_adi):
        if vatandas_adi not in self._yararlanicilar:
            self._yararlanicilar.append(vatandas_adi)
            return f"{vatandas_adi} yararlanıcı listesine eklendi"
        return f"{vatandas_adi} zaten listede"
    
    # Dağıtım kaydı tutan metod
    def dagitim_kaydet(self):
        self._dagitim_sayisi += 1
        self._son_dagitim_tarihi = datetime.now()
        return f"Dağıtım kaydedildi. Toplam: {self._dagitim_sayisi}"
    
    # Son dağıtımdan bu yana geçen gün sayısını hesaplayan metod
    def son_dagitimdan_gecen_gun(self):
        if self._son_dagitim_tarihi:
            fark = datetime.now() - self._son_dagitim_tarihi
            return fark.days
        return None
    
    # Yararlanıcı sayısını döndüren metod
    def yararlanici_sayisi(self):
        return len(self._yararlanicilar)
    
    # Toplam dağıtım maliyetini hesaplayan metod
    def toplam_maliyet(self):
        return self._dagitim_sayisi * self._aylik_tutar
    
    # Yararlanıcı başına ortalama maliyeti hesaplayan metod
    def yararlanici_basina_maliyet(self):
        if len(self._yararlanicilar) > 0:
            return self.toplam_maliyet() / len(self._yararlanicilar)
        return 0
    
    # Detaylı rapor oluşturan metod
    def rapor_olustur(self):
        return {
            "hizmet_tipi": "Gıda Yardımı",
            "aylik_tutar": self._aylik_tutar,
            "dagitim_sayisi": self._dagitim_sayisi,
            "yararlanici_sayisi": len(self._yararlanicilar),
            "toplam_maliyet": self.toplam_maliyet()
        }
    
    # String temsilini döndüren metod
    def __str__(self):
        return f"GidaYardimi(tutar={self._aylik_tutar}, yararlanici={len(self._yararlanicilar)})"
    
    # Toplam gıda yardımı sayısını döndüren class metodu
    @classmethod
    def toplam_gida_yardimi_sayisi(cls):
        return cls._gida_yardimi_sayisi
    
    # Yeni gıda yardımı paketi oluşturan class metodu
    @classmethod
    def standart_paket_olustur(cls, service_id):
        return cls(service_id, 1500, 15)
    
    # Özel paket oluşturan class metodu
    @classmethod
    def ozel_paket_olustur(cls, service_id, paket_tipi):
        paketler = {
            "temel": (1000, 5),
            "standart": (1500, 10),
            "premium": (2500, 20)
        }
        if paket_tipi in paketler:
            tutar, yuzde = paketler[paket_tipi]
            return cls(service_id, tutar, yuzde)
        return cls(service_id, 1500, 10)
    
    # Gelir limitini döndüren static metod
    @staticmethod
    def gelir_limiti():
        return 10000
    
    # Minimum yardım tutarını döndüren static metod
    @staticmethod
    def minimum_yardim():
        return 500
    
    # Maksimum yardım tutarını döndüren static metod
    @staticmethod
    def maksimum_yardim():
        return 5000


# Evsiz vatandaşlara barınma desteği sağlayan sınıf
class BarinmaDestegi(SocialService):
    # Barınma desteği için özel sayaç
    _barinma_destegi_sayisi = 0
    
    # Constructor - barınma desteği için gerekli parametreleri alır
    def __init__(self, service_id, kira_limiti, konut_tipi="daire"):
        super().__init__(service_id, "Barınma Desteği", "Evsiz")
        self._kira_limiti = kira_limiti
        self._konut_tipi = konut_tipi
        self._aktif_kontratlar = []
        self._gecmis_kontratlar = []
        self._toplam_odenen_kira = 0
        BarinmaDestegi._barinma_destegi_sayisi += 1
    
    # Kira limitini döndüren getter metodu
    @property
    def kira_limiti(self):
        return self._kira_limiti
    
    # Kira limitini değiştiren setter metodu
    @kira_limiti.setter
    def kira_limiti(self, value):
        if value > 0:
            self._kira_limiti = value
        else:
            raise ValueError("Kira limiti pozitif olmalıdır")
    
    # Konut tipini döndüren getter metodu
    @property
    def konut_tipi(self):
        return self._konut_tipi
    
    # Vatandaşın barınma desteğine uygun olup olmadığını kontrol eden metod
    def uygunluk_kontrolu(self, vatandas):
        if "evi_var_mi" in vatandas:
            return vatandas["evi_var_mi"] is False
        return False
    
    # Destek miktarını hesaplayan metod
    def destek_hesapla(self):
        return self._kira_limiti
    
    # Aile büyüklüğüne göre kira desteği hesaplayan metod
    def aile_buyuklugune_gore_destek(self, kisi_sayisi):
        if kisi_sayisi <= 2:
            return self._kira_limiti * 0.7
        elif kisi_sayisi <= 4:
            return self._kira_limiti
        else:
            return self._kira_limiti * 1.3
    
    # Konut tipine göre ek destek hesaplayan metod
    def konut_tipine_gore_ek(self, konut_tipi):
        ek_oranlar = {
            "daire": 1.0,
            "müstakil": 1.2,
            "apart": 0.9,
            "hostel": 0.6
        }
        return self._kira_limiti * ek_oranlar.get(konut_tipi, 1.0)
    
    # Yeni kontrat ekleyen metod
    def kontrat_ekle(self, kontrat_bilgisi):
        self._aktif_kontratlar.append(kontrat_bilgisi)
        return f"Kontrat eklendi: {kontrat_bilgisi}"
    
    # Kontratı sonlandıran metod
    def kontrat_sonlandir(self, kontrat_id):
        for kontrat in self._aktif_kontratlar:
            if kontrat.get("id") == kontrat_id:
                self._aktif_kontratlar.remove(kontrat)
                self._gecmis_kontratlar.append(kontrat)
                return f"Kontrat sonlandırıldı: {kontrat_id}"
        return "Kontrat bulunamadı"
    
    # Aylık kira ödemesi kaydeden metod
    def kira_odemesi_kaydet(self, miktar):
        if miktar <= self._kira_limiti:
            self._toplam_odenen_kira += miktar
            return f"Ödeme kaydedildi: {miktar} TL"
        return "Miktar kira limitini aşıyor"
    
    # Aktif kontrat sayısını döndüren metod
    def aktif_kontrat_sayisi(self):
        return len(self._aktif_kontratlar)
    
    # Toplam ödenen kira tutarını döndüren metod
    def toplam_odenen_kira_getir(self):
        return self._toplam_odenen_kira
    
    # Ortalama kira ödemesini hesaplayan metod
    def ortalama_kira_hesapla(self):
        toplam_kontrat = len(self._aktif_kontratlar) + len(self._gecmis_kontratlar)
        if toplam_kontrat > 0:
            return self._toplam_odenen_kira / toplam_kontrat
        return 0
    
    # Uygun konutları filtreleyen metod
    def uygun_konutlari_filtrele(self, konut_listesi):
        uygun_konutlar = []
        for konut in konut_listesi:
            if konut.get("kira", 0) <= self._kira_limiti:
                uygun_konutlar.append(konut)
        return uygun_konutlar
    
    # Detaylı istatistik döndüren metod
    def istatistik_raporu(self):
        return {
            "aktif_kontratlar": len(self._aktif_kontratlar),
            "gecmis_kontratlar": len(self._gecmis_kontratlar),
            "toplam_odenen": self._toplam_odenen_kira,
            "ortalama_kira": self.ortalama_kira_hesapla(),
            "kira_limiti": self._kira_limiti
        }
    
    # String temsilini döndüren metod
    def __str__(self):
        return f"BarinmaDestegi(limit={self._kira_limiti}, aktif={len(self._aktif_kontratlar)})"
    
    # Toplam barınma desteği sayısını döndüren class metodu
    @classmethod
    def toplam_barinma_destegi_sayisi(cls):
        return cls._barinma_destegi_sayisi
    
    # Standart barınma paketi oluşturan class metodu
    @classmethod
    def standart_paket_olustur(cls, service_id):
        return cls(service_id, 5000, "daire")
    
    # Acil barınma paketi oluşturan class metodu
    @classmethod
    def acil_paket_olustur(cls, service_id):
        return cls(service_id, 3000, "hostel")
    
    # Minimum kira limitini döndüren static metod
    @staticmethod
    def minimum_kira_limiti():
        return 2000
    
    # Maksimum kira limitini döndüren static metod
    @staticmethod
    def maksimum_kira_limiti():
        return 8000
    
    # Desteklenen konut tiplerini döndüren static metod
    @staticmethod
    def desteklenen_konut_tipleri():
        return ["daire", "müstakil", "apart", "hostel"]


# Öğrencilere eğitim desteği sağlayan sınıf
class EgitimDestegi(SocialService):
    # Eğitim desteği için özel sayaç
    _egitim_destegi_sayisi = 0
    
    # Constructor - eğitim desteği için gerekli parametreleri alır
    def __init__(self, service_id, burs_miktari, egitim_seviyesi="lise"):
        super().__init__(service_id, "Eğitim Desteği", "Öğrenci")
        self._burs_miktari = burs_miktari
        self._egitim_seviyesi = egitim_seviyesi
        self._bursiyerler = []
        self._toplam_odenen_burs = 0
        self._basari_oranlari = {}
        EgitimDestegi._egitim_destegi_sayisi += 1
    
    # Burs miktarını döndüren getter metodu
    @property
    def burs_miktari(self):
        return self._burs_miktari
    
    # Burs miktarını değiştiren setter metodu
    @burs_miktari.setter
    def burs_miktari(self, value):
        if value > 0:
            self._burs_miktari = value
        else:
            raise ValueError("Burs miktarı pozitif olmalıdır")
    
    # Eğitim seviyesini döndüren getter metodu
    @property
    def egitim_seviyesi(self):
        return self._egitim_seviyesi
    
    # Bursiyerleri döndüren getter metodu
    @property
    def bursiyerler(self):
        return self._bursiyerler
    
    # Vatandaşın eğitim desteğine uygun olup olmadığını kontrol eden metod
    def uygunluk_kontrolu(self, vatandas):
        if "ogrenci_mi" in vatandas:
            return vatandas["ogrenci_mi"] is True
        return False
    
    # Destek miktarını hesaplayan metod
    def destek_hesapla(self):
        return self._burs_miktari
    
    # Başarı durumuna göre burs hesaplayan metod
    def basariya_gore_burs(self, ortalama):
        if ortalama >= 90:
            return self._burs_miktari * 1.5
        elif ortalama >= 80:
            return self._burs_miktari * 1.25
        elif ortalama >= 70:
            return self._burs_miktari
        else:
            return self._burs_miktari * 0.75
    
    # Eğitim seviyesine göre burs hesaplayan metod
    def seviyeye_gore_burs(self, seviye):
        carpanlar = {
            "ilkokul": 0.5,
            "ortaokul": 0.7,
            "lise": 1.0,
            "onlisans": 1.3,
            "lisans": 1.5,
            "yuksek_lisans": 2.0,
            "doktora": 2.5
        }
        return self._burs_miktari * carpanlar.get(seviye, 1.0)
    
    # Yeni bursiyer ekleyen metod
    def bursiyer_ekle(self, ogrenci_bilgisi):
        if ogrenci_bilgisi not in self._bursiyerler:
            self._bursiyerler.append(ogrenci_bilgisi)
            return f"Bursiyer eklendi: {ogrenci_bilgisi.get('ad', 'Bilinmeyen')}"
        return "Bursiyer zaten kayıtlı"
    
    # Bursiyer çıkaran metod
    def bursiyer_cikar(self, ogrenci_id):
        for bursiyer in self._bursiyerler:
            if bursiyer.get("id") == ogrenci_id:
                self._bursiyerler.remove(bursiyer)
                return f"Bursiyer çıkarıldı: {ogrenci_id}"
        return "Bursiyer bulunamadı"
    
    # Burs ödemesi kaydeden metod
    def burs_odemesi_kaydet(self, miktar):
        self._toplam_odenen_burs += miktar
        return f"Burs ödemesi kaydedildi: {miktar} TL"
    
    # Başarı oranı kaydeden metod
    def basari_orani_kaydet(self, ogrenci_id, oran):
        self._basari_oranlari[ogrenci_id] = oran
        return f"Başarı oranı kaydedildi: {ogrenci_id} - {oran}"
    
    # Ortalama başarı oranını hesaplayan metod
    def ortalama_basari_hesapla(self):
        if len(self._basari_oranlari) > 0:
            return sum(self._basari_oranlari.values()) / len(self._basari_oranlari)
        return 0
    
    # Bursiyer sayısını döndüren metod
    def bursiyer_sayisi(self):
        return len(self._bursiyerler)
    
    # Toplam ödenen burs tutarını döndüren metod
    def toplam_odenen_burs_getir(self):
        return self._toplam_odenen_burs
    
    # Bursiyer başına ortalama ödemeyi hesaplayan metod
    def bursiyer_basina_ortalama(self):
        if len(self._bursiyerler) > 0:
            return self._toplam_odenen_burs / len(self._bursiyerler)
        return 0
    
    # Başarılı bursiyerleri filtreleyen metod
    def basarili_bursiyerleri_getir(self, min_oran=70):
        basarililar = []
        for ogrenci_id, oran in self._basari_oranlari.items():
            if oran >= min_oran:
                basarililar.append((ogrenci_id, oran))
        return basarililar
    
    # Detaylı rapor oluşturan metod
    def egitim_raporu(self):
        return {
            "bursiyer_sayisi": len(self._bursiyerler),
            "toplam_odenen": self._toplam_odenen_burs,
            "ortalama_basari": self.ortalama_basari_hesapla(),
            "burs_miktari": self._burs_miktari,
            "egitim_seviyesi": self._egitim_seviyesi
        }
    
    # String temsilini döndüren metod
    def __str__(self):
        return f"EgitimDestegi(burs={self._burs_miktari}, bursiyer={len(self._bursiyerler)})"
    
    # Toplam eğitim desteği sayısını döndüren class metodu
    @classmethod
    def toplam_egitim_destegi_sayisi(cls):
        return cls._egitim_destegi_sayisi
    
    # Lise burs paketi oluşturan class metodu
    @classmethod
    def lise_paketi_olustur(cls, service_id):
        return cls(service_id, 2000, "lise")
    
    # Üniversite burs paketi oluşturan class metodu
    @classmethod
    def universite_paketi_olustur(cls, service_id):
        return cls(service_id, 3500, "lisans")
    
    # Minimum burs tutarını döndüren static metod
    @staticmethod
    def minimum_burs():
        return 1000
    
    # Maksimum burs tutarını döndüren static metod
    @staticmethod
    def maksimum_burs():
        return 10000
    
    # Desteklenen eğitim seviyelerini döndüren static metod
    @staticmethod
    def desteklenen_seviyeler():
        return ["ilkokul", "ortaokul", "lise", "onlisans", "lisans", "yuksek_lisans", "doktora"]
  