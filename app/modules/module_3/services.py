class EmergencyService():
    def __init__(self, repository):
        self.repository = repository

    def creating_case(self, location, case_type, severity):
        if severity > 8:
            is_critical = "Evet"
        else:
            is_critical = "Hayır"
        
        new_case = {
            "location": location,
            "type": case_type,
            "severity": severity,
            "critical_status": is_critical,
            "status": "Active",
            "assigned_unit": None
        }
        
        self.repository.log_incident(new_case)
        
        print(f"[INFO] Yeni vaka oluşturuldu: {case_type} - {location} - {severity}")
        return new_case

    def finding_the_nearest_unit(self, incident_location, unit_type):
        nearest_unit = None
        min_distance = 999999999999

        if self.repository.unit.availability and self.repository.unit.unit_type == unit_type and incident_location in self.repository.unit.patrol_area:
            distance = abs(self.repository.unit.current_location - incident_location) 

        if distance < min_distance:
                min_distance = distance
                nearest_unit = self.repository.unit
                    
        if nearest_unit:
            print(f"[INFO]: {nearest_unit.unit_id} kodlu {nearest_unit.unit_type} olay yerine sevk ediliyor.")
            print(f"           Tahmini Mesafe: {min_distance} km")
            
            nearest_unit.is_it_on_duty = True
            nearest_unit.availability = False 
            nearest_unit.open_siren()
            nearest_unit.update_location(incident_location) 
            return nearest_unit
        else:
            print(f"[-]: {unit_type} türünde müsait araç bulunamadı!")
            return None

    def creating_intervention_plan(self, case_type):
        
        plans = {
            # --- YANGIN & AFET GRUBU (İtfaiye) ---
            "Yangın": (
                "1. [GÜVENLİK] Çevre güvenliğini al, elektrik/gaz akışını kes.\n"
                "2. [MÜDAHALE] Rüzgarı arkana al, alevin kaynağına su/köpük sık.\n"
                "3. [KONTROL] Soğutma çalışması yap ve termal kamerayla kontrol et."
            ),
            "Kimyasal Sızıntı": (
                "1. [KARANTİNA] Bölgeyi 500m çapında boşalt. Maskesiz yaklaşma.\n"
                "2. [KBRN] Koruyucu (sarı) kıyafetleri giy.\n"
                "3. [İMHA] Sızıntıyı kaynağında tıka veya nötralize et."
            ),
            "Sel/Su Baskını": (
                "1. [ENERJİ] Elektrik hatlarını ana şalterden kapat.\n"
                "2. [TAHLİYE] Vatandaşları çatı veya yüksek bölgelere al.\n"
                "3. [TAHLİYE 2] Motopompları kur ve suyu tahliye et."
            ),
            "Mahsur Kalma": (
                "1. [İLETİŞİM] Kazazedeyle konuşarak sakinleştir.\n"
                "2. [ANALİZ] Sıkıştığı yerin stabilitesini kontrol et (göçük riski).\n"
                "3. [KURTARMA] Hidrolik makas/kesici kullanarak alanı aç."
            ),

            # --- ASAYİŞ GRUBU (Polis) ---
            "Trafik Kazası": (
                "1. [İŞARET] Dubalarla yolu daralt, trafiği yavaşlat.\n"
                "2. [YARDIM] Yaralı varsa 112'ye haber ver, araçtan çıkarma.\n"
                "3. [TUTANAK] Kaza krokisini çiz ve tutanak tut."
            ),
            "Hırsızlık": (
                "1. [ÇEVRE] Kaçış yollarını tut, kamera kayıtlarını iste.\n"
                "2. [DELİL] Olay yerini şeritle kapat, parmak izi ekibini çağır.\n"
                "3. [TAKİP] Eşkal bilgilerini merkezle paylaş."
            ),
            "Rehine Krizi": (
                "1. [ABLUKA] Bölgeye kimseyi yaklaştırma, keskin nişancı yerleştir.\n"
                "2. [MÜZAKERE] Saldırganla iletişim kur, taleplerini öğren.\n"
                "3. [OPERASYON] Müzakere başarısız olursa Özel Harekat (PÖH) devreye girsin."
            ),
            "Şüpheli Paket": (
                "1. [BOŞALT] Çevreyi 100m boşalt, sinyal kesici (Jammer) çalıştır.\n"
                "2. [UZMAN] Bomba imha uzmanını çağır.\n"
                "3. [KONTROL] Fünye ile kontrollü patlatma yap."
            ),
            "Kavga/Darp": (
                "1. [AYIR] Tarafları güvenli mesafeye ayır.\n"
                "2. [TESPİT] Kesici/delici alet var mı kontrol et.\n"
                "3. [GÖZALTI] Şikayetçileri ve şüphelileri karakola götür."
            ),

            # --- SAĞLIK GRUBU (Ambulans) ---
            "Kalp Krizi": (
                "1. [VİTAL] Nabız ve solunum kontrolü yap.\n"
                "2. [CPR] Solunum yoksa kalp masajına başla, AED cihazını hazırla.\n"
                "3. [NAKİL] Damar yolu aç, en yakın KVC merkezine götür."
            ),
            "Yaralanma": (
                "1. [KANAMA] Turnike veya bası uygulayarak kanamayı durdur.\n"
                "2. [STABİLİZE] Boyunluk tak, omurga tahtasına al.\n"
                "3. [NAKİL] Travma merkezine hızlı sevk et."
            ),
            "Zehirlenme": (
                "1. [TANIM] Zehirleyen maddeyi tespit et (İlaç kutusu, gaz kokusu).\n"
                "2. [MÜDAHALE] Solunum yolunu açık tut, kusturma (yakıcı madde değilse).\n"
                "3. [ANTİDOT] Uygun panzehiri hazırla, hastaneye bildir."
            ),
            "Doğum": (
                "1. [HAZIRLIK] Steril ortam oluştur, mahremiyeti sağla.\n"
                "2. [KARŞILAMA] Bebeğin başı göründüğünde nazikçe destekle.\n"
                "3. [BAKIM] Kordonu klemple, bebeği ısıt ve anneye ver."
            ),
            "Bayılma": (
                "1. [POZİSYON] Hastayı sırtüstü yatır, ayaklarını 30cm kaldır (Şok pozisyonu).\n"
                "2. [AÇIKLIK] Hava yolunu kontrol et, yakasını gevşet.\n"
                "3. [ŞEKER] Bilinci açılınca kan şekerini ölç."
            )
        }

        return plans.get(case_type, "[+] Standart protokoller uygulandı.")

    def event_log_management():
        pass