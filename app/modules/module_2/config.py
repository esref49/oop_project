"""
Sistem Konfigürasyon Dosyası (config.py)
----------------------------------------
Bu dosya, projede kullanılan tüm sabit değerleri, hata mesajlarını
ve fiyatlandırma politikalarını tek bir merkezi noktada tutar.
"""

# ===========================
# FİYATLANDIRMA POLİTİKALARI
# ===========================
UNIT_PRICES = {
    "Electricity": 1.5,  # TL/kWh
    "Water": 4.0,        # TL/m3
    "Gas": 5.0,          # TL/m3
    "Industrial_Electricity": 2.2 # Sanayi tarifesi (İleri sürümler için)
}

# ===========================
# SİSTEM LİMİTLERİ
# ===========================
SYSTEM_LIMITS = {
    "Max_Voltage": 400,
    "Min_Voltage": 180,
    "Max_Water_Pressure": 10.0,
    "Max_Gas_Pressure": 25.0,
    "Max_Daily_Usage_Alert": 1000.0
}

# ===========================
# DOSYA YOLLARI
# ===========================
PATHS = {
    "Database": "data/meters.json",
    "Logs": "logs/system_logs.txt",
    "Reports": "reports/daily_report.html"
}

# ===========================
# HATA MESAJLARI
# ===========================
ERROR_MESSAGES = {
    "Negative_Usage": "Hata: Kullanım miktarı negatif olamaz!",
    "Invalid_Voltage": "Hata: Voltaj değeri güvenli aralıkta değil!",
    "Meter_Not_Found": "Hata: Belirtilen ID ile eşleşen sayaç bulunamadı.",
    "DB_Connection_Error": "Veritabanına erişim sağlanamadı.",
    "Invalid_Type": "Geçersiz sayaç tipi belirtildi."
}

# ===========================
# RAPORLAMA AYARLARI
# ===========================
REPORT_CONFIG = {
    "Company_Name": "Akıllı Şehir A.Ş.",
    "Version": "1.0.2",
    "Developer": "Module 2 Team"
}