import math
import itertools
import matplotlib.pyplot as plt
import tkinter as tk


def calcular_distancia(lat1, lon1, lat2, lon2):
    # Radio de la Tierra en kilómetros
    radio_tierra = 6371

    # Convertir las latitudes y longitudes a radianes
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Diferencia de latitudes y longitudes
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Fórmula de Haversine
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distancia = radio_tierra * c

    return distancia


def distancia_total(camino, puntos):
    distancia = 0
    for i in range(len(camino) - 1):
        origen = camino[i]
        destino = camino[i + 1]
        lat1, lon1 = puntos[origen]
        lat2, lon2 = puntos[destino]
        distancia += calcular_distancia(lat1, lon1, lat2, lon2)
    return distancia


def fuerza_bruta(puntos, inicio):
    nodos = list(puntos.keys())
    if inicio in nodos:
        nodos.remove(inicio)
    else:
        return None, None

    mejor_camino = None
    mejor_distancia = math.inf

    for perm in itertools.permutations(nodos):
        camino = [inicio] + list(perm) + [inicio]
        distancia = distancia_total(camino, puntos)
        if distancia < mejor_distancia:
            mejor_camino = camino
            mejor_distancia = distancia

    return mejor_camino, mejor_distancia



def backtracking(puntos, inicio):
    nodos = list(puntos.keys())
    nodos.remove(inicio)
    mejor_camino = None
    mejor_distancia = math.inf

    def backtrack(camino, distancia_actual):
        nonlocal mejor_camino, mejor_distancia

        if len(camino) == len(nodos) + 1:
            distancia = distancia_actual + calcular_distancia(puntos[camino[-1]][0], puntos[camino[-1]][1],
                                                              puntos[inicio][0], puntos[inicio][1])
            if distancia < mejor_distancia:
                mejor_camino = camino + [inicio]
                mejor_distancia = distancia
            return

        for nodo in nodos:
            if nodo not in camino:
                distancia = calcular_distancia(puntos[camino[-1]][0], puntos[camino[-1]][1],
                                               puntos[nodo][0], puntos[nodo][1])
                if distancia_actual + distancia < mejor_distancia:
                    backtrack(camino + [nodo], distancia_actual + distancia)

    backtrack([inicio], 0)
    return mejor_camino, mejor_distancia


def goloso(puntos, inicio, punto_final=None):
    nodos = list(puntos.keys())
    nodos.remove(inicio)
    if punto_final:
        nodos.remove(punto_final)
    camino = [inicio]
    distancia = 0

    while nodos:
        mejor_distancia = math.inf
        mejor_nodo = None

        for nodo in nodos:
            dist = calcular_distancia(puntos[camino[-1]][0], puntos[camino[-1]][1],
                                      puntos[nodo][0], puntos[nodo][1])
            if dist < mejor_distancia:
                mejor_distancia = dist
                mejor_nodo = nodo

        camino.append(mejor_nodo)
        distancia += mejor_distancia
        nodos.remove(mejor_nodo)

    if punto_final:
        distancia += calcular_distancia(puntos[camino[-1]][0], puntos[camino[-1]][1],
                                        puntos[punto_final][0], puntos[punto_final][1])
        camino.append(punto_final)

    return camino, distancia


def graficar_puntos(camino, puntos):
    plt.figure(figsize=(8, 6))
    for punto, coord in puntos.items():
        plt.plot(coord[1], coord[0], 'bo')
        plt.text(coord[1], coord[0], punto, ha='center', va='bottom')

    plt.xlabel('Longitud')
    plt.ylabel('Latitud')
    plt.title('GRAFICA DE LA RUTA TRAZADA')

    for i in range(len(camino) - 1):
        punto1 = camino[i]
        punto2 = camino[i + 1]
        coord1 = puntos[punto1]
        coord2 = puntos[punto2]
        plt.plot([coord1[1], coord2[1]], [coord1[0], coord2[0]], 'b')

    plt.show()


