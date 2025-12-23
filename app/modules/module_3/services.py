import os
import time
import numpy as np

from app.modules.module_3.implementations import Criminal, FireStation, Hospital, PoliceStation, Victim

class EmergencyService:
    def __init__(self, repository):
        self.__nearest_unit = None
        self.__repository = repository
        self.__location = None

    @property
    def nearest_unit(self):
        return self.__nearest_unit
    
    @nearest_unit.setter
    def nearest_unit(self, new):
        self.__nearest_unit = new

    @property
    def repository(self):
        return self.__repository
    
    @repository.setter
    def repository(self, new):
        self.__repository = new

    @property
    def location(self):
        return self.__location
    
    @location.setter
    def location(self, new):
        self.__location = new

    def creating_case(self, case_type, severity, unit_list, case_location):
        self.location = case_location
    
        # Olaya verilen puana göre olayın ciddiyetini belirler.
        if severity > 8:
            is_critical = "Evet"
        else:
            is_critical = "Hayır"
    
        # Hangi birim türüne ihtiyaç olduğunu belirle
        needed_unit_type = self.get_unit_type_for_case(case_type)
    
        # En yakın birimi bul
        self.nearest_unit = self.finding_the_nearest_unit(unit_list, needed_unit_type)
    
        # Atanan birim bilgisini hazırla
        assigned_unit_info = []
        if self.nearest_unit:
            assigned_unit_info.append(f"{self.nearest_unit.unit_type} (ID: {self.nearest_unit.unit_id})")
    
        # Vaka bilgilerini sözlük içinde toplar
        new_case = {
            "location": self.location,
            "type": case_type,
            "severity": severity,
            "critical_status": is_critical,
            "status": "Active",
            "assigned_unit": self.nearest_unit.unit_type if self.nearest_unit else None,
            "assigned_unit_id": self.nearest_unit.unit_id if self.nearest_unit else None,
            "assigned_unit_info": assigned_unit_info,  # Bu yeni alan
            "needed_unit_types": [needed_unit_type] if needed_unit_type else []
        }
    
        # Yeni vakanın oluştuğu bilgisini verir
        print("="*30)
        print(f"Vaka konumu: {new_case['location']}")
        print(f"Vaka türü: {new_case['type']}")
        print(f"Vaka seviyesi: {new_case['severity']}")
        print(f"Vaka kritik mi: {new_case['critical_status']}")
        print(f"Görevlendirilen birim: {new_case['assigned_unit']}")
        print(f"Görevlendirilen birim ID: {new_case['assigned_unit_id']}")
        print("="*30)
        print("\n")
    
        self.repository.save_case(new_case)

        # Eğer birim atandıysa müdahale planını çalıştır
        if self.nearest_unit:
            self.creating_intervention_plan(case_type)
    
        return new_case

    def get_unit_type_for_case(self, case_type):
        #Vaka türüne göre gerekli birim türünü döndürür
        case_to_unit = {
            "Yangın": "İtfaiye",
            "Kimyasal Sızıntı": "İtfaiye",
            "Sel/Su Baskını": "İtfaiye",
            "Mahsur Kalma": "İtfaiye", 
            "Trafik Kazası": "Polis",
            "Hırsızlık": "Polis",
            "Rehine Krizi": "Polis",
            "Şüpheli Paket": "Polis",
            "Kavga/Darp": "Polis",
            "Kalp Krizi": "Ambulans",
            "Yaralanma": "Polis",
            "Zehirlenme": "Ambulans",
            "Doğum": "Ambulans",
            "Bayılma": "Ambulans"
        }
        return case_to_unit.get(case_type, "")
        
    def finding_the_nearest_unit(self, unit_list, unit_type, incident_location=None):
        # En yakın aracı bulmak için başlangıç değişkenlerini tanımlar
        min_distance = 999999999999
        self.nearest_unit = None

        # Konum kontrolü
        if incident_location is None:
            if self.location is None:
                print("[HATA] Konum bilgisi bulunamadı!")
                return None
            incident_location = self.location

        # Verilen listedeki tüm araçları tek tek kontrol eder
        for unit in unit_list: 
            if unit.availability and unit.unit_type == unit_type:
                # Olay yeri ile araç arasındaki mesafeyi hesaplar.
                distance = abs(unit.current_location - incident_location) 

                # Eğer bu araç daha önce bulunanlardan daha yakınsa, en yakın olarak bunu seçer
                if distance < min_distance:
                    min_distance = distance
                    self.nearest_unit = unit
                        
        # Eğer uygun bir araç bulunduysa sevk işlemlerini başlatır
        if self.nearest_unit:
            print("\n")
            print("="*30)
            print("[BİLGİ] En yakın birim bulundu")
            print(f"[BİLGİ] {self.nearest_unit.unit_id} kodlu {self.nearest_unit.unit_type} olay yerine sevk ediliyor.")
            print(f"[BİLGİ] Tahmini Mesafe: {min_distance} km")
            print(f"[BİLGİ] {self.nearest_unit.unit_type} biriminin anlık konumu: {self.nearest_unit.current_location}") 
            print("="*30)
            print("\n")
            
            # Aracın durumunu günceller: Göreve çıkarır, meşgul yapar, sireni açar
            self.nearest_unit.is_it_on_duty = True
            self.nearest_unit.availability = False 
            # Çok biçimlilik örneği
            self.nearest_unit.open_siren()
            return self.nearest_unit
        else:
            # Hiçbir araç bulunamazsa hata mesajı verir
            print(f"[BİLGİ]: {unit_type} türünde müsait araç bulunamadı!")
            return None
            # En yakın aracı bulmak için başlangıç değişkenlerini tanımlar
            min_distance = 999999999999
            self.__nearest_unit = None

            # Verilen listedeki tüm araçları tek tek kontrol eder
            for unit in unit_list: 
                if unit.availability and unit.unit_type == unit_type:
                    # Olay yeri ile araç arasındaki mesafeyi hesaplar.
                    distance = abs(unit.current_location - self.__location) 

                    # Eğer bu araç daha önce bulunanlardan daha yakınsa, en yakın olarak bunu seçer
                    if distance < min_distance:
                        min_distance = distance
                        self.nearest_unit = unit
                        
            # Eğer uygun bir araç bulunduysa sevk işlemlerini başlatır
            if self.nearest_unit:
                print("\n")
                print("="*30)
                print("[BİLGİ] Yeni vaka oluşturuldu")
                print(f"[BİLGİ] {self.__nearest_unit.unit_id} kodlu {self.nearest_unit.unit_type} olay yerine sevk ediliyor.")
                print(f"[BİLGİ] Tahmini Mesafe: {min_distance} km")
                print(f"[BİLGİ] {self.__nearest_unit.unit_type} biriminin anlık konumu: {self.__nearest_unit.current_location}") 
                print("="*30)
                print("\n")
                
                # Aracın durumunu günceller: Göreve çıkarır, meşgul yapar, sireni açar ve konumunu değiştirir
                self.__nearest_unit.is_it_on_duty = True
                self.__nearest_unit.availability = False 
                # Çok biçimlilik örneği
                self.__nearest_unit.open_siren()
                return self.__nearest_unit
            else:
                # Hiçbir araç bulunamazsa hata mesajı verir
                print(f"[BİLGİ]: {unit_type} türünde müsait araç bulunamadı!")
                return None

    def creating_intervention_plan(self, case):

        # Her olay türü için yapılması gereken adım adım prosedürleri içeren liste
        plans = {
            "Yangın": [
                "1. [GÜVENLİK] Çevre güvenliğini al, elektrik/gaz akışını kes.",
                "2. [MÜDAHALE] Rüzgarı arkana al, alevin kaynağına su/köpük sık.",
                "3. [KONTROL] Soğutma çalışması yap ve termal kamerayla kontrol et."
            ],
            "Kimyasal Sızıntı": [
                "1. [KARANTİNA] Bölgeyi 500m çapında boşalt. Maskesiz yaklaşma.",
                "2. [KBRN] Koruyucu (sarı) kıyafetleri giy.",
                "3. [İMHA] Sızıntıyı kaynağında tıka veya nötralize et."
            ],
            "Sel/Su Baskını": [
                "1. [ENERJİ] Elektrik hatlarını ana şalterden kapat.",
                "2. [TAHLİYE] Vatandaşları çatı veya yüksek bölgelere al.",
                "3. [TAHLİYE 2] Motopompları kur ve suyu tahliye et."
            ],
            "Mahsur Kalma": [
                "1. [İLETİŞİM] Kazazedeyle konuşarak sakinleştir.",
                "2. [ANALİZ] Sıkıştığı yerin stabilitesini kontrol et (göçük riski).",
                "3. [KURTARMA] Hidrolik makas/kesici kullanarak alanı aç."
            ],
            "Trafik Kazası": [
                "1. [İŞARET] Dubalarla yolu daralt, trafiği yavaşlat.",
                "2. [YARDIM] Yaralı varsa 112'ye haber ver, araçtan çıkarma.",
                "3. [TUTANAK] Kaza krokisini çiz ve tutanak tut."
            ],
            "Hırsızlık": [
                "1. [ÇEVRE] Kaçış yollarını tut, kamera kayıtlarını iste.",
                "2. [DELİL] Olay yerini şeritle kapat, parmak izi ekibini çağır.",
                "3. [TAKİP] Eşkal bilgilerini merkezle paylaş."
            ],
            "Rehine Krizi": [
                "1. [ABLUKA] Bölgeye kimseyi yaklaştırma, keskin nişancı yerleştir.",
                "2. [MÜZAKERE] Saldırganla iletişim kur, taleplerini öğren.",
                "3. [OPERASYON] Müzakere başarısız olursa Özel Harekat (PÖH) devreye girsin."
            ],
            "Şüpheli Paket": [
                "1. [BOŞALT] Çevreyi 100m boşalt, sinyal kesici (Jammer) çalıştır.",
                "2. [UZMAN] Bomba imha uzmanını çağır.",
                "3. [KONTROL] Fünye ile kontrollü patlatma yap."
            ],
            "Kavga/Darp": [
                "1. [AYIR] Tarafları güvenli mesafeye ayır.",
                "2. [TESPİT] Kesici/delici alet var mı kontrol et.",
                "3. [GÖZALTI] Şikayetçileri ve şüphelileri karakola götür."
            ],
            "Kalp Krizi": [
                "1. [VİTAL] Nabız ve solunum kontrolü yap.",
                "2. [CPR] Solunum yoksa kalp masajına başla, AED cihazını hazırla.",
                "3. [NAKİL] Damar yolu aç, en yakın KVC merkezine götür."
            ],
            "Yaralanma": [
                "1. [KANAMA] Turnike veya bası uygulayarak kanamayı durdur.",
                "2. [STABİLİZE] Boyunluk tak, omurga tahtasına al.",
                "3. [NAKİL] Travma merkezine hızlı sevk et."
            ],
            "Zehirlenme": [
                "1. [TANIM] Zehirleyen maddeyi tespit et (İlaç kutusu, gaz kokusu).",
                "2. [MÜDAHALE] Solunum yolunu açık tut, kusturma (yakıcı madde değilse).",
                "3. [ANTİDOT] Uygun panzehiri hazırla, hastaneye bildir."
            ],
            "Doğum": [
                "1. [HAZIRLIK] Steril ortam oluştur, mahremiyeti sağla.",
                "2. [KARŞILAMA] Bebeğin başı göründüğünde nazikçe destekle.",
                "3. [BAKIM] Kordonu klemple, bebeği ısıt ve anneye ver."
            ],
            "Bayılma": [
                "1. [POZİSYON] Hastayı sırtüstü yatır, ayaklarını 30cm kaldır (Şok pozisyonu).",
                "2. [AÇIKLIK] Hava yolunu kontrol et, yakasını gevşet.",
                "3. [ŞEKER] Bilinci açılınca kan şekerini ölç."
            ]
        }

        # Olayın sonucunda oluşacak ölü ve yaralı sayılarını belirler
        number_of_injured = np.random.choice([0,1,2,3,0,0,0,5])
        number_of_death = np.random.choice([0,1,2,3,0,0,1])
    
        # Gelen olay türünü listede arar ve ilgili planı uygular
        for case_type, events in plans.items():
            if case == case_type:
                if self.nearest_unit:
                    # Vakayı tüm adımlarıyla birlikte kaydeder
                    msg_header = f"--- YENİ OPERASYON: {case_type} | BİRİM: {self.nearest_unit.unit_type} (ID: {self.nearest_unit.unit_id}) ---"
                    self.repository.save_event_history(msg_header)

                    print("="*30)
                    print(f"[BİLGİ] {self.nearest_unit.unit_id} ID'ye sahip {self.nearest_unit.unit_type} olay yerine intikal etti.")
                    print("="*30)
                    print("\n")
                else:
                    print("[UYARI] Hiçbir birim atanmamış!")
                    return
                    
                print("="*30)
                print(f"[BİLGİ] Olay: {case_type}")
                print(f"[BİLGİ] Olaya müdahale planı oluşturuluyor...")
                time.sleep(2)               
                print(f"[BİLGİ] Olaya müdahale planı oluşturuldu.")
                print(f"[BİLGİ] Müdahaleye başlanıyor...")
                
                self.repository.save_event_history(f"[BİLGİ] Plan oluşturuldu, müdahale başlıyor.")
                
                time.sleep(1.5)
                print(f"[BİLGİ] Müdahaleye başlandı...")
                time.sleep(1.5)

                # Planın her bir adımını sırayla bekleyerek ekrana yazdırır
                for event in events:
                    print(f"---> {event}")
                    self.repository.save_event_history(f"ADIM UYGULANDI: {event}")
                    time.sleep(2)

                print("[BİLGİ] Müdahale tamamlandı.")
                self.repository.save_event_history("[BİLGİ] Operasyon adımları tamamlandı.")
                
                time.sleep(2)
                print("\n")
                
                # Sadece tehlikeli olaylarda ölü/yaralı raporu verir
                if case_type in ["Trafik Kazası", "Yangın", "Patlama", "Çökme"]:
                     print("="*30)
                     report_msg = f"[SONUÇ RAPORU] Yaralı Sayısı: {number_of_injured} - Ölü Sayısı: {number_of_death}"
                     print(report_msg)
                     self.repository.save_event_history(f"[SONUÇ RAPORU] Yaralı: {number_of_injured} | Vefat: {number_of_death}")
                else:
                     print(f"[SONUÇ RAPORU] Yaralı/Ölü Yok.")
                     self.repository.save_event_history("[SONUÇ RAPORU] Herhangi bir yaralanma veya can kaybı yok.")

                if number_of_injured > 0 or number_of_death > 0:
                    print(["[SİSTEM] Ambulans olay yerine gönderiliyor"])

                print(f"[BİLGİ] Birim olay yerinden ayrılıyor...")
                self.repository.save_event_history("Birim merkeze dönüyor.\n" +f"{'='*50}")

                # İşlemleri tamamlar ve döngüden çıkar
                break

    # Log yönetim paneli
    def event_log_management(self):
        while True:
            print("\n" + "="*40)
            print("📂 LOG YÖNETİM PANELİ")
            print("="*40)
            print(" [1] 📋 Vaka Geçmişi (Case Log)")
            print(" [2] 🚒 Filo Durumu (Units Log)")
            print(" [3] ⚡ Sistem Hareketleri (Event History)")
            print(" [4] 🔙 Ana Menüye Dön")
            print("-" * 40)
            
            text = input("👉 Dosya Seçiniz: ")

            if text == "4":
                print("Log panelinden çıkılıyor...")
                break

            target_file = ""
            if text == "1":
                target_file = self.repository.file_name
            elif text == "2":
                target_file = self.repository.status_file
            elif text == "3":
                target_file = self.repository.event_history_file
            else:
                print("[HATA] Geçersiz seçim.")
                continue

            while True:
                print(f"\n--- İŞLEM MENÜSÜ: {target_file} ---")
                print(" 1- Oku (Tümünü Göster)")
                print(" 2- Hata Bul (Sadece 'HATA' satırları)")
                print(" 3- Sil (Dosyayı Temizle)")
                print(" 4- Geri Dön (Dosya Seçimine)")

                text = input("Seçim: ")

                # okuma
                if text == "1":
                    try:
                        if os.path.exists(target_file):
                            print(f"\n📄 DOSYA İÇERİĞİ:\n" + "-"*30)
                            with open(target_file, "r", encoding="utf-8") as f:
                                print(f.read())
                            print("-" * 30)
                        else:
                            print("[BİLGİ] Dosya henüz oluşmamış")
                    except Exception as e:
                        print(f"[HATA] Okuma hatası: {e}")

                # hata bulma
                elif text == "2":
                    try:
                        if os.path.exists(target_file):
                            print(f"\n🔍 BULUNAN HATALAR:\n" + "-"*30)
                            found = False
                            with open(target_file, "r", encoding="utf-8") as f:
                                for line in f:
                                    if "HATA" in line.upper() or "FAIL" in line.upper() or "ERROR" in line.upper():
                                        print("🔴 " + line.strip())
                                        found = True
                            if not found:
                                print("✅ Hata kaydı bulunamadı")
                            print("-" * 30)
                        else:
                            print("[BİLGİ] Dosya henüz oluşmamış")
                    except Exception as e:
                         print(f"[HATA] Okuma hatası: {e}")

                # silme
                elif text == "3":
                    onay = input("⚠️ Dosya içeriği tamamen silinecek! Emin misin? (E/H): ").upper()
                    if onay == "E":
                        with open(target_file, "w", encoding="utf-8") as f:
                            f.write("") 
                        print("[BİLGİ] Loglar temizlendi. ✅")
                    else:
                        print("[BİLGİ] İşlem iptal edildi.")

                # çık
                elif text == "4":
                    break 
                
                else:
                    print("[UYARI] Geçersiz seçim.")

    def set_unit_in_service(self, target_unit, all_units):
        if target_unit.availability:
            print(f"\n[BİLGİ] {target_unit.unit_id} ID'li araç zaten hizmette ve müsait.")
            return

        # Durumları günceller
        target_unit.availability = True
        target_unit.is_it_on_duty = False  # Görevden döndü varsayıyoruz
        target_unit.is_siren_on = False    # Sirenleri kapat
        
        print(f"\n[İŞLEM] {target_unit.unit_type} (ID: {target_unit.unit_id}) başarıyla HİZMETE ALINDI. ✅")
        print("[SİSTEM] Araç listesi güncelleniyor...")
        
        # Değişikliği anında veritabanına işler
        self.repository.save_unit_info(all_units)

    def set_unit_out_of_service(self, target_unit, all_units, reason):
        if not target_unit.availability:
            print(f"\n[BİLGİ] {target_unit.unit_id} ID'li araç zaten hizmet dışı.")
            return

        # Durumları güncelle
        target_unit.availability = False
        target_unit.is_it_on_duty = False # Görevde değil, sadece pasif
        target_unit.is_siren_on = False
        
        print(f"\n[İŞLEM] {target_unit.unit_type} (ID: {target_unit.unit_id}) HİZMET DIŞI bırakıldı. ⛔")
        print(f"        Sebep: {reason}")
        print("[SİSTEM] Araç listesi güncelleniyor...")

        # Değişikliği anında veritabanına işler
        self.repository.save_unit_info(all_units)

    def manage_unit_status(self, all_units):
        print("\n" + "="*45)
        print("         🔧 FİLO YÖNETİM PANELİ 🔧")
        print("="*45)
        
        # Kullanıcıdan ID alıyoruz
        u_id = input("👉 İşlem yapılacak Araç ID'sini girin: ")
        
        # Sayı girip girmediğini kontrol ediyoruz
        try:
            u_id = int(u_id)
        except ValueError:
            print("! Hata: Lütfen geçerli bir sayı girin.")
            return

        # Aracı listede arıyoruz
        target_unit = None
        for unit in all_units:
            if unit.unit_id == u_id:
                target_unit = unit
                break
        
        # Eğer araç bulunduysa menüyü gösteriyoruz
        if target_unit:
            # Görsel durum belirteci
            status_icon = "🟢" if target_unit.availability else "🔴"
            status_text = "MÜSAİT (HİZMETTE)" if target_unit.availability else "HİZMET DIŞI"
            
            print(f"\nSeçilen Araç: {target_unit.unit_type} (ID: {target_unit.unit_id})")
            print(f"Mevcut Durum: {status_icon} {status_text}")
            print("-" * 45)
            print("  [1] ✅ Hizmete Al (Operasyona Hazırla)")
            print("  [2] ⛔ Hizmet Dışı Bırak (Bakım/Mola/Arıza)")
            print("  [3] 🔧 Bakım/Onarım Yap")
            print("  [4] 🔙 İptal")
            print("-" * 45)
            
            secim = input("Kararınız: ")
            
            if secim == "1":
                self.set_unit_in_service(target_unit, all_units)
                
            elif secim == "2":
                reason = input("Hizmet dışı bırakma sebebi nedir? (Örn: Yemek Molası): ")
                self.set_unit_out_of_service(target_unit, all_units, reason)
                
            elif secim == "3":
                print(f"\n[BAKIM] {target_unit.unit_id} nolu araç için bakım prosedürü başlatılıyor...")
                time.sleep(1)
                
                # Çok biçimlili örneği
                target_unit.refill_tank()
                
                # Eğer araçta arıza varsa düzeltir
                if hasattr(target_unit, 'is_broken'):
                    target_unit.is_broken = False
                
                # Kayıt yapar
                print("[BAKIM] Tüm depolar dolduruldu ve mekanik kontroller yapıldı")
                self.repository.save_unit_info(all_units)
                self.repository.save_event_history(f"[BAKIM] {target_unit.unit_id} serviste bakımdan geçti")

            elif secim == "4":
                print("[BİLGİ] İşlem iptal edildi, ana menüye dönülüyor.")
                
            else:
                print("[HATA] Geçersiz seçim yaptınız.")
                
        else:
            print("[HATA] Bu ID numarasına sahip bir araç bulunamadı.")

    def delete_unit_log(self):
        id = int(input("Silinecek aracın ID: "))

        self.repository.delete_unit_from_file(id)


