import pygame  # Importa la biblioteca Pygame para gráficos y eventos
from queue import PriorityQueue  # Importa PriorityQueue para la cola de prioridad en el algoritmo A*

# Definición de colores en formato RGB
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 255, 0)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
PURPURA = (128, 0, 128)
NARANJA = (255, 165, 0)
GRIS = (128, 128, 128)
TURQUESA = (64, 224, 208)

class Celda:  # Clase que representa una celda en la cuadrícula
    def __init__(self, fila, columna, ancho, total_filas):
        self.fila = fila  # Atributo: Fila de la celda
        self.columna = columna  # Atributo: Columna de la celda
        self.x = fila * ancho  # Atributo: Coordenada x de la celda en la ventana
        self.y = columna * ancho  # Atributo: Coordenada y de la celda en la ventana
        self.color = BLANCO  # Atributo: Color inicial de la celda (blanco)
        self.vecinos = []  # Atributo: Lista de vecinos de la celda
        self.ancho = ancho  # Atributo: Ancho de la celda
        self.total_filas = total_filas  # Atributo: Número total de filas en la cuadrícula

    def obtener_pos(self):  # Método que devuelve la posición de la celda (fila, columna)
        return self.fila, self.columna

    def esta_cerrado(self):  # Método que comprueba si la celda está cerrada (rojo)
        return self.color == ROJO

    def esta_abierto(self):  # Método que comprueba si la celda está abierta (verde)
        return self.color == VERDE

    def es_barrera(self):  # Método que comprueba si la celda es una barrera (negro)
        return self.color == NEGRO

    def es_inicio(self):  # Método que comprueba si la celda es el punto de inicio (naranja)
        return self.color == NARANJA

    def es_final(self):  # Método que comprueba si la celda es el punto final (turquesa)
        return self.color == TURQUESA

    def reiniciar(self):  # Método que restablece el color de la celda a blanco
        self.color = BLANCO

    def hacer_inicio(self):  # Método que marca la celda como el punto de inicio (naranja)
        self.color = NARANJA

    def hacer_cerrado(self):  # Método que marca la celda como cerrada (rojo)
        self.color = ROJO

    def hacer_abierto(self):  # Método que marca la celda como abierta (verde)
        self.color = VERDE

    def hacer_barrera(self):  # Método que marca la celda como una barrera (negro)
        self.color = NEGRO

    def hacer_final(self):  # Método que marca la celda como el punto final (turquesa)
        self.color = TURQUESA

    def hacer_camino(self):  # Método que marca la celda como parte del camino (púrpura)
        self.color = PURPURA

    def dibujar(self, ventana):  # Método que dibuja la celda en la ventana
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))

    def actualizar_vecinos(self, cuadricula):  # Método que actualiza la lista de vecinos de la celda
        self.vecinos = []
        if self.fila < self.total_filas - 1 and not cuadricula[self.fila + 1][self.columna].es_barrera():  # Abajo
            self.vecinos.append(cuadricula[self.fila + 1][self.columna])

        if self.fila > 0 and not cuadricula[self.fila - 1][self.columna].es_barrera():  # Arriba
            self.vecinos.append(cuadricula[self.fila - 1][self.columna])

        if self.columna < self.total_filas - 1 and not cuadricula[self.fila][self.columna + 1].es_barrera():  # Derecha
            self.vecinos.append(cuadricula[self.fila][self.columna + 1])

        if self.columna > 0 and not cuadricula[self.fila][self.columna - 1].es_barrera():  # Izquierda
            self.vecinos.append(cuadricula[self.fila][self.columna - 1])

    def __lt__(self, otro):  # Método necesario para la cola de prioridad, pero no se usa aquí
        return False

