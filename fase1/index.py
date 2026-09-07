"""
1. TEMPERATURA INTERNA (internal_temperature)
✅ Operacional: -40°C a +50°C
⚠️ Alerta: 50°C a 70°C
🚨 Crítico: > 70°C
📌 Ideal: 20°C a 25°C

2. TEMPERATURA EXTERNA (external_temperature)
✅ Operacional: -50°C a +60°C
⚠️ Alerta: -50°C ou > 60°C
🚨 Crítico: < -60°C ou > 80°C
📌 Ideal: 0°C a 30°C (condições de solo)

3. NÍVEL DE ENERGIA (energy_level)
✅ Operacional: 70% a 100%
⚠️ Alerta: 40% a 69%
🚨 Crítico: < 40%
📌 Necessário para decolagem: ≥ 95%

4. PRESSÃO DO TANQUE (pressure_value)
✅ Operacional: 4.0 a 5.5 bar
⚠️ Alerta: 3.5 a 3.9 bar ou 5.6 a 6.0 bar
🚨 Crítico: < 3.5 bar ou > 6.5 bar
📌 Ideal: 4.5 bar


5. STATUS DOS MÓDULOS CRÍTICOS (module_status)
✅ "OK" ou "OPERACIONAL"
🚨 "FALHA" ou "CRÍTICO"
"""

USE_COLORS = True


class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'


def colorize(text, color):
    if USE_COLORS:
        return f"{color}{text}{Colors.RESET}"
    return text


def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Erro: Digite um valor numérico válido.")


def get_status_input(prompt):
    while True:
        status = input(prompt).lower().strip()
        if status in ["ok", "falha", "operacional", "critico"]:
            return status
        print("Erro: Digite 'ok', 'falha', 'operacional' ou 'critico'.")


def get_integrity_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value in [0, 1]:
                return value
            print("Erro: Digite 0 (comprometida) ou 1 (íntegra).")
        except ValueError:
            print("Erro: Digite 0 ou 1.")


def get_system_inputs():
    internal_temperature = get_float_input("Digite a temperatura interna (°C): ")
    external_temperature = get_float_input("Digite a temperatura externa (°C): ")
    structural_integrity = get_integrity_input("Digite a integridade estrutural (0/1): ")
    energy_level = get_float_input("Digite o nível de energia (%): ")
    pressure_value = get_float_input("Digite a pressão do tanque (bar): ")
    module_status = get_status_input("Digite o status dos módulos críticos (ok/falha): ")
    return internal_temperature, external_temperature, structural_integrity, energy_level, pressure_value, module_status


internal_temperature, external_temperature, structural_integrity, energy_level, pressure_value, module_status = get_system_inputs()


def calculate_internal_temperature(internal):
    if internal > 70:
        return "Temperatura interna: CRÍTICA", "critico"
    elif 50 <= internal <= 70:
        return "Temperatura interna: ALERTA", "alerta"
    elif 20 <= internal <= 25:
        return "Temperatura interna: IDEAL", "ok"
    elif -40 <= internal <= 50:
        return "Temperatura interna: OPERACIONAL", "ok"
    else:
        return "Temperatura interna: FORA DA FAIXA", "critico"


def calculate_external_temperature(external):
    if external < -60 or external > 80:
        return "Temperatura externa: CRÍTICA", "critico"
    elif external < -50 or external > 60:
        return "Temperatura externa: ALERTA", "alerta"
    elif 0 <= external <= 30:
        return "Temperatura externa: IDEAL", "ok"
    elif -50 <= external <= 60:
        return "Temperatura externa: OPERACIONAL", "ok"
    else:
        return "Temperatura externa: FORA DA FAIXA", "critico"


def calculate_energy_level(energy):
    if energy < 40:
        return "Energia: CRÍTICA", "critico"
    elif 40 <= energy < 70:
        return "Energia: ALERTA", "alerta"
    elif energy < 95:
        return "Energia: OPERACIONAL", "ok"
    else:
        return "Energia: PRONTA PARA DECOLAGEM", "ok"


def calculate_pressure(pressure_val):
    if pressure_val < 3.5 or pressure_val > 6.5:
        return "Pressão: CRÍTICA", "critico"
    elif (3.5 <= pressure_val <= 3.9) or (5.6 <= pressure_val <= 6.0):
        return "Pressão: ALERTA", "alerta"
    elif 4.0 <= pressure_val <= 5.5:
        return "Pressão: OPERACIONAL", "ok"
    else:
        return "Pressão: ALERTA", "alerta"


def check_structural_integrity(integrity):
    if integrity == 1:
        return "Integridade estrutural: ÍNTEGRA", "ok"
    else:
        return "Integridade estrutural: COMPROMETIDA", "critico"


def check_module_status(status):
    if status.lower() in ["ok", "operacional"]:
        return "Módulos: FUNCIONANDO", "ok"
    else:
        return "Módulos: FALHA", "critico"


def verify_launch(internal_temp, external_temp, integrity, energy, pressure_val, module_status):
    results = []
    
    msg_temp, status_temp = calculate_internal_temperature(internal_temp)
    results.append((msg_temp, status_temp))
    
    msg_ext_temp, status_ext_temp = calculate_external_temperature(external_temp)
    results.append((msg_ext_temp, status_ext_temp))
    
    msg_integrity, status_integrity = check_structural_integrity(integrity)
    results.append((msg_integrity, status_integrity))
    
    msg_energy, status_energy = calculate_energy_level(energy)
    results.append((msg_energy, status_energy))
    
    msg_pressure, status_pressure = calculate_pressure(pressure_val)
    results.append((msg_pressure, status_pressure))
    
    msg_modules, status_modules = check_module_status(module_status)
    results.append((msg_modules, status_modules))
    
    print("\n=== DIAGNÓSTICO DO SISTEMA ===")
    for msg, status in results:
        if status == "critico":
            print(colorize(msg, Colors.RED))
        elif status == "alerta":
            print(colorize(msg, Colors.YELLOW))
        else:
            print(colorize(msg, Colors.GREEN))
    
    has_critical = any(status == "critico" for _, status in results)
    has_alert = any(status == "alerta" for _, status in results)
    
    print("\n=== RESULTADO FINAL ===")
    if has_critical:
        result_msg = "DECOLAGEM ABORTADA - Sistema em estado crítico"
        print(colorize(result_msg, Colors.RED))
        return False
    elif has_alert and energy < 95:
        result_msg = "DECOLAGEM ABORTADA - Alertas detectados e energia insuficiente"
        print(colorize(result_msg, Colors.RED))
        return False
    else:
        result_msg = "PRONTO PARA DECOLAR - Todos os sistemas operacionais"
        print(colorize(result_msg, Colors.GREEN))
        return True


verify_launch(internal_temperature, external_temperature, structural_integrity, energy_level, pressure_value, module_status)
