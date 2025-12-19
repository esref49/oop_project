from datetime import datetime, timedelta

# Sosyal hizmet başvurularını yöneten ana servis sınıfı
class SosyalHizmetServisi:
    # Tüm servis instance'ları için sayaç
    _servis_sayisi = 0
    
    # Constructor - repository'yi alır ve başlatır
    def __init__(self, repository):
        self._repository = repository
        self._islem_gecmisi = []
        self._bildirimler = []
        SosyalHizmetServisi._servis_sayisi += 1
    
    # Repository'yi döndüren getter metodu
    @property
    def repository(self):
        return self._repository
    
    # İşlem geçmişini döndüren getter metodu
    @property
    def islem_gecmisi(self):
        return self._islem_gecmisi
    
    # Bildirimler listesini döndüren getter metodu
    @property
    def bildirimler(self):
        return self._bildirimler
    
    # Vatandaş için başvuru oluşturan metod
    def basvuru_olustur(self, vatandas, hizmet):
        if hizmet.uygunluk_kontrolu(vatandas):
            destek_miktari = hizmet.destek_hesapla()
            basvuru = {
                "vatandas": vatandas["ad"],
                "hizmet": hizmet.name,
                "durum": "onaylandi",
                "miktar": destek_miktari
            }
            basvuru_id = self._repository.basvuru_ekle(basvuru)
            hizmet.basvuru_ekle()
            hizmet.destek_miktari_guncelle(destek_miktari)
            self._islem_kaydet(f"Başvuru oluşturuldu: {basvuru_id}")
            return f"{vatandas['ad']} için {hizmet.name} başvurusu onaylandı. Destek: {destek_miktari} TL"
        else:
            basvuru = {
                "vatandas": vatandas["ad"],
                "hizmet": hizmet.name,
                "durum": "reddedildi",
                "miktar": 0
            }
            self._repository.basvuru_ekle(basvuru)
            self._islem_kaydet(f"Başvuru reddedildi: {vatandas['ad']}")
            return f"{vatandas['ad']}, {hizmet.name} için uygun değil."
    
    # Çoklu başvuru oluşturan metod
    def toplu_basvuru_olustur(self, vatandas_listesi, hizmet):
        sonuclar = []
        for vatandas in vatandas_listesi:
            sonuc = self.basvuru_olustur(vatandas, hizmet)
            sonuclar.append(sonuc)
        return sonuclar
    
    # Vatandaş için uygun hizmetleri bulan metod
    def uygun_hizmetleri_bul(self, vatandas):
        uygun_hizmetler = []
        for hizmet in self._repository.hizmetleri_getir():
            if hizmet.uygunluk_kontrolu(vatandas):
                uygun_hizmetler.append(hizmet)
        return uygun_hizmetler
    
    # Vatandaşa önerilecek en iyi hizmeti bulan metod
    def en_iyi_hizmet_onerisi(self, vatandas):
        uygun_hizmetler = self.uygun_hizmetleri_bul(vatandas)
        if not uygun_hizmetler:
            return None
        en_yuksek_destek = max(uygun_hizmetler, key=lambda h: h.destek_hesapla())
        return en_yuksek_destek
    
    # Başvuruları listeleme metodu
    def basvurulari_listele(self):
        return self._repository.basvurulari_getir()
    
    # Onay bekleyen başvuruları getiren metod
    def bekleyen_basvurulari_getir(self):
        return self._repository.basvurulari_duruma_gore_getir("beklemede")
    
    # Başvuruyu değerlendiren metod
    def basvuru_degerlendir(self, basvuru_id, karar, neden=""):
        basvuru = self._repository.basvuru_bul(basvuru_id)
        if not basvuru:
            return "Başvuru bulunamadı"
        
        yeni_durum = "onaylandi" if karar else "reddedildi"
        self._repository.basvuru_durumu_guncelle(basvuru_id, yeni_durum)
        
        bildirim = {
            "basvuru_id": basvuru_id,
            "durum": yeni_durum,
            "neden": neden,
            "tarih": datetime.now()
        }
        self._bildirimler.append(bildirim)
        self._islem_kaydet(f"Başvuru {basvuru_id} değerlendirildi: {yeni_durum}")
        
        return f"Başvuru {basvuru_id} {yeni_durum}"
    
    # Başvuru durumunu sorgulayan metod
    def basvuru_durumu_sorgula(self, basvuru_id):
        basvuru = self._repository.basvuru_bul(basvuru_id)
        if basvuru:
            return {
                "id": basvuru.get("id"),
                "vatandas": basvuru.get("vatandas"),
                "hizmet": basvuru.get("hizmet"),
                "durum": basvuru.get("durum"),
                "miktar": basvuru.get("miktar"),
                "tarih": basvuru.get("tarih")
            }
        return None
    
    # Vatandaşın tüm başvurularını getiren metod
    def vatandas_basvurulari(self, vatandas_adi):
        return self._repository.vatandasa_gore_basvurular(vatandas_adi)
    
    # Vatandaşın toplam aldığı desteği hesaplayan metod
    def vatandas_toplam_destek(self, vatandas_adi):
        basvurular = self.vatandas_basvurulari(vatandas_adi)
        toplam = sum(b.get("miktar", 0) for b in basvurular if b.get("durum") == "onaylandi")
        return toplam
    
    # Hizmet planı oluşturan metod
    def hizmet_plani_olustur(self, vatandas, baslangic_tarihi):
        uygun_hizmetler = self.uygun_hizmetleri_bul(vatandas)
        plan = {
            "vatandas": vatandas["ad"],
            "baslangic": baslangic_tarihi,
            "hizmetler": [],
            "toplam_destek": 0
        }
        
        for hizmet in uygun_hizmetler:
            hizmet_detay = {
                "hizmet_adi": hizmet.name,
                "miktar": hizmet.destek_hesapla(),
                "hedef_grup": hizmet.target_group
            }
            plan["hizmetler"].append(hizmet_detay)
            plan["toplam_destek"] += hizmet.destek_hesapla()
        
        self._islem_kaydet(f"Hizmet planı oluşturuldu: {vatandas['ad']}")
        return plan
    
    # Acil başvuru oluşturan metod
    def acil_basvuru_olustur(self, vatandas, hizmet, aciliyet_derecesi=5):
        basvuru_sonuc = self.basvuru_olustur(vatandas, hizmet)
        
        if "onaylandı" in basvuru_sonuc:
            hizmet.oncelik_seviyesi = aciliyet_derecesi
            bildirim = {
                "tip": "acil",
                "mesaj": f"Acil başvuru: {vatandas['ad']} - {hizmet.name}",
                "aciliyet": aciliyet_derecesi,
                "tarih": datetime.now()
            }
            self._bildirimler.append(bildirim)
            self._islem_kaydet(f"Acil başvuru oluşturuldu: {vatandas['ad']}")
        
        return basvuru_sonuc
    
    # Periyodik hizmet kontrolü yapan metod
    def periyodik_kontrol_yap(self, gun_sayisi=30):
        son_tarih = datetime.now() - timedelta(days=gun_sayisi)
        eski_basvurular = []
        
        for basvuru in self._repository.basvurulari_getir():
            if basvuru.get("tarih", datetime.now()) < son_tarih:
                eski_basvurular.append(basvuru)
        
        return {
            "kontrol_edilen_gun": gun_sayisi,
            "eski_basvuru_sayisi": len(eski_basvurular),
            "eski_basvurular": eski_basvurular
        }
    
    # Hizmet performansını değerlendiren metod
    def hizmet_performansi_analiz(self, hizmet_adi):
        basvurular = self._repository.hizmete_gore_basvurular(hizmet_adi)
        if not basvurular:
            return None
        
        onaylanan = len([b for b in basvurular if b.get("durum") == "onaylandi"])
        reddedilen = len([b for b in basvurular if b.get("durum") == "reddedildi"])
        toplam = len(basvurular)
        
        return {
            "hizmet": hizmet_adi,
            "toplam_basvuru": toplam,
            "onaylanan": onaylanan,
            "reddedilen": reddedilen,
            "onay_orani": (onaylanan / toplam * 100) if toplam > 0 else 0,
            "red_orani": (reddedilen / toplam * 100) if toplam > 0 else 0
        }
    
    # Tüm hizmetlerin performansını karşılaştıran metod
    def hizmet_karsilastirma_raporu(self):
        hizmetler = self._repository.hizmetleri_getir()
        rapor = []
        
        for hizmet in hizmetler:
            analiz = self.hizmet_performansi_analiz(hizmet.name)
            if analiz:
                rapor.append(analiz)
        
        return sorted(rapor, key=lambda x: x["onay_orani"], reverse=True)
    
    # Bütçe tahmini yapan metod
    def butce_tahmini_yap(self, gelecek_ay_sayisi=3):
        mevcut_ortalama = self._repository.ortalama_destek_tutari()
        aylik_basvuru_sayisi = len(self._repository.basvurulari_getir()) / 12
        
        tahmini_butce = mevcut_ortalama * aylik_basvuru_sayisi * gelecek_ay_sayisi
        
        return {
            "tahmini_ay_sayisi": gelecek_ay_sayisi,
            "aylik_ortalama_destek": mevcut_ortalama,
            "aylik_tahmini_basvuru": aylik_basvuru_sayisi,
            "toplam_tahmini_butce": tahmini_butce
        }
    
    # İstatistiksel rapor oluşturan metod
    def istatistik_raporu_olustur(self):
        return {
            "genel_ozet": self._repository.ozet_rapor(),
            "hizmet_istatistikleri": self._repository.hizmet_istatistikleri_hesapla(),
            "en_populer_hizmet": self._repository.en_populer_hizmet(),
            "en_cok_basvuranlar": self._repository.en_cok_basvuru_yapanlar(3)
        }
    
    # Bildirim gönderen metod
    def bildirim_gonder(self, alici, mesaj, tip="bilgi"):
        bildirim = {
            "alici": alici,
            "mesaj": mesaj,
            "tip": tip,
            "tarih": datetime.now(),
            "okundu": False
        }
        self._bildirimler.append(bildirim)
        self._islem_kaydet(f"Bildirim gönderildi: {alici}")
        return "Bildirim gönderildi"
    
    # Okunmamış bildirimleri getiren metod
    def okunmamis_bildirimler(self):
        return [b for b in self._bildirimler if not b.get("okundu", False)]
    
    # Bildirimi okundu olarak işaretleyen metod
    def bildirimi_okundu_isaretle(self, bildirim_index):
        if 0 <= bildirim_index < len(self._bildirimler):
            self._bildirimler[bildirim_index]["okundu"] = True
            return True
        return False
    
    # İşlem geçmişi kaydeden private metod
    def _islem_kaydet(self, mesaj):
        islem = {
            "mesaj": mesaj,
            "tarih": datetime.now()
        }
        self._islem_gecmisi.append(islem)
    
    # İşlem geçmişini getiren metod
    def islem_gecmisini_getir(self, limit=20):
        return self._islem_gecmisi[-limit:]
    
    # Sistem sağlık kontrolü yapan metod
    def sistem_saglik_kontrolu(self):
        return {
            "toplam_hizmet": len(self._repository.hizmetleri_getir()),
            "aktif_hizmet": len(self._repository.hizmetleri_duruma_gore_getir("aktif")),
            "toplam_basvuru": self._repository.toplam_basvuru_sayisi(),
            "bekleyen_basvuru": self._repository.bekleyen_basvuru_sayisi(),
            "toplam_destek": self._repository.toplam_destek_tutari(),
            "okunmamis_bildirim": len(self.okunmamis_bildirimler()),
            "sistem_durumu": "saglikli"
        }
    
    # Detaylı rapor oluşturan metod
    def detayli_rapor_olustur(self, baslangic_tarihi, bitis_tarihi):
        basvurular = self._repository.tarih_araligina_gore_basvurular(baslangic_tarihi, bitis_tarihi)
        
        return {
            "baslangic": baslangic_tarihi,
            "bitis": bitis_tarihi,
            "toplam_basvuru": len(basvurular),
            "onaylanan": len([b for b in basvurular if b.get("durum") == "onaylandi"]),
            "reddedilen": len([b for b in basvurular if b.get("durum") == "reddedildi"]),
            "bekleyen": len([b for b in basvurular if b.get("durum") == "beklemede"]),
            "toplam_destek": sum(b.get("miktar", 0) for b in basvurular if b.get("durum") == "onaylandi")
        }
    
    # String temsilini döndüren metod
    def __str__(self):
        return f"SosyalHizmetServisi(basvurular={self._repository.toplam_basvuru_sayisi()})"
    
    # Toplam servis sayısını döndüren class metodu
    @classmethod
    def servis_sayisi(cls):
        return cls._servis_sayisi
    
    # Yeni servis oluşturan class metodu
    @classmethod
    def yeni_servis_olustur(cls, repository):
        return cls(repository)
    
    # Servis sayısını sıfırlayan class metodu
    @classmethod
    def servis_sayisini_sifirla(cls):
        cls._servis_sayisi = 0
        return "Servis sayısı sıfırlandı"
    
    # Vatandaşın sosyal yardım geçmişini analiz eden metod
    def vatandas_gecmis_analizi(self, vatandas_adi):
        basvurular = self.vatandas_basvurulari(vatandas_adi)
        if not basvurular:
            return None
        
        return {
            "toplam_basvuru": len(basvurular),
            "onaylanan_sayi": len([b for b in basvurular if b.get("durum") == "onaylandi"]),
            "toplam_alinan_destek": self.vatandas_toplam_destek(vatandas_adi),
            "ilk_basvuru": min([b.get("tarih", datetime.now()) for b in basvurular]),
            "son_basvuru": max([b.get("tarih", datetime.now()) for b in basvurular])
        }
    
    # Desteklenen bildirim tiplerini döndüren static metod
    @staticmethod
    def bildirim_tipleri():
        return ["bilgi", "uyari", "hata", "acil", "basari"]
    
    # Maksimum aylık başvuru limitini döndüren static metod
    @staticmethod
    def maksimum_aylik_basvuru():
        return 5
    
    # İşlem önceliklerini döndüren static metod
    @staticmethod
    def islem_oncelikleri():
        return {
            1: "Düşük",
            2: "Normal",
            3: "Orta",
            4: "Yüksek",
            5: "Acil"
        }