class HumanService:
    def __init__(self, repository):
        self.__population_registry = []
        self.__repository = repository

    @property
    def population_registry(self):
        return self.__population_registry
    
    @population_registry.setter
    def population_registry(self, new):
        self.__population_registry = new

    @property
    def repository(self):
        return self.__repository
    
    @repository.setter
    def repository(self, new):
        self.__repository = new

    def register_human(self, human):
        if human in None:
            print("[HATA] Geçersiz kayıt denemesi")

        if human not in self.__population_registry:
            self.__population_registry.append(human)
            self.__repository.save_human_registry(human)
            print(f"[SİSTEM] {human.name} {human.lastname} suçlu olarak sisteme kaydedildi.")
            return True
        else:
            print(f"[SİSTEM] {human.name} zaten sistemde kayıtlı.")
            return False

    def register_criminal(self, criminal):
        if criminal is None:
            print("[HATA] Geçersiz kayıt denemesi")
            return False
            
        if criminal not in self.__population_registry:
            self.__population_registry.append(criminal)
            self.__repository.save_criminal_record(criminal)
            print(f"[SİSTEM] {criminal.name} {criminal.lastname} suçlu olarak sisteme kaydedildi.")
            return True
        else:
            print(f"[SİSTEM] {criminal.name} zaten sistemde kayıtlı.")
            return False

    def register_victim(self, victim):
        if victim is None:
            print("[HATA] Geçersiz kayıt denemesi: Nesne boş.")
            return False
            
        if victim not in self.__population_registry:
            self.__population_registry.append(victim)
            self.__repository.save_victim_record(victim)
            print(f"[SİSTEM] {victim.name} {victim.lastname} mağdur olarak sisteme kaydedildi.")
            return True
        else:
            print(f"[SİSTEM] {victim.name} zaten sistemde kayıtlı.")
            return False

    def update_criminal_status(self, criminal_id, is_caught):
        for person in self.__population_registry:
            if isinstance(person, Criminal) and person.id == criminal_id:
                person.is_caught = is_caught
                self.__repository.update_criminal_status(criminal_id, is_caught)
                return True
        
        print(f"[HATA] {criminal_id} TC'li suçlu sistemde bulunamadı")
        return False

    def find_person_by_id(self, person_id):
        print(f"[ARAMA] ID: {person_id} için veritabanı taranıyor...")
        
        for person in self.__population_registry:
            if person.id == person_id:
                print(f"[BULUNDU] Kişi: {person.name} {person.lastname}")
                return person
        
        print("[BULUNAMADI] Belirtilen ID ile eşleşen kayıt yok.")
        return None

    def filter_critical_victims(self, min_severity=5):
        critical_list = []
        print(f"[SİSTEM] Yaralanma derecesi {min_severity} ve üzeri olanlar listeleniyor...")
        
        for person in self.__population_registry:
            if isinstance(person, Victim) and person.is_alive:
                if person.degree_of_injury >= min_severity:
                    critical_list.append(person)
                    print(f" [SİSTEM] Eklendi: {person.name} (Derece: {person.degree_of_injury})")
        
        return critical_list

    def get_registry_count(self):
        count = len(self.__population_registry)
        print(f"[BİLGİ] Şu an sistemde {count} kayıtlı insan var.")
        return count

    def list_all_criminals(self):
        criminals = [p for p in self.__population_registry if isinstance(p, Criminal)]
        
        if not criminals:
            print("[BİLGİ] Sistemde kayıtlı suçlu bulunmamaktadır.")
            return
        
        print("\n" + "="*50)
        print("          🚨 SUÇLU LİSTESİ 🚨")
        print("="*50)
        
        for criminal in criminals:
            status = "🔴 FİRARDA" if not criminal.is_caught else "🟢 GÖZALTINDA"
            print(f"TC: {criminal.id} | {criminal.name} {criminal.lastname}")
            print(f"   Tehlike: {criminal.danger_level}/10 | Durum: {status}")
            print("-" * 50)

    def list_all_victims(self):
        victims = [p for p in self.__population_registry if isinstance(p, Victim)]
        
        if not victims:
            print("[BİLGİ] Sistemde kayıtlı mağdur bulunmamaktadır.")
            return
        
        print("\n" + "="*50)
        print("          🚑 MAĞDUR LİSTESİ 🚑")
        print("="*50)
        
        for victim in victims:
            severity = "🔴 KRİTİK" if victim.degree_of_injury > 7 else "🟡 CİDDİ" if victim.degree_of_injury > 4 else "🟢 HAFİF"
            print(f"TC: {victim.id} | {victim.name} {victim.lastname}")
            print(f"   Yaralanma: {victim.degree_of_injury}/10 | Durum: {severity}")
            print("-" * 50)


