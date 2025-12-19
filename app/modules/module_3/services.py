import time
import numpy as np

class EmergencyService:
    def __init__(self, repository):
        self.nearest_unit = None
        self.repository = repository
        self.location = np.random.randint(0,22)

    def creating_case(self, case_type, severity, unit_list):
        # Olaya verilen puana göre olayın ciddiyetini belirler.
        if severity > 8:
            is_critical = "Evet"
        else:
            is_critical = "Hayır"
        
        # En yakın birimi bul
        self.nearest_unit = self.finding_the_nearest_unit(unit_list, self.get_unit_type_for_case(case_type))
        
        # Vaka bilgilerini sözlük içinde toplar.
        new_case = {
            "location": self.location,
            "type": case_type,
            "severity": severity,
            "critical_status": is_critical,
            "status": "Active",
            "assigned_unit": self.nearest_unit.unit_type if self.nearest_unit else None,
            "assigned_unit_id": self.nearest_unit.unit_id if self.nearest_unit else None
        }
        
        # Yeni vakanın oluştuğu bilgisini verir.
        print("="*30)
        print(f"Vaka konumu: {new_case['location']}")
        print(f"Vaka türü: {new_case['type']}")
        print(f"Vaka seviyesi: {new_case['severity']}")
        print(f"Vaka kritik mi: {new_case['critical_status']}")
        print(f"Görevlendirilen birim: {new_case['assigned_unit']}")
        print(f"Görevlendirilen birim ID: {new_case['assigned_unit_id']}")
        print("="*30)
        print("\n")
        
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
        
    def finding_the_nearest_unit(self, unit_list, unit_type):
        # En yakın aracı bulmak için başlangıç değişkenlerini tanımlar.
        min_distance = 999999999999
        self.nearest_unit = None  # Reset each time

        # Verilen listedeki tüm araçları tek tek kontrol eder.
        for unit in unit_list: 
            # Aracın müsait olup olmadığını ve olay tipine uygunluğunu kontrol eder.
            if unit.availability and unit.unit_type == unit_type:
                # Olay yeri ile araç arasındaki mesafeyi hesaplar.
                distance = abs(unit.current_location - self.location) 

                # Eğer bu araç daha önce bulunanlardan daha yakınsa, en yakın olarak bunu seçer.
                if distance < min_distance:
                    min_distance = distance
                    self.nearest_unit = unit
                    
        # Eğer uygun bir araç bulunduysa sevk işlemlerini başlatır.
        if self.nearest_unit:
            print("\n")
            print("="*30)
            print("[INFO] Yeni vaka oluşturuldu")
            print(f"[INFO] {self.nearest_unit.unit_id} kodlu {self.nearest_unit.unit_type} olay yerine sevk ediliyor.")
            print(f"[INFO] Tahmini Mesafe: {min_distance} km")
            print(f"[INFO] {self.nearest_unit.unit_type} biriminin anlık konumu: {self.nearest_unit.current_location}") 
            print("="*30)
            print("\n")
            
            # Aracın durumunu günceller: Göreve çıkarır, meşgul yapar, sireni açar ve konumunu değiştirir.
            self.nearest_unit.is_it_on_duty = True
            self.nearest_unit.availability = False 
            self.nearest_unit.open_siren()
            return self.nearest_unit
        else:
            # Hiçbir araç bulunamazsa hata mesajı verir.
            print(f"[-]: {unit_type} türünde müsait araç bulunamadı!")  # DÜZELTİLDİ
            return None

    def creating_intervention_plan(self, case):
        # Her olay türü için yapılması gereken adım adım prosedürleri içeren liste.
        
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

        # Olayın sonucunda oluşacak rastgele ölü ve yaralı sayılarını belirler.
        number_of_injured = np.random.choice([0,1,2,3,0,0,0,5])
        death_toll = np.random.choice([0,1,2,3,0,0,1])
    
        # Gelen olay türünü listede arar ve ilgili planı uygular.
        for case_type, events in plans.items():
            if case == case_type:
                # Olay yerine ulaşan birimin bilgisini verir.
                if self.nearest_unit:
                    print("="*30)
                    print(f"[INFO] {self.nearest_unit.unit_id} ID'ye sahip {self.nearest_unit.unit_type} olay yerine intikal etti.")
                    print("="*30)
                    print("\n")
                else:
                    print("[UYARI] Hiçbir birim atanmamış!")
                    return
                    
                print("="*30)
                print(f"[INFO] Olay: {case_type}")
                print(f"[INFO] Olaya müdahale planı oluşturuluyor...")
                time.sleep(2)               
                print(f"[INFO] Olaya müdahale planı oluşturuldu.")
                print(f"[INFO] Müdahaleye başlanıyor...")
                time.sleep(1.5)
                print(f"[INFO] Müdahaleye başlandı...")
                time.sleep(1.5)

                # Planın her bir adımını sırayla bekleyerek ekrana yazdırır.
                for event in events:
                    print(f">> {event}")
                    time.sleep(2)

                print("[INFO] Müdahale tamamlandı.")
                time.sleep(2)
                print("\n")
                
                # Sadece tehlikeli olaylarda ölü/yaralı raporu verir.
                if case_type in ["Trafik Kazası", "Yangın", "Patlama", "Çökme"]:
                     print("="*30)
                     print(f"[INFO] Yaralı Sayısı: {number_of_injured} - Ölü Sayısı: {death_toll}")
                else:
                     print(f"[INFO] Yaralı/Ölü Yok.")

                # Birimin görevini tamamlayıp ayrıldığını bildirir.
                print(f"[INFO] Birim olay yerinden ayrılıyor...")
                break
            
    def event_log_management(self):
        file_name = "old_case_logs.txt"
        
        # Konsol menüsüyle logları yönetiyoruz.
        while True:
            print("\n--- LOG PANELİ: 1-Oku, 2-Hata Bul, 3-Sil, 4-Çık ---")
            text = input("Seçim: ")

            if text == "":
                print("! Boş seçim yapma.")
            
            elif text in ["4", "çıkış", "q"]:
                break
            
            elif text == "1":
                try:
                    with open(file_name, "r", encoding="utf-8") as f:
                        print(f.read())
                except FileNotFoundError:
                    print("! Henüz log oluşmamış.")
            
            elif text == "2":
                try:
                    with open(file_name, "r", encoding="utf-8") as f:
                        for line in f:
                            # Sadece hataları filtreliyoruz.
                            if "HATA" in line: 
                                print(line.strip())
                except FileNotFoundError:
                    print("! Henüz log oluşmamış.")
            
            elif text == "3":
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write("") 
                print("Loglar temizlendi.")
            
            else:
                print("! Geçersiz seçim.")