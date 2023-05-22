import math
import itertools
import matplotlib.pyplot as plt


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


def distancia_total(camino, lugares):
    distancia = 0
    for i in range(len(camino) - 1):
        origen = camino[i]
        destino = camino[i + 1]
        lat1, lon1 = lugares[origen]
        lat2, lon2 = lugares[destino]
        distancia += calcular_distancia(lat1, lon1, lat2, lon2)
    return distancia


def fuerza_bruta(lugares, inicio):
    nodos = list(lugares.keys())
    nodos.remove(inicio)
    mejor_camino = None
    mejor_distancia = math.inf

    for perm in itertools.permutations(nodos):
        camino = [inicio] + list(perm) + [inicio]
        distancia = distancia_total(camino, lugares)
        if distancia < mejor_distancia:
            mejor_camino = camino
            mejor_distancia = distancia

    return mejor_camino, mejor_distancia


def backtracking(lugares, inicio):
    nodos = list(lugares.keys())
    nodos.remove(inicio)
    nodos.remove("Ayaviri")  # Omitir "Ayaviri" en el camino
    mejor_camino = None
    mejor_distancia = math.inf

    def backtrack(camino, distancia_actual):
        nonlocal mejor_camino, mejor_distancia

        if len(camino) == len(nodos) + 1:
            distancia = distancia_actual + calcular_distancia(lugares[camino[-1]][0], lugares[camino[-1]][1],
                                                              lugares[inicio][0], lugares[inicio][1])
            if distancia < mejor_distancia:
                mejor_camino = camino + [inicio]
                mejor_distancia = distancia
            return

        for nodo in nodos:
            if nodo not in camino:
                distancia = calcular_distancia(lugares[camino[-1]][0], lugares[camino[-1]][1],
                                               lugares[nodo][0], lugares[nodo][1])
                if distancia_actual + distancia < mejor_distancia:
                    backtrack(camino + [nodo], distancia_actual + distancia)

    backtrack([inicio], 0)
    return mejor_camino, mejor_distancia



def goloso(lugares, inicio, punto_final=None):
    nodos = list(lugares.keys())
    nodos.remove(inicio)
    if punto_final:
        nodos.remove(punto_final)
    if "Juliaca" in nodos:
        nodos.remove("Juliaca")
    if "Ayaviri" in nodos:
        nodos.remove("Ayaviri")
    camino = [inicio]
    distancia = 0

    while nodos:
        mejor_vecino = None
        mejor_distancia = math.inf

        for vecino in nodos:
            distancia_vecino = calcular_distancia(lugares[camino[-1]][0], lugares[camino[-1]][1],
                                                  lugares[vecino][0], lugares[vecino][1])
            if distancia_vecino < mejor_distancia:
                mejor_vecino = vecino
                mejor_distancia = distancia_vecino

        if mejor_vecino is None:
            return None, math.inf  # Camino inválido

        camino.append(mejor_vecino)
        distancia += mejor_distancia
        nodos.remove(mejor_vecino)

    if punto_final:
        distancia += calcular_distancia(lugares[camino[-1]][0], lugares[camino[-1]][1],
                                        lugares[punto_final][0], lugares[punto_final][1])
        camino.append(punto_final)
        distancia += calcular_distancia(lugares[punto_final][0], lugares[punto_final][1],
                                        lugares[inicio][0], lugares[inicio][1])
        camino.append(inicio)

    return camino, distancia


