# FIAP - Atividade Integradora (Fase 1)

Verificação pré-decolagem da missão Aurora em Python. O programa lê a telemetria da nave, decide entre **PRONTO PARA DECOLAR** e **DECOLAGEM ABORTADA**, calcula a autonomia da bateria e pede uma análise para a IA do Gemini.

## Integrantes

- **Murilo Ribeiro Falconeri**
- **Gabriel Ferreira da Silva**
- **Gustavo Rocha Caxias**
- **José Kauan Medeiros Machado**

## Arquivos

- `fase1/index.py`: script principal
- `fase1/analise_ia.py`: análise com a IA
- `fase1/relatorio_pre_decolagem.ipynb`: notebook
- `Relatorio Missao Aurora.pdf`: relatório

## Como rodar

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python fase1/index.py
```

Para a análise por IA, crie um arquivo `.env` na raiz com `GEMINI_API_KEY=sua_chave` (a chave é grátis em [aistudio.google.com/apikey](https://aistudio.google.com/apikey)). Sem ele o programa roda normal e só pula essa parte.

O notebook pode ser aberto no [Google Colab](https://colab.research.google.com/github/Murilo1501/FIAP-atividade-integradora-fase-1/blob/main/fase1/relatorio_pre_decolagem.ipynb). É só executar todas as células. Para a IA, cadastre a chave em Secrets com o nome `GEMINI_API_KEY`.

## Fluxograma

```mermaid
flowchart TD
    Start([Início]) --> ReadTemp[Ler temperatura interna e externa]
    Start --> ReadIntegrity[Ler integridade estrutural]
    Start --> ReadEnergy[Ler nível de energia]
    Start --> ReadPressure[Ler pressão do tanque]
    Start --> ReadModules[Ler status dos módulos críticos]

    ReadTemp --> ClassifyIntTemp[Classificar temperatura interna]
    ReadTemp --> ClassifyExtTemp[Classificar temperatura externa]
    ReadIntegrity --> ClassifyIntegrity[Verificar integridade estrutural]
    ReadEnergy --> ClassifyEnergy[Classificar nível de energia]
    ReadPressure --> ClassifyPressure[Classificar pressão do tanque]
    ReadModules --> ClassifyModules[Verificar status dos módulos]

    ClassifyIntTemp --> Merge[Reunir diagnóstico dos 6 parâmetros]
    ClassifyExtTemp --> Merge
    ClassifyIntegrity --> Merge
    ClassifyEnergy --> Merge
    ClassifyPressure --> Merge
    ClassifyModules --> Merge

    Merge --> Critical{Alguma leitura crítica?}
    Critical -->|Sim| AbortCritical[DECOLAGEM ABORTADA sistema em estado crítico]
    Critical -->|Não| Alert{Alguma leitura em alerta?}
    Alert -->|Sim| AbortAlert[DECOLAGEM ABORTADA alertas detectados]
    Alert -->|Não| Ready[PRONTO PARA DECOLAR todos os sistemas operacionais]

    AbortCritical --> Autonomy[Calcular autonomia energética]
    AbortAlert --> Autonomy
    Ready --> Autonomy

    Autonomy --> Stored[Energia armazenada = capacidade x carga atual]
    Stored --> Losses["Subtrair perdas energéticas de 10%"]
    Losses --> Usable[Energia útil resultante]
    Usable --> Consumption[Subtrair consumo estimado da decolagem]
    Consumption --> Reserve["Subtrair reserva operacional de 20%"]

    Reserve --> Enough{Sobrou energia?}
    Enough -->|Não| NoAutonomy[Autonomia insuficiente para a missão]
    Enough -->|Sim| Hours[Converter energia restante em horas de autonomia]

    NoAutonomy --> BuildTelemetry[Montar dicionário com toda a telemetria e o veredito]
    Hours --> BuildTelemetry
    BuildTelemetry --> HasKey{Tem chave da API?}
    HasKey -->|Não| End
    HasKey -->|Sim| AI[Enviar telemetria, veredito e autonomia estimada para a IA Gemini]
    AI --> AIAnalysis[IA classifica cada dado, aponta possíveis anomalias e sugere riscos]
    AIAnalysis --> End([Fim - diagnóstico, autonomia e análise da IA exibidos])
```

## Prints

Decolagem autorizada:

![Decolagem autorizada](prints/01_sistemas_nominais.png)

Energia abaixo do mínimo para decolar:

![Energia abaixo do mínimo](prints/02_energia_abaixo_minimo.png)

Várias falhas ao mesmo tempo:

![Múltiplas falhas](prints/08_multiplas_falhas.png)

Os outros cenários estão na pasta [prints](prints/).
