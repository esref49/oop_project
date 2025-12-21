import os
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
        
        # Vaka bilgilerini sözlük içinde toplar
        new_case = {
            "location": self.location,
            "type": case_type,
            "severity": severity,
            "critical_status": is_critical,
            "status": "Active",
            "assigned_unit": self.nearest_unit.unit_type if self.nearest_unit else None,
            "assigned_unit_id": self.nearest_unit.unit_id if self.nearest_unit else None
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
        # En yakın aracı bulmak için başlangıç değişkenlerini tanımlar
        min_distance = 999999999999
        self.nearest_unit = None

        # Verilen listedeki tüm araçları tek tek kontrol eder
        for unit in unit_list: 
            # Aracın müsait olup olmadığını ve olay tipine uygunluğunu kontrol eder
            if unit.availability and unit.unit_type == unit_type:
                # Olay yeri ile araç arasındaki mesafeyi hesaplar.
                distance = abs(unit.current_location - self.location) 

                # Eğer bu araç daha önce bulunanlardan daha yakınsa, en yakın olarak bunu seçer
                if distance < min_distance:
                    min_distance = distance
                    self.nearest_unit = unit
                    
        # Eğer uygun bir araç bulunduysa sevk işlemlerini başlatır
        if self.nearest_unit:
            print("\n")
            print("="*30)
            print("[BİLGİ] Yeni vaka oluşturuldu")
            print(f"[BİLGİ] {self.nearest_unit.unit_id} kodlu {self.nearest_unit.unit_type} olay yerine sevk ediliyor.")
            print(f"[BİLGİ] Tahmini Mesafe: {min_distance} km")
            print(f"[BİLGİ] {self.nearest_unit.unit_type} biriminin anlık konumu: {self.nearest_unit.current_location}") 
            print("="*30)
            print("\n")
            
            # Aracın durumunu günceller: Göreve çıkarır, meşgul yapar, sireni açar ve konumunu değiştirir
            self.nearest_unit.is_it_on_duty = True
            self.nearest_unit.availability = False 
            # Çok biçimlilik örneği
            self.nearest_unit.open_siren()
            return self.nearest_unit
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
        death_toll = np.random.choice([0,1,2,3,0,0,1])
    
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
                # --- REPOSITORY KAYDI ---
                self.repository.save_event_history("[BİLGİ] Operasyon adımları tamamlandı.")
                
                time.sleep(2)
                print("\n")
                
                # Sadece tehlikeli olaylarda ölü/yaralı raporu verir
                if case_type in ["Trafik Kazası", "Yangın", "Patlama", "Çökme"]:
                     print("="*30)
                     report_msg = f"[SONUÇ RAPORU] Yaralı Sayısı: {number_of_injured} - Ölü Sayısı: {death_toll}"
                     print(report_msg)
                     self.repository.save_event_history(f"[SONUÇ RAPORU] Yaralı: {number_of_injured} | Vefat: {death_toll}")
                else:
                     print(f"[SONUÇ RAPORU] Yaralı/Ölü Yok.")
                     self.repository.save_event_history("[SONUÇ RAPORU] Herhangi bir yaralanma veya can kaybı yok.")

                # Birimin görevini tamamlayıp ayrıldığını bildirir
                print(f"[BİLGİ] Birim olay yerinden ayrılıyor...")
                # Yaptığı tüm işlemleri hem ekrana hem de veritabanına kaydeder ve 50 tane - ile kaydı bitirir
                self.repository.save_event_history(f"Birim merkeze dönüyor.\n {"-"*50}")

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