import heapq

class Mapa:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.mapa = [[0 for _ in range(columnas)] for _ in range(filas)]

    def agregar_obstaculo(self, coordenadas):
        x, y = coordenadas
        if 0 <= x < self.filas and 0 <= y < self.columnas:
            self.mapa[x][y] = 1
        else:
            raise ValueError("Coordenadas fuera de los límites del mapa")

    def mostrar(self, ruta=None, inicio=None, fin=None):
        mapa_viz = [['.' if celda == 0 else 'X' for celda in fila] for fila in self.mapa]
        if ruta:
            for (x, y) in ruta:
                mapa_viz[x][y] = '*'
        if inicio:
            mapa_viz[inicio[0]][inicio[1]] = 'E'
        if fin:
            mapa_viz[fin[0]][fin[1]] = 'S'
        for fila in mapa_viz:
            print(' '.join(fila))

class Ruta:
    def __init__(self, mapa):
        self.mapa = mapa.mapa
        self.filas = mapa.filas
        self.columnas = mapa.columnas

    def heuristica(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def encontrar_ruta(self, inicio, fin):
        movimientos = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # derecha, abajo, izquierda, arriba
        open_list = []
        heapq.heappush(open_list, (0 + self.heuristica(inicio, fin), 0, inicio))
        g_costs = {inicio: 0}
        came_from = {}

        while open_list:
            _, current_g, current = heapq.heappop(open_list)

            if current == fin:
                ruta = []
                while current in came_from:
                    ruta.append(current)
                    current = came_from[current]
                ruta.append(inicio)
                ruta.reverse()
                return ruta

            for movimiento in movimientos:
                neighbor = (current[0] + movimiento[0], current[1] + movimiento[1])

                if 0 <= neighbor[0] < self.filas and 0 <= neighbor[1] < self.columnas:
                    if self.mapa[neighbor[0]][neighbor[1]] == 1:
                        continue

                    tentative_g = current_g + 1

                    if neighbor not in g_costs or tentative_g < g_costs[neighbor]:
                        g_costs[neighbor] = tentative_g
                        f_cost = tentative_g + self.heuristica(neighbor, fin)
                        heapq.heappush(open_list, (f_cost, tentative_g, neighbor))
                        came_from[neighbor] = current

        return None

def ingresar_coordenadas(mensaje):
    x, y = map(int, input(mensaje).split())
    return (x, y)

def main():
    filas = int(input("Ingrese la cantidad de filas del mapa: "))
    columnas = int(input("Ingrese la cantidad de columnas del mapa: "))
    mapa = Mapa(filas, columnas)

    # Ingreso de coordenadas por el usuario
    inicio = ingresar_coordenadas("Ingrese las coordenadas del punto de inicio (formato: x y): ")
    fin = ingresar_coordenadas("Ingrese las coordenadas del punto de destino (formato: x y): ")

    # Agregar obstáculos
    num_obstaculos = int(input("¿Cuántos obstáculos desea agregar? "))
    for _ in range(num_obstaculos):
        obstaculo = ingresar_coordenadas("Ingrese las coordenadas del nuevo obstáculo (formato: x y): ")
        try:
            mapa.agregar_obstaculo(obstaculo)
        except ValueError as e:
            print(e)

    # Encontrar y mostrar la ruta
    ruta = Ruta(mapa)
    camino = ruta.encontrar_ruta(inicio, fin)
    if camino:
        mapa.mostrar(camino, inicio, fin)
    else:
        print("No se encontró una ruta.")

if __name__ == "__main__":
    main()
