# Guia de Instalação e Configuração

## 📋 Pré-requisitos

### 1. Python 3.8+
Certifique-se de ter Python 3.8 ou superior instalado:
```bash
python --version
```

### 2. Ollama com DeepSeek R1
Instale o Ollama e baixe o modelo DeepSeek R1:

**Windows:**
1. Baixe o instalador: https://ollama.ai/download
2. Execute o instalador
3. Abra o terminal e execute:
```bash
ollama pull deepseek-r1:latest
```

**Verificar instalação:**
```bash
ollama list
# Deve mostrar deepseek-r1:latest
```

### 3. Google ADK (Agent Development Kit)
```bash
pip install google-adk==1.21.0
```

### 4. Dependências Adicionais
```bash
pip install litellm python-dotenv
```

## 🚀 Instalação do Projeto

### Passo 1: Clone ou navegue até o projeto
```bash
cd d:\Projetos\NewAngleAI\artifex-agents
```

### Passo 2: Instale as dependências
```bash
pip install -r requirements.txt
```

### Passo 3: Configure variáveis de ambiente (opcional)
Crie um arquivo `.env` em `clinic_agent/`:
```env
# clinic_agent/.env
OLLAMA_HOST=http://localhost:11434
MODEL_NAME=deepseek-r1:latest
```

### Passo 4: Verifique a instalação
```bash
python -c "from clinic_agent.agent import clinic_root_agent; print('✓ Instalação OK!')"
```

## 🧪 Executando os Testes

### Teste Completo
```bash
cd clinic_agent
python test_parallel_agents.py
```

### Teste Individual de Tools
```python
from clinic_agent.agent import greet_patient

result = greet_patient(patient_name="Teste")
print(result)
```

## 🔧 Configuração do Ollama

### Verificar se o Ollama está rodando
```bash
ollama list
```

### Iniciar o serviço Ollama (se necessário)
```bash
ollama serve
```

### Testar o modelo DeepSeek R1
```bash
ollama run deepseek-r1:latest "Olá, como você está?"
```

## 📁 Estrutura do Projeto

```
artifex-agents/
│
├── clinic_agent/                    # Sistema de agentes paralelos
│   ├── .env                        # Configurações (criar)
│   ├── __init__.py
│   ├── agent.py                    # ⭐ Agentes e tools principais
│   ├── test_parallel_agents.py     # Testes completos
│   ├── examples.py                 # Exemplos de uso
│   └── README.md                   # Documentação
│
├── clinic_system/                   # Sistema de banco de dados
│   ├── database_models.py          # Modelos e DB
│   ├── clinic_agent.py
│   └── workflow_agents.py
│
└── requirements.txt                 # Dependências
```

## 🐛 Solução de Problemas

### Erro: "No module named 'google.adk'"
**Solução:**
```bash
pip install google-adk==1.21.0
```

### Erro: "Connection refused" ao usar Ollama
**Solução:**
1. Verifique se o Ollama está rodando:
```bash
ollama list
```
2. Se não estiver, inicie:
```bash
ollama serve
```

### Erro: "Model not found: deepseek-r1:latest"
**Solução:**
```bash
ollama pull deepseek-r1:latest
```

### Erro: "ModuleNotFoundError: No module named 'clinic_system'"
**Solução:**
Execute a partir do diretório raiz:
```bash
cd d:\Projetos\NewAngleAI\artifex-agents
python -m clinic_agent.test_parallel_agents
```

## 🎯 Primeiros Passos

### 1. Teste Simples
```python
from clinic_agent.agent import greet_patient, understand_appointment_request

# Cumprimentar paciente
greeting = greet_patient(patient_name="João")
print(greeting['message'])

# Entender solicitação
request = understand_appointment_request(
    patient_message="Preciso de um cardiologista"
)
print(f"Especialidade: {request['specialty']}")
```

### 2. Busca de Médicos
```python
from clinic_agent.agent import search_available_doctors

doctors = search_available_doctors(
    specialty="Cardiologia",
    insurance_plan_id=1,
    city="São Paulo"
)

print(f"Médicos encontrados: {doctors['doctors_found']}")
```

### 3. Fluxo Completo
Execute o arquivo de testes:
```bash
python clinic_agent/test_parallel_agents.py
```

## 📊 Verificação de Performance

### Teste de Latência do Modelo
```bash
time ollama run deepseek-r1:latest "Teste rápido"
```

### Monitorar Uso de Recursos
```bash
# Windows
tasklist | findstr ollama

# Ver uso de GPU (se disponível)
nvidia-smi
```

## 🔐 Segurança e Boas Práticas

### Variáveis de Ambiente
Nunca commite o arquivo `.env` com credenciais:
```bash
# Adicione ao .gitignore
echo "clinic_agent/.env" >> .gitignore
```

### Validação de Dados
O sistema já inclui validações básicas, mas para produção:
- Valide CPF com algoritmo apropriado
- Sanitize inputs do usuário
- Use HTTPS para comunicação
- Implemente rate limiting

## 📚 Recursos Adicionais

### Documentação Oficial
- **Google ADK**: https://github.com/google/adk
- **Ollama**: https://ollama.ai/
- **DeepSeek**: https://www.deepseek.com/

### Exemplos de Código
Veja `examples.py` para exemplos detalhados de uso.

### Suporte
Para problemas ou dúvidas:
1. Verifique a seção "Solução de Problemas" acima
2. Consulte os logs de erro
3. Verifique a documentação do ADK

## ✅ Checklist de Instalação

- [ ] Python 3.8+ instalado
- [ ] Ollama instalado e rodando
- [ ] Modelo deepseek-r1:latest baixado
- [ ] Google ADK instalado (`pip install google-adk`)
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Testes executados com sucesso
- [ ] Arquivo `.env` configurado (opcional)

## 🎉 Pronto para Usar!

Após completar todos os passos acima, você está pronto para usar o sistema de agentes paralelos!

Execute:
```bash
python clinic_agent/test_parallel_agents.py
```

E veja a mágica acontecer! ✨