def mostrar_grafica(camino_bruta, camino_backtrack, camino_goloso, lugares, inicio, punto_final):
    latitudes = [coord[0] for coord in lugares.values()]
    longitudes = [coord[1] for coord in lugares.values()]

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    colors = {'Puno': 'red', 'Juliaca': 'green', 'Ayaviri': 'blue', 'Putina': 'purple'}

    for ax, camino, metodo in zip(axes, [camino_bruta, camino_backtrack, camino_goloso], ["Fuerza Bruta", "Backtracking", "Goloso"]):
        ax.plot(longitudes, latitudes, 'ro', label='Lugares')

        for nombre, (lat, lon) in lugares.items():
            color = colors.get(nombre, 'purple')
            ax.annotate(nombre, (lon, lat), textcoords="offset points", xytext=(0, 10),
                         ha='center', fontsize=8, color='black')
            ax.scatter(lon, lat, marker='o', s=50, color=color)
            ax.text(lon, lat - 0.1, f"{nombre} ({lat:.4f}, {lon:.4f})", fontsize=6,
                     ha='center', va='top', color='gray')

        # Dibujar solo el camino más corto
        if camino:
            for i in range(len(camino) - 1):
                origen = camino[i]
                destino = camino[i + 1]
                latitudes_camino = [lugares[origen][0], lugares[destino][0]]
                longitudes_camino = [lugares[origen][1], lugares[destino][1]]
                ax.plot(longitudes_camino, latitudes_camino, 'b--', linewidth=1)
                distancia = calcular_distancia(lugares[origen][0], lugares[origen][1],
                                               lugares[destino][0], lugares[destino][1])
                distancia_texto = f"{distancia:.2f} km"
                latitud_media = (lugares[origen][0] + lugares[destino][0]) / 2
                longitud_media = (lugares[origen][1] + lugares[destino][1]) / 2
                ax.text(longitud_media, latitud_media, distancia_texto, fontsize=8,
                         ha='center', va='center', color='blue')

        ax.scatter(lugares[inicio][1], lugares[inicio][0], marker='o', s=50, color='green')
        ax.text(lugares[inicio][1], lugares[inicio][0] - 0.1,
                 f"{inicio} ({lugares[inicio][0]:.4f}, {lugares[inicio][1]:.4f})",
                 fontsize=6, ha='center', va='top', color='gray')

        if punto_final:
            ax.scatter(lugares[punto_final][1], lugares[punto_final][0], marker='o', s=50, color='green')
            ax.text(lugares[punto_final][1], lugares[punto_final][0] - 0.1,
                     f"{punto_final} ({lugares[punto_final][0]:.4f}, {lugares[punto_final][1]:.4f})",
                     fontsize=6, ha='center', va='top', color='gray')

        ax.set_xlabel('Longitud')
        ax.set_ylabel('Latitud')
        ax.set_title(f'Camino más corto ({metodo})')
        ax.legend(list(lugares.keys()) + [f"Inicio: {inicio}", f" Final: {punto_final}"], handlelength=2)
        ax.grid(True)

        # Agregar cuadro con distancia correspondiente al método
        distancia = distancia_bruta if metodo == "Fuerza Bruta" else distancia_backtrack if metodo == "Backtracking" else distancia_goloso
        text_distancia = f"{metodo}: {distancia:.2f} km"
        ax.text(0.02, 0.02, text_distancia, transform=ax.transAxes,
                fontsize=10, verticalalignment='bottom', bbox=dict(facecolor='white', edgecolor='gray', alpha=0.5))

    plt.tight_layout()
    plt.show()


# Ejemplo de uso
lugares = {
    'Puno': (-15.8402, -70.0219),
    'Putina': (-15.4776, -69.4222),
    'Ayaviri': (-14.8819, -70.5881),
    'Juliaca': (-15.5000, -70.1333)
}

inicio = 'Puno'
punto_final = 'Putina'

camino_bruta, distancia_bruta = fuerza_bruta(lugares, inicio)
camino_backtrack, distancia_backtrack = backtracking(lugares, inicio)
camino_goloso, distancia_goloso = goloso(lugares, inicio, punto_final)

print("Fuerza Bruta:")
print("Camino:", camino_bruta)
print("Distancia:", distancia_bruta)

print("\nBacktracking:")
print("Camino:", camino_backtrack)
print("Distancia:", distancia_backtrack)

print("\nGoloso:")
print("Camino:", camino_goloso)
print("Distancia:", distancia_goloso)

mostrar_grafica(camino_bruta, camino_backtrack, camino_goloso, lugares, inicio, punto_final)

