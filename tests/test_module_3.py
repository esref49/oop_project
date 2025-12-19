from app.modules.module_3.implementations import AmbulanceUnit, PoliceUnit, FireFightingUnit
from app.modules.module_3.repository import EmergencyRepository
from app.modules.module_3.services import EmergencyService


ambulance1 = AmbulanceUnit(unit_id=1, fuel_level=30, is_enough_staff=True, medical_supply_level=70, is_sterilized=True)
ambulance2 = AmbulanceUnit(unit_id=2, fuel_level=40, is_enough_staff=True, medical_supply_level=50, is_sterilized=True)
ambulance3 = AmbulanceUnit(unit_id=3, fuel_level=60, is_enough_staff=True, medical_supply_level=76, is_sterilized=True)
ambulance4 = AmbulanceUnit(unit_id=4, fuel_level=90, is_enough_staff=True, medical_supply_level=53, is_sterilized=True)
itfaiye1 = FireFightingUnit(unit_id=2,fuel_level=414,is_enough_staff=True, water_level=515, foam_level=451, ladder_length=617)


ambulances = [itfaiye1]

ambulance_service = EmergencyService(repository=EmergencyRepository())
ambulance_service.creating_case("Yangın", 9, ambulances)  # unit_list parametresi eklendi