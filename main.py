import asyncio
import os
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from dotenv import load_dotenv
from agents import agentes

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

def call_agent(agent, mensagem):
    sessao = InMemorySessionService()
    sessao.create_session(app_name=agent.name, user_id="user1", session_id="session1")
    runner = Runner(agent=agent, app_name=agent.name, session_service=sessao)
    content = types.Content(role="user", parts=[types.Part(text=mensagem)])
    resposta = ""
    for evento in runner.run(user_id="user1", session_id="session1", new_message=content):
        if evento.is_final_response():
            for part in evento.content.parts:
                if part.text:
                    resposta += part.text + "\n"
    return resposta

def agente_explorador(consulta, contexto=""):
    return call_agent(agentes["explorador"], f"Consulta: {consulta}\nContexto: {contexto}")

def agente_detalhista(evento, contexto=""):
    return call_agent(agentes["detalhista"], f"Evento: {evento}\nContexto: {contexto}")

def agente_logistica(evento, local_usuario, contexto=""):
    return call_agent(agentes["logistica"], f"Evento: {evento}\nLocal do Usuário: {local_usuario}\nContexto: {contexto}")

def agente_midia(evento, contexto=""):
    return call_agent(agentes["midia"], f"Evento: {evento}\nContexto: {contexto}")

def agente_orquestrador(mensagem, contexto=""):
    return call_agent(agentes["orquestrador"], f"Mensagem do Usuário: {mensagem}\nContexto: {contexto}")

async def main():
    print("🚀 Iniciando EventHorizon AI 🚀")

    while True:
        # 1. Entrada inicial
        consulta = input("🎯 Que tipo de evento você quer curtir? (ou 'sair') ")
        if consulta.lower() == "sair":
            print("👋 Até a próxima!")
            break
        if not consulta:
            print("❗ Por favor, informe o tipo de evento!")
            continue

        while True:
            eventos_raw = agente_explorador(consulta)
            eventos = [e.strip() for e in eventos_raw.split("\n") if e.strip()]

            if not eventos:
                print("⚠️ Nenhum evento encontrado. Deseja tentar outra busca? (S/N)")
                if input().strip().upper() == "S":
                    break
                else:
                    return

            print("\n🎉 Eventos encontrados:\n")
            for i, evento in enumerate(eventos, 1):
                print(f"[{i}] {evento}")
            print("[0] 🔁 Buscar novamente")

            escolha = input("📌 Escolha um número ou digite 0 para nova busca: ")

            if escolha == "0":
                break
            try:
                idx = int(escolha) - 1
                if 0 <= idx < len(eventos):
                    evento_selecionado = eventos[idx]
                    detalhes = agente_detalhista(evento_selecionado)
                    print("\nℹ️ Detalhes do Evento:\n")
                    print(detalhes)

                    # Escolhas após detalhes
                    while True:
                        prox = input("🚦 Deseja ver a logística (L), mídias (M), voltar à busca (B), ou sair (S)? ").upper()
                        if prox == "L":
                            local = input("📍 De onde você vai sair? ")
                            logistica = agente_logistica(evento_selecionado, local)
                            print("\n🗺️ Logística:\n")
                            print(logistica)
                        elif prox == "M":
                            midia = agente_midia(evento_selecionado)
                            print("\n🎬 Mídias Relacionadas:\n")
                            print(midia)
                        elif prox == "B":
                            break
                        elif prox == "S":
                            print("👋 Até a próxima!")
                            return
                        else:
                            print("❗ Opção inválida. Use L, M, B ou S.")
                    break
                else:
                    print("❗ Escolha inválida.")
            except ValueError:
                print("❗ Digite um número válido.")


if __name__ == "__main__":
    asyncio.run(main())
