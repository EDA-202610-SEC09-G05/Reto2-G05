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

    top5 = [format_output(c) for c in lista_temp[:5]]
    bottom5 = [format_output(c) for c in lista_temp[-5:]]

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

def req_1(catalog):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
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
