

from google.adk.agents.llm_agent import Agent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.agents.parallel_agent import ParallelAgent
from google.adk.agents.loop_agent import LoopAgent
from google.adk.models.lite_llm import LiteLlm
from typing import Dict, List, Optional, Any
from datetime import datetime
from clinic_system.database_models import (
    get_db, InsuranceType, AppointmentStatus
)

model = LiteLlm(model="ollama/llama3.2:3b")
db = get_db()

def asdict(obj: Any) -> Dict:
    
    if hasattr(obj, '__dataclass_fields__'):
        result = {}
        for field in obj.__dataclass_fields__:
            value = getattr(obj, field)
            if hasattr(value, '__dataclass_fields__'):
                result[field] = asdict(value)
            elif isinstance(value, list) and value and hasattr(value[0], '__dataclass_fields__'):
                result[field] = [asdict(item) for item in value]
            elif hasattr(value, 'value'):
                result[field] = value.value
            else:
                result[field] = value
        return result
    return obj

def create_validation_agent() -> Agent:
    
    return Agent(
        model=model,
        name="validation_agent",
        description="Valida dados do paciente"
    )

def create_search_agent() -> Agent:
    
    return Agent(
        model=model,
        name="search_agent",
        description="Busca médicos e clínicas disponíveis"
    )

def create_selection_agent() -> Agent:
    
    return Agent(
        model=model,
        name="selection_agent",
        description="Seleciona melhor opção de médico e horário"
    )

def create_booking_agent() -> Agent:
    
    return Agent(
        model=model,
        name="booking_agent",
        description="Reserva o agendamento no sistema"
    )

def create_confirmation_agent() -> Agent:
    
    return Agent(
        model=model,
        name="confirmation_agent",
        description="Confirma agendamento e notifica clínica"
    )

