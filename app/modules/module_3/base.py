from abc import ABC, abstractmethod

class EmergencyUnit(ABC):
    total_fleet_count = 0

    def __init__(self, unit_id, unit_type, current_location, availability, fuel_level, is_enough_staff, is_siren_on = False, is_it_on_duty = False, max_fuel_level = 50):
        self.__unit_id = unit_id
        self.__unit_type = unit_type
        self.__current_location = current_location
        self.__availability = availability
        self.__fuel_level = fuel_level
        self.__is_enough_staff = is_enough_staff
        self.__is_siren_on = is_siren_on
        self.__is_it_on_duty = is_it_on_duty
        self.__max_fuel_level = max_fuel_level
        EmergencyUnit.total_fleet_count +=1

    @property
    def unit_id(self):
        return self.__unit_id
    
    @unit_id.setter
    def unit_id(self, new_id):
        self.__unit_id = new_id

    @property
    def unit_type(self):
        return self.__unit_type
    
    @unit_type.setter
    def unit_type(self, new):
        self.__unit_type = new

    @property
    def current_location(self):
        return self.__current_location
    
    @current_location.setter
    def current_location(self, new_locate):
        self.__current_location = new_locate


    @property
    def availability(self):
        return self.__availability
    
    @availability.setter
    def availability(self, status):
        self.__availability = status

    @property
    def fuel_level(self):
        return self.__fuel_level
    
    @fuel_level.setter
    def fuel_level(self, level):
        self.__fuel_level = level

    @property
    def is_enough_staff(self):
        return self.__is_enough_staff
    
    @is_enough_staff.setter
    def is_enough_staff(self, status):
        self.__is_enough_staff = status

    @property
    def is_siren_on(self):
        return self.__is_siren_on
    
    @is_siren_on.setter
    def is_siren_on(self, status):
        self.__is_siren_on = status

    @property
    def is_it_on_duty(self):
        return self.__is_it_on_duty
    
    @is_it_on_duty.setter
    def is_it_on_duty(self, status):
        self.__is_it_on_duty = status

    @property
    def max_fuel_level(self):
        return self.__max_fuel_level
    
    @max_fuel_level.setter
    def max_fuel_level(self, level):
        self.__max_fuel_level = level

    @abstractmethod
    def update_location(self):
        pass

    @abstractmethod
    def open_siren(self):
        pass

    @abstractmethod
    def report_location(self):
        pass
    
    @abstractmethod
    def report_accident(self):
        pass

    @abstractmethod
    def determine_availability(self):
        pass

    @abstractmethod
    def get_detailed_status(self):
        pass
    
    @abstractmethod
    def refill_tank(self):
        pass

    @classmethod
    def show_fleet_summary(cls):
        return f"[SİSTEM] Şu an envanterde toplam {cls.total_fleet_count} adet araç kayıtlıdır."
    

class Human(ABC):
    total_population = 0

    def __init__(self, id, name, lastname, age, blood_group, height, weight, is_alive):
        self.__id = id
        self.__name = name
        self.__lastname = lastname
        self.__age = age
        self.__blood_group = blood_group
        self.__height  = height
        self.__weight = weight
        self.__is_alive = is_alive
        Human.total_population += 1

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, new):
        self.__id = new

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, new):
        self.__name = new

    @property
    def lastname(self):
        return self.__lastname
    
    @lastname.setter
    def lastname(self, new):
        self.__lastname = new

    @property
    def age(self):
        return self.__age
    
    @age.setter
    def age(self, new):
        self.__age = new

    @property
    def blood_group(self):
        return self.__blood_group
    
    @blood_group.setter
    def blood_group(self, new):
        self.__blood_group = new

    @property
    def height(self):
        return self.__height
    
    @height.setter
    def height(self, new):
        self.__height = new

    @property
    def weight(self):
        return self.__weight
    
    @weight.setter
    def weight(self, new):
        self.__weight = new

    @property
    def is_alive(self):
        return self.__is_alive
    
    @is_alive.setter
    def is_alive(self, new):
        self.__is_alive = new

    @abstractmethod
    def report_status(self):
        pass

    @abstractmethod
    def get_role_description(self):
        pass

    @classmethod
    def get_population_count(cls):
        return f"Toplam İnsan Sayısı: {cls.total_population}"

    @staticmethod
    def calculate_bmi(weight, height):
        if height > 0:
            height_m = height / 100
            return weight / (height_m ** 2)
        return 0
    
class Structure(ABC):
    total_structures = 0

    def __init__(self, structure_id, name, address, capacity, current_occupancy, location):
        self.__structure_id = structure_id
        self.__name = name
        self.__address = address
        self.__capacity = capacity
        self.__current_occupancy = current_occupancy
        self.__location = location
        Structure.total_structures += 1

    @property
    def structure_id(self):
        return self.__structure_id

    @structure_id.setter
    def structure_id(self, new_id):
        self.__structure_id = new_id

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @property
    def address(self):
        return self.__address
    
    @address.setter
    def address(self, new_address):
        self.__address = new_address

    @property
    def capacity(self):
        return self.__capacity
    
    @capacity.setter
    def capacity(self, new_capacity):
        self.__capacity = new_capacity

    @property
    def current_occupancy(self):
        return self.__current_occupancy
    
    @current_occupancy.setter
    def current_occupancy(self, new_occupancy):
        self.__current_occupancy = new_occupancy

    @property
    def location(self):
        return self.__location
    
    @location.setter
    def location(self, new_loc):
        self.__location = new_loc

    # Binanın yıllık çalışma maliyetini hesaplar
    @abstractmethod
    def calculate_maintenance_cost(self):
        pass

    # O türdeki toplam bina sayısı verir
    @classmethod
    def get_total_structure_count(cls):
        return f"Toplam Bina Sayısı: {cls.total_structures}"

    # Konumu doğrular
    @staticmethod
    def validate_location(location):
        if 0 <= location <= 100:
            return True
        return False
