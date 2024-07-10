import heapq

# Algoritmo de Búsqueda de Ruta (A*)
def a_star(mapa, inicio, fin):
    filas, columnas = len(mapa), len(mapa[0])
    movimientos = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # derecha, abajo, izquierda, arriba

    def heuristica(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_list = []
    heapq.heappush(open_list, (0 + heuristica(inicio, fin), 0, inicio))
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

            if 0 <= neighbor[0] < filas and 0 <= neighbor[1] < columnas:
                if mapa[neighbor[0]][neighbor[1]] == 1:
                    continue

                tentative_g = current_g + 1

                if neighbor not in g_costs or tentative_g < g_costs[neighbor]:
                    g_costs[neighbor] = tentative_g
                    f_cost = tentative_g + heuristica(neighbor, fin)
                    heapq.heappush(open_list, (f_cost, tentative_g, neighbor))
                    came_from[neighbor] = current

    return None

# Visualización del Mapa
def mostrar_mapa(mapa, ruta, inicio, fin):
    mapa_viz = []
    for fila in mapa:
        mapa_viz.append(['.' if celda == 0 else 'X' for celda in fila])
    
    for (x, y) in ruta:
        mapa_viz[x][y] = '*'
    
    mapa_viz[inicio[0]][inicio[1]] = 'E'
    mapa_viz[fin[0]][fin[1]] = 'S'
    
    for fila in mapa_viz:
        print(' '.join(fila))

# Interacción con el Usuario
def ingresar_coordenadas(mensaje):
    x, y = map(int, input(mensaje).split())
    return (x, y)

# Creación del mapa
def crear_mapa(filas, columnas):
    return [[0 for _ in range(columnas)] for _ in range(filas)]

# Principal
def main():
    filas = int(input("Ingrese la cantidad de filas del mapa: "))
    columnas = int(input("Ingrese la cantidad de columnas del mapa: "))
    mapa = crear_mapa(filas, columnas)

    # Ingreso de coordenadas por el usuario
    inicio = ingresar_coordenadas("Ingrese las coordenadas del punto de inicio (formato: x y): ")
    fin = ingresar_coordenadas("Ingrese las coordenadas del punto de destino (formato: x y): ")

    # Agregar obstáculos
    num_obstaculos = int(input("¿Cuántos obstáculos desea agregar? "))
    for _ in range(num_obstaculos):
        obstaculo = ingresar_coordenadas("Ingrese las coordenadas del nuevo obstáculo (formato: x y): ")
        if 0 <= obstaculo[0] < filas and 0 <= obstaculo[1] < columnas:
            mapa[obstaculo[0]][obstaculo[1]] = 1
        else:
            print("Coordenadas inválidas. Por favor, intente de nuevo.")

    # Encontrar y mostrar la ruta
    ruta = a_star(mapa, inicio, fin)
    if ruta:
        mostrar_mapa(mapa, ruta, inicio, fin)
    else:
        print("No se encontró una ruta.")

if __name__ == "__main__":
    main()
