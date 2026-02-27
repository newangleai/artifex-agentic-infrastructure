"""
Agente FAQ especializado em Artifex - IMA com interpretação inteligente
Base de conhecimento com processamento semântico
"""

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from typing import Dict, Any
import json
from dotenv import load_dotenv

load_dotenv()

# ==================== KNOWLEDGE BASE ====================
KNOWLEDGE_BASE = {
    "about_artifex": {
        "keywords": ["artifex", "plataforma", "missão", "o que é", "quem é"],
        "content": {
            "nome": "Artifex - IMA",
            "tipo": "Infraestrutura Médica Agentificada",
            "missão": "Automatizar completamente o fluxo ambulatorial através de agentes inteligentes",
            "diferenciais": ["automatização total", "sem interferência humana", "sistema integrado"],
            "tecnologia": "Rede de agentes IA orquestrados"
        }
    },
    "booking_flow": {
        "keywords": ["agendamento", "como funciona", "fluxo", "processo", "etapas", "consulta"],
        "content": {
            "etapas": [
                "interpretação_solicitação",
                "busca_filtragem_clínicas",
                "apresentação_médicos",
                "seleção_profissional",
                "confirmação",
                "fila_virtual",
                "notificação_atendimento"
            ],
            "características": ["automático", "sem esperas", "real-time"]
        }
    },
    "clinic_management": {
        "keywords": ["clínica", "médico", "profissional", "especialidade", "horário", "agenda"],
        "content": {
            "gerenciamento": ["cadastro", "integração", "sincronização"],
            "filtros": ["plano de saúde", "localização", "disponibilidade", "especialidade"],
            "integrações": ["google calendar", "sincronização automática"]
        }
    },
    "patient_data": {
        "keywords": ["dados", "paciente", "informações", "privacidade", "lgpd", "segurança"],
        "content": {
            "dados_coletados": ["nome", "cpf", "data_nascimento", "contato", "plano_saúde", "localização"],
            "proteção": ["criptografia", "lgpd", "backup automático", "acesso controlado"],
            "histórico": ["consultas", "médicos", "especialidades", "preferências"]
        }
    },
    "insurance": {
        "keywords": ["plano", "seguro", "cobertura", "elegibilidade", "validação", "faturamento"],
        "content": {
            "validações": ["compatibilidade", "cobertura", "elegibilidade", "credenciamento"],
            "tipos": ["planos de saúde", "seguros privados", "planos corporativos", "particular"],
            "fluxo": ["seleção", "validação", "faturamento", "comprovante"]
        }
    },
    "quality": {
        "keywords": ["qualidade", "experiência", "satisfação", "feedback", "performance", "monitoramento"],
        "content": {
            "diferenciais": ["100% automatizado", "resposta imediata", "24/7", "múltiplos canais"],
            "garantias": ["confirmação imediata", "validação automática", "sincronização real-time"],
            "monitoramento": ["rastreamento", "logs", "alertas", "relatórios"]
        }
    },
    "rules": {
        "keywords": ["regra", "restrição", "elegibilidade", "cancelamento", "fila", "comunicação"],
        "content": {
            "elegibilidade": ["plano válido", "clínica credenciada", "especialidade coberta", "médico disponível"],
            "agendamento": ["um simultâneo", "cancelamento 24h", "reagendamento automático"],
            "fila": ["fifo", "prioridade emergências", "sincronização", "notificações"],
            "comunicação": ["confirmação", "lembretes", "notificações", "informações"]
        }
    },
    "troubleshooting": {
        "keywords": ["problema", "erro", "não funciona", "falha", "ajuda", "solução"],
        "content": {
            "problemas_comuns": {
                "sem_clínicas": "Verificar plano, data/horário, zona de abrangência, cobertura de especialidade",
                "cancelamento": "Reagendamento automático, outras clínicas oferecidas",
                "confirmação_perdida": "Verificar telefone/email, spam, reenvio, app",
                "sem_cheguei": "Enviar quando lembrar, não perde consulta",
                "consultório": "Informação via APP quando hora aproxima"
            },
            "contato": ["suporte 24/7", "email", "whatsapp automático"]
        }
    }
}

# ==================== SEMANTIC ANALYSIS ====================

def analyze_user_intent(user_message: str) -> Dict:
    """
    Analisa a intenção semântica da mensagem do usuário
    
    Args:
        user_message: Mensagem do usuário
        
    Returns:
        Dicionário com análise de intenção
    """
    message_lower = user_message.lower()
    
    matched_topics = []
    relevance_scores = {}
    
    for topic, topic_data in KNOWLEDGE_BASE.items():
        keywords = topic_data.get("keywords", [])
        matches = sum(1 for keyword in keywords if keyword in message_lower)
        
        if matches > 0:
            relevance_scores[topic] = matches
            matched_topics.append(topic)
    
    primary_topic = max(relevance_scores, key=relevance_scores.get) if relevance_scores else None
    
    return {
        "primary_topic": primary_topic,
        "matched_topics": matched_topics,
        "relevance_scores": relevance_scores,
        "question_type": classify_question_type(user_message),
        "is_problem": "problema" in message_lower or "erro" in message_lower or "não" in message_lower
    }

