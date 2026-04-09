import time
import csv
import sys

# Configuración obligatoria PDF pág. 11
csv.field_size_limit(2147483647)
sys.setrecursionlimit(10000)

from DataStructures.Map import map_separate_chaining as sc 
from DataStructures.Map import map_linear_probing as lp 
from DataStructures.List import array_list as al
from DataStructures.List import single_linked_list as sl
# Importa la función merge_sort desde tu archivo sort.py y dale el alias 'ms'
from DataStructures.List.sort import merge_sort as ms
from DataStructures.List.sort import quick_sort as qs
from tabulate import tabulate


def new_logic():
    return {
        "computer": al.new_list(),
        "year": lp.new_map(500, 0.5),
        "brand": sc.new_map(500, 0.5),
        "cpu_brand": lp.new_map(500, 0.5),
        "gpu_model": sc.new_map(500, 0.5),
        "form_factor": sc.new_map(500, 0.5),
        "os": lp.new_map(500, 0.5),
        "brand_gpu": sc.new_map(500, 0.5)
    }

def load_year(catalog, comp):
    year = comp["release_year"].lower()
    years = catalog["year"]
    if not lp.contains(years,year):
        lp.put(years,year,al.new_list())
    al.add_last(lp.get(years,year),comp)
    pass

def load_brand(catalog, comp):
    brand = comp["brand"].lower()
    brands = catalog["brand"]
    if not sc.contains(brands,brand):
        sc.put(brands,brand,al.new_list())
    al.add_last(sc.get(brands,brand),comp)
    pass

def load_cpu_brand(catalog, comp):
    cpu_brand = comp["cpu_brand"].lower()
    cpu_brands = catalog["cpu_brand"]
    if not lp.contains(cpu_brands,cpu_brand):
        lp.put(cpu_brands,cpu_brand,al.new_list())
    al.add_last(lp.get(cpu_brands,cpu_brand),comp)
    pass

def load_gpu_model(catalog, comp):
    gpu_model = comp["gpu_model"].lower()
    gpu_models = catalog["gpu_model"]
    if not sc.contains(gpu_models,gpu_model):
        sc.put(gpu_models,gpu_model,al.new_list())
    al.add_last(sc.get(gpu_models,gpu_model),comp)
    pass

def load_form_factor(catalog, comp):
    form_factor = comp["form_factor"].lower()
    form_factors = catalog["form_factor"]
    if not sc.contains(form_factors,form_factor):
        sc.put(form_factors,form_factor,al.new_list())
    al.add_last(sc.get(form_factors,form_factor),comp)
    pass

