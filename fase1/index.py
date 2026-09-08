"""
faixas seguras da missao Aurora usadas na verificacao pre-decolagem

temperatura interna: ok de -40 a 50, alerta de 50 a 70, critico acima de 70
temperatura externa: ok de -50 a 60, alerta de 60 a 80, critico fora de -60 a 80
energia: ok a partir de 95%, alerta de 40 a 94, critico abaixo de 40
pressao: ok de 4.0 a 5.5 bar, alerta de 3.5 a 3.9 e de 5.6 a 6.5, critico fora disso
integridade estrutural: 1 passa, 0 aborta
modulos criticos: ok ou operacional passa, o resto aborta
"""

USE_COLORS = True

# numeros de energia da orion da NASA
BATTERY_CAPACITY_KWH = 14.4    # 4 baterias de 3.6 kwh cada
LAUNCH_CONSUMPTION_KWH = 3.0   # gasto da subida ate abrir os paineis solares
ENERGY_LOSS_RATE = 0.10        # perda de conversao e cabo
CRUISE_CONSUMPTION_KW = 1.2
RESERVE_RATE = 0.20            # nao deixa descarregar tudo


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


def get_percentage_input(prompt):
    # carga de bateria so faz sentido de 0 a 100
    while True:
        value = get_float_input(prompt)
        if 0 <= value <= 100:
            return value
        print("Erro: O nível de energia deve estar entre 0 e 100%.")


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
    energy_level = get_percentage_input("Digite o nível de energia (%): ")
    pressure_value = get_float_input("Digite a pressão do tanque (bar): ")
    module_status = get_status_input("Digite o status dos módulos críticos (ok/falha): ")
    return internal_temperature, external_temperature, structural_integrity, energy_level, pressure_value, module_status


try:
    internal_temperature, external_temperature, structural_integrity, energy_level, pressure_value, module_status = get_system_inputs()
except (EOFError, KeyboardInterrupt):
    print("\nLeitura interrompida.")
    raise SystemExit(1)


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
        # da pra ligar tudo mas nao pra decolar
        return "Energia: ABAIXO DO MÍNIMO PARA DECOLAGEM", "alerta"
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


def calculate_energy_autonomy(energy):
    # tira as perdas, o gasto da decolagem e a reserva, o que sobra vira tempo de voo
    stored_energy = BATTERY_CAPACITY_KWH * (energy / 100)
    energy_losses = stored_energy * ENERGY_LOSS_RATE
    usable_energy = stored_energy - energy_losses
    reserve_energy = BATTERY_CAPACITY_KWH * RESERVE_RATE
    remaining_energy = usable_energy - LAUNCH_CONSUMPTION_KWH - reserve_energy

    if remaining_energy <= 0:
        autonomy_hours = 0.0
    else:
        autonomy_hours = remaining_energy / CRUISE_CONSUMPTION_KW

    return stored_energy, energy_losses, usable_energy, reserve_energy, remaining_energy, autonomy_hours


def print_energy_analysis(energy):
    stored, losses, usable, reserve, remaining, hours = calculate_energy_autonomy(energy)

    print("\n=== ANÁLISE ENERGÉTICA ===")
    print(f"Capacidade total do banco: {BATTERY_CAPACITY_KWH:.1f} kWh")
    print(f"Carga atual: {energy:.1f}%")
    print(f"Energia armazenada: {stored:.1f} kWh")
    print(f"Perdas energéticas ({ENERGY_LOSS_RATE * 100:.0f}%): -{losses:.1f} kWh")
    print(f"Energia útil: {usable:.1f} kWh")
    print(f"Consumo na decolagem: -{LAUNCH_CONSUMPTION_KWH:.1f} kWh")
    print(f"Reserva operacional ({RESERVE_RATE * 100:.0f}%): -{reserve:.1f} kWh")
    print(f"Energia disponível após a decolagem: {remaining:.1f} kWh")

    if hours <= 0:
        print(colorize("Autonomia estimada: INSUFICIENTE PARA A MISSÃO", Colors.RED))
    else:
        print(colorize(f"Autonomia estimada: {hours:.1f} horas", Colors.CYAN))

    return hours


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
    elif has_alert:
        # alerta em qualquer sistema ja segura o lancamento
        result_msg = "DECOLAGEM ABORTADA - Alertas detectados nos sistemas"
        print(colorize(result_msg, Colors.RED))
        return False
    else:
        result_msg = "PRONTO PARA DECOLAR - Todos os sistemas operacionais"
        print(colorize(result_msg, Colors.GREEN))
        return True


verify_launch(internal_temperature, external_temperature, structural_integrity, energy_level, pressure_value, module_status)

print_energy_analysis(energy_level)
