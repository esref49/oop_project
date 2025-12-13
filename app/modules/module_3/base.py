from abc import ABC, abstractmethod

class EmergencyUnit(ABC):
    def __init__(self, unit_id, unit_type, current_location, availability, fuel_level, is_enough_staff, is_siren_on = False, is_it_on_duty = False):
        self.unit_id = unit_id
        self.unit_type = unit_type
        self.current_location = current_location
        self.availability = availability
        self.fuel_level = fuel_level
        self.is_enough_staff = is_enough_staff
        self.is_siren_on = is_siren_on
        self.is_it_on_duty = is_it_on_duty

    @abstractmethod
    def update_location(self):
        # Birimin konumunu güncelleme
        pass

    @abstractmethod
    def open_siren(self):
        # Birimin konumunu güncelleme
        pass

    @abstractmethod
    def report_location(self):
        # Konumu bildirir
        pass

    @abstractmethod
    def report_status(self):
        # Durum bildirir
        pass
    
    @abstractmethod
    def report_fault(self):
        # Arıza bildirimi yapar
        pass

    @abstractmethod
    def determine_availability(self):
        # Müsaitlik durumunu belirler
        pass