import os
import logging
from typing import Dict, Optional, Any
from datetime import datetime
from google.adk.agents.llm_agent import Agent, LlmAgent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv

from .database import (
    search_specialty_availability, 
)

load_dotenv()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Modelo via Ollama
llm_model = LiteLlm(
    model=os.getenv("MODEL"),
    temperature=0.2,
    top_p=float(os.getenv("LLM_TOP_P", "0.9")),
    top_k=int(os.getenv("LLM_TOP_K", "40")),
)

# ==================== VALIDADORES ====================

def validate_cpf(cpf: str) -> bool:
    """Valida se CPF tem 11 dígitos"""
    if not cpf:
        return False
    cpf_clean = str(cpf).replace(".", "").replace("-", "").strip()
    return len(cpf_clean) == 11 and cpf_clean.isdigit()

def validate_date_of_birth(date_str: str) -> bool:
    """Valida data de nascimento em formato DD/MM/YYYY ou YYYY-MM-DD"""
    if not date_str:
        return False
    try:
        try:
            datetime.strptime(str(date_str).strip(), "%d/%m/%Y")
            return True
        except ValueError:
            datetime.strptime(str(date_str).strip(), "%Y-%m-%d")
            return True
    except:
        return False

def convert_date_to_iso(date_str: str) -> str:
    """Converte data DD/MM/YYYY para YYYY-MM-DD"""
    if not date_str:
        return None
    try:
        date_obj = datetime.strptime(str(date_str).strip(), "%d/%m/%Y")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        # Já está em formato ISO
        return str(date_str).strip()

# ==================== TOOLS ====================

def schedule_search(specialty: str) -> Dict[str, Any]:
    """
    Busca disponibilidade de clínicas, médicos e horários para uma determinada especialidade.
    IMPORTANTE: Esta ferramenta DEVE ser chamada quando o paciente mencionar uma especialidade.
    """
    logger.info(f"========== SCHEDULE_SEARCH INICIADO ==========")
    
    # Conversão segura de entrada
    specialty = str(specialty).strip() if specialty else ""
    logger.info(f"Especialidade solicitada: '{specialty}'")
    
    if not specialty:
        logger.warning("Especialidade vazia ou inválida recebida")
        return {"status": "error", "message": "Por favor, informe uma especialidade válida."}

    try:
        logger.debug(f"Chamando search_specialty_availability com: '{specialty}'")
        results = search_specialty_availability(specialty)
        
        logger.info(f"Resposta do banco de dados recebida")
        logger.info(f"Número de resultados encontrados: {len(results) if results else 0}")
        
        if not results:
            logger.warning(f"Nenhuma disponibilidade encontrada para '{specialty}'")
            return {
                "status": "not_found",
                "message": f"Não encontrei disponibilidade para '{specialty}' no momento.",
                "data": []
            }

        logger.info(f"✓ Sucesso! {len(results)} resultado(s) encontrado(s)")
        
        return {
            "status": "success",
            "specialty": specialty,
            "total_results": len(results),
            "data": results,
            "message": f"Encontrei disponibilidade em {len(results)} clinica(s) para {specialty}."
        }
        
    except Exception as e:
        logger.error(f"❌ EXCEÇÃO em schedule_search: {type(e).__name__}: {str(e)}")
        return {
            "status": "error",
            "message": f"Erro ao buscar: {str(e)}",
            "data": []
        }
    finally:
        logger.info(f"========== SCHEDULE_SEARCH FINALIZADO ==========\n")

# ==================== AGENTS ====================

schedule_agent = LlmAgent(
    model=llm_model,
    name="agendador_virtual",
    description="Agente especialista em buscar e confirmar agendamentos de consultas médicas.",
    instruction="""
    # VOCÊ É O AGENDADOR VIRTUAL

    Sua missão é ajudar pacientes a agendar consultas médicas usando as ferramentas disponíveis.

    ## FLUXO OBRIGATÓRIO:

    ### PASSO 1: Buscar Disponibilidade
    - Quando o paciente mencionar uma especialidade (ex: "cardiologia", "oftalmologia"), 
      IMEDIATAMENTE use a ferramenta `schedule_search` com essa especialidade.
    - Não invente dados! Sempre use `schedule_search` para buscar informações reais.
    - Apresente os resultados de forma clara e organizada.
    - Mostre: Clínica, Médico, Especialidade, Data, Hora, Valor da Consulta

    ## REGRAS CRÍTICAS:
    1. SEMPRE use `schedule_search` quando uma especialidade é mencionada
    2. NUNCA invente dados - use sempre dados do banco
    3. SEMPRE confirme dados ANTES de usar `schedule_appointment`
    4. SEMPRE mostre: clínica, médico, especialidade, data, hora, valor
    5. NUNCA mostre IDs técnicos diretamente ao paciente
    10. Mantenha tom profissional e educado

    - SEMPRE use `schedule_appointment` após confirmação
    - NUNCA responda "agendamento feito" sem chamar a ferramenta
    - Se o paciente confirma, CHAMAR A FERRAMENTA É OBRIGATÓRIO

    ## SE NÃO HOUVER DISPONIBILIDADE:
    - Informe com empatia
    - Sugira outras especialidades ou datas
    """,

    tools=[schedule_search]
)

clinic_root_agent = Agent(
    model=llm_model,
    name="clinic_appointment_system",
    description="Sistema de agendamento de consultas médicas com persistência real no banco de dados.",
    instruction="""
    # VOCÊ É O COORDENADOR DO SISTEMA DE AGENDAMENTO da open-network

    Sua função é atender pacientes profissionalmente e garantir que os dados sejam coletados corretamente.

    ## FLUXO PADRÃO:

    1. Cumprimentar: Dê boas-vindas educadamente
    2. Entender necessidade: Pergunte qual especialidade o paciente precisa
    3. DELEGAR IMEDIATAMENTE: Após confirmação explícita, repasse para `agendador_virtual`

    ## DADOS OBRIGATÓRIOS:
    - Nome completo (mínimo 3 caracteres, sem abreviações)
    - CPF (EXATAMENTE 11 dígitos: 12345678900)
    - Data de nascimento (DD/MM/YYYY: 15/03/1990)
    - Especialidade desejada

    ## QUALIDADE DO ATENDIMENTO:
    - Fale no idioma Português do Brasil
    - NUNCA invente informações
    - Mantenha tom profissional e amigável
    - Respeite a privacidade do paciente
    - Seja direto, não fale mais que o necessário
    """,

    sub_agents=[schedule_agent],
    tools=[]
)

root_agent = clinic_root_agent