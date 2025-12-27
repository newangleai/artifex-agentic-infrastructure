"""
Exemplo de uso do sistema de agentes paralelos
Este arquivo demonstra como usar os agentes sem executar (para documentação)
"""

# ==================== EXEMPLO 1: Fluxo Completo de Agendamento ====================

"""
Cenário: Paciente João precisa marcar consulta de cardiologia

Passo 1: Atendimento Inicial
------------------------------
from clinic_agent.agent import greet_patient

result = greet_patient(patient_name="João Silva")
# Output:
# {
#     "status": "success",
#     "message": "Olá, João Silva! Bem-vindo(a) à nossa clínica.",
#     "next_steps": "Como posso ajudá-lo(a) hoje? Você gostaria de marcar uma consulta?"
# }


Passo 2: Entender Solicitação
------------------------------
from clinic_agent.agent import understand_appointment_request

result = understand_appointment_request(
    patient_message="Estou com dores no peito e preciso de um cardiologista urgente"
)
# Output:
# {
#     "status": "success",
#     "understood": True,
#     "specialty": "Cardiologia",  # Detectado automaticamente!
#     "preferred_date": None,
#     "original_message": "Estou com dores no peito...",
#     "needs_more_info": False,
#     "message": "Entendi que você precisa de uma consulta. Especialidade: Cardiologia"
# }


Passo 3: PROCESSAMENTO PARALELO (Plano + Médicos)
--------------------------------------------------
# Estes dois processos rodam SIMULTANEAMENTE usando ParallelAgent!

# 3a. Verificar Plano de Saúde
from clinic_agent.agent import check_patient_insurance

insurance_result = check_patient_insurance(
    patient_name="João Silva",
    patient_email="joao@email.com",
    insurance_plan_id=1  # Unimed
)
# Output:
# {
#     "status": "success",
#     "has_insurance": True,
#     "plan_id": 1,
#     "plan_name": "Unimed",
#     "coverage_percentage": 80,
#     "specialties_covered": ["Cardiologia", "Oftalmologia", "Pediatria"],
#     "message": "Plano Unimed identificado com 80% de cobertura."
# }

# 3b. Buscar Médicos Disponíveis (executa em paralelo com 3a)
from clinic_agent.agent import search_available_doctors

doctors_result = search_available_doctors(
    specialty="Cardiologia",
    insurance_plan_id=1,
    city="São Paulo"
)
# Output:
# {
#     "status": "success",
#     "message": "Encontramos 1 médico(s) disponível(is).",
#     "doctors_found": 1,
#     "doctors": [
#         {
#             "doctor_id": 1,
#             "doctor_name": "Dr. Carlos Santos",
#             "specialty": "Cardiologia",
#             "clinic_id": 1,
#             "clinic_name": "Clínica Cardio Center",
#             "consultation_price": 350.0,
#             "available_slots": [
#                 {
#                     "slot_id": 1,
#                     "doctor_id": 1,
#                     "date": "2025-12-15",
#                     "time": "14:00",
#                     "datetime": "2025-12-15 14:00"
#                 },
#                 {
#                     "slot_id": 2,
#                     "doctor_id": 1,
#                     "date": "2025-12-15",
#                     "time": "14:30",
#                     "datetime": "2025-12-15 14:30"
#                 }
#             ]
#         }
#     ],
#     "specialty": "Cardiologia",
#     "city": "São Paulo"
# }


Passo 4: Apresentar Opções ao Paciente
---------------------------------------
from clinic_agent.agent import show_doctors_and_schedules

presentation = show_doctors_and_schedules(doctors_result['doctors'])
# Output:
# {
#     "status": "success",
#     "message": '''
#         Médicos disponíveis:
#         
#         1. Dr(a). Dr. Carlos Santos
#            Clínica: Clínica Cardio Center
#            Valor da consulta: R$ 350.00
#            Horários disponíveis:
#               - 2025-12-15 às 14:00 (ID: 1)
#               - 2025-12-15 às 14:30 (ID: 2)
#               - 2025-12-15 às 15:00 (ID: 3)
#         
#         Por favor, escolha o médico e horário desejado.
#     ''',
#     "total_doctors": 1
# }


Passo 5: Validar Cobertura do Plano
------------------------------------
from clinic_agent.agent import validate_insurance_coverage

coverage = validate_insurance_coverage(
    insurance_plan_id=1,
    specialty="Cardiologia",
    consultation_price=350.0
)
# Output:
# {
#     "status": "success",
#     "is_covered": True,
#     "plan_name": "Unimed",
#     "coverage_percentage": 80,
#     "copay_amount": 70.0,  # 20% de 350
#     "message": "Seu plano Unimed cobre esta consulta! Você pagará R$ 70.00 (co-participação de 20%)."
# }


Passo 6: Confirmar Agendamento
-------------------------------
from clinic_agent.agent import book_appointment

booking = book_appointment(
    patient_name="João Silva",
    patient_email="joao@email.com",
    patient_phone="(11) 98765-4321",
    patient_cpf="123.456.789-00",
    doctor_id=1,
    clinic_id=1,
    slot_id=1,
    appointment_datetime="2025-12-15 14:00",
    insurance_plan_id=1,
    specialty="Cardiologia"
)
# Output:
# {
#     "status": "success",
#     "message": "✅ Consulta marcada com sucesso!",
#     "appointment_id": 1,
#     "details": {
#         "patient": "João Silva",
#         "doctor": "Dr. Carlos Santos",
#         "specialty": "Cardiologia",
#         "clinic": "Clínica Cardio Center",
#         "clinic_address": "Av. Paulista 1000",
#         "clinic_phone": "(11) 3000-0001",
#         "date_time": "2025-12-15 14:00",
#         "status": "Confirmada"
#     }
# }
"""


