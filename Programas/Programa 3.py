import random
import time
import os
from pynput import keyboard as kb

# Constantes para representar los estados
NUEVO = 0
LISTO = 1
EJECUCION = 2
BLOQUEADO = 3
TERMINADO = 4

procesos = []
cola_nuevos = []
cola_listos = []
cola_bloqueados = []
proceso_en_ejecucion = None
programa_pausado = False
tiempo_inicial = time.time()

# Clase para representar un proceso
class Proceso:
    def __init__(self, pid, tiempo_maximo_estimado, datos_operacion):
        self.pid = pid
        self.tiempo_maximo_estimado = tiempo_maximo_estimado
        self.tiempo_transcurrido = 0
        self.datos_operacion = datos_operacion
        self.estado = NUEVO
        self.resultado = None
        self.operador = None
        self.operando1 = None
        self.operando2 = None

# Función para generar procesos
def generar_procesos(n):
    for i in range(n):
        tiempo_maximo_estimado = random.randint(5, 18)
        operador = random.choice(['+', '-', '*', '/'])
        operando1 = random.randint(1, 100)
        operando2 = random.randint(1, 100)
        datos_operacion = f"{operando1} {operador} {operando2}"
        proceso = Proceso(i + 1, tiempo_maximo_estimado, datos_operacion)
        cola_nuevos.append(proceso)

# Función para manejar la entrada E
def interrupcion_entrada_salida():
    global proceso_en_ejecucion
    if proceso_en_ejecucion:
        proceso_en_ejecucion.estado = BLOQUEADO
        proceso_en_ejecucion = None
        tiempo_bloqueo = 8
        proceso_bloqueado = cola_bloqueados[-1]  # El último proceso agregado a la cola de bloqueados
        proceso_bloqueado.tiempo_transcurrido = tiempo_bloqueo
        mostrar_procesos(0)

# Función para mover procesos de la cola de bloqueados a la cola de listos
def mover_bloqueado_a_listo():
    if cola_bloqueados:
        proceso = cola_bloqueados.pop(0)
        proceso.estado = LISTO
        cola_listos.append(proceso)

# Función para manejar la entrada W
def error_proceso():
    global proceso_en_ejecucion
    if proceso_en_ejecucion:
        proceso_en_ejecucion.estado = TERMINADO
        proceso_en_ejecucion.resultado = "Error"
        procesos.append(proceso_en_ejecucion)  # Agregar el proceso a la lista de procesos terminados
        proceso_en_ejecucion = None

# Función para mostrar los procesos en pantalla
def mostrar_procesos(tiempo):
    os.system("cls" if os.name == "nt" else "clear")
    print("Procesos nuevos:", len(cola_nuevos))
    print("\nProcesos listos:")
    for proceso in cola_listos:
        print("ID:", proceso.pid)
        print("TME (Tiempo Máximo Estimado):", proceso.tiempo_maximo_estimado)
        print("TT (Tiempo transcurrido):", proceso.tiempo_transcurrido)
        print()
    print("\nProceso en Ejecución:")
    if proceso_en_ejecucion:
        print("ID:", proceso_en_ejecucion.pid)
        print("Operación:", proceso_en_ejecucion.datos_operacion)
        print("TME (Tiempo Máximo Estimado):", proceso_en_ejecucion.tiempo_maximo_estimado)
        print("TT (Tiempo transcurrido):", proceso_en_ejecucion.tiempo_transcurrido)
        if proceso_en_ejecucion.resultado:
            print("Resultado:", proceso_en_ejecucion.resultado)
        print("TR (Tiempo restante por ejecutar):", proceso_en_ejecucion.tiempo_maximo_estimado - proceso_en_ejecucion.tiempo_transcurrido)
        print()
    print("\nTerminados:")
    for proceso in procesos:
        print("ID:", proceso.pid)
        print("Operación:", proceso.datos_operacion)
        print("Respuesta:", proceso.resultado if proceso.resultado else "Normal")
        print()
    print("\nBloqueados:")
    for proceso in cola_bloqueados:
        print("ID:", proceso.pid)
        print("TTB (Tiempo transcurrido en bloqueados):", proceso.tiempo_transcurrido)
        print()
    print("\nContador general:", tiempo)

# Función para calcular los tiempos de los procesos
def calcular_tiempos(procesos):
    for proceso in procesos:
        proceso.tiempo_finalizacion = tiempo_inicial + proceso.tiempo_transcurrido
        proceso.tiempo_retorno = proceso.tiempo_finalizacion - proceso.tiempo_llegada
        proceso.tiempo_respuesta = proceso.tiempo_llegada - tiempo_inicial
        proceso.tiempo_espera = proceso.tiempo_retorno - proceso.tiempo_servicio
        proceso.tiempo_servicio = proceso.tiempo_transcurrido if proceso.resultado != "Error" else proceso.tiempo_maximo_estimado

