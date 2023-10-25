import math
import copy
import pygame
import time

#Clase nodo que representa al estado
class nodo:

    def __init__(self, estado, costo_g, costo_h, padre):
        self.estado = estado#representa el estado en listas
        self.costo_g = costo_g#costo de llegar a este nodo desde el nodo inicial
        self.costo_h = costo_h#costo para llegar al nodo objetivo
        self.costo_f = costo_g+costo_h#costo acumulativo,suma de ambos costos
        self.padre = padre#nodo que se usó para llegar a este nodo
    #sobrecarga de metodo lt, se utiliza para comparar dos nodos y determinar cuál tiene el menor costo_f.
    def __lt__(self, other):
        return self.costo_f < other.costo_f
    #sobrecarga de metodo eq, se utiliza para comparar dos nodos y determinar si tienen el mismo estado.
    def __eq__(self, other):
        return self.estado == other.estado
"""
Función vectorAcum
Descripción: calcula la suma de los elementos en cada torre del estado actual 
    y del estado objetivo, para que se pueda usar la distancia euclidiana entre estos vectores para estimar el costo h.
Recibe: torres, representa el estado en listas
Devuleve: vectores que contiene la suma de los tamaños de los discos
"""
def vectorAcum(torres):
    vector = []
    for torre in torres:
        vector.append(sum(torre))
    return vector
"""
Función Asterico
Descripcion: Realiza la buqueda A*
Recibe: El estado inicial y el estado objetivo
Devuelve: La trayectoria de la solucion
"""
def Asterisco(raiz, objetivo):
    candidatos = []#Lista de estados candidatos, frontera
    explorados = []#lista de estados explorados
    
    #Se crea el nodo inicial, con el estado inicial
    nodo_inicial=nodo(raiz, 0, distancia(vectorAcum(raiz),vectorAcum(objetivo)),None)
    #Se añade el nodo inicial a lista de candidatos
    candidatos.append(nodo_inicial)
    
    #Mientras haya estados candidatos
    while candidatos:
        #Ordenamos los estados candidatos por el costo
        candidatos.sort(key=lambda estado: estado.costo_f)
        #Sacamos el estado con menor costo para revisar
        revisado=candidatos.pop(0)

        #se prueba si el estado a revisar es el estado objetivo
        if revisado.estado == objetivo:
            optimo = []#Se guardara el camino optimo
            #Mientras revisado sea diferente de null, entonce aun se ha llegado al estado inicial
            while revisado:
                #Se van agregando los estados que permitieron llegar al estado objetivo
                optimo.append(revisado.estado)
                #se va al estado que genero el estado
                revisado = revisado.padre 
            #Se devuelve la trayectoria
            return optimo[::-1]
        #Se agrega a explorados el nodo que revisamos
        explorados.append(revisado)

        #Generamos los sucesores del estado a revisar
        sucesores=funcionSucesor(revisado.estado)
        #Para cada sucesor, calculamos los costos g y h
        for sucesor in sucesores:
            costo_g = revisado.costo_g + 1
            costo_h = distancia(vectorAcum(sucesor), vectorAcum(objetivo))
            #Generamos el nodo del sucesor
            nodo_sucesor = nodo(sucesor, costo_g, costo_h, revisado)
            
            if nodo_sucesor not in explorados:
                if nodo_sucesor not in candidatos:
                    candidatos.append(nodo_sucesor)
                else:
                    # Si el nodo sucesor ya está en la lista candidatos, se compara el costo_g del nodo actual con el costo_g del nodo en la lista abierta
                    for i, n in enumerate(candidatos):
                        if n == nodo_sucesor and n.costo_f > nodo_sucesor.costo_f:
                            # Si el costo_g del nodo en la lista candidatos es mayor al costo_g
                            # del nodo siguiente, se reemplaza el nodo en la lista candidatos
                            # con el nodo siguiente
                            candidatos[i] = nodo_sucesor
        
    