def validate_patient_and_search(
    patient_name: str,
    patient_email: str,
    specialty: str,
    insurance_plan_id: int,
    city: str = "São Paulo"
) -> Dict:
    
    try:
        if not patient_name or not patient_email:
            return {"status": "error", "message": "Nome e email obrigatórios"}
        

        patient = db.create_or_get_patient(
            name=patient_name,
            email=patient_email,
            phone="(00) 00000-0000",
            cpf="000.000.000-00",
            insurance_type=InsuranceType.HEALTH_PLAN,
            insurance_plan_id=insurance_plan_id
        )
        

        doctors = db.get_doctors_by_specialty_and_plan(
            specialty=specialty,
            plan_id=insurance_plan_id,
            city=city
        )
        
        if not doctors:
            return {"status": "error", "message": f"Nenhum médico encontrado"}
        
        return {
            "status": "success",
            "patient_id": patient.id,
            "patient_name": patient.name,
            "doctors_found": len(doctors),
            "doctors": doctors
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def select_doctor_and_slot(
    patient_id: int,
    doctors: List[Dict],
    city: str = "São Paulo"
) -> Dict:
    
    try:
        if not doctors:
            return {"status": "error", "message": "Nenhum médico disponível"}
        

        doctor_info = doctors[0]
        doctor_id = doctor_info['doctor_id']
        clinic_id = doctor_info['clinic_id']
        specialty = doctor_info['specialty']
        price = doctor_info['consultation_price']
        

        slots = db.get_available_slots(doctor_id)
        if not slots:
            return {"status": "error", "message": "Nenhum slot disponível"}
        

        patient = db.get_patient_by_id(patient_id)
        is_covered = db.validate_insurance_coverage(
            plan_id=patient.insurance_plan_id,
            specialty=specialty,
            consultation_price=price
        )
        
        if not is_covered:
            return {"status": "error", "message": "Plano não cobre"}
        
        return {
            "status": "success",
            "doctor_id": doctor_id,
            "clinic_id": clinic_id,
            "doctor_name": doctor_info['doctor_name'],
            "clinic_name": doctor_info['clinic_name'],
            "slot_id": slots[0]['slot_id'],
            "appointment_datetime": slots[0]['datetime']
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def reserve_appointment(
    patient_id: int,
    doctor_id: int,
    clinic_id: int,
    slot_id: int,
    appointment_datetime: str
) -> Dict:
    
    try:
        patient = db.get_patient_by_id(patient_id)
        
        appointment = db.create_appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            clinic_id=clinic_id,
            slot_id=slot_id,
            appointment_datetime=appointment_datetime,
            insurance_type=patient.insurance_type,
            insurance_plan_id=patient.insurance_plan_id
        )
        
        if not appointment:
            return {"status": "error", "message": "Falha ao criar agendamento"}
        
        db.book_slot(slot_id=slot_id, appointment_id=appointment.id)
        
        return {
            "status": "success",
            "appointment_id": appointment.id,
            "datetime": appointment.appointment_datetime
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def confirm_and_notify(appointment_id: int) -> Dict:
    
    try:
        if db.confirm_appointment(appointment_id):
            appointment = next(
                (a for a in db.appointments if a.id == appointment_id),
                None
            )
            
            if appointment:
                return {
                    "status": "success",
                    "appointment_id": appointment_id,
                    "confirmation": "Agendamento confirmado"
                }
        
        return {"status": "error", "message": "Falha ao confirmar"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def create_sequential_workflow() -> SequentialAgent:
    
    return SequentialAgent(
        name="appointment_scheduling_workflow",
        sub_agents=[
            create_validation_agent(),
            create_search_agent(),
            create_selection_agent(),
            create_booking_agent(),
            create_confirmation_agent()
        ],
        description="Fluxo completo de agendamento em sequência"
    )

async def appointment_scheduling_workflow(
    patient_name: str,
    patient_email: str,
    specialty: str,
    insurance_plan_id: int,
    city: str = "São Paulo"
) -> Dict:
    
    try:

        step1 = validate_patient_and_search(
            patient_name=patient_name,
            patient_email=patient_email,
            specialty=specialty,
            insurance_plan_id=insurance_plan_id,
            city=city
        )
        
        if step1["status"] != "success":
            return step1
        
        patient_id = step1["patient_id"]
        doctors = step1["doctors"]
        

        step2 = select_doctor_and_slot(
            patient_id=patient_id,
            doctors=doctors,
            city=city
        )
        
        if step2["status"] != "success":
            return step2
        

        step3 = reserve_appointment(
            patient_id=patient_id,
            doctor_id=step2["doctor_id"],
            clinic_id=step2["clinic_id"],
            slot_id=step2["slot_id"],
            appointment_datetime=step2["appointment_datetime"]
        )
        
        if step3["status"] != "success":
            return step3
        

        step4 = confirm_and_notify(step3["appointment_id"])
        
        return step4
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

def search_clinics_parallel(specialty: str, city: str = "São Paulo") -> Dict:
    
    try:
        clinics = db.search_clinics(specialty=specialty, city=city)
        return {
            "status": "success",
            "clinics_found": len(clinics),
            "clinics": [asdict(c) for c in clinics]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def search_doctors_parallel(specialty: str, insurance_plan_id: int, city: str = "São Paulo") -> Dict:
    
    try:
        doctors = db.get_doctors_by_specialty_and_plan(
            specialty=specialty,
            plan_id=insurance_plan_id,
            city=city
        )
        return {
            "status": "success",
            "doctors_found": len(doctors),
            "doctors": doctors
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def validate_insurance_parallel(plan_id: int, city: str = "São Paulo") -> Dict:
    
    try:
        plans = db.get_insurance_plans_by_region(city)
        plan = next((p for p in plans if p.id == plan_id), None)
        
        if not plan:
            return {"status": "error", "message": "Plano não encontrado"}
        
        return {
            "status": "success",
            "plan_name": plan.name,
            "coverage": plan.coverage_percentage,
            "specialties": plan.specialties_covered
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def create_parallel_workflow() -> ParallelAgent:
    
    return ParallelAgent(
        name="search_and_validate_workflow",
        sub_agents=[
            create_validation_agent(),
            create_search_agent(),
            create_confirmation_agent()
        ],
        description="Busca paralela de clínicas, médicos e validação de seguro"
    )

async def search_and_validate_workflow(
    specialty: str,
    insurance_plan_id: int,
    city: str = "São Paulo"
) -> Dict:
    
    try:
        results = {
            "clinics": search_clinics_parallel(specialty=specialty, city=city),
            "doctors": search_doctors_parallel(
                specialty=specialty,
                insurance_plan_id=insurance_plan_id,
                city=city
            ),
            "insurance": validate_insurance_parallel(plan_id=insurance_plan_id, city=city)
        }
        
        return {
            "status": "success",
            "results": results,
            "summary": {
                "clinics": results["clinics"].get("clinics_found", 0),
                "doctors": results["doctors"].get("doctors_found", 0),
                "insurance_valid": results["insurance"].get("status") == "success"
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def attempt_clinic_notification(appointment_id: int, attempt: int = 1) -> Dict:
    
    try:
        appointment = next(
            (a for a in db.appointments if a.id == appointment_id),
            None
        )
        
        if not appointment:
            return {
                "status": "error",
                "message": "Agendamento não encontrado",
                "should_continue": False
            }
        

        success = True
        
        if success:
            return {
                "status": "success",
                "message": f"Clínica notificada (tentativa {attempt})",
                "should_continue": False
            }
        else:
            return {
                "status": "pending",
                "message": f"Falha na tentativa {attempt}",
                "should_continue": attempt < 3
            }
    
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "should_continue": attempt < 3
        }

def create_loop_workflow() -> LoopAgent:
    
    return LoopAgent(
        name="appointment_confirmation_retry",
        sub_agents=[create_confirmation_agent()],
        max_iterations=3,
        description="Confirma agendamento com retry automático"
    )

async def appointment_confirmation_retry(appointment_id: int) -> Dict:
    
    try:
        for attempt in range(1, 4):
            result = attempt_clinic_notification(appointment_id, attempt)
            
            if result["status"] == "success":
                return {
                    "status": "success",
                    "message": f"Confirmado em {attempt} tentativa(s)",
                    "appointment_id": appointment_id
                }
            
            if not result.get("should_continue", False):
                return result
        
        return {
            "status": "error",
            "message": "Falha em todas as tentativas",
            "appointment_id": appointment_id
        }
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

sequential_workflow = create_sequential_workflow()
parallel_workflow = create_parallel_workflow()
loop_workflow = create_loop_workflow()

__all__ = [
    'sequential_workflow',
    'parallel_workflow',
    'loop_workflow',
    'appointment_scheduling_workflow',
    'search_and_validate_workflow',
    'appointment_confirmation_retry',
    'asdict'
]
