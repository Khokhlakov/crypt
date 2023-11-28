# pip install graphviz
# pip install ipython
#from IPython.display import Image
import pydot
import os
import sys


colours = ["aqua","brown1","aquamarine4","blueviolet","coral","chartreuse4","crimson",
           "darkblue","cyan3","darkorchid1","darkorange1","darkgreen","darkslateblue",
           "goldenrod4","gold3","darkviolet","deeppink4","deepskyblue1","firebrick4",
           "darksalmon","cornflowerblue","darkolivegreen","indianred1","hotpink4"]

def procesar_texto(texto):
    palabras = texto.split()
    palabras_sin_espacios = [palabra.replace(" ", "").lower() for palabra in palabras]
    todos_los_simbolos = "".join(palabras_sin_espacios)
    simbolos_distintos = set(todos_los_simbolos)
    numero_simbolos_distintos = len(simbolos_distintos)
    lista_simbolos_distintos = list(simbolos_distintos)

    return palabras_sin_espacios, numero_simbolos_distintos, lista_simbolos_distintos

def mapear_posiciones(strings, simbolos):
    posiciones_mapeadas = {simbolo: [] for simbolo in simbolos}
    
    for cadena_index, cadena in enumerate(strings):
        for simbolo in simbolos:
            apariciones = cadena.count(simbolo)
            posiciones_repetidas = ["W" + str(cadena_index+1)] * apariciones

            posiciones_mapeadas[simbolo].extend(posiciones_repetidas)
    
    for simbolo in simbolos:
        posiciones_mapeadas[simbolo].append(posiciones_mapeadas[simbolo][0])
    
    return posiciones_mapeadas

def contar_valencia_y_evaluar(strings, simbolos):
    resultados = {}
    
    for simbolo in simbolos:
        valencia = sum(cadena.count(simbolo) for cadena in strings)
        multiplicidad = 2 if valencia == 1 else 1 if valencia > 1 else 0
        resultados[simbolo] = [valencia, multiplicidad]
    
    return resultados

def contar_ocurrencias_consecutivas(posiciones_mapeadas):
    ocurrencias_consecutivas = {}
    
    for simbolo, posiciones in posiciones_mapeadas.items():
        contador = 0
        for i in range(len(posiciones) - 1):
            if posiciones[i] == posiciones[i + 1]:
                contador += 1
        ocurrencias_consecutivas[simbolo] = contador
    
    return ocurrencias_consecutivas

def generar_tuplas(lista, etiqueta):
    # Utilizar una comprensión de lista para generar las tuplas con la etiqueta
    tuplas = [(lista[i], lista[i+1], etiqueta+str(i+1)) for i in range(len(lista)-1)]
    return tuplas

def calcular_dim_k_N(r1, val_y_multi):
    tamanio_r1 = len(r1)
    sumatoria = sum(val * ((val * multi) - 1) for val, [val, multi] in val_y_multi.items())
    dim_k_N = 2 * tamanio_r1 + sumatoria
    return dim_k_N

def calcular_dim_Z_k_N(r1, r0, val_y_multi, loops):
    tamanio_r0 = len(r0)
    num_simbolos_val_1 = sum(1 for val, [val, multi] in val_y_multi.items() if val == 1)
    dim_Z_k_N = 1 + sum(multi for val, [val, multi] in val_y_multi.items()) + len(r1) + sum(loops.values()) - tamanio_r0 - num_simbolos_val_1
    return dim_Z_k_N

def crear_grafo(mapeo_posiciones, target_path = None):
    if target_path == None:
        target_path = os.path.join(os.path.dirname(sys.argv[0]),"PiCKED App", "algBr42h399rh23ru8934.png")
    # Crear un grafo dirigido con Graphviz
    dot = pydot.Dot(graph_type = "digraph")

    # Añadir nodos y arcos con etiquetas
    contadorColores = 0
    for key, lista_posiciones in mapeo_posiciones.items():
        # Generar tuplas con la etiqueta correspondiente a la clave
        tuplas = generar_tuplas(lista_posiciones, key)

        # Añadir nodos y arcos con etiquetas al grafo
        for tupla in tuplas:
            node = pydot.Node(str(tupla[0]))
            dot.add_node(node)
            node = pydot.Node(str(tupla[1]))
            dot.add_node(node)
            edge = pydot.Edge(str(tupla[0]), str(tupla[1]), label=f'{tupla[2]}', color = colours[contadorColores%24])
            dot.add_edge(edge)
        contadorColores += 1

    # Especificar el formato de salida
    output_format = 'png'
    output_file = 'grafo_mapeo_posiciones'

    # Guardar el grafo en un archivo en formato DOT
    #dot.render(output_file, format='png', cleanup=True)


    dot.write_png(target_path)

    # Mostrar la imagen
    return target_path


def obtener_resultados(texto):
    # Procesar texto
    r1, _, r0 = procesar_texto(texto)

    # Mapear posiciones
    mapeo_posiciones = mapear_posiciones(r1, r0)

    # Contar valencia y evaluar
    val_y_multi = contar_valencia_y_evaluar(r1, r0)

    # Contar ocurrencias consecutivas usando las posiciones mapeadas
    loops = contar_ocurrencias_consecutivas(mapeo_posiciones)

    # Calcular dim_k_N
    dim_k_N = calcular_dim_k_N(r1, val_y_multi)

    # Calcular dim_Z_k_N
    dim_Z_k_N = calcular_dim_Z_k_N(r1, r0, val_y_multi, loops)

    # Crear el grafo y obtener el archivo
    # archivo_grafo = crear_grafo(mapeo_posiciones)

    # Retornar todos los resultados
    resultados = {
        "D": dim_k_N,
        "DZ": dim_Z_k_N,
        "Ciclos": mapeo_posiciones,
        "Diccionario de vertices con sus valencias y multiplicidad": val_y_multi,
        "NLoops": loops,
        "R1": r1,
        "R0": r0
    }

    return resultados

# Ejemplo de uso
#texto_entrada = "cotyyhogapmf adrps rota xe mregh"

# Obtener todos los resultados
#resultados = obtener_resultados(texto_entrada)

# Imprimir todos los resultados
#for nombre, valor in resultados.items():
#    print(f"{nombre}: {valor}\n\n")
#crear_grafo(resultados["Ciclos"])