class AlgoritmoAEstrella:  # Clase que encapsula la lógica del algoritmo A*
    def __init__(self, cuadricula, inicio, final, dibujar):
        self.cuadricula = cuadricula  # Atributo: La cuadrícula de celdas
        self.inicio = inicio  # Atributo: Celda de inicio
        self.final = final  # Atributo: Celda final
        self.dibujar = dibujar  # Atributo: Función para dibujar la cuadrícula

    @staticmethod
    def h(p1, p2):  # Método estático que calcula la distancia Manhattan entre dos puntos
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

    def reconstruir_camino(self, de_donde_vino, actual):  # Método que reconstruye el camino desde el nodo final al nodo inicial
        while actual in de_donde_vino:
            actual = de_donde_vino[actual]
            actual.hacer_camino()  # Marca las celdas del camino
            self.dibujar()  # Dibuja la cuadrícula

    def ejecutar(self):  # Método que contiene la lógica principal del algoritmo A*
        contador = 0  # Contador para desempate en la cola de prioridad
        conjunto_abierto = PriorityQueue()  # Cola de prioridad para nodos abiertos
        conjunto_abierto.put((0, contador, self.inicio))  # Añade el nodo inicial a la cola
        de_donde_vino = {}  # Diccionario para reconstruir el camino
        g_score = {celda: float("inf") for fila in self.cuadricula for celda in fila}  # Inicializa g_score para todos los nodos
        g_score[self.inicio] = 0  # g_score del nodo inicial es 0
        f_score = {celda: float("inf") for fila in self.cuadricula for celda in fila}  # Inicializa f_score para todos los nodos
        f_score[self.inicio] = self.h(self.inicio.obtener_pos(), self.final.obtener_pos())  # f_score del nodo inicial

        conjunto_abierto_hash = {self.inicio}  # Conjunto para seguimiento de nodos abiertos

        while not conjunto_abierto.empty():
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()  # Maneja el evento de salida de Pygame

            actual = conjunto_abierto.get()[2]  # Obtiene el nodo con el menor f_score
            conjunto_abierto_hash.remove(actual)  # Elimina el nodo actual del conjunto de nodos abiertos

            if actual == self.final:  # Si el nodo actual es el final
                self.reconstruir_camino(de_donde_vino, self.final)  # Reconstruye el camino
                self.final.hacer_final()  # Marca el nodo final
                return True  # Termina el algoritmo

            for vecino in actual.vecinos:  # Para cada vecino del nodo actual
                temp_g_score = g_score[actual] + 1  # Calcula el g_score temporal

                if temp_g_score < g_score[vecino]:  # Si el nuevo g_score es mejor
                    de_donde_vino[vecino] = actual  # Actualiza el camino
                    g_score[vecino] = temp_g_score  # Actualiza g_score
                    f_score[vecino] = temp_g_score + self.h(vecino.obtener_pos(), self.final.obtener_pos())  # Actualiza f_score
                    if vecino not in conjunto_abierto_hash:
                        contador += 1
                        conjunto_abierto.put((f_score[vecino], contador, vecino))  # Añade el vecino a la cola de prioridad
                        conjunto_abierto_hash.add(vecino)  # Añade el vecino al conjunto de nodos abiertos
                        vecino.hacer_abierto()  # Marca el vecino como abierto

            self.dibujar()  # Dibuja la cuadrícula

            if actual != self.inicio:
                actual.hacer_cerrado()  # Marca el nodo actual como cerrado

        return False  # Si no se encuentra el camino, devuelve False

