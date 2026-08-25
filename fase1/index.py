
"""
1. TEMPERATURA INTERNA (internTemperature)
✅ Operacional: -40°C a +50°C
⚠️ Alerta: 50°C a 70°C
🚨 Crítico: > 70°C
📌 Ideal: 20°C a 25°C

2. TEMPERATURA EXTERNA (externalTemperature)
✅ Operacional: -50°C a +60°C
⚠️ Alerta: -50°C ou > 60°C
🚨 Crítico: < -60°C ou > 80°C
📌 Ideal: 0°C a 30°C (condições de solo)

3. NÍVEL DE ENERGIA (energyLevel)
✅ Operacional: 70% a 100%
⚠️ Alerta: 40% a 69%
🚨 Crítico: < 40%
📌 Necessário para decolagem: ≥ 95%

4. PRESSÃO DO TANQUE (Pressure)
✅ Operacional: 4.0 a 5.5 bar
⚠️ Alerta: 3.5 a 3.9 bar ou 5.6 a 6.0 bar
🚨 Crítico: < 3.5 bar ou > 6.5 bar
📌 Ideal: 4.5 bar


5. STATUS DOS MÓDULOS CRÍTICOS (status)
✅ "OK" ou "OPERACIONAL"
🚨 "FALHA" ou "CRÍTICO"
"""


internTemperature = float(input("Digite a temperatura interna: "));
externalTemperature = float(input("Digite a temperatura externa: "));
energyLevel = float(input( "Digite o nivel de energia: "));
pressure = float(input( "Digite a pressao do tanque: "));
status = str(input("Digite o status dos modulos criticos: "));


def calculateInternalTemperature(internal):

  # Temperatura interna | Gabriel
  
  if internTemperature > 70:
    return "Temperatura interna: CRÍTICA"

  elif internTemperature > 50:
    print("Temperatura interna: ALERTA")

  elif -40 <= internTemperature <= 50:
    print("Temperatura interna: OPERACIONAL")

  if 20 <= internTemperature <= 25:
    print("Temperatura interna IDEAL")
  else:
      print("Temperatura interna abaixo da faixa operacional")

  
def calculateEntryLevel(entryLevel):
  ##Nivel de enegeria | Murilo

  if energyLevel >= 70 and energyLevel <= 100:
    return "Energia suficiente para decolagem"
  
  elif energyLevel <= 40 and energyLevel <= 69:
    return "Energia baixa"

  elif entryLevel < 40:
    return "Energia insuficiente para decolagem"

def calculatepressure(pressure):
    if pressure < 3.5 or pressure > 6.5:
        return "CRITICO"
    elif (3.5 <= pressure <= 3.9) or (5.6 <= pressure <= 6.0):
        return "ALERTA"
    elif 4.0 <= pressure <= 5.5:
        return "OPERACIONAL"
    else:
        return "ALERTA"

def modulestatus(status):
 #STATUS DOS MÓDULOS
  if status == "Ok":
    print("Modulos Funcionando")
  else:
    print("Falha")



def launchVerify(internTemperature, externalTemperature, energyLevel, ressure,status ):


  calculateInternalTemperature(internTemperature)

  calculateEntryLevel(energyLevel)

  calculatepressure(pressure)

  modulestatus(status)

  
 
launchVerify(internTemperature, externalTemperature, energyLevel, pressure, status)   
        









