import time
import csv
from DataStructures.List import array_list as al
from DataStructures.List import single_linked_list as sl
from DataStructures.List import list_node as n
from DataStructures.Set import set as s

def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    catalog = {
        "computer": al.new_list(),
        "brandCPU": {},
        "year": {},
        "brand": {},
        "gpu_model": {},
        "form_factor": {},
        "os": {},
        "brandGPU": s.new_set(),
        "resolution": s.new_set()
    }
    return catalog


# Funciones para la carga de datos

def load_data(catalog, size):
    """
    Carga los datos del reto
    """
    inicio = get_time()
    url = f"./Data/computer_prices_{size}.csv"

    max_precio = {"price": float("-inf")}
    min_precio = {"price": float("inf")}
    min_year = float("inf")
    max_year = float("-inf")

    total = 0
    os_count = {}

    lista_temp = []

    with open(url, encoding="utf-8") as f:
        filas = csv.DictReader(f)

        for comp in filas:
            al.add_last(catalog["computer"], comp)
            lista_temp.append(comp)
            total += 1

            # tus cargas
            load_brands(catalog, comp)
            load_years(catalog, comp)
            load_brands_cpu(catalog, comp)
            load_brands_gpu(catalog, comp)
            load_resolutions(catalog, comp)

            load_gpu_model(catalog, comp)
            load_form_factor(catalog, comp)
            load_os(catalog, comp)

            price = float(comp["price"])
            year = int(comp["release_year"])

            if price < float(min_precio["price"]):
                min_precio = comp
            if price > float(max_precio["price"]):
                max_precio = comp

            if year < min_year:
                min_year = year
            if year > max_year:
                max_year = year

            os_name = comp["os"]
            if os_name not in os_count:
                os_count[os_name] = 0
            os_count[os_name] += 1

    lista_temp = sort_computers(lista_temp)

    # -------- TOP 5 --------
    top5 = []
    i = 0

    while i < 5 and i < len(lista_temp):
        top5.append(format_output(lista_temp[i]))
        i += 1

    # -------- BOTTOM 5 --------
    # -------- BOTTOM 5 --------
    bottom5 = []
    i = len(lista_temp) - 1
    count = 0

    while count < 5 and i >= 0:
        bottom5.insert(0, format_output(lista_temp[i]))  
        i -= 1
        count += 1

    dtime = delta_time(inicio, get_time())

    return catalog, dtime, total, os_count, min_year, max_year, min_precio, max_precio, top5, bottom5

def format_output(comp):
    return {
        "brand": comp["brand"],
        "model": comp["model"],
        "device_type": comp["device_type"],
        "cpu_model": comp["cpu_model"],
        "ram_gb": comp["ram_gb"],
        "storage_capacity": comp["storage_gb"],
        "release_year": comp["release_year"],
        "price": comp["price"]
    }
    
def sort_computers(lista):
    size = len(lista)

    for i in range(1, size):
        actual = lista[i]
        j = i - 1

        while j >= 0 and compare_computers(actual, lista[j]):
            lista[j + 1] = lista[j]
            j -= 1

        lista[j + 1] = actual

    return lista

def compare_computers(c1, c2):
    """
    Retorna True si c1 debe ir antes que c2
    Orden:
    1. Precio DESC
    2. Modelo ASC
    """
    price1 = float(c1["price"])
    price2 = float(c2["price"])
    # mayor precio primero
    if price1 > price2:
        return True
    if price1 < price2:
        return False
    # empate 
    if c1["model"] < c2["model"]:
        return True
    else:
        return False
    
def load_brands(catalog, comp):
    brands = catalog["brand"]
    brand = comp["brand"].lower()

    if brand not in brands:
        brands[brand] = sl.new_list()
    sl.add_last(brands[brand], comp)
    return catalog


def load_years(catalog, comp):
    years = catalog["year"]
    year = comp["release_year"]

    if year not in years:
        years[year] = sl.new_list()
    sl.add_last(years[year], comp)
    return catalog


def load_brands_cpu(catalog, comp):
    brands = catalog["brandCPU"]
    brand = comp["cpu_brand"].lower()

    if brand not in brands:
        brands[brand] = al.new_list()
    al.add_last(brands[brand], comp)
    return catalog

def load_brands_gpu(catalog, comp):
    # si quieres mantener set como en reto 1
    # asegúrate de tener "brandGPU" en new_logic
    if "brandGPU" not in catalog:
        catalog["brandGPU"] = s.new_set()

    brand = comp["gpu_brand"].lower()
    s.add_element(catalog["brandGPU"], brand)
    return catalog


def load_resolutions(catalog, comp):
    if "resolution" not in catalog:
        catalog["resolution"] = s.new_set()

    resolution = comp["resolution"]
    s.add_element(catalog["resolution"], resolution)
    return catalog

def load_gpu_model(catalog, comp):
    gpu = comp["gpu_model"].lower()

    if gpu not in catalog["gpu_model"]:
        catalog["gpu_model"][gpu] = sl.new_list()
    sl.add_last(catalog["gpu_model"][gpu], comp)
    return catalog


def load_form_factor(catalog, comp):
    form = comp["form_factor"].lower()

    if form not in catalog["form_factor"]:
        catalog["form_factor"][form] = sl.new_list()
    sl.add_last(catalog["form_factor"][form], comp)
    return catalog


def load_os(catalog, comp):
    os_name = comp["os"]

    if os_name not in catalog["os"]:
        catalog["os"][os_name] = sl.new_list()
    sl.add_last(catalog["os"][os_name], comp)
    return catalog

def req_1(control, brand, form_factor):
    time_start = get_time()
    sl_brands = catalog["brand"][brand]
    precios = 0
    
    comp_filter = al.new_list()
    for comp in sl_brands["elements"]:
        if comp["form_factor"].lower() == form_factor:
            al.add_last(comp_filter, comp)
            precios += float(comp["price"])
    comp_filter = sort.merge_sort(comp_filter, compare_computers, al)
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

    pass

def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog, cpu_brand, gpu_model):
    time_start = get_time()
    count = 0
    precios = 0
    ram = 0
    vram = 0
    boost = 0
    mayor_precio1 = None
    mayor_precio2 = None
    
    comps_gpu = catalog["gpu_model"][gpu_model]
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