# Función para mostrar los tiempos de los procesos al finalizar
def mostrar_tiempos_finales(procesos):
    print("\nTiempos finales de los procesos:")
    for proceso in procesos:
        print("ID:", proceso.pid)
        print("Tiempo de Llegada:", proceso.tiempo_llegada)
        print("Tiempo de Finalización:", proceso.tiempo_finalizacion)
        print("Tiempo de Retorno:", proceso.tiempo_retorno)
        print("Tiempo de Respuesta:", proceso.tiempo_respuesta)
        print("Tiempo de Espera:", proceso.tiempo_espera)
        print("Tiempo de Servicio:", proceso.tiempo_servicio)
        print()

# Función para ejecutar los procesos
def ejecutar_procesos():
    global proceso_en_ejecucion
    global programa_pausado
    tiempo_transcurrido = 0
    programa_pausado = False
    while cola_listos or proceso_en_ejecucion or cola_nuevos:
        if not programa_pausado:
            if cola_nuevos:
                proceso = cola_nuevos.pop(0)
                proceso.estado = LISTO
                proceso.tiempo_llegada = time.time() - tiempo_inicial
                # Analizar la operación para obtener operandos y operador
                operacion = proceso.datos_operacion.split()
                operando1 = int(operacion[0])
                operando2 = int(operacion[2])
                operador = operacion[1]
                proceso.operando1 = operando1
                proceso.operando2 = operando2
                proceso.operador = operador
                cola_listos.append(proceso)
            if cola_listos and not proceso_en_ejecucion:
                proceso_en_ejecucion = cola_listos.pop(0)
                proceso_en_ejecucion.estado = EJECUCION
            if proceso_en_ejecucion:
                proceso_en_ejecucion.tiempo_transcurrido += 1
                if proceso_en_ejecucion.tiempo_transcurrido >= proceso_en_ejecucion.tiempo_maximo_estimado:
                    proceso_en_ejecucion.estado = TERMINADO
                    proceso_en_ejecucion.tiempo_finalizacion = time.time() - tiempo_inicial
                    procesos.append(proceso_en_ejecucion)
                    proceso_en_ejecucion = None
                elif random.random() < 0.05:  # Simulación de E/S con probabilidad del 5%
                    proceso_en_ejecucion.estado = BLOQUEADO
                    cola_bloqueados.append(proceso_en_ejecucion)
                    proceso_en_ejecucion = None
                    mover_bloqueado_a_listo()
                else:
                    # Realizar operación aritmética
                    resultado = None
                    try:
                        if proceso_en_ejecucion.operador == '+':
                            resultado = proceso_en_ejecucion.operando1 + proceso_en_ejecucion.operando2
                        elif proceso_en_ejecucion.operador == '-':
                            resultado = proceso_en_ejecucion.operando1 - proceso_en_ejecucion.operando2
                        elif proceso_en_ejecucion.operador == '*':
                            resultado = proceso_en_ejecucion.operando1 * proceso_en_ejecucion.operando2
                        elif proceso_en_ejecucion.operador == '/':
                            resultado = proceso_en_ejecucion.operando1 / proceso_en_ejecucion.operando2
                        proceso_en_ejecucion.resultado = resultado
                    except ZeroDivisionError:
                        proceso_en_ejecucion.resultado = "Error: División por cero"
            mostrar_procesos(tiempo_transcurrido)
            time.sleep(1)
            tiempo_transcurrido += 1
        else:
            time.sleep(0.1)  # Espera corta para evitar consumo excesivo de CPU

# Función principal
def main():
    n = int(input("Ingrese el número de procesos: "))
    generar_procesos(n)
    ejecutar_procesos()
    calcular_tiempos(procesos)
    mostrar_tiempos_finales(procesos)

# Oyente de teclado
def on_press(key):
    try:
        if key.char == 'e':
            interrupcion_entrada_salida()
        elif key.char == 'w':
            error_proceso()
        elif key.char == 'p':
            pausar_programa()
        elif key.char == 'c':
            continuar_programa()
    except AttributeError:
        pass

def pausar_programa():
    global programa_pausado
    programa_pausado = True

def continuar_programa():
    global programa_pausado
    programa_pausado = False

# Configuración del oyente de teclado
listener = kb.Listener(on_press=on_press)
listener.start()

if __name__ == "__main__":
    main()