from datetime import datetime, timedelta

class SosyalHizmetAI:
    """Basit AI asistan - sosyal hizmetler için soru-cevap sistemi"""
    
    def __init__(self, repository, servis):
        self.repo = repository
        self.servis = servis
        self.komutlar = {
            "basvuru": self.bugun_basvuranlar,
            "acil": self.acil_destek_yap,
            "rapor": self.ozet_rapor_ver,
            "yardim": self.yardim_goster,
            "onay": self.onay_bekleyenler,
            "red": self.reddedilenler,
            "gelir": self.gelire_gore_analiz,
            "istatistik": self.istatistik_goster
        }
    
    def sor(self, soru):
        """AI asistana soru sor"""
        soru = soru.lower().strip()
        
        if "bugün" in soru and ("başvur" in soru or "basvur" in soru):
            return self.bugun_basvuranlar()
        
        elif "acil" in soru or "aciliyet" in soru:
            if "2" in soru or "iki" in soru:
                return self.acil_destek_yap(2)
            elif "3" in soru or "üç" in soru or "uc" in soru:
                return self.acil_destek_yap(3)
            return self.acil_destek_yap()
        
        elif "onay" in soru and "bekle" in soru:
            return self.onay_bekleyenler()
        
        elif "red" in soru or "reddedil" in soru:
            return self.reddedilenler()
        
        elif "rapor" in soru or "özet" in soru or "ozet" in soru:
            return self.ozet_rapor_ver()
        
        elif "gelir" in soru:
            return self.gelire_gore_analiz()
        
        elif "istatistik" in soru or "sayı" in soru or "sayi" in soru:
            return self.istatistik_goster()
        
        elif "yardım" in soru or "yardim" in soru or "help" in soru:
            return self.yardim_goster()
        
        else:
            return self.anlamadim()
    
    def bugun_basvuranlar(self):
        """Bugün başvuru yapanları listele"""
        bugun = datetime.now().date()
        bugun_basvurular = [
            b for b in self.repo.basvurulari_getir()
            if b.get("tarih") and b["tarih"].date() == bugun
        ]
        
        if not bugun_basvurular:
            return "Bugün henüz başvuru yapılmadı."
        
        sonuc = f"Bugün {len(bugun_basvurular)} başvuru yapıldı:\n\n"
        for b in bugun_basvurular:
            durum_text = "[ONAYLANDI]" if b.get("durum") == "onaylandi" else "[REDDEDİLDİ]" if b.get("durum") == "reddedildi" else "[BEKLEMEDE]"
            sonuc += f"{durum_text} {b.get('vatandas')} - {b.get('hizmet')} ({b.get('durum')})\n"
            if b.get("durum") == "onaylandi":
                sonuc += f"   Destek: {b.get('miktar', 0)} TL\n"
        
        return sonuc
    
    def acil_destek_yap(self, kisi_sayisi=2):
        """Acil durumda olanlara öncelikli destek yap"""
        tum_vatandaslar = self.repo.vatandaslari_getir()
        
        sirali = sorted(tum_vatandaslar, key=lambda v: v.get("gelir", 999999))
        acil_vatandaslar = sirali[:kisi_sayisi]
        
        if not acil_vatandaslar:
            return "Acil destek verilecek vatandaş bulunamadı."
        
        sonuc = f"ACİL DESTEK - En düşük gelirli {kisi_sayisi} kişiye destek veriliyor:\n\n"
        
        for vatandas in acil_vatandaslar:
            uygun_hizmetler = self.servis.uygun_hizmetleri_bul(vatandas)
            
            if uygun_hizmetler:
                en_iyi_hizmet = max(uygun_hizmetler, key=lambda h: h.destek_hesapla())
                sonuc_mesaj = self.servis.acil_basvuru_olustur(vatandas, en_iyi_hizmet, aciliyet_derecesi=5)
                
                sonuc += f"{vatandas['ad']} (Gelir: {vatandas.get('gelir', 0)} TL)\n"
                sonuc += f"   {sonuc_mesaj}\n\n"
            else:
                sonuc += f"{vatandas['ad']} - Uygun hizmet bulunamadı\n\n"
        
        return sonuc
    
    def onay_bekleyenler(self):
        """Onay bekleyen başvuruları listele"""
        bekleyenler = self.repo.basvurulari_duruma_gore_getir("beklemede")
        
        if not bekleyenler:
            return "Onay bekleyen başvuru yok."
        
        sonuc = f"{len(bekleyenler)} başvuru onay bekliyor:\n\n"
        for b in bekleyenler:
            sonuc += f"• ID: {b.get('id')} - {b.get('vatandas')} - {b.get('hizmet')}\n"
        
        return sonuc
    
    def reddedilenler(self):
        """Reddedilen başvuruları listele"""
        reddedilenler = self.repo.basvurulari_duruma_gore_getir("reddedildi")
        
        if not reddedilenler:
            return "Reddedilen başvuru yok."
        
        sonuc = f"{len(reddedilenler)} başvuru reddedildi:\n\n"
        for b in reddedilenler:
            sonuc += f"• {b.get('vatandas')} - {b.get('hizmet')}\n"
        
        return sonuc
    
    def gelire_gore_analiz(self):
        """Gelir durumuna göre analiz yap"""
        vatandaslar = self.repo.vatandaslari_getir()
        
        if not vatandaslar:
            return "Henüz vatandaş kaydı yok."
        
        dusuk_gelir = [v for v in vatandaslar if v.get("gelir", 0) < 5000]
        orta_gelir = [v for v in vatandaslar if 5000 <= v.get("gelir", 0) < 10000]
        yuksek_gelir = [v for v in vatandaslar if v.get("gelir", 0) >= 10000]
        
        ortalama_gelir = sum(v.get("gelir", 0) for v in vatandaslar) / len(vatandaslar)
        
        sonuc = "GELİR DURUMU ANALİZİ\n\n"
        sonuc += f"Toplam Vatandaş: {len(vatandaslar)}\n"
        sonuc += f"Ortalama Gelir: {ortalama_gelir:.2f} TL\n\n"
        sonuc += f"Düşük Gelir (<5000 TL): {len(dusuk_gelir)} kişi\n"
        sonuc += f"Orta Gelir (5000-10000 TL): {len(orta_gelir)} kişi\n"
        sonuc += f"Yüksek Gelir (>10000 TL): {len(yuksek_gelir)} kişi\n\n"
        
        if dusuk_gelir:
            sonuc += "UYARI: Düşük gelirli vatandaşlar acil destege ihtiyaç duyabilir!\n"
        
        return sonuc
    
    def istatistik_goster(self):
        """Genel istatistikleri göster"""
        ozet = self.repo.ozet_rapor()
        
        sonuc = "SİSTEM İSTATİSTİKLERİ\n\n"
        sonuc += f"Toplam Hizmet: {ozet['toplam_hizmet']}\n"
        sonuc += f"Toplam Vatandaş: {ozet['toplam_vatandas']}\n"
        sonuc += f"Toplam Başvuru: {ozet['toplam_basvuru']}\n\n"
        sonuc += f"Onaylanan: {ozet['onaylanan']}\n"
        sonuc += f"Reddedilen: {ozet['reddedilen']}\n"
        sonuc += f"Bekleyen: {ozet['bekleyen']}\n\n"
        sonuc += f"Toplam Destek: {ozet['toplam_destek']:.2f} TL\n"
        sonuc += f"Ortalama Destek: {ozet['ortalama_destek']:.2f} TL\n"
        
        return sonuc
    
    def ozet_rapor_ver(self):
        """Özet rapor hazırla"""
        return self.istatistik_goster()
    
    def yardim_goster(self):
        """Yardım menüsünü göster"""
        sonuc = "AI ASISTAN YARDIM\n\n"
        sonuc += "Soru örnekleri:\n"
        sonuc += "• 'Bugün kimler başvurdu?'\n"
        sonuc += "• 'Acil olan 2 kişiye destek yap'\n"
        sonuc += "• 'Onay bekleyen başvurular'\n"
        sonuc += "• 'Reddedilen başvurular'\n"
        sonuc += "• 'Gelir durumu analizi'\n"
        sonuc += "• 'İstatistikleri göster'\n"
        sonuc += "• 'Özet rapor'\n"
        
        return sonuc
    
    def anlamadim(self):
        """Anlaşılamayan sorular için"""
        return "Sizi anlayamadım. 'yardım' yazarak komutları görebilirsiniz."
    
    def interaktif_mod(self):
        """İnteraktif mod - kullanıcı sürekli soru sorabilir"""
        print("\n" + "="*60)
        print("SOSYAL HİZMETLER AI ASİSTAN")
        print("="*60)
        print("'çıkış' yazarak çıkabilirsiniz.")
        print("'yardım' yazarak komutları görebilirsiniz.\n")
        
        while True:
            try:
                soru = input("Soru: ").strip()
                
                if not soru:
                    continue
                
                if soru.lower() in ['çıkış', 'cikis', 'exit', 'quit', 'q']:
                    print("\nGörüşürüz!")
                    break
                
                cevap = self.sor(soru)
                print(f"\n{cevap}\n")
                
            except KeyboardInterrupt:
                print("\n\nGörüşürüz!")
                break
            except Exception as e:
                print(f"\nHata: {str(e)}\n")
