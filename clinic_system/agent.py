from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from typing import Dict, List
from clinic_system.database_models import get_db, InsuranceType
import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

model = LiteLlm(
    model="ollama_chat/mistral-small3.1"
)
db = get_db()

def clinic_search(specialty: str = "", location: str = "São Paulo") -> Dict:
    
    try:
        clinics = db.search_clinics(specialty=specialty or None, city=location)
        return {
            "status": "success",
            "clinics_found": len(clinics),
            "clinics": [
                {"id": c.id, "name": c.name, "address": c.address, "phone": c.phone, "doctors": len(c.doctors)}
                for c in clinics
            ]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_available_doctors(specialty: str, insurance_plan_id: int = None, city: str = "São Paulo") -> Dict:
    
    try:
        doctors = db.get_doctors_by_specialty_and_plan(specialty=specialty, plan_id=insurance_plan_id, city=city)
        return {"status": "success", "doctors_found": len(doctors), "doctors": doctors}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def list_slots(doctor_id: int) -> List:
    
    try:
        slots = db.get_available_slots(doctor_id)
        return slots
    except Exception as e:
        return []

def validate_insurance_plan(plan_id: int, specialty: str, consultation_price: float) -> Dict:
    
    try:
        covered = db.validate_insurance_coverage(plan_id, specialty, consultation_price)
        return {"status": "success", "covered": covered}
    except Exception as e:
        return {"status": "error", "covered": False}

def book_appointment(patient_name: str, patient_email: str, patient_phone: str, cpf: str,
                     doctor_id: int, clinic_id: int, slot_id: int, appointment_datetime: str,
                     insurance_type: str = "particular", insurance_plan_id: int = None) -> Dict:
    
    try:
        patient = db.create_or_get_patient(
            name=patient_name, email=patient_email, phone=patient_phone, cpf=cpf,
            insurance_type=InsuranceType.HEALTH_PLAN if insurance_type == "plano" else InsuranceType.PARTICULAR,
            insurance_plan_id=insurance_plan_id
        )
        
        appointment = db.create_appointment(
            patient_id=patient.id, doctor_id=doctor_id, clinic_id=clinic_id, slot_id=slot_id,
            appointment_datetime=appointment_datetime,
            insurance_type=InsuranceType.HEALTH_PLAN if insurance_type == "plano" else InsuranceType.PARTICULAR,
            insurance_plan_id=insurance_plan_id
        )
        
        db.book_slot(slot_id, appointment.id)
        db.confirm_appointment(appointment.id)
        
        return {"status": "success", "appointment_id": appointment.id, "message": "Agendado com sucesso"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


root_agent = Agent(
    model=model,
    name='clinic_system',
    description="Sistema de agendamento de consultas",
    instruction="Use as funções para buscar clínicas, médicos e agendar consultas com dados reais.",
    tools=[clinic_search, get_available_doctors, list_slots, validate_insurance_plan, book_appointment],
)

__all__ = ['root_agent', 'clinic_search', 'get_available_doctors', 'list_slots', 'validate_insurance_plan', 'book_appointment']
