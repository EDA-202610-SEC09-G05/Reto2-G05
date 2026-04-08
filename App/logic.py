import time
import csv
import sys

# Configuración obligatoria PDF pág. 11
csv.field_size_limit(2147483647)
sys.setrecursionlimit(10000)

from DataStructures.Map import map_separate_chaining as sc 
from DataStructures.List import array_list as al
from DataStructures.List import single_linked_list as sl
# Importa la función merge_sort desde tu archivo sort.py y dale el alias 'ms'
from DataStructures.Sort.sort import merge_sort as ms


def new_logic():
    """
    Crea el catálogo inicial con tus estructuras de Mapas.
    """
    return {
        "computer": al.new_list(),
        "year": sc.new_map(500, 0.5),
        "brand": sc.new_map(500, 0.5),
        "cpu_brand": sc.new_map(500, 0.5),
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

def get_price(item):
    """Función de apoyo para ordenar sin usar lambda"""
    return float(item["price"])

def load_data(catalog, size):
    """
    Carga de datos sin lambdas y con columnas filtradas para la tabla.
    """
    inicio = get_time()
    url = f"./Data/computer_prices_{size}.csv"
    
    max_p, min_p = {"price": 0}, {"price": 0}
    min_y, max_y = 9999, 0
    total, os_count = 0, {}
    lista_temp = []

    # 1. Lectura del archivo
    with open(url, encoding="utf-8") as f:
        filas = csv.DictReader(f)
        for comp in filas:
            # Guardamos en el catálogo original (ArrayList)
            al.add_last(catalog["computer"], comp)
            # Guardamos en lista temporal para los Tops
            lista_temp.append(comp)
            total += 1
            
            p_actual = float(comp["price"])
            y_actual = int(comp["release_year"])
            
            # Estadísticas básicas
            if total == 1 or p_actual < float(min_p["price"]): min_p = comp
            if total == 1 or p_actual > float(max_p["price"]): max_p = comp
            if y_actual < min_y: min_y = y_actual
            if y_actual > max_y: max_y = y_actual
            
            # Conteo de OS
            os_name = comp["os"]
            os_count[os_name] = os_count.get(os_name, 0) + 1

    # 2. Ordenamiento usando la función de apoyo (SIN LAMBDA)
    # Ordenamos de mayor a menor precio
    lista_temp.sort(key=get_price, reverse=True)
    
    # 3. Construcción de TOP 5 (Primeros 5)
    top5 = []
    num_top = 5
    if len(lista_temp) < 5:
        num_top = len(lista_temp)
        
    for i in range(num_top):
        c = lista_temp[i]
        # Solo las columnas que se ven en tu terminal
        top5.append({
            "brand": c["brand"],
            "model": c["model"],
            "device_type": c["device_type"],
            "CPU": c["cpu_model"],
            "RAM": c["ram_gb"],
            "Storage": c["storage_gb"],
            "release_year": c["release_year"],
            "price": c["price"]
        })

    # 4. Construcción de BOTTOM 5 (Últimos 5)
    bottom5 = []
    total_items = len(lista_temp)
    inicio_bottom = total_items - 5
    if inicio_bottom < 0:
        inicio_bottom = 0

    for i in range(inicio_bottom, total_items):
        c = lista_temp[i]
        bottom5.append({
            "brand": c["brand"],
            "model": c["model"],
            "device_type": c["device_type"],
            "CPU": c["cpu_model"],
            "RAM": c["ram_gb"],
            "Storage": c["storage_gb"],
            "release_year": c["release_year"],
            "price": c["price"]
        })
    
    return (catalog, delta_time(inicio, get_time()), total, os_count, min_y, max_y, 
            min_p, max_p, top5, bottom5)


def compare_req1(c1, c2):
    """Descendente por precio. Empate: Ascendente por modelo."""
    p1, p2 = float(c1["price"]), float(c2["price"])
    if p1 != p2:
        return p1 > p2
    return c1["model"] < c2["model"]

def req_1(control, brand, form_factor):
    inicio = get_time()
    l_brand = sc.get(control["brand"], brand.lower())
    filtrados = al.new_list()
    suma_precios = 0
    
    if l_brand:
        actual = l_brand["first"]
        while actual:
            c = actual["info"]
            if c["form_factor"].lower() == form_factor.lower():
                al.add_last(filtrados, c)
                suma_precios += float(c["price"])
            actual = actual["next"]

    n = al.size(filtrados)
    promedio = suma_precios / n if n > 0 else 0
    ordenados = ms.sort(filtrados, compare_req1)
    
    return delta_time(inicio, get_time()), n, round(promedio, 2), ordenados

def compare_req2(c1, c2):
    """Ascendente por peso. Empate: Ascendente por modelo."""
    w1, w2 = float(c1["weight_kg"]), float(c2["weight_kg"])
    if w1 != w2:
        return w1 < w2
    return c1["model"] < c2["model"]

def req_2(catalog, num_nucleos, anio_lanzamiento):
    inicio = get_time()
    l_anio = sc.get(catalog["year"], str(anio_lanzamiento))
    filtrados = al.new_list()
    suma_peso = 0
    
    if l_anio:
        actual = l_anio["first"]
        while actual:
            c = actual["info"]
            if int(c["cpu_cores"]) == int(num_nucleos):
                al.add_last(filtrados, c)
                suma_peso += float(c["weight_kg"])
            actual = actual["next"]

    n = al.size(filtrados)
    promedio = suma_peso / n if n > 0 else 0
    ordenados = ms.sort(filtrados, compare_req2)
    
    return delta_time(inicio, get_time()), n, round(promedio, 2), ordenados



def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def compare_req4(c1, c2):
    """Descendente por precio. Empate: Menor peso primero."""
    p1, p2 = float(c1["price"]), float(c2["price"])
    if p1 != p2:
        return p1 > p2
    return float(c1["weight_kg"]) < float(c2["weight_kg"])


def req_4(catalog, cpu, gpu):
    inicio = get_time()
    l_gpu = sc.get(catalog["gpu_model"], gpu.lower())
    count, precios, ram, vram, boost = 0, 0, 0, 0, 0
    filtrados = al.new_list()
    
    if l_gpu:
        actual = l_gpu["first"]
        while actual:
            c = actual["info"]
            if c["cpu_brand"].lower() == cpu.lower():
                count += 1
                precios += float(c["price"])
                ram += int(c["ram_gb"])
                vram += int(c["vram_gb"])
                boost += float(c["cpu_boost_ghz"])
                al.add_last(filtrados, c)
            actual = actual["next"]
                
    ordenados = ms.sort(filtrados, compare_req4)
    tops = []
    if count >= 1: tops.append(al.get_element(ordenados, 0))
    if count >= 2: tops.append(al.get_element(ordenados, 1))
    
    proms = {
        "p": precios/count if count > 0 else 0, 
        "r": ram/count if count > 0 else 0,
        "v": vram/count if count > 0 else 0,
        "b": boost/count if count > 0 else 0
    }
    return delta_time(inicio, get_time()), count, proms, tops


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass



def compare_req6(c1, c2):
    """Descendente por eficiencia. Empate: Precio ascendente."""
    s1, s2 = float(c1["efficient_score"]), float(c2["efficient_score"])
    if s1 != s2:
        return s1 > s2
    return float(c1["price"]) < float(c2["price"])

def req_6(catalog, n_top, form_factor, screen_type, y_min, y_max):
    inicio = get_time()
    filtrados = al.new_list()
    win, lin = 0, 0

    size = al.size(catalog["computer"])
    for i in range(size):
        c = al.get_element(catalog["computer"], i)
        if (c["form_factor"].lower() == form_factor.lower() and 
            c["display_type"].lower() == screen_type.lower() and 
            int(y_min) <= int(c["release_year"]) <= int(y_max)):
            
            # Cálculo Eficiencia = (Battery_wh * CPU_Boost) / Charger_Watts
            bat, bst, wts = float(c["battery_wh"]), float(c["cpu_boost_ghz"]), float(c["charger_watts"])
            c["efficient_score"] = (bat * bst) / wts if wts > 0 else 0
            
            al.add_last(filtrados, c)
            if "windows" in c["os"].lower(): win += 1
            elif "linux" in c["os"].lower(): lin += 1

    ordenados = ms.sort(filtrados, compare_req6)
    
    top_final = []
    limite = min(int(n_top), al.size(ordenados))
    for i in range(limite):
        top_final.append(al.get_element(ordenados, i))

    return {
        "tiempo": delta_time(inicio, get_time()),
        "total": al.size(ordenados),
        "windows": win,
        "linux": lin,
        "top": top_final
    }

# Funciones para medir tiempos de ejecucion

def get_time():
    return time.perf_counter() * 1000

def delta_time(start, end):
    return end - start