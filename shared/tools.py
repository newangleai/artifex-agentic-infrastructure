# agents/shared/tools.py

from typing import Dict, List, Optional

from .database import db


def greet_patient(patient_name: Optional[str] = None) -> Dict:
    greeting = f"Olá{', ' + patient_name if patient_name else ''}! Bem-vindo(a) à nossa clínica."
    return {
        "status": "success",
        "message": greeting,
        "next_steps": "Como posso ajudar?",
    }


def understand_appointment_request(
    patient_message: str,
    specialty: Optional[str] = None,
    preferred_date: Optional[str] = None,
) -> Dict:

    message = patient_message.lower()

    specialties_map = {
        "cardio": "Cardiologia",
        "coração": "Cardiologia",
        "olho": "Oftalmologia",
        "vista": "Oftalmologia",
        "criança": "Pediatria",
        "pediatra": "Pediatria",
    }

    detected = specialty
    if not detected:
        for key, value in specialties_map.items():
            if key in message:
                detected = value
                break

    return {
        "status": "success",
        "specialty": detected,
        "preferred_date": preferred_date,
        "needs_more_info": detected is None,
    }


def check_patient_insurance(
    insurance_plan_name: Optional[str] = None,
    insurance_plan_id: Optional[int] = None,
) -> Dict:

    if insurance_plan_id:
        plan = db.get_insurance_plan(insurance_plan_id)
        if plan:
            return {
                "status": "success",
                "has_insurance": True,
                "plan_id": plan.id,
                "plan_name": plan.name,
                "coverage_percentage": plan.coverage_percentage,
                "specialties_covered": plan.specialties_covered,
            }

    if insurance_plan_name:
        for plan in db.insurance_plans.values():
            if plan.name.lower() in insurance_plan_name.lower():
                return {
                    "status": "success",
                    "has_insurance": True,
                    "plan_id": plan.id,
                    "plan_name": plan.name,
                    "coverage_percentage": plan.coverage_percentage,
                    "specialties_covered": plan.specialties_covered,
                }

    return {
        "status": "success",
        "has_insurance": False,
        "available_plans": [
            {"id": p.id, "name": p.name} for p in db.insurance_plans.values()
        ],
    }


def search_available_doctors(
    specialty: str,
    insurance_plan_id: Optional[int] = None,
    city: str = "São Paulo",
) -> Dict:

    doctors = db.find_doctors_by_specialty(specialty, insurance_plan_id)

    if not doctors:
        return {
            "status": "error",
            "message": "Nenhum médico encontrado.",
        }

    return {
        "status": "success",
        "doctors": doctors,
        "total": len(doctors),
    }


def show_doctors_and_schedules(doctors_data: List[Dict]) -> Dict:
    return {
        "status": "success",
        "doctors": doctors_data,
    }


def validate_insurance_coverage(
    insurance_plan_id: int,
    specialty: str,
    consultation_price: float,
) -> Dict:

    plan = db.get_insurance_plan(insurance_plan_id)
    if not plan:
        return {"status": "error", "message": "Plano não encontrado"}

    covered = specialty in plan.specialties_covered
    copay = consultation_price * (1 - plan.coverage_percentage / 100)

    return {
        "status": "success",
        "is_covered": covered,
        "copay": copay if covered else consultation_price,
    }


def book_appointment(
    patient_name: str,
    patient_email: str,
    patient_phone: str,
    patient_cpf: str,
    doctor_id: int,
    clinic_id: int,
    slot_id: int,
    appointment_datetime: str,
    insurance_plan_id: Optional[int] = None,
    specialty: str = "",
) -> Dict:

    patient = {
        "name": patient_name,
        "email": patient_email,
        "phone": patient_phone,
        "cpf": patient_cpf,
    }

    appointment = db.create_appointment(
        patient,
        doctor_id,
        clinic_id,
        slot_id,
        appointment_datetime,
        insurance_plan_id,
    )

    return {
        "status": "success",
        "appointment": appointment,
    }
