# agents/shared/database.py

from datetime import datetime
from typing import Dict, List, Optional

from .models import InsurancePlan, Doctor, Clinic


class ClinicDatabase:
    def __init__(self):
        self.insurance_plans: Dict[int, InsurancePlan] = {}
        self.doctors: Dict[int, Doctor] = {}
        self.clinics: Dict[int, Clinic] = {}
        self.appointments: Dict[int, Dict] = {}

        self._init_data()

    def _init_data(self):
        self.insurance_plans[1] = InsurancePlan(
            id=1,
            name="Unimed",
            coverage_percentage=80.0,
            specialties_covered=["Cardiologia", "Oftalmologia", "Pediatria"],
        )

        self.insurance_plans[2] = InsurancePlan(
            id=2,
            name="Amil",
            coverage_percentage=85.0,
            specialties_covered=["Cardiologia", "Dermatologia", "Oftalmologia"],
        )

        self.clinics[1] = Clinic(
            id=1,
            name="Clínica Cardio Center",
            address="Av. Paulista 1000",
            city="São Paulo",
            phone="(11) 3000-0001",
        )

        self.doctors[1] = Doctor(
            id=1,
            name="Dr. Carlos Santos",
            specialty="Cardiologia",
            crm="12345",
            clinic_id=1,
            consultation_price=350.0,
            available_slots=[
                {"slot_id": 1, "date": "2025-12-27", "time": "14:00", "datetime": "2025-12-27 14:00"},
                {"slot_id": 2, "date": "2025-12-27", "time": "14:30", "datetime": "2025-12-27 14:30"},
            ],
        )

    # ---------------- Queries ----------------

    def get_insurance_plan(self, plan_id: int) -> Optional[InsurancePlan]:
        return self.insurance_plans.get(plan_id)

    def find_doctors_by_specialty(
        self, specialty: str, plan_id: Optional[int] = None
    ) -> List[Dict]:

        results = []

        for doctor in self.doctors.values():
            if doctor.specialty.lower() != specialty.lower():
                continue

            if plan_id:
                plan = self.insurance_plans.get(plan_id)
                if not plan or specialty not in plan.specialties_covered:
                    continue

            clinic = self.clinics.get(doctor.clinic_id)

            results.append(
                {
                    "doctor_id": doctor.id,
                    "doctor_name": doctor.name,
                    "specialty": doctor.specialty,
                    "clinic_id": doctor.clinic_id,
                    "clinic_name": clinic.name if clinic else "N/A",
                    "clinic_address": clinic.address if clinic else "N/A",
                    "clinic_phone": clinic.phone if clinic else "N/A",
                    "consultation_price": doctor.consultation_price,
                    "available_slots": doctor.available_slots,
                }
            )

        return results

    def create_appointment(
        self,
        patient_data: Dict,
        doctor_id: int,
        clinic_id: int,
        slot_id: int,
        appointment_datetime: str,
        insurance_plan_id: Optional[int] = None,
    ) -> Dict:

        appointment_id = len(self.appointments) + 1

        appointment = {
            "id": appointment_id,
            "patient": patient_data,
            "doctor_id": doctor_id,
            "clinic_id": clinic_id,
            "slot_id": slot_id,
            "appointment_datetime": appointment_datetime,
            "insurance_plan_id": insurance_plan_id,
            "status": "confirmed",
            "created_at": datetime.utcnow().isoformat(),
        }

        self.appointments[appointment_id] = appointment
        return appointment


# Instância global (ADK-friendly)
db = ClinicDatabase()