class VentanaJuego:  # Clase que maneja la ventana del juego y la interacción del usuario
    def __init__(self, ancho_ventana, filas):
        self.ancho_ventana = ancho_ventana  # Atributo: Ancho de la ventana
        self.filas = filas  # Atributo: Número de filas en la cuadrícula
        self.ventana = pygame.display.set_mode((ancho_ventana, ancho_ventana))  # Atributo: Crea la ventana Pygame
        pygame.display.set_caption("A* Path Finding Algorithm")  # Establece el título de la ventana
        self.cuadricula = self.crear_cuadricula()  # Atributo: Crea la cuadrícula de celdas
        self.inicio = None  # Atributo: Celda de inicio (inicialmente None)
        self.final = None  # Atributo: Celda final (inicialmente None)

    def crear_cuadricula(self):  # Método que crea la cuadrícula de celdas
        cuadricula = []
        ancho_celda = self.ancho_ventana // self.filas  # Calcula el ancho de cada celda
        for i in range(self.filas):
            cuadricula.append([])
            for j in range(self.filas):
                celda = Celda(i, j, ancho_celda, self.filas)  # Crea una nueva celda
                cuadricula[i].append(celda)  # Añade la celda a la cuadrícula
        return cuadricula

    def dibujar_cuadricula(self):  # Método que dibuja las líneas de la cuadrícula
        ancho_celda = self.ancho_ventana // self.filas  # Calcula el ancho de cada celda
        for i in range(self.filas):
            pygame.draw.line(self.ventana, GRIS, (0, i * ancho_celda), (self.ancho_ventana, i * ancho_celda))  # Dibuja línea horizontal
            for j in range(self.filas):
                pygame.draw.line(self.ventana, GRIS, (j * ancho_celda, 0), (j * ancho_celda, self.ancho_ventana))  # Dibuja línea vertical

    def dibujar(self):  # Método que dibuja toda la ventana
        self.ventana.fill(BLANCO)  # Llena la ventana con color blanco
        for fila in self.cuadricula:
            for celda in fila:
                celda.dibujar(self.ventana)  # Dibuja cada celda
        self.dibujar_cuadricula()  # Dibuja las líneas de la cuadrícula
        pygame.display.update()  # Actualiza la pantalla

    def obtener_pos_clic(self, pos):  # Método que obtiene la posición del clic en la cuadrícula
        ancho_celda = self.ancho_ventana // self.filas  # Calcula el ancho de cada celda
        y, x = pos
        fila = y // ancho_celda
        columna = x // ancho_celda
        return fila, columna

    def correr(self):  # Método que contiene el bucle principal del juego y maneja los eventos del usuario
        corriendo = True
        while corriendo:
            self.dibujar()  # Dibuja la ventana
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:  # Maneja el evento de salida
                    corriendo = False

                if pygame.mouse.get_pressed()[0]:  # Si se hace clic izquierdo
                    pos = pygame.mouse.get_pos()
                    fila, columna = self.obtener_pos_clic(pos)
                    celda = self.cuadricula[fila][columna]
                    if not self.inicio and celda != self.final:
                        self.inicio = celda  # Establece la celda de inicio
                        self.inicio.hacer_inicio()

                    elif not self.final and celda != self.inicio:
                        self.final = celda  # Establece la celda final
                        self.final.hacer_final()

                    elif celda != self.inicio and celda != self.final:
                        celda.hacer_barrera()  # Marca la celda como una barrera

                elif pygame.mouse.get_pressed()[2]:  # Si se hace clic derecho
                    pos = pygame.mouse.get_pos()
                    fila, columna = self.obtener_pos_clic(pos)
                    celda = self.cuadricula[fila][columna]
                    celda.reiniciar()  # Reinicia el color de la celda
                    if celda == self.inicio:
                        self.inicio = None  # Reinicia la celda de inicio
                    elif celda == self.final:
                        self.final = None  # Reinicia la celda final

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE and self.inicio and self.final:  # Si se presiona la barra espaciadora
                        for fila in self.cuadricula:
                            for celda in fila:
                                celda.actualizar_vecinos(self.cuadricula)  # Actualiza los vecinos de cada celda

                        algoritmo = AlgoritmoAEstrella(self.cuadricula, self.inicio, self.final, self.dibujar)  # Crea una instancia del algoritmo A*
                        algoritmo.ejecutar()  # Ejecuta el algoritmo A*

                    if evento.key == pygame.K_c:  # Si se presiona la tecla C
                        self.inicio = None
                        self.final = None
                        self.cuadricula = self.crear_cuadricula()  # Reinicia la cuadrícula

        pygame.quit()  # Finaliza Pygame

if __name__ == "__main__":
    ANCHO_VENTANA = 800  # Ancho de la ventana
    FILAS = 50  # Número de filas
    juego = VentanaJuego(ANCHO_VENTANA, FILAS)  # Crea una instancia de VentanaJuego
    juego.correr()  # Ejecuta el juego
