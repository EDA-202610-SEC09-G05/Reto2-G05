import time
import csv
import sys

# Configuración obligatoria PDF pág. 11
csv.field_size_limit(2147483647)
sys.setrecursionlimit(10000)

from DataStructures.Map import map_separate_chaining as sc 
from DataStructures.List import array_list as al
from DataStructures.List import single_linked_list as sl

def get_time():
    return time.perf_counter() * 1000

def delta_time(start, end):
    return end - start

def new_logic():
    """
    Crea el catálogo inicial con tus estructuras de Mapas.
    """
    return {
        "computer": al.new_list(),
        "year": sc.new_map(500, 0.5),
        "brand": sc.new_map(500, 0.5),
        "brandCPU": sc.new_map(500, 0.5),
        "gpu_model": sc.new_map(500, 0.5),
        "form_factor": sc.new_map(500, 0.5),
        "os": sc.new_map(500, 0.5)
    }
    
def criterio_precio_desc(comp):
    """Ordena por precio de mayor a menor."""
    return -float(comp["price"]), comp["model"]

def criterio_peso_asc(comp):
    """Ordena por peso de menor a mayor."""
    return float(comp["weight_kg"]), comp["model"]

def load_data(catalog, size):
    """Carga datos, llena los mapas y genera estadísticas."""
    inicio = get_time()
    url = f"./Data/computer_prices_{size}.csv"

    max_precio = {"price": float("-inf")}
    min_precio = {"price": float("inf")}
    min_year, max_year = float("inf"), float("-inf")
    total = 0
    os_count = {} 
    lista_temp = []

    with open(url, encoding="utf-8") as f:
        filas = csv.DictReader(f)
        for comp in filas:
            al.add_last(catalog["computer"], comp)
            lista_temp.append(comp)
            total += 1

            # Estadísticas
            p_actual = float(comp["price"])
            y_actual = int(comp["release_year"])
            if p_actual < float(min_precio["price"]): min_precio = comp
            if p_actual > float(max_precio["price"]): max_precio = comp
            if y_actual < min_year: min_year = y_actual
            if y_actual > max_year: max_year = y_actual

            # Conteo OS
            os_name = comp["os"]
            os_count[os_name] = os_count.get(os_name, 0) + 1

            # Llenar Mapas (Separate Chaining)
            y_key = comp["release_year"]
            lista_y = sc.get(catalog["year"], y_key)
            if lista_y is None:
                lista_y = sl.new_list()
                sc.put(catalog["year"], y_key, lista_y)
            sl.add_last(lista_y, comp)

            b_key = comp["brand"].lower()
            lista_b = sc.get(catalog["brand"], b_key)
            if lista_b is None:
                lista_b = sl.new_list()
                sc.put(catalog["brand"], b_key, lista_b)
            sl.add_last(lista_b, comp)

    # Ordenar lista temporal para Tops (Sin lambda)
    lista_temp.sort(key=criterio_precio_desc)
    
    top5 = []
    for i in range(min(5, total)):
        c = lista_temp[i]
        top5.append({"brand": c["brand"], "model": c["model"], "price": c["price"]})
        
    bottom5 = []
    for i in range(total - 1, max(-1, total - 6), -1):
        c = lista_temp[i]
        bottom5.append({"brand": c["brand"], "model": c["model"], "price": c["price"]})

    return (catalog, delta_time(inicio, get_time()), total, os_count, min_year, max_year, 
            min_precio, max_precio, top5, bottom5)

def req_1(catalog):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass



def req_2(catalog, num_nucleos, anio_lanzamiento):
    """Requerimiento 2: Filtrado eficiente por mapa y ordenado por peso."""
    inicio = get_time()
    
    # 1. Búsqueda en Mapa (Uso de tus estructuras)
    # Devuelve la lista enlazada guardada para ese año
    lista_equipos = sc.get(catalog["year"], str(anio_lanzamiento))
    
    resultados_filtrados = []
    if lista_equipos is not None:
        # IMPORTANTE: Revisa si tu nodo usa 'info' o 'value'
        actual = lista_equipos["first"] 
        while actual is not None:
            comp = actual["info"] 
            if int(comp["cpu_cores"]) == int(num_nucleos):
                resultados_filtrados.append(comp)
            actual = actual["next"]

    # 2. Ordenar por peso (Sin lambda)
    resultados_filtrados.sort(key=criterio_peso_asc)

    # 3. Cálculos
    n = len(resultados_filtrados)
    total_peso = 0
    for c in resultados_filtrados:
        total_peso += float(c["weight_kg"])
    promedio_peso = (total_peso / n) if n > 0 else 0

    # 4. Formateo y Regla de 20 elementos
    lista_final = []
    if n > 0:
        indices = []
        if n > 20:
            for i in range(10): indices.append(i)
            for i in range(n - 10, n): indices.append(i)
        else:
            for i in range(n): indices.append(i)

        for idx in indices:
            c = resultados_filtrados[idx]
            lista_final.append({
                "Tipo": c["device_type"],
                "Modelo": c["model"],
                "OS": c["os"],
                "CPU Brand": c["cpu_brand"],
                "RAM": c["ram_gb"],
                "Storage": c["storage_gb"],
                "Peso": c["weight_kg"]
            })

    return delta_time(inicio, get_time()), n, round(promedio_peso, 2), lista_final


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