def classify_question_type(user_message: str) -> str:
    """Classifica o tipo de pergunta"""
    msg = user_message.lower()
    
    if any(word in msg for word in ["como", "funciona", "processo", "fluxo"]):
        return "explicativo"
    elif any(word in msg for word in ["por que", "qual", "qual é", "quais são"]):
        return "informativo"
    elif any(word in msg for word in ["problema", "erro", "não funciona", "ajuda"]):
        return "suporte"
    elif any(word in msg for word in ["posso", "conseguir", "é possível"]):
        return "validação"
    else:
        return "geral"

def build_contextual_response(intent_analysis: Any, user_message: str) -> str:
    """
    Constrói resposta contextual baseada na análise de intenção
    
    Args:
        intent_analysis: Análise da intenção do usuário (pode ser dict ou JSON string)
        user_message: Mensagem original
        
    Returns:
        Resposta construída dinamicamente
    """
    # Se recebeu uma string (ex: output de outra tool), tenta converter para dict
    if isinstance(intent_analysis, str):
        try:
            intent_analysis = json.loads(intent_analysis)
        except json.JSONDecodeError:
            # Caso não seja JSON, assumimos que possa ser o identificador do tópico
            intent_analysis = {"primary_topic": intent_analysis}

    if not isinstance(intent_analysis, dict):
        return "Desculpe, houve um erro ao processar sua pergunta. Poderia reformular?"

    topic = intent_analysis.get("primary_topic")
    question_type = intent_analysis.get("question_type")
    is_problem = intent_analysis.get("is_problem")
    
    if not topic or topic not in KNOWLEDGE_BASE:
        return "Desculpe, não identifiquei claramente sua pergunta. Poderia detalhar mais? Fale sobre: agendamento, clínicas, dados, planos, qualidade, regras ou problemas."
    
    topic_data = KNOWLEDGE_BASE[topic]
    content = topic_data.get("content", {})
    
    response = _generate_response_by_type(question_type, topic, content, user_message)
    
    return response

def _generate_response_by_type(q_type: str, topic: str, content: Dict, user_msg: str) -> str:
    """Gera resposta conforme tipo de pergunta"""
    
    if q_type == "explicativo":
        return _explain_topic(topic, content, user_msg)
    elif q_type == "informativo":
        return _inform_topic(topic, content, user_msg)
    elif q_type == "suporte":
        return _solve_problem(topic, content, user_msg)
    elif q_type == "validação":
        return _validate_capability(topic, content, user_msg)
    else:
        return _general_response(topic, content, user_msg)

def _explain_topic(topic: str, content: Dict, user_msg: str) -> str:
    """Explica um tópico detalhadamente"""
    explanations = {
        "booking_flow": f"O agendamento no Artifex funciona em {len(content.get('etapas', []))} etapas automáticas. Começamos interpretando sua solicitação, buscando clínicas compatíveis com seu plano e localização, apresentando médicos disponíveis, confirmando a reserva e gerenciando sua fila virtual até o atendimento. Tudo sem qualquer interferência humana.",
        
        "clinic_management": f"As clínicas são gerenciadas através de integração automática. Sincronizamos agendas em tempo real com {', '.join(content.get('integrações', []))}, aplicando filtros por {', '.join(content.get('filtros', []))} para oferecer as melhores opções.",
        
        "about_artifex": f"Artifex é uma {content.get('tipo')} que {content.get('missão')}. Nossos principais diferenciais são: {', '.join(content.get('diferenciais', []))}.",
        
        "patient_data": f"Coletamos informações essenciais como {', '.join(content.get('dados_coletados', [])[:3])} e mais, todas protegidas com {', '.join(content.get('proteção', [])[:2])}.",
        
        "insurance": f"Validamos automaticamente sua {', '.join(content.get('validações', []))} em tempo real, cobrindo {', '.join(content.get('tipos', [])[:2])} e mais.",
        
        "quality": f"Garantimos experiência de qualidade com diferenciais como: {', '.join(content.get('diferenciais', [])[:3])}.",
        
        "rules": f"O sistema segue regras rigorosas de {', '.join(list(content.keys())[:3])} para garantir conformidade e segurança.",
        
        "troubleshooting": "Identificamos problemas e oferecemos soluções diretas e automáticas para cada situação."
    }
    
    return explanations.get(topic, "Detalhes disponíveis para este tópico.")

