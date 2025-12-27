# Sistema de Agentes Paralelos para Clínica Médica

Sistema completo de agendamento de consultas médicas utilizando **Google ADK** (Agent Development Kit) com **DeepSeek R1** como modelo de linguagem.

## 🎯 Funcionalidades

O sistema utiliza **agentes paralelos** para processar múltiplas tarefas simultaneamente, proporcionando um atendimento rápido e eficiente:

### Agentes Especializados

1. **Patient Service Agent** (`patient_service_agent`)
   - Atende e cumprimenta o paciente
   - Entende a solicitação de marcação de consulta
   - Identifica a especialidade médica desejada
   - Coleta informações básicas do paciente

2. **Insurance Verification Agent** (`insurance_agent`)
   - Verifica o plano de saúde do paciente
   - Valida cobertura para especialidades
   - Calcula valores de co-participação
   - Informa sobre planos aceitos

3. **Doctor Search Agent** (`doctor_search_agent`)
   - Busca médicos disponíveis por especialidade
   - Filtra por plano de saúde
   - Verifica disponibilidade de horários
   - Apresenta opções ao paciente

4. **Booking Agent** (`booking_agent`)
   - Confirma dados do paciente
   - Realiza a marcação da consulta
   - Fornece confirmação detalhada

5. **Parallel Search Agent** (`parallel_search_agent`)
   - **Executa busca de médicos e validação de plano SIMULTANEAMENTE**
   - Reduz tempo de resposta significativamente

6. **Clinic Root Agent** (`clinic_root_agent`)
   - Agente principal que coordena todo o fluxo
   - Gerencia a comunicação entre agentes
   - Mantém o paciente informado em cada etapa

## 🛠️ Ferramentas (Tools)

### Atendimento
- `greet_patient()` - Cumprimenta o paciente
- `understand_appointment_request()` - Interpreta a solicitação

### Plano de Saúde
- `check_patient_insurance()` - Verifica plano do paciente
- `validate_insurance_coverage()` - Valida cobertura

### Busca e Agendamento
- `search_available_doctors()` - Busca médicos disponíveis
- `show_doctors_and_schedules()` - Apresenta opções formatadas
- `book_appointment()` - Realiza a marcação

## 🚀 Como Usar

### Pré-requisitos

1. **Ollama** instalado com o modelo DeepSeek R1:
```bash
ollama pull deepseek-r1:latest
```

2. **Google ADK** instalado:
```bash
pip install google-adk
```

3. **Dependências do projeto**:
```bash
pip install -r requirements.txt
```

### Executando os Testes

```bash
cd clinic_agent
python test_parallel_agents.py
```

### Usando os Agentes

```python
from clinic_agent.agent import (
    clinic_root_agent,
    parallel_search_agent,
    # ... outros agentes
)

# Exemplo: Busca paralela de médicos e validação de plano
# O parallel_search_agent executa ambas as tarefas simultaneamente
```

## 📊 Fluxo de Atendimento

```
1. Paciente solicita consulta
   ↓
2. Patient Service Agent atende e entende a necessidade
   ↓
3. Parallel Search Agent executa SIMULTANEAMENTE:
   - Busca médicos disponíveis (Doctor Search Agent)
   - Verifica plano de saúde (Insurance Agent)
   ↓
4. Sistema apresenta opções ao paciente
   ↓
5. Booking Agent finaliza a marcação
   ↓
6. Confirmação enviada ao paciente
```

## 🎨 Exemplo de Uso Completo

```python
# 1. Atender paciente
greeting = greet_patient(patient_name="João Silva")

# 2. Entender solicitação
request = understand_appointment_request(
    patient_message="Preciso de um cardiologista",
    specialty=None  # Detecta automaticamente
)

# 3. Verificar plano (executa em paralelo com busca)
insurance = check_patient_insurance(
    patient_name="João Silva",
    insurance_plan_id=1  # Unimed
)

# 4. Buscar médicos (executa em paralelo com verificação)
doctors = search_available_doctors(
    specialty="Cardiologia",
    insurance_plan_id=1,
    city="São Paulo"
)

# 5. Validar cobertura
coverage = validate_insurance_coverage(
    insurance_plan_id=1,
    specialty="Cardiologia",
    consultation_price=350.00
)

# 6. Marcar consulta
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
```

## 🏥 Dados de Exemplo

### Planos de Saúde Disponíveis
- **Unimed** (ID: 1) - 80% cobertura
  - Especialidades: Cardiologia, Oftalmologia, Pediatria
- **Amil** (ID: 2) - 85% cobertura
  - Especialidades: Cardiologia, Dermatologia, Oftalmologia
- **Bradesco Saúde** (ID: 3) - 75% cobertura
  - Especialidades: Cardiologia, Pediatria, Dermatologia

### Clínicas
- **Clínica Cardio Center** (São Paulo)
  - Dr. Carlos Santos - Cardiologia
  - Dra. Marina Silva - Pediatria
- **Clínica Oftalmológica Vision** (São Paulo)
  - Dr. Roberto Costa - Oftalmologia

## 🔧 Arquitetura

```
clinic_agent/
├── agent.py                    # Agentes e ferramentas principais
├── test_parallel_agents.py     # Testes completos
└── README.md                   # Esta documentação

clinic_system/
├── database_models.py          # Modelos de dados e banco
├── clinic_agent.py             # Agentes adicionais
└── workflow_agents.py          # Workflows sequenciais e paralelos
```

## 🌟 Vantagens do Processamento Paralelo

- ⚡ **Redução de latência**: Múltiplas tarefas executadas simultaneamente
- 🎯 **Eficiência**: Melhor uso de recursos
- 📈 **Escalabilidade**: Fácil adicionar novos agentes paralelos
- 🔄 **Confiabilidade**: Cada agente tem responsabilidade específica

## 📝 Notas Importantes

1. O sistema usa **DeepSeek R1** via Ollama para processamento de linguagem natural
2. Os agentes paralelos compartilham o estado da sessão (`session.state`)
3. Cada agente escreve em chaves únicas para evitar conflitos
4. O banco de dados é em memória (para produção, usar banco persistente)

## 🤝 Contribuindo

Para adicionar novos agentes ou ferramentas:

1. Crie a função/tool em `agent.py`
2. Adicione ao agente apropriado
3. Atualize os testes em `test_parallel_agents.py`
4. Documente as mudanças

## 📄 Licença

Este projeto é parte do sistema Artifex Agents.

---

**Desenvolvido com Google ADK e DeepSeek R1** 🚀
