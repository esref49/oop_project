# Module 4 - Sosyal Hizmetler Demo Senaryosu
import sys
import os

# Proje kök dizinini path'e ekle
if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    from app.modules.module_4.implementations import GidaYardimi, BarinmaDestegi, EgitimDestegi
    from app.modules.module_4.repository import SosyalHizmetRepository
    from app.modules.module_4.services import SosyalHizmetServisi
else:
    from .implementations import GidaYardimi, BarinmaDestegi, EgitimDestegi
    from .repository import SosyalHizmetRepository
    from .services import SosyalHizmetServisi

def main():
    print("=" * 60)
    print("SOSYAL HIZMETLER YONETIM SISTEMI - DEMO")
    print("=" * 60)
    print()
    
    # Repository ve servis katmanlarini initialize et
    repo = SosyalHizmetRepository()
    servis = SosyalHizmetServisi(repo)
    
    print("[INFO] Sistem baslat...")
    print()
    
    # Hizmet instance'larini olustur ve repository'ye kaydet
    print("[SETUP] Hizmet nesneleri olusturuluyor...")
    hizmet1 = GidaYardimi(1, 1500, 15)
    hizmet2 = BarinmaDestegi(2, 5000, "daire")
    hizmet3 = EgitimDestegi(3, 2000, "lise")
    
    # Hizmetleri aktif duruma getir
    hizmet1.aktif_et()
    hizmet2.aktif_et()
    hizmet3.aktif_et()
    
    repo.hizmet_ekle(hizmet1)
    repo.hizmet_ekle(hizmet2)
    repo.hizmet_ekle(hizmet3)
    
    print(f"[OK] {hizmet1.name} eklendi - Durum: {hizmet1.status}")
    print(f"[OK] {hizmet2.name} eklendi - Durum: {hizmet2.status}")
    print(f"[OK] {hizmet3.name} eklendi - Durum: {hizmet3.status}")
    print()
    
    # Vatandas profilleri olustur
    print("[SETUP] Vatandas varliklari olusturuluyor...")
    vatandas1 = {
        "ad": "Ali Yılmaz",
        "gelir": 8000,
        "evi_var_mi": False,
        "ogrenci_mi": True,
        "cocuk_sayisi": 0
    }
    
    vatandas2 = {
        "ad": "Ayşe Kaya",
        "gelir": 4500,
        "evi_var_mi": True,
        "ogrenci_mi": False,
        "cocuk_sayisi": 3
    }
    
    vatandas3 = {
        "ad": "Mehmet Demir",
        "gelir": 15000,
        "evi_var_mi": True,
        "ogrenci_mi": False,
        "cocuk_sayisi": 1
    }
    
    vatandas4 = {
        "ad": "Zeynep Arslan",
        "gelir": 6000,
        "evi_var_mi": False,
        "ogrenci_mi": True,
        "cocuk_sayisi": 0
    }
    
    # Vatandaşları repository'ye ekleme
    repo.vatandas_ekle(vatandas1)
    repo.vatandas_ekle(vatandas2)
    repo.vatandas_ekle(vatandas3)
    repo.vatandas_ekle(vatandas4)
    
    print(f"[OK] {vatandas1['ad']} kaydedildi")
    print(f"[OK] {vatandas2['ad']} kaydedildi")
    print(f"[OK] {vatandas3['ad']} kaydedildi")
    print(f"[OK] {vatandas4['ad']} kaydedildi")
    print()
    
    # POLIMORFIZM ORNEGI 1: Farkli hizmet tipleri ayni liste icinde
    print("[POLIMORFIZM-1] Tum hizmetler icin ortak interface kullanimi")
    print("-" * 60)
    hizmetler = [hizmet1, hizmet2, hizmet3]
    
    for hizmet in hizmetler:
        # Polimorfizm: Her hizmet kendi uygunluk_kontrolu metodunu kullanıyor
        print(f"Hizmet: {hizmet.name}")
        print(f"  - Servis Tipi: {hizmet.servis_tipi()}")
        print(f"  - Hedef Grup: {hizmet.target_group}")
        print(f"  - Durum: {hizmet.status}")
        print()
    
    # Vatandas 1 icin basvuru islemleri
    print("[BASVURU] Ali Yilmaz icin basvuru isleme")
    print("-" * 60)
    
    # POLIMORFIZM ORNEGI 2: Ayni metod farkli hizmetlerde farkli davranis
    for hizmet in hizmetler:
        # Her hizmet kendi destek_hesapla ve uygunluk_kontrolu metodunu calistiriyor
        sonuc = servis.basvuru_olustur(vatandas1, hizmet)
        print(f"[RESULT] {sonuc}")
    print()
    
    # Vatandas 2 icin basvuru islemleri
    print("[BASVURU] Ayse Kaya icin basvuru isleme")
    print("-" * 60)
    for hizmet in hizmetler:
        sonuc = servis.basvuru_olustur(vatandas2, hizmet)
        print(f"[RESULT] {sonuc}")
    print()
    
    # Vatandas 3 icin basvuru islemleri (yuksek gelirli, reddedilmeli)
    print("[BASVURU] Mehmet Demir icin basvuru isleme (Yuksek Gelir)")
    print("-" * 60)
    for hizmet in hizmetler:
        sonuc = servis.basvuru_olustur(vatandas3, hizmet)
        print(f"[RESULT] {sonuc}")
    print()
    
    # Uygun hizmet bulma algoritması
    print("[ANALIZ] Zeynep Arslan icin uygun hizmet analizi")
    print("-" * 60)
    uygun_hizmetler = servis.uygun_hizmetleri_bul(vatandas4)
    print(f"Zeynep Arslan icin uygun hizmet sayisi: {len(uygun_hizmetler)}")
    for hizmet in uygun_hizmetler:
        print(f"  [MATCH] {hizmet.name} - Destek: {hizmet.destek_hesapla()} TL")
    print()
    
    # En iyi hizmet onerisi algoritması
    en_iyi = servis.en_iyi_hizmet_onerisi(vatandas4)
    if en_iyi:
        print(f"[RECOMMENDATION] En iyi oneri: {en_iyi.name} ({en_iyi.destek_hesapla()} TL)")
    print()
    
    # Class metodlari ile sinif seviyesi islemler
    print("[CLASS-METHODS] Sinif seviyesi metod cagrilari")
    print("-" * 60)
    print(f"Toplam Gıda Yardımı Sayısı: {GidaYardimi.toplam_gida_yardimi_sayisi()}")
    print(f"Toplam Barınma Desteği Sayısı: {BarinmaDestegi.toplam_barinma_destegi_sayisi()}")
    print(f"Toplam Eğitim Desteği Sayısı: {EgitimDestegi.toplam_egitim_destegi_sayisi()}")
    print(f"Toplam Sosyal Hizmet Sayısı: {hizmet1.toplam_hizmet_sayisi()}")
    print()
    
    # Static metodlar ile utilite fonksiyonlari
    print("[STATIC-METHODS] Utilite metod cagrilari")
    print("-" * 60)
    print(f"Belediye Politikası: {hizmet1.belediye_politikasi()}")
    print(f"Gıda Yardımı Gelir Limiti: {GidaYardimi.gelir_limiti()} TL")
    print(f"Barınma Min Kira: {BarinmaDestegi.minimum_kira_limiti()} TL")
    print(f"Eğitim Min Burs: {EgitimDestegi.minimum_burs()} TL")
    print(f"Öncelik Kategorileri: {hizmet1.oncelik_kategorileri()}")
    print()
    
    # Repository katmani istatistikleri
    print("[REPOSITORY] Veri katmani istatistik raporu")
    print("-" * 60)
    ozet = repo.ozet_rapor()
    print(f"Toplam Hizmet: {ozet['toplam_hizmet']}")
    print(f"Toplam Başvuru: {ozet['toplam_basvuru']}")
    print(f"Onaylanan: {ozet['onaylanan']}")
    print(f"Reddedilen: {ozet['reddedilen']}")
    print(f"Toplam Destek: {ozet['toplam_destek']:.2f} TL")
    print(f"Ortalama Destek: {ozet['ortalama_destek']:.2f} TL")
    print()
    
    # Hizmet performans metrikleri
    print("[ANALYTICS] Hizmet performans metrikleri")
    print("-" * 60)
    for hizmet in hizmetler:
        performans = servis.hizmet_performansi_analiz(hizmet.name)
        if performans:
            print(f"{performans['hizmet']}:")
            print(f"  - Toplam Başvuru: {performans['toplam_basvuru']}")
            print(f"  - Onay Oranı: {performans['onay_orani']:.1f}%")
            print(f"  - Red Oranı: {performans['red_orani']:.1f}%")
            print()
    
    # En yuksek talep goren hizmet
    print("[ANALYTICS] En yuksek talep goren hizmet")
    print("-" * 60)
    en_populer = repo.en_populer_hizmet()
    if en_populer:
        print(f"Hizmet: {en_populer[0]}")
        print(f"Başvuru Sayısı: {en_populer[1]}")
    print()
    
    # Hizmet planlama modulu
    print("[PLANNING] Ali Yilmaz icin hizmet plani olusturma")
    print("-" * 60)
    from datetime import datetime
    plan = servis.hizmet_plani_olustur(vatandas1, datetime.now())
    print(f"Vatandaş: {plan['vatandas']}")
    print(f"Toplam Destek: {plan['toplam_destek']} TL")
    print(f"Uygun Hizmetler:")
    for h in plan['hizmetler']:
        print(f"  - {h['hizmet_adi']}: {h['miktar']} TL")
    print()
    
    # Acil basvuru islemleri
    print("[EMERGENCY] Zeynep Arslan icin acil basvuru")
    print("-" * 60)
    acil_sonuc = servis.acil_basvuru_olustur(vatandas4, hizmet2, aciliyet_derecesi=5)
    print(f"[RESULT] {acil_sonuc}")
    print()
    
    # Bildirim sistemi
    print("[NOTIFICATIONS] Bildirim sistemi durumu")
    print("-" * 60)
    servis.bildirim_gonder("Yönetici", "Sistem sağlıklı çalışıyor", "bilgi")
    servis.bildirim_gonder("Yönetici", "Acil başvuru mevcut", "acil")
    
    okunmamis = servis.okunmamis_bildirimler()
    print(f"Okunmamış Bildirim Sayısı: {len(okunmamis)}")
    for bildirim in okunmamis:
        print(f"  - [{bildirim['tip'].upper()}] {bildirim['mesaj']}")
    print()
    
    # Sistem health check
    print("[HEALTH-CHECK] Sistem saglik kontrolu")
    print("-" * 60)
    saglik = servis.sistem_saglik_kontrolu()
    print(f"Sistem Durumu: {saglik['sistem_durumu'].upper()}")
    print(f"Toplam Hizmet: {saglik['toplam_hizmet']}")
    print(f"Aktif Hizmet: {saglik['aktif_hizmet']}")
    print(f"Toplam Başvuru: {saglik['toplam_basvuru']}")
    print(f"Bekleyen Başvuru: {saglik['bekleyen_basvuru']}")
    print(f"Okunmamış Bildirim: {saglik['okunmamis_bildirim']}")
    print()
    
    # Ozel hesaplama algoritmalari
    print("[ALGORITHMS] Ozel hesaplama metodlari")
    print("-" * 60)
    
    # Gıda yardımı için çocuk desteği
    cocuk_destegi = hizmet1.cocuk_destegi_hesapla(vatandas2["cocuk_sayisi"])
    print(f"Ayşe Kaya için çocuk desteğiyle: {cocuk_destegi} TL")
    
    # Barınma için aile büyüklüğüne göre
    aile_destegi = hizmet2.aile_buyuklugune_gore_destek(4)
    print(f"4 kişilik aile için barınma desteği: {aile_destegi} TL")
    
    # Eğitim için başarı bazlı
    basari_bursu = hizmet3.basariya_gore_burs(85)
    print(f"85 ortalama ile burs miktarı: {basari_bursu} TL")
    print()
    
    # Vatandas gecmis kayit analizi
    print("[HISTORY-ANALYSIS] Ali Yilmaz gecmis kayit analizi")
    print("-" * 60)
    gecmis = servis.vatandas_gecmis_analizi("Ali Yılmaz")
    if gecmis:
        print(f"Toplam Başvuru: {gecmis['toplam_basvuru']}")
        print(f"Onaylanan: {gecmis['onaylanan_sayi']}")
        print(f"Alınan Toplam Destek: {gecmis['toplam_alinan_destek']} TL")
    print()
    
    # Python magic metodlari (dunder methods)
    print("[DUNDER-METHODS] Magic metod implementasyonlari")
    print("-" * 60)
    print(f"str(hizmet1): {str(hizmet1)}")
    print(f"repr(hizmet1): {repr(hizmet1)}")
    print(f"hizmet1 == hizmet2: {hizmet1 == hizmet2}")
    print(f"hizmet1 == hizmet1: {hizmet1 == hizmet1}")
    print()
    
    # Log tracking sistemi
    print("[LOGS] Son islem kayitlari")
    print("-" * 60)
    son_loglar = repo.son_loglari_getir(5)
    for log in son_loglar:
        print(f"  [{log['tarih'].strftime('%H:%M:%S')}] {log['mesaj']}")
    print()
    
    print("=" * 60)
    print("DEMO EXECUTION COMPLETED")
    print("=" * 60)

# Demo'yu çalıştırma
if __name__ == "__main__":
    main()
