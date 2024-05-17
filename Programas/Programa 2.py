"""
Programa 2. Simular el procesamiento por lotes con Multiprogramación.
Alumno: Jessica Alexandra Magaña Salcedo
Código: 215616229
"""



import os
import time
import random
from pynput import keyboard as kb

class Proceso:
    def __init__(self):
        self.operacion = ""
        self.numero1 = 0
        self.numero2 = 0
        self.tiempo_maximo = 0
        self.id_programa = 0
        self.resultado_operacion = 0
        self.cadena_operacion = ""

def funcionOperacion(operador, proceso):
    proceso.numero1 = random.randint(1, 100)
    proceso.numero2 = random.randint(1, 100)
    proceso.cadena_operacion = f"{proceso.numero1} {operador} {proceso.numero2}"
    proceso.resultado_operacion = eval(proceso.cadena_operacion)

tecla2 = ""
lista_lotes = []  # [[lote],[lote]] -> lote: [proc, proc, proc, proc]
lotes = []
procesos = []  # [Op, Res, TME, ID, TT]
listaAux = []
proc_terminados = []  # [[id, op, res, lote]]
operador = ['+', '-', '*', '/', '%']

contador_global = 0
contadorTiempoTrascurrido = 0
contador_procesos = 0
id_operacion = 1
error = False

def pulsa2(letra):
    if letra == kb.KeyCode.from_char('c'):
        return False

def pulsa(tecla):
    global tecla2
    tecla2 = ""
    tecla2 = tecla
    return tecla2

cantidad = int(input("Ingrese la cantidad de procesos a realizar: "))

while contador_procesos < cantidad:
    proceso = Proceso()

    while True:
        proceso.operacion = random.choice(operador)
        
        if proceso.operacion in ['+', '-', '*', '%']:
            funcionOperacion(proceso.operacion, proceso)
            break
        elif proceso.operacion == '/':
            proceso.numero1 = random.randint(1, 100)
            proceso.numero2 = random.randint(1, 100)
            
            while proceso.numero2 == 0:
                proceso.numero2 = random.randint(1, 100)

            proceso.cadena_operacion = f"{proceso.numero1} / {proceso.numero2}"
            proceso.resultado_operacion = proceso.numero1 / proceso.numero2
            break

    proceso.tiempo_maximo = random.randint(5, 20)
    proceso.id_programa = id_operacion
    id_operacion += 1

    tiempo_transcurrido = 0

    procesos.extend([
        proceso.operacion,
        proceso.resultado_operacion,
        proceso.tiempo_maximo,
        proceso.id_programa,
        tiempo_transcurrido
    ])

    lotes.append(procesos)
    procesos = []
    contador_procesos += 1

if len(lotes) % 4 == 0:
    indexI = 0
    indexF = 4

    for proc in range(len(lotes) // 4):
        lista_lotes.append(lotes[indexI:indexF])
        indexI += 4
        indexF += 4

if len(lotes) % 4 != 0:
    indexI = 0
    indexF = 4

    if len(lotes) < 4:
        lista_lotes.append(lotes[indexI:len(lotes)])
    else:    
        for proc in range(len(lotes) // 4):
            lista_lotes.append(lotes[indexI:indexF])
            indexI += 4
            indexF += 4

        indexF -= 4
        for proc in range(len(lotes) % 4):
            listaAux.append(lotes[indexF+proc])

        lista_lotes.append(listaAux)

os.system("pause")

i = 0
longitudLista = len(lista_lotes)

while i < longitudLista:
    j = 0
    longitudProcesos = len(lista_lotes[i])
    
    while j < longitudProcesos:
        contadorTiempoTrascurrido = 0
        tiempoRestante = 1

        while tiempoRestante >= 0:          
            tiempoRestante = lista_lotes[i][j][2] - lista_lotes[i][j][4]
            contadorTiempoTrascurrido = lista_lotes[i][j][4]

            os.system("cls")      

            print('----------Contador Global----------')
            print(contador_global)

            print('----Cantidad de lotes pendientes---')
            print(len(lista_lotes) - (i+1))

            print('------------Lote Actual------------')
            
            for k in range(j+1, len(lista_lotes[i])):    
                print('ID: {} Tiempo maximo estimado: {} TT: {}'.format(lista_lotes[i][k][3], lista_lotes[i][k][2], lista_lotes[i][k][4]), end=' |') 

            print('\n-------Proceso en Ejecucion--------')
            print("Operacion: {} \nTT: {} \nId: {} \nTiempo trascurrido: {} \nTiempo restante: {}".format(
                lista_lotes[i][j][0], lista_lotes[i][j][2], lista_lotes[i][j][3], contadorTiempoTrascurrido, tiempoRestante)
            )
            
            print('--------Procesos Terminados--------') 
            if len(proc_terminados) >= 0:
                for proc in range(len(proc_terminados)):                    
                    print("Id: {} \tOperacion: {} \tResultado: {} \t--> Lote: {}".format(
                        proc_terminados[proc][0], proc_terminados[proc][1], proc_terminados[proc][2], proc_terminados[proc][3])
                    ) 

            if tiempoRestante == 0:             
                listaAux = []           
                listaAux.extend([
                    lista_lotes[i][j][3],
                    lista_lotes[i][j][0],
                    lista_lotes[i][j][1],
                    i+1
                ])   
                proc_terminados.append(listaAux)
                print("Id: {} \tOperacion: {} \tResultado: {} \t--> Lote: {}".format(
                    lista_lotes[i][j][3], lista_lotes[i][j][0], lista_lotes[i][j][1], i+1)
                )

            
            tiempoRestante -= 1
            contadorTiempoTrascurrido += 1
            lista_lotes[i][j][4] = contadorTiempoTrascurrido
            contador_global += 1
            time.sleep(0.3) 

            escuchador = kb.Listener(pulsa)
            escuchador.start()

            if tecla2 == kb.KeyCode.from_char('i'):  
                procesoActual = lista_lotes[i][j]
                procesoActual[4] = contadorTiempoTrascurrido-1
                del lista_lotes[i][j]
                lista_lotes[i].append(procesoActual)

            if tecla2 == kb.KeyCode.from_char('e'):
                listaAux = []           
                listaAux.extend([
                    lista_lotes[i][j][3],
                    lista_lotes[i][j][0],
                    'ERROR!',
                    i+1
                ])
                proc_terminados.append(listaAux)

                procesoActual = lista_lotes[i][j]
                if j == longitudProcesos-1:
                    if i == longitudLista-1:
                        print("Id: {} \tOperacion: {} \tResultado: {} \t--> Lote: {}".format(
                            lista_lotes[i][j][3], lista_lotes[i][j][0], 'ERROR!', i+1)
                        )
                        break
                    else:              
                        break                    
                
                else:
                    del lista_lotes[i][j]
                    longitudProcesos -= 1                
                    j = 0
                    
                
            if tecla2 == kb.KeyCode.from_char('p'):                
                print("\n\tTeclea 'c' para continuar...")

                with kb.Listener(pulsa2) as escucha:
                    escucha.join()

            tecla2 = ''
            letra = ''

        j += 1

    tecla2 = ''
    i += 1

