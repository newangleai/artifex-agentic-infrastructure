from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from typing import Dict, List, Optional
from clinic_system.database_models import get_db, AppointmentStatus
from google.adk.models.google_llm import Gemini

from dotenv import load_dotenv
load_dotenv()


model = Gemini(
    model="gemini-2.5-flash"
)

db = get_db()

def register_appointment(
    patient_name: str,
    patient_email: str,
    patient_phone: str,
    cpf: str,
    appointment_time: str,
    doctor_id: int,
    specialty: str,
    clinic_id: int,
    insurance_type: str,
    insurance_plan: Optional[str] = None,''
    slot_id: Optional[int] = None,
    notes: Optional[str] = None
) -> Dict:
    
    try:

        patient_data = {
            'name': patient_name,
            'email': patient_email,
            'phone': patient_phone,
            'cpf': cpf,
            'insurance_type': insurance_type,
            'insurance_plan_id': None
        }
        
        patient = db.create_or_get_patient(**patient_data)
        

        appointment = db.create_appointment(
            patient_id=patient.id,
            doctor_id=doctor_id,
            clinic_id=clinic_id,
            slot_id=slot_id,
            appointment_datetime=appointment_time,
            insurance_type=insurance_type,
            insurance_plan_id=None,
            notes=notes
        )
        
        if not appointment:
            return {
                "status": "error",
                "message": "Falha ao registrar agendamento"
            }
        

        db.confirm_appointment(appointment.id)
        

        doctor = db.get_doctor_by_id(doctor_id)
        clinic = db.get_clinic_by_id(clinic_id)
        
        return {
            "status": "success",
            "message": f"Consulta registrada com sucesso! ID: {appointment.id}",
            "appointment_id": appointment.id,
            "appointment_details": {
                "patient": patient.name,
                "patient_email": patient.email,
                "patient_phone": patient.phone,
                "doctor": doctor.name if doctor else "N/A",
                "specialty": specialty,
                "clinic": clinic.name if clinic else "N/A",
                "appointment_datetime": appointment.appointment_datetime,
                "insurance_type": insurance_type,
                "insurance_plan": insurance_plan,
                "status": appointment.status.value
            }
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Erro ao registrar: {str(e)}"
        }

def list_appointments(filter_by: Optional[str] = None, filter_value: Optional[str] = None) -> List[Dict]:
    
    try:
        if filter_by == "patient_id":
            appointments = db.get_appointments_by_patient(int(filter_value))
        elif filter_by == "clinic_id":
            appointments = db.get_appointments_by_clinic(int(filter_value))
        else:
            appointments = list(db.appointments.values())
        
        return [
            {
                "id": a.id,
                "patient_id": a.patient_id,
                "doctor_id": a.doctor_id,
                "clinic_id": a.clinic_id,
                "appointment_datetime": a.appointment_datetime,
                "status": a.status.value,
                "insurance_type": a.insurance_type.value,
                "created_at": a.created_at
            }
            for a in appointments
        ]
    except Exception as e:
        return [{"error": str(e)}]

def get_appointment_details(appointment_id: int) -> Dict:
    
    try:
        appointment = db.get_appointment_by_id(appointment_id)
        
        if not appointment:
            return {
                "status": "error",
                "message": f"Agendamento {appointment_id} não encontrado"
            }
        

        patient = db.get_patient_by_id(appointment.patient_id)
        doctor = db.get_doctor_by_id(appointment.doctor_id)
        clinic = db.get_clinic_by_id(appointment.clinic_id)
        
        return {
            "status": "success",
            "appointment": {
                "id": appointment.id,
                "patient": {
                    "name": patient.name,
                    "email": patient.email,
                    "phone": patient.phone,
                    "cpf": patient.cpf
                },
                "doctor": {
                    "name": doctor.name,
                    "specialty": doctor.specialty,
                    "crm": doctor.crm
                },
                "clinic": {
                    "name": clinic.name,
                    "address": clinic.address,
                    "phone": clinic.phone,
                    "email": clinic.email
                },
                "appointment_datetime": appointment.appointment_datetime,
                "insurance_type": appointment.insurance_type.value,
                "status": appointment.status.value,
                "created_at": appointment.created_at
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

def cancel_appointment(appointment_id: int, reason: Optional[str] = None) -> Dict:
    
    try:
        if not db.cancel_appointment(appointment_id, reason or ""):
            return {
                "status": "error",
                "message": f"Agendamento {appointment_id} não encontrado"
            }
        
        return {
            "status": "success",
            "message": f"Agendamento {appointment_id} cancelado com sucesso",
            "reason": reason or "Não especificado"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

def process_scheduling_request(clinic_id: int, doctor_id: int, slot_id: int, 
                               patient_name: str, patient_email: str, 
                               patient_phone: str, cpf: str) -> Dict:
    
    try:

        if not all([patient_name, patient_email, patient_phone, cpf]):
            return {
                "status": "error",
                "message": "Dados do paciente incompletos"
            }
        

        doctor = db.get_doctor_by_id(doctor_id)
        clinic = db.get_clinic_by_id(clinic_id)
        
        if not doctor or not clinic:
            return {
                "status": "error",
                "message": "Médico ou clínica não encontrados"
            }
        
        return {
            "status": "pending",
            "message": f"Requisição de agendamento recebida pela clínica {clinic.name}. Aguardando confirmação final.",
            "clinic_id": clinic_id,
            "clinic_name": clinic.name,
            "doctor_id": doctor_id,
            "doctor_name": doctor.name,
            "doctor_specialty": doctor.specialty,
            "slot_id": slot_id,
            "patient_name": patient_name,
            "patient_email": patient_email,
            "patient_phone": patient_phone,
            "cpf": cpf
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

clinic_registration_agent = Agent(
    model=model,
    name='clinic_registration_agent',
    description="Agente para registrar consultas com dados reais",
    instruction="Você registra novas consultas no sistema da clínica com todas as informações necessárias.",
    tools=[process_scheduling_request, register_appointment]
)

appointment_manager_agent = Agent(
    model=model,
    name='appointment_manager_agent',
    description="Agente para gerenciar agendamentos com dados reais",
    instruction="Você gerencia agendamentos no sistema da clínica, permitindo listar, consultar e cancelar consultas.",
    tools=[list_appointments, get_appointment_details, cancel_appointment]
)

clinic_root_agent = Agent(
    model=model,
    name='clinic_registration_system',
    description="Sistema completo de registro e gerenciamento com dados reais",
    instruction="Você é o agente principal que coordena registro e gerenciamento de agendamentos na clínica.",
    sub_agents=[clinic_registration_agent, appointment_manager_agent],
)

__all__ = [
    'clinic_root_agent',
    'clinic_registration_agent',
    'appointment_manager_agent',
    'register_appointment',
    'list_appointments',
    'get_appointment_details',
    'cancel_appointment',
    'process_scheduling_request'
]