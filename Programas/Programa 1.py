import os
import time

class InfoProceso:
    def __init__(self, nombreProgramador, operador, tiempoMaximo, numeroPrograma, num1, num2):
        self.nombreProgramador = nombreProgramador
        self.operador = operador
        self.tiempoMaximo = tiempoMaximo
        self.numeroPrograma = numeroPrograma
        self.num1 = num1
        self.num2 = num2
        self.resultado = None
        self.tiempoEjecutado = 0

class ProcesamientoPorLotes:
    MAX = 5
    lote = []

    @staticmethod
    def main():
        numProcesos = int(input("Dame el número de procesos: "))
        ProcesamientoPorLotes.capturar_informacion(numProcesos)

    @staticmethod
    def capturar_informacion(numProcesos):
        for _ in range(numProcesos):
            os.system("cls")
            nombre = input("Dame Nombre de Programador: ")
            operador = ''
            op_valido = False
            while not op_valido:
                operador = input("Dame la Operacion (+, -, *, /): ")
                op_valido = ProcesamientoPorLotes.validar_operador(operador)
                if not op_valido:
                    print("Operador no válido. Introducir dato nuevamente.")

            tiempo_valido = False
            while not tiempo_valido:
                tiempo = int(input("Dame el tiempo maximo estimado: "))
                tiempo_valido = ProcesamientoPorLotes.validar_tiempo(tiempo)
                if not tiempo_valido:
                    print("Tiempo invalido (debe ser mayor a 0). Introducir dato nuevamente.")

            id_repetido = False
            while not id_repetido:
                numero = int(input("Dame el numero de programa: "))
                id_repetido = ProcesamientoPorLotes.verificar_id(numero)
                if not id_repetido:
                    print("El número de programa ya está en uso. Introducir dato nuevamente.")

            num1 = int(input("Dame el numero1: "))
            num2 = int(input("Dame el numero2: "))

            proceso = InfoProceso(nombre, operador, tiempo, numero, num1, num2)
            ProcesamientoPorLotes.lote.append(proceso)

    @staticmethod
    def verificar_id(numero):
        for proceso in ProcesamientoPorLotes.lote:
            if proceso.numeroPrograma == numero:
                return False
        return True

    @staticmethod
    def validar_operador(op):
        return op in ['+', '-', '*', '/']

    @staticmethod
    def validar_tiempo(tiempo):
        return tiempo > 0

    @staticmethod
    def ejecutar_lotes():
        while ProcesamientoPorLotes.lote:
            
            os.system ("cls")
            proceso_actual = ProcesamientoPorLotes.lote.pop(0)
            print("\nLote en Ejecución: 1")
            print("---------------------------------------------------")
            print(f"Numero de programa ID: {proceso_actual.numeroPrograma}")
            print()
            print(f"Tiempo Máximo Estimado: {proceso_actual.tiempoMaximo}")
            print()
            tiempo_restante = proceso_actual.tiempoMaximo - proceso_actual.tiempoEjecutado
            print("\nProceso en Ejecución:")
            print()
            print(f"Nombre de Programador: {proceso_actual.nombreProgramador}")
            print()
            print(f"Operación:  {proceso_actual.num1}{proceso_actual.operador} {proceso_actual.num2}")
            print()
            print(f"Tiempo transcurrido en ejecución: {proceso_actual.tiempoEjecutado}")
            print()
            print(f"Tiempo restante por ejecutar: {tiempo_restante}")
            print()

            if proceso_actual.operador == '+':
                resultado = proceso_actual.num1 + proceso_actual.num2
            elif proceso_actual.operador == '-':
                resultado = proceso_actual.num1 - proceso_actual.num2
            elif proceso_actual.operador == '*':
                resultado = proceso_actual.num1 * proceso_actual.num2
            elif proceso_actual.operador == '/':
                resultado = proceso_actual.num1 / proceso_actual.num2
            proceso_actual.resultado = resultado

            print("\nProceso Terminado")
            print()
            print(f"Número de Programa: {proceso_actual.numeroPrograma}")
            print()
            print(f"Operación y datos: {proceso_actual.operador} {proceso_actual.num1} {proceso_actual.num2}")
            print()
            print(f"Resultado de la operación: {proceso_actual.resultado}")
            print()
            time.sleep(3)
    @staticmethod
    def iniciar():
        ProcesamientoPorLotes.main()
        ProcesamientoPorLotes.ejecutar_lotes()

if __name__ == "__main__":
    ProcesamientoPorLotes.iniciar()
