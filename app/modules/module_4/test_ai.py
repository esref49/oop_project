"""
Module 4 - AI Asistan Test ve Demo
"""
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.modules.module_4.implementations import GidaYardimi, BarinmaDestegi, EgitimDestegi
from app.modules.module_4.repository import SosyalHizmetRepository
from app.modules.module_4.services import SosyalHizmetServisi
from app.modules.module_4.ai_assistant import SosyalHizmetAI

def setup_sistem():
    """Test için sistem kurulumu"""
    repo = SosyalHizmetRepository()
    servis = SosyalHizmetServisi(repo)
    
    hizmet1 = GidaYardimi(1, 1500, 15)
    hizmet2 = BarinmaDestegi(2, 5000, "daire")
    hizmet3 = EgitimDestegi(3, 2000, "lise")
    
    hizmet1.aktif_et()
    hizmet2.aktif_et()
    hizmet3.aktif_et()
    
    repo.hizmet_ekle(hizmet1)
    repo.hizmet_ekle(hizmet2)
    repo.hizmet_ekle(hizmet3)
    
    vatandas1 = {"ad": "Ali Yılmaz", "gelir": 8000, "evi_var_mi": False, "ogrenci_mi": True, "cocuk_sayisi": 0}
    vatandas2 = {"ad": "Ayşe Kaya", "gelir": 4500, "evi_var_mi": True, "ogrenci_mi": False, "cocuk_sayisi": 3}
    vatandas3 = {"ad": "Mehmet Demir", "gelir": 15000, "evi_var_mi": True, "ogrenci_mi": False, "cocuk_sayisi": 1}
    vatandas4 = {"ad": "Zeynep Arslan", "gelir": 6000, "evi_var_mi": False, "ogrenci_mi": True, "cocuk_sayisi": 0}
    
    repo.vatandas_ekle(vatandas1)
    repo.vatandas_ekle(vatandas2)
    repo.vatandas_ekle(vatandas3)
    repo.vatandas_ekle(vatandas4)
    
    for hizmet in [hizmet1, hizmet2, hizmet3]:
        servis.basvuru_olustur(vatandas1, hizmet)
        servis.basvuru_olustur(vatandas2, hizmet)
        servis.basvuru_olustur(vatandas4, hizmet)
    
    return repo, servis

def main():
    print("="*70)
    print("SOSYAL HİZMETLER AI ASİSTAN - TEST")
    print("="*70)
    print()
    
    repo, servis = setup_sistem()
    ai = SosyalHizmetAI(repo, servis)
    
    test_sorulari = [
        "Bugün kimler başvurdu?",
        "Acil olan 2 kişiye destek yap",
        "İstatistikleri göster",
        "Gelir durumu analizi",
        "Onay bekleyen başvurular",
        "Reddedilen başvurular"
    ]
    
    print("TEST SORULARI VE CEVAPLARI:\n")
    
    for i, soru in enumerate(test_sorulari, 1):
        print(f"\n{'='*70}")
        print(f"Soru {i}: {soru}")
        print(f"{'='*70}")
        cevap = ai.sor(soru)
        print(cevap)
    
    print("\n" + "="*70)
    print("Test tamamlandı!")
    print("="*70)
    print()
    print("İnteraktif mod için: python app/modules/module_4/demo.py")
    print()

if __name__ == "__main__":
    main()
