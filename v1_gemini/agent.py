"""
Agente FAQ independente para dúvidas sobre o sistema da clínica
Segue o padrão ADK, não depende do root_agent
"""

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from typing import Dict

# ==================== TOOL FAQ ====================

def describe_system(question: str) -> Dict:
    """
    Responde dúvidas sobre qualquer aspecto do sistema da clínica.

    Args:
        question: Pergunta do usuário sobre o sistema

    Returns:
        Resposta detalhada sobre o funcionamento, regras, fluxos ou integrações do sistema
    """
    # Aqui pode ser integrado com base de conhecimento, documentação, etc.
    return {
        "status": "success",
        "message": (
            "Sou o agente FAQ. Por favor, detalhe sua dúvida sobre o sistema da clínica "
            "para que eu possa fornecer uma explicação clara e completa."
        )
    }

# ==================== PROMPT FAQ ====================

FAQ_PROMPT = """
Você é um agente especialista em responder dúvidas sobre o sistema da clínica.

Objetivos:
1. Responder qualquer dúvida do usuário sobre funcionalidades, fluxos, regras, etc.
2. Ser claro, objetivo e detalhado.
3. Não inventar informações. Se não souber, peça para o usuário detalhar a dúvida.

Regras:
- Não execute ações, apenas explique e oriente.
- Não encaminhe para outros agentes.
- Use apenas o conhecimento do sistema.
"""

# ==================== AGENT FAQ ====================

faq_model = LiteLlm(model="ollama_chat/llama3.2:1b")

faq_agent = Agent(
    model=faq_model,
    name="faq_agent",
    description="Agente independente para responder dúvidas sobre o sistema da clínica",
    instruction=FAQ_PROMPT,
    tools=[describe_system]
)

# Alias para compatibilidade com ADK Web
root_agent = faq_agent

# ==================== EXPORTS ====================

__all__ = [
    "root_agent",
]