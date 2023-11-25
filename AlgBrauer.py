# pip install graphviz
# pip install ipython
import graphviz
from IPython.display import Image

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
            posiciones_repetidas = [cadena_index] * apariciones
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
    tuplas = [(lista[i], lista[i+1], etiqueta) for i in range(len(lista)-1)]
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

def crear_grafo(mapeo_posiciones):
    # Crear un grafo dirigido con Graphviz
    dot = graphviz.Digraph()

    # Añadir nodos y arcos con etiquetas
    for key, lista_posiciones in mapeo_posiciones.items():
        # Generar tuplas con la etiqueta correspondiente a la clave
        tuplas = generar_tuplas(lista_posiciones, key)

        # Añadir nodos y arcos con etiquetas al grafo
        for tupla in tuplas:
            dot.node(str(tupla[0]))
            dot.node(str(tupla[1]))
            dot.edge(str(tupla[0]), str(tupla[1]), label=f'{tupla[2]}')

    # Especificar el formato de salida
    output_format = 'png'
    output_file = 'grafo_mapeo_posiciones'

    # Guardar el grafo en un archivo en formato DOT
    dot_file = f"{output_file}.dot"
    dot.render(dot_file, format='png', cleanup=True)

    # Mostrar la imagen
    return dot_file

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
    archivo_grafo = crear_grafo(mapeo_posiciones)

    # Retornar todos los resultados
    resultados = {
        "Valor de dimension del algebra de configuracion de brauer (dim_k_N)": dim_k_N,
        "Valor de dimension del centro del álgebra de una configuración de Brauer (dim_Z_k_N)": dim_Z_k_N,
        "Grafo (archivo_grafo)": archivo_grafo,
        "Ciclos": mapeo_posiciones,
        "Diccionario de vertices con sus valencias y multiplicidad": val_y_multi,
        "Numero de loops:": loops,
        "R1 (Poligonos)": r1,
        "R0 (Vertices)": r0,
    }

    return resultados

# Ejemplo de uso
texto_entrada = "cotyyhogapmf adrps rota xe mregh"

# Obtener todos los resultados
resultados = obtener_resultados(texto_entrada)

# Imprimir todos los resultados
for nombre, valor in resultados.items():
    print(f"{nombre}: {valor}\n\n")