"""
Función Heuritica
Descripción: calcula la distancia euclidiana entre un estado y el estado objetivo

Recibe: estado a evaluar y estado objetivo
Devuleve: distancia resultante, valor heuristico
"""
def distancia(vector1, vector2):
    return math.sqrt((vector1[0]-vector2[0])**2 + (vector1[1]-vector2[1])**2 + (vector1[2]-vector2[2])**2)

"""
Operadores

Descripción:Implementan los movimientos permitidos en el juego de las Torres de Hanoi. 
            Cada función recibe el estado actual y devuelve el siguiente estado generado al mover un disco de una torre a otra. 
            Si un movimiento no es posible, se devuelve None.
Recibe: estado a evaluar 
Devuleve: estado sucersor o nada, dependiendo si el movimiento es valido
"""
def moverAtoB(estado):
    if len(estado[0]) != 0:
        sucesor = estado.copy()
        if len(estado[1]) != 0:
            if estado[0][-1] < estado[1][-1]:
                sucesor[1].append(sucesor[0].pop())
                return sucesor
            else:
                return None
        else:
            sucesor[1].append(sucesor[0].pop())
            return sucesor
    return None

def moverAtoC(estado):
    if len(estado[0]) != 0:
        sucesor = estado.copy()
        if len(estado[2]) != 0:
            if estado[0][-1] < estado[2][-1]:
                sucesor[2].append(sucesor[0].pop())
                return sucesor
            else:
                return None
        else:
            sucesor[2].append(sucesor[0].pop())
            return sucesor
    return None

def moverBtoA(estado):
    if len(estado[1]) != 0:
        sucesor = estado.copy()
        if len(estado[0]) != 0:
            if estado[1][-1] < estado[0][-1]:
                sucesor[0].append(sucesor[1].pop())
                return sucesor
            else:
                return None
        else:
            sucesor[0].append(sucesor[1].pop())
            return sucesor
    return None

def moverBtoC(estado):
    if len(estado[1]) != 0:
        sucesor = estado.copy()
        if len(estado[2]) != 0:
            if estado[1][-1] < estado[2][-1]:
                sucesor[2].append(sucesor[1].pop())
                return sucesor
            else:
                return None
        else:
            sucesor[2].append(sucesor[1].pop())
            return sucesor
    return None

def moverCtoA(estado):
    if len(estado[2]) != 0:
        sucesor = estado.copy()
        if len(estado[0]) != 0:
            if estado[2][-1] < estado[0][-1]:
                sucesor[0].append(sucesor[2].pop())
                return sucesor
            else:
                return None
        else:
            sucesor[0].append(sucesor[2].pop())
            return sucesor
    return None

def moverCtoB(estado):
    if len(estado[2]) != 0:
        sucesor = estado.copy()
        if len(estado[1]) != 0:
            if estado[2][-1] < estado[1][-1]:
                sucesor[1].append(sucesor[2].pop())
                return sucesor
            else:
                return None
        else:
            sucesor[1].append(sucesor[2].pop())
            return sucesor
    return None

"""
Función Sucesor
Descripción: Aplica los operadores y genera una lista de sucesores
Recibe: estado a generar sucesores
Devuleve: lista de sucesores
"""
def funcionSucesor(estado):
    sucesores = []#lista donde se guardan los sucersores
    #Se van aplicar los 6 operadoees, si genra un sucesor se guarda en la lista de sucesores
    sucesor = moverAtoB(copy.deepcopy(estado))
    if sucesor != None:
        sucesores.append(sucesor)
        #print("AtoB: ", sucesor)
    
    sucesor = moverAtoC(copy.deepcopy(estado))
    if sucesor != None:
        sucesores.append(sucesor)
        #print("AtoC: ", sucesor)
    
    sucesor = moverBtoA(copy.deepcopy(estado))
    if sucesor != None:
        sucesores.append(sucesor)
        #print("BtoA: ", sucesor)
    
    sucesor = moverBtoC(copy.deepcopy(estado))
    if sucesor != None:
        sucesores.append(sucesor)
        #print("BtoC: ", sucesor)
    
    sucesor = moverCtoA(copy.deepcopy(estado))
    if sucesor != None:
        sucesores.append(sucesor)
        #print("CtoA: ", sucesor)
    
    sucesor = moverCtoB(copy.deepcopy(estado))
    if sucesor != None:
        sucesores.append(sucesor)
        #print("CtoB: ", sucesor)

    return sucesores #devuelve la lista de sucesores


