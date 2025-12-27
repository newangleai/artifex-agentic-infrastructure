"""
Sistema de Agentes Paralelos para Clínica Médica
Utiliza o modelo deepseek-r1:latest para processar múltiplas tarefas simultaneamente
Versão standalone - não depende de clinic_system
"""

from google.adk.agents.llm_agent import Agent
from google.adk.agents.parallel_agent import ParallelAgent
from google.adk.models.lite_llm import LiteLlm
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field

# ==================== MODELOS DE DADOS ====================

class InsuranceType(Enum):
    """Tipos de seguro de saúde"""
    PARTICULAR = "particular"
    HEALTH_PLAN = "plano_saude"

class AppointmentStatus(Enum):
    """Status de agendamento"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"

@dataclass
class InsurancePlan:
    """Plano de saúde"""
    id: int
    name: str
    coverage_percentage: float
    specialties_covered: List[str]

@dataclass
class Doctor:
    """Médico"""
    id: int
    name: str
    specialty: str
    crm: str
    clinic_id: int
    consultation_price: float
    available_slots: List[Dict] = field(default_factory=list)

@dataclass
class Clinic:
    """Clínica"""
    id: int
    name: str
    address: str
    city: str
    phone: str

# ==================== BANCO DE DADOS EM MEMÓRIA ====================

class ClinicDatabase:
    """Banco de dados simplificado em memória"""
    
    def __init__(self):
        self.insurance_plans = {}
        self.doctors = {}
        self.clinics = {}
        self.appointments = {}
        self.patients = {}
        self.slots = {}
        self._init_data()
    
    def _init_data(self):
        """Inicializa dados de exemplo"""
        
        # Planos de saúde
        self.insurance_plans[1] = InsurancePlan(
            id=1,
            name="Unimed",
            coverage_percentage=80.0,
            specialties_covered=["Cardiologia", "Oftalmologia", "Pediatria"]
        )
        
        self.insurance_plans[2] = InsurancePlan(
            id=2,
            name="Amil",
            coverage_percentage=85.0,
            specialties_covered=["Cardiologia", "Dermatologia", "Oftalmologia"]
        )
        
        self.insurance_plans[3] = InsurancePlan(
            id=3,
            name="Bradesco Saúde",
            coverage_percentage=75.0,
            specialties_covered=["Cardiologia", "Pediatria", "Dermatologia"]
        )
        
        # Clínicas
        self.clinics[1] = Clinic(
            id=1,
            name="Clínica Cardio Center",
            address="Av. Paulista 1000",
            city="São Paulo",
            phone="(11) 3000-0001"
        )
        
        self.clinics[2] = Clinic(
            id=2,
            name="Clínica Oftalmológica Vision",
            address="Rua Augusta 500",
            city="São Paulo",
            phone="(11) 3000-0002"
        )
        
        # Médicos e horários
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
                {"slot_id": 3, "date": "2025-12-27", "time": "15:00", "datetime": "2025-12-27 15:00"},
            ]
        )
        
        self.doctors[2] = Doctor(
            id=2,
            name="Dra. Marina Silva",
            specialty="Pediatria",
            crm="12346",
            clinic_id=1,
            consultation_price=250.0,
            available_slots=[
                {"slot_id": 4, "date": "2025-12-28", "time": "10:00", "datetime": "2025-12-28 10:00"},
                {"slot_id": 5, "date": "2025-12-28", "time": "10:30", "datetime": "2025-12-28 10:30"},
            ]
        )
        
        self.doctors[3] = Doctor(
            id=3,
            name="Dr. Roberto Costa",
            specialty="Oftalmologia",
            crm="12347",
            clinic_id=2,
            consultation_price=300.0,
            available_slots=[
                {"slot_id": 6, "date": "2025-12-29", "time": "16:00", "datetime": "2025-12-29 16:00"},
                {"slot_id": 7, "date": "2025-12-29", "time": "16:30", "datetime": "2025-12-29 16:30"},
            ]
        )
    
    def get_insurance_plan(self, plan_id: int) -> Optional[InsurancePlan]:
        """Busca plano de saúde por ID"""
        return self.insurance_plans.get(plan_id)
    
    def find_doctors_by_specialty(self, specialty: str, plan_id: Optional[int] = None) -> List[Dict]:
        """Busca médicos por especialidade e plano"""
        results = []
        
        for doctor in self.doctors.values():
            if doctor.specialty.lower() != specialty.lower():
                continue
            
            # Se tem plano, verifica se o plano cobre a especialidade
            if plan_id:
                plan = self.insurance_plans.get(plan_id)
                if not plan or specialty not in plan.specialties_covered:
                    continue
            
            clinic = self.clinics.get(doctor.clinic_id)
            
            results.append({
                "doctor_id": doctor.id,
                "doctor_name": doctor.name,
                "specialty": doctor.specialty,
                "clinic_id": doctor.clinic_id,
                "clinic_name": clinic.name if clinic else "N/A",
                "clinic_address": clinic.address if clinic else "N/A",
                "clinic_phone": clinic.phone if clinic else "N/A",
                "consultation_price": doctor.consultation_price,
                "available_slots": doctor.available_slots
            })
        
        return results
    
    def create_appointment(self, patient_data: Dict, doctor_id: int, clinic_id: int, 
                          slot_id: int, appointment_datetime: str, 
                          insurance_plan_id: Optional[int] = None) -> Dict:
        """Cria um agendamento"""
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
            "created_at": datetime.now().isoformat()
        }
        
        self.appointments[appointment_id] = appointment
        return appointment

# Instância global do banco de dados
db = ClinicDatabase()

# Modelo DeepSeek R1 via Ollama
deepseek_model = LiteLlm(model="ollama_chat/gpt-oss:latest")

# ==================== TOOLS ====================

def greet_patient(patient_name: Optional[str] = None) -> Dict:
    """
    Cumprimenta o paciente e inicia o atendimento.
    
    Args:
        patient_name: Nome do paciente (opcional)
    
    Returns:
        Mensagem de boas-vindas
    """
    greeting = f"Olá{', ' + patient_name if patient_name else ''}! Bem-vindo(a) à nossa clínica."
    return {
        "status": "success",
        "message": greeting,
        "next_steps": "Como posso ajudá-lo(a) hoje? Você gostaria de marcar uma consulta?"
    }


def understand_appointment_request(
    patient_message: str,
    specialty: Optional[str] = None,
    preferred_date: Optional[str] = None
) -> Dict:
    """
    Interpreta a solicitação do paciente para marcação de consulta.
    
    Args:
        patient_message: Mensagem do paciente descrevendo o que precisa
        specialty: Especialidade médica desejada (se já identificada)
        preferred_date: Data preferencial (se mencionada)
    
    Returns:
        Informações extraídas da solicitação
    """
    try:
        message_lower = patient_message.lower()
        
        # Detecta especialidades comuns
        specialties_map = {
            "coração": "Cardiologia",
            "cardio": "Cardiologia",
            "cardiologia": "Cardiologia",
            "olho": "Oftalmologia",
            "vista": "Oftalmologia",
            "oftalmologia": "Oftalmologia",
            "criança": "Pediatria",
            "pediatra": "Pediatria",
            "pediatria": "Pediatria",
        }
        
        detected_specialty = specialty
        if not detected_specialty:
            for keyword, spec in specialties_map.items():
                if keyword in message_lower:
                    detected_specialty = spec
                    break
        
        return {
            "status": "success",
            "understood": True,
            "specialty": detected_specialty,
            "preferred_date": preferred_date,
            "original_message": patient_message,
            "needs_more_info": not detected_specialty,
            "message": f"Entendi que você precisa de {'uma consulta' if detected_specialty else 'atendimento'}. "
                      f"{'Especialidade: ' + detected_specialty if detected_specialty else 'Qual especialidade você procura?'}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Erro ao processar solicitação: {str(e)}"
        }


def check_patient_insurance(
    patient_name: str,
    patient_email: Optional[str] = None,
    insurance_plan_name: Optional[str] = None,
    insurance_plan_id: Optional[int] = None
) -> Dict:
    """
    Verifica o plano de saúde do paciente.
    
    Args:
        patient_name: Nome do paciente
        patient_email: Email do paciente
        insurance_plan_name: Nome do plano de saúde
        insurance_plan_id: ID do plano de saúde
    
    Returns:
        Informações do plano de saúde do paciente
    """
    try:
        # Se o ID do plano foi fornecido, busca diretamente
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
                    "message": f"Plano {plan.name} identificado com {plan.coverage_percentage}% de cobertura."
                }
        
        # Se o nome do plano foi fornecido, tenta encontrar
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
                        "message": f"Plano {plan.name} identificado com {plan.coverage_percentage}% de cobertura."
                    }
        
        # Lista todos os planos disponíveis
        available_plans = [
            {"id": p.id, "name": p.name, "coverage": p.coverage_percentage}
            for p in db.insurance_plans.values()
        ]
        
        return {
            "status": "success",
            "has_insurance": False,
            "message": "Não identificamos seu plano. Por favor, informe qual plano você possui.",
            "available_plans": available_plans
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Erro ao verificar plano de saúde: {str(e)}"
        }


def search_available_doctors(
    specialty: str,
    insurance_plan_id: Optional[int] = None,
    city: str = "São Paulo",
    preferred_date: Optional[str] = None
) -> Dict:
    """
    Busca médicos disponíveis para a especialidade e plano especificados.
    
    Args:
        specialty: Especialidade médica
        insurance_plan_id: ID do plano de saúde (opcional)
        city: Cidade para busca
        preferred_date: Data preferencial (opcional)
    
    Returns:
        Lista de médicos disponíveis com horários
    """
    try:
        doctors = db.find_doctors_by_specialty(specialty, insurance_plan_id)
        
        if not doctors:
            return {
                "status": "error",
                "message": f"Nenhum médico de {specialty} encontrado para seu plano em {city}.",
                "doctors_found": 0
            }
        
        return {
            "status": "success",
            "message": f"Encontramos {len(doctors)} médico(s) disponível(is).",
            "doctors_found": len(doctors),
            "doctors": doctors,
            "specialty": specialty,
            "city": city
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Erro ao buscar médicos: {str(e)}"
        }


def show_doctors_and_schedules(doctors_data: List[Dict]) -> Dict:
    """
    Formata e apresenta os médicos e horários disponíveis para o paciente.
    
    Args:
        doctors_data: Lista de médicos com horários disponíveis
    
    Returns:
        Apresentação formatada dos médicos e horários
    """
    try:
        if not doctors_data:
            return {
                "status": "error",
                "message": "Nenhum médico disponível para mostrar."
            }
        
        presentation = []
        for idx, doctor in enumerate(doctors_data, 1):
            doctor_info = f"\n{idx}. Dr(a). {doctor['doctor_name']}"
            doctor_info += f"\n   Clínica: {doctor['clinic_name']}"
            doctor_info += f"\n   Endereço: {doctor.get('clinic_address', 'N/A')}"
            doctor_info += f"\n   Telefone: {doctor.get('clinic_phone', 'N/A')}"
            doctor_info += f"\n   Valor da consulta: R$ {doctor['consultation_price']:.2f}"
            doctor_info += f"\n   Horários disponíveis:"
            
            for slot in doctor.get('available_slots', [])[:3]:
                doctor_info += f"\n      - {slot['date']} às {slot['time']} (ID: {slot['slot_id']})"
            
            presentation.append(doctor_info)
        
        formatted_message = "".join(presentation)
        
        return {
            "status": "success",
            "message": f"Médicos disponíveis:{formatted_message}\n\nPor favor, escolha o médico e horário desejado.",
            "total_doctors": len(doctors_data)
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Erro ao formatar apresentação: {str(e)}"
        }


def validate_insurance_coverage(
    insurance_plan_id: int,
    specialty: str,
    consultation_price: float
) -> Dict:
    """
    Valida se o plano de saúde cobre a consulta.
    
    Args:
        insurance_plan_id: ID do plano de saúde
        specialty: Especialidade médica
        consultation_price: Preço da consulta
    
    Returns:
        Resultado da validação de cobertura
    """
    try:
        plan = db.get_insurance_plan(insurance_plan_id)
        
        if not plan:
            return {
                "status": "error",
                "message": "Plano de saúde não encontrado."
            }
        
        is_covered = specialty in plan.specialties_covered
        
        if is_covered:
            copay = consultation_price * (1 - plan.coverage_percentage / 100)
            return {
                "status": "success",
                "is_covered": True,
                "plan_name": plan.name,
                "coverage_percentage": plan.coverage_percentage,
                "copay_amount": copay,
                "message": f"Seu plano {plan.name} cobre esta consulta! "
                          f"Você pagará R$ {copay:.2f} (co-participação de {100 - plan.coverage_percentage}%)."
            }
        else:
            return {
                "status": "warning",
                "is_covered": False,
                "plan_name": plan.name,
                "message": "Seu plano não cobre esta especialidade. "
                          f"Valor integral: R$ {consultation_price:.2f}"
            }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Erro ao validar cobertura: {str(e)}"
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
    specialty: str = ""
) -> Dict:
    """
    Realiza a marcação da consulta.
    
    Args:
        patient_name: Nome do paciente
        patient_email: Email do paciente
        patient_phone: Telefone do paciente
        patient_cpf: CPF do paciente
        doctor_id: ID do médico
        clinic_id: ID da clínica
        slot_id: ID do horário
        appointment_datetime: Data e hora da consulta
        insurance_plan_id: ID do plano de saúde (opcional)
        specialty: Especialidade
    
    Returns:
        Confirmação da marcação
    """
    try:
        patient_data = {
            "name": patient_name,
            "email": patient_email,
            "phone": patient_phone,
            "cpf": patient_cpf
        }
        
        appointment = db.create_appointment(
            patient_data=patient_data,
            doctor_id=doctor_id,
            clinic_id=clinic_id,
            slot_id=slot_id,
            appointment_datetime=appointment_datetime,
            insurance_plan_id=insurance_plan_id
        )
        
        doctor = db.doctors.get(doctor_id)
        clinic = db.clinics.get(clinic_id)
        
        return {
            "status": "success",
            "message": "✅ Consulta marcada com sucesso!",
            "appointment_id": appointment["id"],
            "details": {
                "patient": patient_name,
                "doctor": doctor.name if doctor else "N/A",
                "specialty": specialty,
                "clinic": clinic.name if clinic else "N/A",
                "clinic_address": clinic.address if clinic else "N/A",
                "clinic_phone": clinic.phone if clinic else "N/A",
                "date_time": appointment_datetime,
                "status": "Confirmada"
            }
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Erro ao marcar consulta: {str(e)}"
        }


# ==================== AGENTS ====================

# Agente de Atendimento ao Paciente
patient_service_agent = Agent(
    model=deepseek_model,
    name="patient_service_agent",
    description="Agente responsável por atender o paciente, cumprimentar e entender suas necessidades",
    instruction="""
    Você é um atendente virtual de uma clínica médica. Seja cordial, profissional e empático.
    Sua função é:
    1. Cumprimentar o paciente
    2. Entender o que ele precisa (marcação de consulta, informações, etc.)
    3. Identificar a especialidade médica desejada
    4. Coletar informações básicas do paciente
    
    Use as ferramentas disponíveis para processar as solicitações.
    Sempre seja claro e objetivo nas respostas.
    """,
    tools=[greet_patient, understand_appointment_request]
)

# Agente de Verificação de Plano de Saúde
insurance_agent = Agent(
    model=deepseek_model,
    name="insurance_verification_agent",
    description="Agente responsável por verificar e validar planos de saúde",
    instruction="""
    Você é especialista em planos de saúde. Sua função é:
    1. Identificar qual plano de saúde o paciente possui
    2. Verificar a cobertura do plano para a especialidade solicitada
    3. Informar ao paciente sobre valores de co-participação
    4. Orientar sobre planos aceitos pela clínica
    
    Seja claro sobre coberturas e valores.
    """,
    tools=[check_patient_insurance, validate_insurance_coverage]
)

# Agente de Busca de Médicos
doctor_search_agent = Agent(
    model=deepseek_model,
    name="doctor_search_agent",
    description="Agente responsável por buscar médicos disponíveis",
    instruction="""
    Você é responsável por encontrar médicos disponíveis. Sua função é:
    1. Buscar médicos pela especialidade solicitada
    2. Filtrar por plano de saúde do paciente
    3. Verificar disponibilidade de horários
    4. Apresentar opções ao paciente de forma clara
    
    Mostre sempre as melhores opções disponíveis.
    """,
    tools=[search_available_doctors, show_doctors_and_schedules]
)

# Agente de Marcação de Consultas
booking_agent = Agent(
    model=deepseek_model,
    name="booking_agent",
    description="Agente responsável por realizar a marcação de consultas",
    instruction="""
    Você é responsável por finalizar a marcação de consultas. Sua função é:
    1. Confirmar todos os dados do paciente
    2. Confirmar médico, horário e clínica escolhidos
    3. Realizar a marcação no sistema
    4. Fornecer confirmação detalhada ao paciente
    
    Seja meticuloso e confirme todos os detalhes antes de marcar.
    """,
    tools=[book_appointment]
)

# ==================== PARALLEL AGENT ====================

# Agente Paralelo para Busca e Validação Simultâneas
parallel_search_agent = ParallelAgent(
    name="parallel_search_and_validation",
    description="Executa busca de médicos e validação de plano simultaneamente",
    sub_agents=[
        doctor_search_agent,
        insurance_agent
    ]
)

# ==================== ROOT AGENT ====================

# Agente Principal que coordena todo o fluxo
clinic_root_agent = Agent(
    model=deepseek_model,
    name="clinic_appointment_system",
    description="Sistema completo de agendamento de consultas médicas com processamento paralelo",
    instruction="""
    Você é o coordenador principal do sistema de agendamento de consultas.
    
    Fluxo de atendimento:
    1. Use o patient_service_agent para atender e entender a solicitação do paciente
    2. Use o parallel_search_and_validation para buscar médicos E validar plano simultaneamente
    3. Apresente as opções ao paciente
    4. Use o booking_agent para finalizar a marcação
    
    Coordene os agentes de forma eficiente e mantenha o paciente informado em cada etapa.
    Seja profissional, claro e eficiente.
    """,
    sub_agents=[
        patient_service_agent,
        parallel_search_agent,
        booking_agent
    ],
    tools=[
        greet_patient,
        understand_appointment_request,
        check_patient_insurance,
        search_available_doctors,
        show_doctors_and_schedules,
        validate_insurance_coverage,
        book_appointment
    ]
)

# Alias para compatibilidade com ADK Web
root_agent = clinic_root_agent

# ==================== EXPORTS ====================

__all__ = [
    'root_agent',
    'clinic_root_agent',
    'patient_service_agent',
    'insurance_agent',
    'doctor_search_agent',
    'booking_agent',
    'parallel_search_agent',
    'greet_patient',
    'understand_appointment_request',
    'check_patient_insurance',
    'search_available_doctors',
    'show_doctors_and_schedules',
    'validate_insurance_coverage',
    'book_appointment'
]
