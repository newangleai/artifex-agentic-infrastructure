# 📚 Índice de Documentação - Sistema de Agentes Paralelos

## 🎯 Comece Aqui

Novo no projeto? Siga esta ordem:

1. **[QUICKSTART.md](QUICKSTART.md)** ⚡
   - Início rápido em 5 minutos
   - Exemplo mínimo de código
   - Comandos essenciais

2. **[README.md](README.md)** 📖
   - Visão geral completa
   - Funcionalidades detalhadas
   - Exemplos de uso

3. **[INSTALL.md](INSTALL.md)** 🔧
   - Guia de instalação passo a passo
   - Solução de problemas
   - Configuração do ambiente

---

## 📁 Estrutura de Arquivos

### 📄 Documentação

| Arquivo | Descrição | Para Quem |
|---------|-----------|-----------|
| **QUICKSTART.md** | Início rápido | Iniciantes |
| **README.md** | Documentação principal | Todos |
| **INSTALL.md** | Guia de instalação | Desenvolvedores |
| **SUMMARY.md** | Resumo executivo | Gestores/Overview |
| **INDEX.md** | Este arquivo | Navegação |

### 💻 Código

| Arquivo | Descrição | Linhas |
|---------|-----------|--------|
| **agent.py** | Código principal (agentes + tools) | ~565 |
| **test_parallel_agents.py** | Testes completos | ~300 |
| **examples.py** | Exemplos documentados | ~250 |

### 🗄️ Outros

| Arquivo | Descrição |
|---------|-----------|
| **.env** | Configurações (criar se necessário) |
| **__init__.py** | Módulo Python |

---

## 🎓 Guias por Objetivo

### Quero Começar Rapidamente
→ **[QUICKSTART.md](QUICKSTART.md)**

### Quero Entender o Sistema
→ **[README.md](README.md)** → **[SUMMARY.md](SUMMARY.md)**

### Quero Instalar e Configurar
→ **[INSTALL.md](INSTALL.md)**

### Quero Ver Exemplos de Código
→ **[examples.py](examples.py)** → **[test_parallel_agents.py](test_parallel_agents.py)**

### Quero Modificar o Sistema
→ **[agent.py](agent.py)** → **[README.md](README.md)** (seção Arquitetura)

---

## 🔍 Busca Rápida

### Conceitos Principais

- **Agentes Paralelos**: [README.md](README.md#agentes-especializados)
- **Ferramentas (Tools)**: [README.md](README.md#ferramentas-tools)
- **Fluxo de Atendimento**: [SUMMARY.md](SUMMARY.md#fluxo-de-atendimento)
- **Arquitetura**: [SUMMARY.md](SUMMARY.md#arquitetura-do-sistema)

### Tarefas Comuns

- **Instalar**: [INSTALL.md](INSTALL.md)
- **Testar**: [test_parallel_agents.py](test_parallel_agents.py)
- **Usar**: [examples.py](examples.py)
- **Troubleshooting**: [INSTALL.md](INSTALL.md#solução-de-problemas)

### Código

- **Cumprimentar Paciente**: `greet_patient()` em [agent.py](agent.py)
- **Buscar Médicos**: `search_available_doctors()` em [agent.py](agent.py)
- **Marcar Consulta**: `book_appointment()` em [agent.py](agent.py)
- **Verificar Plano**: `check_patient_insurance()` em [agent.py](agent.py)

---

## 📊 Visão Geral do Sistema

```
Sistema de Agentes Paralelos
├── 6 Agentes Especializados
│   ├── clinic_root_agent (Coordenador)
│   ├── patient_service_agent (Atendimento)
│   ├── insurance_agent (Planos)
│   ├── doctor_search_agent (Busca)
│   ├── booking_agent (Marcação)
│   └── parallel_search_agent (Paralelo)
│
├── 7 Ferramentas (Tools)
│   ├── greet_patient()
│   ├── understand_appointment_request()
│   ├── check_patient_insurance()
│   ├── validate_insurance_coverage()
│   ├── search_available_doctors()
│   ├── show_doctors_and_schedules()
│   └── book_appointment()
│
└── Tecnologias
    ├── Google ADK 1.21.0
    ├── DeepSeek R1 (via Ollama)
    └── Python 3.8+
```

---

## 🚀 Próximos Passos

1. ✅ Leia o [QUICKSTART.md](QUICKSTART.md)
2. ✅ Instale seguindo [INSTALL.md](INSTALL.md)
3. ✅ Execute os testes: `python test_parallel_agents.py`
4. ✅ Explore os exemplos: `python examples.py`
5. ✅ Leia a documentação completa: [README.md](README.md)

---

## 💡 Dicas

- 📌 **Primeiro uso?** Comece pelo QUICKSTART.md
- 🔧 **Problemas?** Veja INSTALL.md → Solução de Problemas
- 📚 **Quer aprender?** Leia README.md e SUMMARY.md
- 💻 **Quer código?** Veja examples.py e test_parallel_agents.py
- 🏗️ **Quer modificar?** Estude agent.py

---

## 📞 Recursos

### Documentação Externa
- [Google ADK](https://github.com/google/adk)
- [Ollama](https://ollama.ai/)
- [DeepSeek](https://www.deepseek.com/)

### Arquivos Relacionados
- `../clinic_system/database_models.py` - Modelos de dados
- `../clinic_system/workflow_agents.py` - Workflows adicionais
- `../requirements.txt` - Dependências do projeto

---

## ✨ Destaques

- ⚡ **Performance**: 50% mais rápido com processamento paralelo
- 🤖 **6 Agentes**: Cada um especializado em uma tarefa
- 🛠️ **7 Tools**: Funções prontas para uso
- 📚 **Documentação Completa**: 5 guias diferentes
- 🧪 **Testes**: Suite completa de testes

---

**Desenvolvido com Google ADK e DeepSeek R1** 🚀  
*Versão 1.0.0 - Dezembro 2025*
