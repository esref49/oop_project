from app.modules.module_3.implementations import AmbulanceUnit, PoliceUnit, FireFightingUnit


ambulance = AmbulanceUnit(unit_id=1, fuel_level=30, is_enough_staff=True, medical_supply_level=70, is_sterilized=True)
print("-"*30)
ambulance.report_status()
print("-"*30)
ambulance.report_fault(faulty_part="Motor",faulty_level=2)
print("-"*30)


police = PoliceUnit(1, 30, True, [10,20], 1, unit_specialty="Trafik")
print("-"*30)
police.perform_gbt_control()
police.perform_gbt_control()
police.report_status()