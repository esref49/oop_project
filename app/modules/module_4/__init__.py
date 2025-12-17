# Module 4 - Sosyal Hizmetler Modülü
# Bu modül belediyenin sosyal hizmet ve destek programlarını yönetir
from .base import SocialService
from .implementations import GidaYardimi, BarinmaDestegi, EgitimDestegi
from .repository import SosyalHizmetRepository
from .services import SosyalHizmetServisi
from app.modules.module_4 import GidaYardimi, BarinmaDestegi
# Modülden dışarı açılacak sınıflar
__all__ = [
    'SocialService',
    'GidaYardimi',
    'BarinmaDestegi',
    'EgitimDestegi',
    'SosyalHizmetRepository',
    'SosyalHizmetServisi'
]
# Modül versiyonu
__version__ = '1.0.0'
# Modül bilgileri
__author__ = 'Module 4 Team'
__description__ = 'Sosyal Hizmetler Yönetim Modülü'