"""
Función animacion
Descripción: A partir de la trayectoria encontrada, se muestra una animacion donde se ven los movimientos (estados) 
            que se realizan para llegar a la solucion
Recibe: Trayectoria de la solucion
Devuleve: ------
"""    
def animacion(trayectoria):
    # se ajusta la longitud de las listas en "trayectoria" para que todas tengan la misma longitud
    for i in range(0,len(trayectoria)):
        for k in range(0,3):
            if(len(trayectoria[i][k])!=len(trayectoria[0][0])):
                for l in range(0,(len(trayectoria[0][0])-len(trayectoria[i][k]))):
                    trayectoria[i][k].append(0)
    n1=len(trayectoria)
    n2=len(trayectoria[0][0])
    CAFE = (218, 142, 84)
    pygame.init()
    Dimensiones = (1220,500)
    Pantalla = pygame.display.set_mode(Dimensiones)
    pygame.display.set_caption("Torres de Hanoi")
    Terminar = False
    #Se define para poder gestionar cada cuando se ejecuta un fotograma
    reloj = pygame.time.Clock()
    #Se manejan los eventos del juego y se actualiza la pantalla con los dibujos de las torres y los discos.
    while not Terminar:
        #---Manejo de eventos
        for Evento in pygame.event.get():
            if Evento.type == pygame.QUIT:
                Terminar = True
        #---La lógica del juego
        #---Código de dibujo----
        anchodisco=300
        deltaposx=(anchodisco/n2)/2
        deltamx=anchodisco/n2
        tamy=50
        for j in range(0,n1):
            Pantalla.fill((255,255,255))
            pygame.draw.line(Pantalla, CAFE, (10, 450), (1210, 450), 10)
            pygame.draw.line(Pantalla, CAFE, (210, 450), (210, 100), 10)
            pygame.draw.line(Pantalla, CAFE, (610, 450), (610, 100), 10)
            pygame.draw.line(Pantalla, CAFE, (1010, 450), (1010, 100), 10)
            for i in range(0,n2):
                posx=210-(deltaposx*trayectoria[j][0][i])
                posy=400-(i*50)
                tamx=deltamx*trayectoria[j][0][i]
                pygame.draw.rect(Pantalla, (118, 193, 231), [posx, posy, tamx, tamy], 7)
            for i in range(0,n2):
                posx=610-(deltaposx*trayectoria[j][1][i])
                posy=400-(i*50)
                tamx=deltamx*trayectoria[j][1][i]
                pygame.draw.rect(Pantalla, (118, 193, 231), [posx, posy, tamx, tamy], 7)
            for i in range(0,n2):
                posx=1010-(deltaposx*trayectoria[j][2][i])
                posy=400-(i*50)
                tamx=deltamx*trayectoria[j][2][i]
                pygame.draw.rect(Pantalla, (118, 193, 231), [posx, posy, tamx, tamy], 7)
            time.sleep(1)
            
            #--Todos los dibujos van antes de esta línea
            pygame.display.flip()
            reloj.tick(20)  # Limitamos a 20 fotogramas por segundo
    pygame.quit()

#numero de discos
n = 6
#Se inicializa el nodo inicial y obetivo a partir del numero de disco
raiz = [list(range(n, 0, -1)),[],[]]
objetivo = [[],[],list(range(n, 0, -1))]

#Mandamos a llamar la busqeuda A*
trayecto = Asterisco(raiz, objetivo)
#Se muestran los movimientos realidos
print(f"\n\nMovimientos minimos: {len(trayecto) - 1}")
#Mostramos la solucion encontrada
print("El trayecto es: ", trayecto)
#Mostramos la animacion de la solucion
animacion(trayecto)





