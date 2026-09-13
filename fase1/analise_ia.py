import os

MODELS = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite"]

SYSTEM_PROMPT = """Você analisa a telemetria de pré-decolagem de um foguete.

Faixas seguras:
- temperatura interna: -40 a 50 °C (alerta até 70)
- temperatura externa: -50 a 60 °C (alerta até -60 e 80)
- energia: mínimo de 95% para decolar (crítico abaixo de 40%)
- pressão do tanque: 4.0 a 5.5 bar (alerta de 3.5 a 6.5)
- integridade estrutural: 1 ok, 0 comprometida
- módulos críticos: ok ou operacional

Responda em português, curto e sem markdown, com:
1. Classificação de cada dado (normal, atenção ou crítico)
2. Possíveis anomalias
3. Sugestões de risco

Use só os dados recebidos. A decisão de decolar é do algoritmo, não sua."""


def load_api_key():
    key = os.getenv("GEMINI_API_KEY")
    if key:
        return key

    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    if os.path.exists(env_path):
        with open(env_path, encoding="utf-8-sig") as file:
            for line in file:
                if line.startswith("GEMINI_API_KEY="):
                    return line.split("=", 1)[1].strip()
    return None


def run_ai_analysis(telemetry, launch_ok, autonomy_hours):
    api_key = load_api_key()
    if not api_key:
        print("\nAnálise por IA ignorada: GEMINI_API_KEY não encontrada no .env")
        return

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        print("\nAnálise por IA ignorada.")
        return

    verdict = "PRONTO PARA DECOLAR" if launch_ok else "DECOLAGEM ABORTADA"
    data = "\n".join(f"- {name}: {value}" for name, value in telemetry.items())
    prompt = f"Telemetria:\n{data}\nVeredito do algoritmo: {verdict}\nAutonomia estimada: {autonomy_hours:.1f} horas"

    client = genai.Client(api_key=api_key, http_options=types.HttpOptions(timeout=30000))
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=0.2,
        thinking_config=types.ThinkingConfig(thinking_level="minimal"),
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )

    print("\nConsultando a IA...")
    response = None
    for model in MODELS:
        try:
            response = client.models.generate_content(model=model, contents=prompt, config=config)
            break
        except Exception as error:
            last_error = getattr(error, "message", error)

    if response is None:
        print("Não foi possível consultar a IA:", last_error)
        return

    print("\nAnálise da IA:")
    print((response.text or "A IA não retornou resposta.").strip())
    print()