def graficar_resultados(camino_goloso, puntos):
    plt.figure(figsize=(8, 6))
    for punto, coord in puntos.items():
        plt.plot(coord[1], coord[0], 'bo')
        plt.text(coord[1], coord[0], punto, ha='center', va='bottom')

    plt.xlabel('Longitud')
    plt.ylabel('Latitud')
    plt.title('RUTA TRAZADA - Camino más corto ENCONTRADO por (Método Goloso)')

    distancia_total = 0  # Variable para almacenar la distancia total

    for i in range(len(camino_goloso) - 1):
        punto1 = camino_goloso[i]
        punto2 = camino_goloso[i + 1]
        coord1 = puntos[punto1]
        coord2 = puntos[punto2]

        # Calcular la distancia entre los puntos
        distancia = calcular_distancia(coord1[0], coord1[1], coord2[0], coord2[1])

        # Agregar la distancia al total
        distancia_total += distancia

        # Mostrar la distancia en el gráfico
        plt.plot([coord1[1], coord2[1]], [coord1[0], coord2[0]], 'b')
        plt.text((coord1[1] + coord2[1]) / 2, (coord1[0] + coord2[0]) / 2, f'{distancia:.2f} km',
                 ha='center', va='bottom')

    plt.show()

    # Imprimir la distancia total
    print("Distancia total:", distancia_total, "kilómetros")



def mostrar_ventana_puntos():
    ventana = tk.Tk()
    ventana.title("Ingresar Puntos - Camino más corto")
    
    puntos = {}

    def crear_punto_entry(row):
        punto_label = tk.Label(ventana, text=f"Punto {row}:")
        punto_entry = tk.Entry(ventana, width=10)
        latitud_label = tk.Label(ventana, text="Latitud:")
        latitud_entry = tk.Entry(ventana, width=10)
        longitud_label = tk.Label(ventana, text="Longitud:")
        longitud_entry = tk.Entry(ventana, width=10)
        
        punto_label.grid(row=row, column=0, padx=5, pady=5)
        punto_entry.grid(row=row, column=1, padx=5, pady=5)
        latitud_label.grid(row=row, column=2, padx=5, pady=5)
        latitud_entry.grid(row=row, column=3, padx=5, pady=5)
        longitud_label.grid(row=row, column=4, padx=5, pady=5)
        longitud_entry.grid(row=row, column=5, padx=5, pady=5)
        
        return punto_entry, latitud_entry, longitud_entry
    
    def agregar_punto():
        num_puntos = len(puntos_entries) + 1
        punto_entry = crear_punto_entry(num_puntos)
        puntos_entries.append(punto_entry)
    
    def eliminar_punto():
        if puntos_entries:
            punto_entry, latitud_entry, longitud_entry = puntos_entries.pop()
            punto_entry.destroy()
            latitud_entry.destroy()
            longitud_entry.destroy()
    
    def guardar_puntos():
        puntos.clear()
        for punto_entry, latitud_entry, longitud_entry in puntos_entries:
            punto = punto_entry.get()
            latitud = float(latitud_entry.get())
            longitud = float(longitud_entry.get())
            puntos[punto] = (latitud, longitud)
    
    def graficar_metodos():
        inicio = puntos_entries[0][0].get()
        camino_bruta, distancia_bruta = fuerza_bruta(puntos, inicio)
        camino_backtrack, distancia_backtrack = backtracking(puntos, inicio)
        camino_goloso, distancia_goloso = goloso(puntos, inicio)

        print("Método de Fuerza Bruta:")
        print("Camino:", camino_bruta)
        print("Distancia:", distancia_bruta)

        print("Método de Backtracking:")
        print("Camino:", camino_backtrack)
        print("Distancia:", distancia_backtrack)

        print("Método Goloso:")
        print("Camino:", camino_goloso)
        print("Distancia:", distancia_goloso)

        graficar_resultados(camino_goloso, puntos)
    
    puntos_entries = []
    
    agregar_button = tk.Button(ventana, text="Agregar punto", command=agregar_punto)
    agregar_button.grid(row=0, column=0, padx=5, pady=5)
    
    eliminar_button = tk.Button(ventana, text="Eliminar punto", command=eliminar_punto)
    eliminar_button.grid(row=0, column=1, padx=5, pady=5)
    
    guardar_button = tk.Button(ventana, text="Guardar puntos", command=guardar_puntos)
    guardar_button.grid(row=0, column=2, padx=5, pady=5)
    
    graficar_button = tk.Button(ventana, text="Graficar métodos", command=graficar_metodos)
    graficar_button.grid(row=0, column=3, padx=5, pady=5)
    
    ventana.mainloop()


mostrar_ventana_puntos()