def _inform_topic(topic: str, content: Dict, user_msg: str) -> str:
    """Fornece informações específicas"""
    if topic == "booking_flow":
        return f"O Artifex realiza {len(content.get('etapas', []))} etapas automáticas de agendamento, sendo um processo {' e '.join(content.get('características', []))}."
    
    elif topic == "clinic_management":
        return f"Gerenciamos clínicas com integração automática, filtrando por {', '.join(content.get('filtros', []))}."
    
    elif topic == "insurance":
        return f"Validamos {', '.join(content.get('validações', []))} automaticamente para cada agendamento."
    
    elif topic == "patient_data":
        return f"Coletamos e protegemos {len(content.get('dados_coletados', []))} tipos de informações do paciente."
    
    else:
        return f"Informações disponíveis sobre {topic.replace('_', ' ')}."

def _solve_problem(topic: str, content: Dict, user_msg: str) -> str:
    """Resolve problemas identificados"""
    if topic == "troubleshooting" or "problema" in user_msg.lower():
        problems = content.get("problemas_comuns", {})
        
        for problem_key, solution in problems.items():
            if any(word in user_msg.lower() for word in problem_key.split("_")):
                return f"Para este problema: {solution}"
        
        return "Nosso suporte 24/7 está disponível via FAQ para ajudar com qualquer problema específico."
    
    return "Identifique melhor o problema para que eu possa ajudar."

def _validate_capability(topic: str, content: Dict, user_msg: str) -> str:
    """Valida se algo é possível no Artifex"""
    capabilities = {
        "booking_flow": "Sim, você pode agendar consultas de forma totalmente automática",
        "clinic_management": "Sim, sincronizamos com múltiplas clínicas automaticamente",
        "insurance": "Sim, validamos cobertura de qualquer plano em tempo real",
        "quality": "Sim, oferecemos experiência 24/7 sem esperas por humanos",
        "patient_data": "Sim, protegemos seus dados conforme LGPD"
    }
    
    return capabilities.get(topic, "Sim, o Artifex oferece esta funcionalidade.")

def _general_response(topic: str, content: Dict, user_msg: str) -> str:
    """Resposta geral para tópicos"""
    return f"Sobre {topic.replace('_', ' ')}: posso detalhar aspectos específicos. Qual aspecto interessa mais?"

# ==================== PROMPT INTELIGENTE ====================

INTELLIGENT_FAQ_PROMPT = """
Você é um agente especialista em ARTIFEX - a primeira plataforma de IMA (Infraestrutura Médica Agentificada) do Brasil.

MODO DE OPERAÇÃO - INTERPRETAÇÃO INTELIGENTE:

1. ANÁLISE DE INTENÇÃO:
   - Identifique o tópico principal da pergunta do usuário
   - Classifique o tipo de pergunta (explicativa, informativa, suporte, validação)
   - Determine o contexto e necessidade real do usuário

2. RESPOSTA CONTEXTUAL:
   - NÃO use respostas prontas ou templates
   - Construa respostas baseadas na intenção identificada
   - Adapte o nível de detalhe à pergunta específica
   - Seja direto e evite redundâncias

3. REGRAS DE RESPOSTA:
   ✓ Responda APENAS o que foi perguntado
   ✓ Ofereça contexto relevante
   ✓ Não repita informações já mencionadas
   ✓ Use linguagem natural e conversacional
   ✓ Quando necessário aprofundamento, pergunte

4. TÓPICOS DE EXPERTISE:
   - Fluxo de agendamento e seus mecanismos
   - Integração e gerenciamento de clínicas
   - Validação de seguros em tempo real
   - Gestão de dados de pacientes
   - Qualidade e monitoramento
   - Regras clínicas e operacionais
   - Solução de problemas específicos

NUNCA:
   ✗ Leia respostas prontas
   ✗ Diga "de acordo com a documentação"
   ✗ Use frases genéricas
   ✗ Forneça mais do que foi perguntado
   ✗ Redirecione desnecessariamente

SEMPRE:
   ✓ Analise a intenção real
   ✓ Responda inteligentemente
   ✓ Seja conciso e preciso
   ✓ Demonstre compreensão do contexto
"""

# ==================== AGENT FAQ MELHORADO ====================
faq_model = LiteLlm(model="ollama_chat/llama3.2:1b")

faq_agent = Agent(
    model=faq_model,
    name="faq_agent_intelligent",
    description="Agente inteligente de FAQ Artifex - interpreta intenção e responde contextuamente",
    instruction=INTELLIGENT_FAQ_PROMPT,
    tools=[
        analyze_user_intent,
        build_contextual_response,
        classify_question_type
    ]
)

root_agent = faq_agent

__all__ = [
    "root_agent",
    "faq_agent",
    "analyze_user_intent",
    "build_contextual_response",
    "classify_question_type",
    "KNOWLEDGE_BASE"
]