# ==================== EXEMPLO 2: Usando os Agentes Diretamente ====================

"""
Uso com Google ADK Agents (quando instalado)

from clinic_agent.agent import (
    clinic_root_agent,
    parallel_search_agent,
    patient_service_agent,
    insurance_agent,
    doctor_search_agent,
    booking_agent
)

# Agente Principal coordena todo o fluxo
# O clinic_root_agent usa os sub-agentes automaticamente

# Exemplo de conversa com o agente principal:
session = clinic_root_agent.create_session()

# Usuário: "Olá, preciso marcar uma consulta"
response = session.send_message("Olá, preciso marcar uma consulta")
# Agente usa patient_service_agent para atender

# Usuário: "Preciso de um cardiologista, tenho Unimed"
response = session.send_message("Preciso de um cardiologista, tenho Unimed")
# Agente usa parallel_search_agent que executa:
#   - doctor_search_agent (busca médicos)
#   - insurance_agent (valida plano)
# SIMULTANEAMENTE!

# Usuário: "Quero o primeiro médico, horário 14:00"
response = session.send_message("Quero o primeiro médico, horário 14:00")
# Agente usa booking_agent para finalizar
"""


# ==================== EXEMPLO 3: Agente Paralelo Customizado ====================

"""
Criando seu próprio agente paralelo

from google.adk.agents.parallel_agent import ParallelAgent
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

model = LiteLlm(model="ollama_chat/deepseek-r1:latest")

# Criar agentes especializados
agent_1 = Agent(
    model=model,
    name="specialist_1",
    description="Faz tarefa A",
    tools=[tool_a]
)

agent_2 = Agent(
    model=model,
    name="specialist_2",
    description="Faz tarefa B",
    tools=[tool_b]
)

# Criar agente paralelo que executa ambos simultaneamente
parallel_agent = ParallelAgent(
    name="parallel_processor",
    description="Executa A e B em paralelo",
    sub_agents=[agent_1, agent_2]
)

# Usar o agente paralelo
result = parallel_agent.run(input_data)
# agent_1 e agent_2 executam ao mesmo tempo!
# Resultado é agregado quando ambos terminam
"""


# ==================== EXEMPLO 4: Múltiplas Especialidades ====================

"""
Buscar médicos em várias especialidades

specialties = ["Cardiologia", "Oftalmologia", "Pediatria"]
results = {}

for specialty in specialties:
    results[specialty] = search_available_doctors(
        specialty=specialty,
        insurance_plan_id=1,
        city="São Paulo"
    )

# Output:
# {
#     "Cardiologia": {
#         "doctors_found": 1,
#         "doctors": [...]
#     },
#     "Oftalmologia": {
#         "doctors_found": 1,
#         "doctors": [...]
#     },
#     "Pediatria": {
#         "doctors_found": 1,
#         "doctors": [...]
#     }
# }
"""


# ==================== VANTAGENS DO PROCESSAMENTO PARALELO ====================

"""
Comparação de Performance:

SEQUENCIAL (tradicional):
1. Verificar plano (2s)
2. Buscar médicos (3s)
3. Validar cobertura (1s)
Total: 6 segundos

PARALELO (com ParallelAgent):
1. Verificar plano (2s) } Executam
2. Buscar médicos (3s)  } simultaneamente
Total: 3 segundos (50% mais rápido!)

O ParallelAgent do ADK gerencia:
- Execução simultânea dos sub-agentes
- Sincronização de resultados
- Estado compartilhado (session.state)
- Tratamento de erros
"""


# ==================== ESTRUTURA DOS AGENTES ====================

"""
Hierarquia de Agentes:

clinic_root_agent (Coordenador Principal)
├── patient_service_agent
│   ├── greet_patient()
│   └── understand_appointment_request()
│
├── parallel_search_agent (EXECUÇÃO PARALELA)
│   ├── doctor_search_agent
│   │   ├── search_available_doctors()
│   │   └── show_doctors_and_schedules()
│   │
│   └── insurance_agent
│       ├── check_patient_insurance()
│       └── validate_insurance_coverage()
│
└── booking_agent
    └── book_appointment()

Fluxo de Dados:
1. Paciente → patient_service_agent → entende necessidade
2. parallel_search_agent → executa busca + validação SIMULTANEAMENTE
3. Resultados agregados → apresentados ao paciente
4. booking_agent → finaliza marcação
"""

print(__doc__)