def load_os(catalog, comp):
    os = comp["os"].lower()
    oss = catalog["os"]
    if not lp.contains(oss,os):
        lp.put(oss,os,al.new_list())
    al.add_last(lp.get(oss,os),comp)
    pass

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
    
    max_p, min_p = None, None
    min_y, max_y = 9999, 0
    total = 0
    os_count = lp.new_map(10, 0.5)

    # 1. Lectura del archivo
    with open(url, encoding="utf-8") as f:
        filas = csv.DictReader(f)
        for comp in filas:
            # Guardamos en el catálogo original (ArrayList)
            al.add_last(catalog["computer"], comp)
            # Guardamos en lista temporal para los Tops
            total += 1
            
            y_actual = int(comp["release_year"])
            
            # Estadísticas básicas
            if compare_comp2(comp, max_p): max_p = comp
            if compare_comp(comp, min_p): min_p = comp
            if y_actual < min_y: min_y = y_actual
            if y_actual > max_y: max_y = y_actual
            
            # Conteo de OS
            os_name = comp["os"]
            if not lp.contains(os_count,os_name):
                lp.put(os_count, os_name, 0)
            num = lp.get(os_count,os_name)
            lp.put(os_count,os_name,num+1)
            
            load_brand(catalog, comp)
            load_cpu_brand(catalog, comp)
            load_form_factor(catalog, comp)
            load_gpu_model(catalog, comp)
            load_os(catalog, comp)
            load_year(catalog, comp)
            
            key = (comp["brand"].lower() + comp["gpu_model"].lower()).strip()
            if not sc.contains(catalog["brand_gpu"], key):
                sc.put(catalog["brand_gpu"], key, al.new_list())
            al.add_last(sc.get(catalog["brand_gpu"], key), comp)


    prim5 = al.sub_list(catalog["computer"], 0, 5)
    ult5 = al.sub_list(catalog["computer"], al.size(catalog["computer"])-5,5)
    ms(prim5,compare_comp2,al)
    ms(ult5,compare_comp2,al)
    
    print_first5 = []   
    for c in prim5["elements"]:
        print_first5.append({
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
    print_last5 = []

    for c in ult5["elements"]:

        print_last5.append({
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
            min_p, max_p, print_first5, print_last5)


def compare_comp(c1, c2):
    """Descendente por precio. Empate: Ascendente por modelo."""
    if c2 is None: return True 
    p1, p2 = float(c1["price"]), float(c2["price"])
    if p1 != p2:
        return p1 < p2
    return c1["model"] < c2["model"]

def compare_comp2(c1, c2):
    """Descendente por precio. Empate: Ascendente por modelo."""
    if c2 is None: return True 
    p1, p2 = float(c1["price"]), float(c2["price"])
    if p1 != p2:
        return p1 > p2
    return c1["model"] < c2["model"]

def compare_computers_w(c1, c2):
    if c2 is None:
        return True

    price1 = float(c1["price"])
    price2 = float(c2["price"])
    weight1 = float(c1["weight_kg"])
    weight2 = float(c2["weight_kg"])

    if price1 > price2:
        return True
    if price1 < price2:
        return False

    return weight1 < weight2

def req_1(catalog, brand, form_factor):
    time_start = get_time()
    sl_brands = sc.get(catalog["brand"],brand)
    precios = 0
    
    comp_filter = al.new_list()
    for comp in sl_brands["elements"]:
        if comp["form_factor"].lower() == form_factor:
            al.add_last(comp_filter, comp)
            precios += float(comp["price"])
    comp_filter = ms(comp_filter, compare_req2, al)
    promedio_precios = precios / al.size(comp_filter) if al.size(comp_filter) > 0 else 0
    total = al.size(comp_filter)

    if comp_filter["size"] > 20:
        lista1 = al.sub_list(comp_filter, 0, 10)
        lista2 = al.sub_list(comp_filter, comp_filter["size"] - 10, 10)
        lista1 = al.join_lists(lista1, lista2)
    else:
        lista1 = comp_filter
    
    lista_resultado = [
        ["Tiempo de ejecución (ms)", delta_time(time_start, get_time())],
        ["Total de computadoras", total],
        ["Promedio de precios", promedio_precios]
    ]
    
    lista_computadores = [
        [
            f"Computador {i+1}",
            tabulate([
                ['Tipo de dispositivo', comp["device_type"]],
                ['Modelo', comp["model"]],
                ['Sistema Operativo', comp["os"]],
                ['Marca CPU', comp["cpu_brand"]],
                ['RAM (GB)', comp["ram_gb"]],
                ['Almacenamiento (GB)', comp["storage_gb"]],
                ['Precio', comp["price"]]
            ], tablefmt='grid')
        ] for i, comp in enumerate(lista1["elements"])
    ]
    return lista_resultado, lista_computadores

def compare_req2(c1, c2):
    """Ascendente por peso. Empate: Ascendente por modelo."""
    w1, w2 = float(c1["weight_kg"]), float(c2["weight_kg"])
    if w1 != w2:
        return w1 < w2
    return c1["model"] < c2["model"]

def req_2(catalog, num_nucleos, anio_lanzamiento):
    inicio = get_time()
    l_anio = lp.get(catalog["year"], str(anio_lanzamiento))
    filtrados = al.new_list()
    suma_peso = 0
    
    if l_anio:
        actual = l_anio["elements"]
        for c in actual:
            if int(c["cpu_cores"]) == int(num_nucleos):
                al.add_last(filtrados, c)
                suma_peso += float(c["weight_kg"])

    n = al.size(filtrados)
    promedio = suma_peso / n if n > 0 else 0
    ordenados = ms(filtrados, compare_req2, al)
    
    return delta_time(inicio, get_time()), n, round(promedio, 2), ordenados



def compare_req3(c1, c2):
    """Precio desc. Empate: peso desc."""
    p1, p2 = float(c1["price"]), float(c2["price"])
    if p1 != p2:
        return p1 > p2
    return float(c1["weight_kg"]) > float(c2["weight_kg"])


def req_3(catalog, n, brand, gpu_model):
    inicio = get_time()
    key = (brand.lower() + gpu_model.lower()).strip()

    lista = sc.get(catalog["brand_gpu"], key)
    if not lista or al.size(lista) == 0:
        return delta_time(inicio, get_time()), 0, 0, []

    # Ordenar
    qs.quick_sort(lista, compare_req3, al)

    total = al.size(lista)
    suma_ram = 0
    top_n = []

    limite = min(int(n), total)
    for i in range(total):
        c = al.get_element(lista, i)
        suma_ram += int(c["ram_gb"])
        if i < limite:
            top_n.append(c)

    promedio_ram = suma_ram / total if total > 0 else 0

    return delta_time(inicio, get_time()), total, round(promedio_ram, 2), top_n


def compare_req4(c1, c2):
    """Descendente por precio. Empate: Menor peso primero."""
    p1, p2 = float(c1["price"]), float(c2["price"])
    if p1 != p2:
        return p1 > p2
    return float(c1["weight_kg"]) < float(c2["weight_kg"])


def req_4(catalog, cpu_brand, gpu_model):
    time_start = get_time()
    count = 0
    precios = 0
    ram = 0
    vram = 0
    boost = 0
    mayor_precio1 = None
    mayor_precio2 = None
    
    comps_gpu = sc.get(catalog["gpu_model"],gpu_model)
    for comp in comps_gpu["elements"]:
        if comp["cpu_brand"].lower() == cpu_brand:
            count += 1
            precios += float(comp["price"])
            ram += int(comp["ram_gb"])
            vram += int(comp["vram_gb"])
            boost += float(comp["cpu_boost_ghz"])
            
            if compare_computers_w(comp, mayor_precio1):
                mayor_precio2 = mayor_precio1
                mayor_precio1 = comp
            elif comp is not mayor_precio1 and compare_computers_w(comp, mayor_precio2):
                mayor_precio2 = comp
                
    promedio_precios = precios / count if count > 0 else 0
    promedio_ram = ram / count if count > 0 else 0
    promedio_vram = vram / count if count > 0 else 0
    promedio_boost = boost / count if count > 0 else 0
    
    lista_resultado = [
        ["Tiempo de ejecución (ms)", delta_time(time_start, get_time())],
        ["Total de computadoras", count],
        ["Promedio de precios", promedio_precios],
        ["Promedio de VRAM (GB)", promedio_vram],
        ["Promedio de RAM (GB)", promedio_ram],
        ["Promedio de GPU Boost Clock (GHz)", promedio_boost]
    ]
    
    lista_computadores = [
        [
            "Primer Computador mas Caro",
            tabulate([
                ['Modelo', mayor_precio1["model"] if mayor_precio1 else "N/A"],
                ['Marca', mayor_precio1["brand"] if mayor_precio1 else "N/A"],
                ['Año de Lanzamiento', mayor_precio1["release_year"] if mayor_precio1 else "N/A"],
                ['Modelo CPU', mayor_precio1["cpu_model"] if mayor_precio1 else "N/A"],
                ['Precio', mayor_precio1["price"] if mayor_precio1 else "N/A"]
            ], tablefmt='grid')
        ],
        [
            "Segundo Computador mas Caro",
            tabulate([
                ['Modelo', mayor_precio2["model"] if mayor_precio2 else "N/A"],
                ['Marca', mayor_precio2["brand"] if mayor_precio2 else "N/A"],
                ['Año de Lanzamiento', mayor_precio2["release_year"] if mayor_precio2 else "N/A"],
                ['Modelo CPU', mayor_precio2["cpu_model"] if mayor_precio2 else "N/A"],
                ['Precio', mayor_precio2["price"] if mayor_precio2 else "N/A"]
            ], tablefmt='grid')
        ]
    ]

    return lista_resultado, lista_computadores


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