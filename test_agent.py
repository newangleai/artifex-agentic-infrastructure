import vertexai
from vertexai import agent_engines

vertexai.init(
    project="artifex-482515",
    location="us-central1",
)

agent = agent_engines.get("projects/819128507112/locations/us-central1/reasoningEngines/5576418411358978048")

# Criar sessão
session = agent.create_session(user_id="test_user")
session_id = session["id"]

print(f"Sessão criada: {session_id}")
print("Digite 'sair' para encerrar\n")

while True:
    message = input("Você: ")
    if message.lower() == "sair":
        break

    response_text = ""
    for event in agent.stream_query(
        user_id="test_user",
        session_id=session_id,
        message=message,
    ):
        if "content" in event and "parts" in event["content"]:
            for part in event["content"]["parts"]:
                if "text" in part:
                    response_text += part["text"]

    print(f"Agente: {response_text}\n")