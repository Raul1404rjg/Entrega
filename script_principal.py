from red_distribucion import RedDistribucion

# Crear la red de distribución
red = RedDistribucion()
red.agregar_ciudad('Central')
red.agregar_ciudad('Leon')
red.agregar_ciudad('Madrid')
red.agregar_ciudad('Valencia')
red.agregar_ciudad('Oviedo')
red.agregar_ciudad('Ourense')
red.agregar_ciudad('Palencia')
red.agregar_ciudad('Merida')
red.agregar_ciudad('Barcelona')
red.agregar_ciudad('Sevilla')
red.agregar_ciudad('Soria')

red.agregar_conexion('Central', 'Leon', distancia=5, resistencia=1)
red.agregar_conexion('Central', 'Madrid', distancia=10, resistencia=2)
red.agregar_conexion('Leon', 'Madrid', distancia=3, resistencia=0.5)
red.agregar_conexion('Leon', 'Valencia', distancia=2, resistencia=1)
red.agregar_conexion('Madrid', 'Oviedo', distancia=7, resistencia=1.5)
red.agregar_conexion('Valencia', 'Ourense', distancia=4, resistencia=1)
red.agregar_conexion('Oviedo', 'Ourense', distancia=1, resistencia=0.2)
red.agregar_conexion('Madrid', 'Palencia', distancia=6, resistencia=1.1)
red.agregar_conexion('Valencia', 'Merida', distancia=8, resistencia=2.3)
red.agregar_conexion('Oviedo', 'Barcelona', distancia=9, resistencia=2.5)
red.agregar_conexion('Ourense', 'Sevilla', distancia=5, resistencia=1)
red.agregar_conexion('Palencia', 'Soria', distancia=11, resistencia=3)
red.agregar_conexion('Merida', 'Soria', distancia=10, resistencia=2.7)
red.agregar_conexion('Barcelona', 'Soria', distancia=12, resistencia=3.2)
red.agregar_conexion('Sevilla', 'Soria', distancia=4, resistencia=1.5)

# Energía inicial
energia_inicial = 100

# Preguntar al usuario la ciudad de destino
ciudad_destino = input("Ingrese la ciudad de destino: ")

# Verificar si la ciudad de destino existe en la red
if ciudad_destino not in red.grafo.nodes:
    print(f"La ciudad {ciudad_destino} no existe en la red.")
else:
    # Ajuste de parámetros 
    factor_resistencia = 0.1
    factor_distancia =  0.05

    # Encontrar el camino y la energía que llega a la ciudad de destino
    camino, energia = red.encontrar_camino_y_energia('Central', ciudad_destino, energia_inicial, factor_resistencia, factor_distancia)

    # Mostrar los resultados
    print(f'Camino más eficiente a {ciudad_destino}: {camino}')
    print(f'Energía que llega a {ciudad_destino}: {energia:.2f}')

    # Visualizar la red
    energia_en_ciudades, _ = red.simular_perdida_energia('Central', energia_inicial, factor_resistencia, factor_distancia)
    red.visualizar_red(energia_en_ciudades)

