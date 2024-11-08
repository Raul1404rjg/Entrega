import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import heapq

class RedDistribucion:
    def __init__(self):
        self.grafo = nx.DiGraph()

    def agregar_ciudad(self, ciudad):
        self.grafo.add_node(ciudad)

    def agregar_conexion(self, ciudad1, ciudad2, distancia, resistencia):
        self.grafo.add_edge(ciudad1, ciudad2, distancia=distancia, resistencia=resistencia)

    def dijkstra(self, inicio, factor_resistencia=0.1, factor_distancia=0.05):
        peso_acumulado_min = {nodo: float('inf') for nodo in self.grafo.nodes}# Inicializar diccionario de peso acumulado minimo con infinito para todos los nodos excepto el nodo inicial
        peso_acumulado_min[inicio] = 0
        caminos = {inicio: [inicio]}
        pq = [(0, 0, inicio)]  # Cola de prioridad que guarda (distancia_total, resistencia_total, nodo)

        while pq:# Mientras haya nodos en la cola de prioridad
           # Extrae el nodo con el peso acumulado mínima
            dist, res, nodo_actual = heapq.heappop(pq)   
            for vecino in self.grafo.neighbors(nodo_actual):
                resistencia = self.grafo[nodo_actual][vecino]['resistencia']
                distancia = self.grafo[nodo_actual][vecino]['distancia']

                distancia_total = dist + distancia
                resistencia_total = res + resistencia
                
                peso = factor_distancia * distancia_total + factor_resistencia * resistencia_total
                
                if peso < peso_acumulado_min[vecino]:# Si el peso acumulado de esa nueva ruta calculado es menor que el peso almacenado de otra ruta, actualiza
                    peso_acumulado_min[vecino] = peso
                    heapq.heappush(pq, (distancia_total, resistencia_total, vecino))
                    caminos[vecino] = caminos[nodo_actual] + [vecino]

        return peso_acumulado_min, caminos

    def simular_perdida_energia(self, inicio, energia_inicial, factor_resistencia=0.1, factor_distancia=0.05):
        peso_acumulado_min, caminos = self.dijkstra(inicio, factor_resistencia, factor_distancia)
        energia_en_ciudades = {}
        for ciudad in peso_acumulado_min.keys():
            resistencia_total = sum(self.grafo[caminos[ciudad][i]][caminos[ciudad][i+1]]['resistencia'] for i in range(len(caminos[ciudad])-1))
            distancia_total = sum(self.grafo[caminos[ciudad][i]][caminos[ciudad][i+1]]['distancia'] for i in range(len(caminos[ciudad])-1))
            energia_en_ciudades[ciudad] = energia_inicial * np.exp(-(factor_resistencia * resistencia_total + factor_distancia * distancia_total))  # pérdida exponencial basada en resistencia y distancia

        return energia_en_ciudades, caminos

    def visualizar_red(self, energia_en_ciudades):
        pos = nx.spring_layout(self.grafo)
        nx.draw(self.grafo, pos, with_labels=True, node_color='lightblue', edge_color='gray')
        
        etiquetas_distancia = nx.get_edge_attributes(self.grafo, 'distancia')
        etiquetas_resistencia = nx.get_edge_attributes(self.grafo, 'resistencia')

        # Combinar las etiquetas de distancia y resistencia
        etiquetas_combinadas = {k: f'D: {etiquetas_distancia[k]}, R: {etiquetas_resistencia[k]}' for k in etiquetas_distancia.keys()}
        nx.draw_networkx_edge_labels(self.grafo, pos, edge_labels=etiquetas_combinadas)

        # Añadir una escala de colores basada en la energía
        valores_energia = list(energia_en_ciudades.values())
        minimo_energia = min(valores_energia)
        maximo_energia = max(valores_energia)
        norm = plt.Normalize(minimo_energia, maximo_energia)
        cmap = plt.cm.Reds

        for ciudad, energia in energia_en_ciudades.items():
            x, y = pos[ciudad]
            color = cmap(norm(energia))
            plt.scatter(x, y, color=color, s=200)
            plt.text(x, y + 0.1, s=f'{energia:.2f}', bbox=dict(facecolor='white', alpha=0.5), horizontalalignment='center')

        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        

        plt.show()

    def encontrar_camino_y_energia(self, inicio, destino, energia_inicial, factor_resistencia=0.1, factor_distancia=0.05):
        energia_en_ciudades, caminos = self.simular_perdida_energia(inicio, energia_inicial, factor_resistencia, factor_distancia)
        camino = caminos[destino]
        energia = energia_en_ciudades[destino]
        return camino, energia
