# 🚀 Guia Rápido de Início

## ⚡ Início Rápido (5 minutos)

### 1. Instale o Ollama e DeepSeek R1
```bash
# Baixe e instale Ollama: https://ollama.ai/download
# Depois execute:
ollama pull deepseek-r1:latest
```

### 2. Instale as Dependências
```bash
cd d:\Projetos\NewAngleAI\artifex-agents
pip install -r requirements.txt
```

### 3. Execute o Teste
```bash
python -m clinic_agent.test_parallel_agents
```

---

## 📝 Exemplo Mínimo

```python
from clinic_agent.agent import (
    greet_patient,
    search_available_doctors,
    book_appointment
)

# 1. Cumprimentar
print(greet_patient("João")['message'])

# 2. Buscar médicos
doctors = search_available_doctors(
    specialty="Cardiologia",
    insurance_plan_id=1
)
print(f"Encontrados: {doctors['doctors_found']} médicos")

# 3. Marcar consulta
if doctors['doctors']:
    doctor = doctors['doctors'][0]
    slot = doctor['available_slots'][0]
    
    result = book_appointment(
        patient_name="João Silva",
        patient_email="joao@email.com",
        patient_phone="(11) 98765-4321",
        patient_cpf="123.456.789-00",
        doctor_id=doctor['doctor_id'],
        clinic_id=doctor['clinic_id'],
        slot_id=slot['slot_id'],
        appointment_datetime=slot['datetime'],
        insurance_plan_id=1,
        specialty="Cardiologia"
    )
    
    print(result['message'])
    # ✅ Consulta marcada com sucesso!
```

---

## 🎯 Principais Comandos

### Verificar Instalação
```bash
python -c "from clinic_agent.agent import clinic_root_agent; print('OK!')"
```

### Listar Agentes Disponíveis
```python
from clinic_agent.agent import __all__
print(__all__)
```

### Ver Planos de Saúde
```python
from clinic_agent.agent import check_patient_insurance

result = check_patient_insurance(
    patient_name="Teste",
    insurance_plan_name="Unimed"
)
print(result)
```

### Buscar Médicos
```python
from clinic_agent.agent import search_available_doctors

doctors = search_available_doctors(
    specialty="Cardiologia",
    insurance_plan_id=1,
    city="São Paulo"
)

for doc in doctors.get('doctors', []):
    print(f"{doc['doctor_name']} - {doc['clinic_name']}")
```

---

## 🔍 Especialidades Disponíveis

- **Cardiologia** - Dr. Carlos Santos
- **Oftalmologia** - Dr. Roberto Costa  
- **Pediatria** - Dra. Marina Silva

---

## 💳 Planos de Saúde

| ID | Nome | Cobertura |
|----|------|-----------|
| 1 | Unimed | 80% |
| 2 | Amil | 85% |
| 3 | Bradesco Saúde | 75% |

---

## 📚 Documentação Completa

- **README.md** - Documentação principal
- **INSTALL.md** - Guia de instalação detalhado
- **SUMMARY.md** - Resumo executivo
- **examples.py** - Exemplos de código

---

## 🆘 Problemas Comuns

### Erro: "No module named 'google.adk'"
```bash
pip install google-adk==1.21.0
```

### Erro: "Connection refused"
```bash
ollama serve
```

### Erro: "Model not found"
```bash
ollama pull deepseek-r1:latest
```

---

## ✅ Pronto!

Agora você pode usar o sistema completo de agentes paralelos! 🎉

Para mais informações, consulte **README.md**