class StructureService():
    def __init__(self, repository):
        self.__structures = []
        self.__repository = repository

    @property
    def structures(self):
        return self.__structures

    @structures.setter
    def structures(self, new):
        self.__structures = new

    @property
    def repository(self):
        return self.__repository

    @repository.setter
    def repository(self, new):
        self.__repository = new

    def register_structure(self, structure):
        if structure not in self.__structures:
            self.__structures.append(structure)
            self.__repository.save_structure_registry(self.__structures)
            print(f"[SİSTEM] Yeni yapı sisteme eklendi: {structure.name} (Konum: {structure.location})")

    def dispatch_nearest_unit(self, incident_location, needed_type):
        best_candidate = None
        min_dist = 9999999

        structures = [s for s in self.__structures if isinstance(s, needed_type)]

        print(f"\n[SİSTEM] Konum {incident_location} için en uygun {needed_type.__name__} aranıyor...")

        for struct in structures:
            dist = StructureService.calculate_logistical_cost(incident_location, struct.location)
        
            if struct.current_occupancy < struct.capacity:
                if dist < min_dist:
                    min_dist = dist
                    best_candidate = struct
    
        if best_candidate:
            print(f"✅ BULUNDU: {best_candidate.name})")
            return best_candidate
        else:
            print("❌ KRİTİK: Uygun kapasiteye sahip birim bulunamadı!")
            return None

    @staticmethod
    def calculate_logistical_cost(loc1, loc2):
        return abs(loc1 - loc2) * 1.5

    def list_all_structures(self):
        if not self.__structures:
            print("[BİLGİ] Sistemde kayıtlı yapı bulunmamaktadır.")
            return
    
        print("\n" + "="*50)
        print("          🏥 YAPI LİSTESİ 🏥")
        print("="*50)
    
        for structure in self.__structures:
            if isinstance(structure, Hospital):
                struct_type = "🏥 Hastane"
                info = f"Yatak: {structure.current_occupancy}/{structure.capacity}"
            elif isinstance(structure, PoliceStation):
                struct_type = "🚓 Karakol"
                info = f"Gözaltı: {structure.current_occupancy}/{structure.capacity}"
            elif isinstance(structure, FireStation):
                struct_type = "🚒 İtfaiye"
                info = f"Araç: {structure.current_occupancy}/{structure.capacity}"
            else:
                struct_type = "🏛 Diğer"
                info = f"Kapasite: {structure.current_occupancy}/{structure.capacity}"
        
            print(f"{struct_type} | {structure.name}")
            print(f"   Konum: {structure.location} | {info}")
            print("-" * 50)

    def manage_structure_capacity(self):
        if not self.__structures:
            print("[BİLGİ] Yönetilecek yapı bulunmamaktadır.")
            return
    
        print("\n" + "="*50)
        print("         📊 YAPI KAPASİTE YÖNETİMİ")
        print("="*50)
    
        for i, structure in enumerate(self.__structures):
            print(f"[{i+1}] {structure.name} ({type(structure).__name__})")
            print(f"     Mevcut: {structure.current_occupancy}/{structure.capacity}")
    
        try:
            choice = int(input("\n👉 İşlem yapmak istediğiniz yapı numarası: ")) - 1
            if choice < 0 or choice >= len(self.__structures):
                print("[HATA] Geçersiz seçim!")
                return
        except ValueError:
            print("[HATA] Lütfen sayı giriniz!")
            return
    
        selected = self.__structures[choice]
    
        print(f"\nSeçilen yapı: {selected.name}")
        print(f"Mevcut durum: {selected.current_occupancy}/{selected.capacity}")
    
        print("\n[1] Kapasiteyi Artır (Yeni hasta/gözaltı ekle)")
        print("[2] Kapasiteyi Azalt (Taburcu/serbest bırak)")
        print("[3] Kapasite Bilgilerini Güncelle")
        print("[4] İptal")
    
        try:
            text = input("Seçiminiz: ")
        
            if text == "1":
                if selected.current_occupancy < selected.capacity:
                    selected.current_occupancy += 1
                    print(f"[BAŞARILI] Kapasite artırıldı: {selected.current_occupancy}/{selected.capacity}")
                    self.__repository.save_structure_registry(self.__structures)
                    self.__repository.save_event_history(f"[KAPASİTE] {selected.name} kapasitesi artırıldı")
                else:
                    print("[UYARI] Maksimum kapasiteye ulaşıldı!")
        
            elif text == "2":
                if selected.current_occupancy > 0:
                    selected.current_occupancy -= 1
                    print(f"[BAŞARILI] Kapasite azaltıldı: {selected.current_occupancy}/{selected.capacity}")
                    self.__repository.save_structure_registry(self.__structures)
                    self.__repository.save_event_history(f"[KAPASİTE] {selected.name} kapasitesi azaltıldı")
                else:
                    print("[UYARI] Zaten boş!")
        
            elif text == "3":
                try:
                    new_current = int(input("Yeni mevcut doluluk: "))
                    new_capacity = int(input("Yeni toplam kapasite: "))
                
                    if new_current < 0 or new_capacity < 0:
                        print("[HATA] Negatif değer olamaz!")
                        return
                
                    if new_current > new_capacity:
                        print("[HATA] Mevcut doluluk kapasiteden fazla olamaz!")
                        return
                
                    selected.current_occupancy = new_current
                    selected.capacity = new_capacity
                    print(f"[BAŞARILI] Kapasite güncellendi: {selected.current_occupancy}/{selected.capacity}")
                    self.__repository.save_structure_registry(self.__structures)
                    self.__repository.save_event_history(f"[KAPASİTE] {selected.name} kapasitesi tamamen güncellendi")
                except ValueError:
                    print("[HATA] Geçersiz sayı formatı!")
        
            elif text == "4":
                print("[BİLGİ] İşlem iptal edildi.")
        
            else:
                print("[HATA] Geçersiz seçim!")
    
        except Exception as e:
            print(f"[HATA] İşlem sırasında hata: {e}")

    def find_structure_by_name(self, name):
        for structure in self.__structures:
            if structure.name.lower() == name.lower():
                return structure
        return None

    def get_structure_statistics(self):
        stats = {
            "total": len(self.__structures),
            "hospitals": 0,
            "police_stations": 0,
            "fire_stations": 0,
            "total_capacity": 0,
            "total_occupancy": 0
        }
    
        for structure in self.__structures:
            stats["total_capacity"] += structure.capacity
            stats["total_occupancy"] += structure.current_occupancy
        
            if isinstance(structure, Hospital):
                stats["hospitals"] += 1
            elif isinstance(structure, PoliceStation):
                stats["police_stations"] += 1
            elif isinstance(structure, FireStation):
                stats["fire_stations"] += 1
    
        return stats

    def show_statistics(self):
        stats = self.get_structure_statistics()
    
        print("\n" + "="*50)
        print("          📈 YAPI İSTATİSTİKLERİ")
        print("="*50)
    
        print(f"Toplam Yapı Sayısı: {stats['total']}")
        print(f"🏥 Hastane Sayısı: {stats['hospitals']}")
        print(f"🚓 Karakol Sayısı: {stats['police_stations']}")
        print(f"🚒 İtfaiye Sayısı: {stats['fire_stations']}")
        print(f"Toplam Kapasite: {stats['total_capacity']}")
        print(f"Toplam Doluluk: {stats['total_occupancy']}")
        print(f"Doluluk Oranı: %{(stats['total_occupancy']/stats['total_capacity']*100 if stats['total_capacity']>0 else 0):.1f}")
    
        if stats['total_occupancy'] > stats['total_capacity'] * 0.8:
            print("[UYARI] Sistem kapasitesi kritik seviyede!")
    
        print("="*50)