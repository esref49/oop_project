from abc import ABC, abstractmethod

class EmergencyUnit(ABC):
    def __init__(self, unit_id, unit_type, current_location, availability, fuel_level, is_enough_staff, is_siren_on = False, is_it_on_duty = False, max_fuel_level = 50):
        self.__unit_id = unit_id
        self.unit_type = unit_type
        self.__current_location = current_location
        self.availability = availability
        self.fuel_level = fuel_level
        self.is_enough_staff = is_enough_staff
        self.is_siren_on = is_siren_on
        self.is_it_on_duty = is_it_on_duty
        self.max_fuel_level = max_fuel_level

    @property
    def unit_id(self):
        return self.__unit_id
    
    @unit_id.setter
    def unit_id(self, new_id):
        self.__unit_id = new_id

    @property
    def current_location(self):
        return self.__current_location
    
    @current_location.setter
    def current_location(self, new_locate):
        self.__current_location = new_locate

    @abstractmethod
    def update_location(self):
        # Birimin konumunu günceller
        pass

    @abstractmethod
    def open_siren(self):
        # Birimin sirenini açar
        pass

    @abstractmethod
    def report_location(self):
        # Birimin konumunu bildirir
        pass
    
    @abstractmethod
    def report_fault(self):
        # Birimin arıza bildirimini yapar
        pass

    @abstractmethod
    def determine_availability(self):
        # Birimin müsaitlik durumunu belirler
        pass

    @abstractmethod
    def get_detailed_status(self):
        # Birime özel araç kimlik kartı oluşturur
        pass
    
    @abstractmethod
    def refill_tank(self):
        # Birimim depolarını doldurur
        pass