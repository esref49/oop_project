from app.modules.module_1.implementations import (
    Base1SubClass1, Base1SubClass2
)

from app.modules.module_2.implementations import (
     ElectricityMeter, WaterMeter, GasMeter
)
from app.modules.module_2.demo import run_demo as run_module_2_demo

from app.modules.module_3.implementations import (
    Base3SubClass1, Base3SubClass2
)

from app.modules.module_4.implementations import (
    Base4SubClass1, Base4SubClass2
)

def run_demo():
    print("=== PROJECT MENU ===")

    # Ogrenci 1 (Modul 1)
    base_1 = [
        Base1SubClass1("parametre1"),
        Base1SubClass2("parametre2")
    ]
    for n in base_1:
        n.method1()

    # Ogrenci 2 (Modul 2)
    print("\n--- [Modül 2] Akıllı Şehir Altyapı Sistemi ---")
    run_module_2_demo()
    print("----------------------------------------------\n")

        
    # Ogrenci 3 (Modul 3)
    base_3 = [
        Base3SubClass1("parametre5"),
        Base3SubClass2("parametre6")
    ]
    for p in base_3:
        p.method3()

    # Ogrenci 4 (Modul 4)
    object1 = Base4SubClass1("parametre7")
    object2 = Base4SubClass2("parametre8")
    object1.method4()
    object2.method4()

if __name__ == "__main__":
    run_demo()