import time
import csv
from DataStructures.List import array_list as al
from DataStructures.List import single_linked_list as sl
from DataStructures.List import list_node as n
from DataStructures.Set import set as s

def get_time():
    return time.perf_counter() * 1000

def delta_time(start, end):
    return end - start

def new_logic():
    """
    Crea el catálogo con las estructuras de datos vacías.
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

def criterio_orden(comp):
    """
    Criterio de ordenamiento sin lambda:
    1. Precio descendente.
    2. Modelo ascendente en caso de empate.
    """
    return -float(comp["price"]), comp["model"]

def format_output(comp):
    """
    Formatea el diccionario para la presentación en tablas.
    """
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

def load_data(catalog, size):
    """
    Carga de datos ultra eficiente (artesanal).
    """
    inicio = get_time()
    url = f"./Data/computer_prices_{size}.csv"

    # Variables de resumen inicializadas
    max_precio = {"price": float("-inf")}
    min_precio = {"price": float("inf")}
    min_year = float("inf")
    max_year = float("-inf")
    total = 0
    os_count = {}
    lista_temp = []

    # Referencias locales para evitar búsquedas repetitivas en el catálogo
    cat_comp = catalog["computer"]
    cat_brand = catalog["brand"]
    cat_year = catalog["year"]
    cat_bcpu = catalog["brandCPU"]
    cat_bgpu = catalog["brandGPU"]
    cat_res = catalog["resolution"]
    cat_gmod = catalog["gpu_model"]
    cat_form = catalog["form_factor"]
    cat_os = catalog["os"]

    with open(url, encoding="utf-8") as f:
        filas = csv.DictReader(f)
        for comp in filas:
            # 1. Almacenamiento base
            al.add_last(cat_comp, comp)
            lista_temp.append(comp)
            total += 1

            # 2. Conversiones únicas y estadísticas
            current_price = float(comp["price"])
            current_year = int(comp["release_year"])

            if current_price < float(min_precio["price"]): min_precio = comp
            if current_price > float(max_precio["price"]): max_precio = comp
            if current_year < min_year: min_year = current_year
            if current_year > max_year: max_year = current_year

            # 3. Conteo de Sistemas Operativos
            os_name = comp["os"]
            os_count[os_name] = os_count.get(os_name, 0) + 1

            # 4. CARGAS ARTESANALES (Directas en estructuras)
            # Marcas
            b_name = comp["brand"].lower()
            if b_name not in cat_brand: cat_brand[b_name] = sl.new_list()
            sl.add_last(cat_brand[b_name], comp)
            
            # Años
            y_val = comp["release_year"]
            if y_val not in cat_year: cat_year[y_val] = sl.new_list()
            sl.add_last(cat_year[y_val], comp)
            
            # CPU
            bc_name = comp["cpu_brand"].lower()
            if bc_name not in cat_bcpu: cat_bcpu[bc_name] = al.new_list()
            al.add_last(cat_bcpu[bc_name], comp)
            
            # Sets (GPU Brand y Resolution)
            s.add_element(cat_bgpu, comp["gpu_brand"].lower())
            s.add_element(cat_res, comp["resolution"])
            
            # Resto de estructuras (GPU Model, Form Factor, OS)
            # OS se procesa sin .lower() para mantener consistencia con os_count
            for key, target_map in [("gpu_model", cat_gmod), ("form_factor", cat_form), ("os", cat_os)]:
                val = comp[key].lower() if key != "os" else comp[key]
                if val not in target_map: target_map[val] = sl.new_list()
                sl.add_last(target_map[val], comp)

    # --- ORDENAMIENTO EFICIENTE ---
    lista_temp.sort(key=criterio_orden)

    # --- TOP 5 Y BOTTOM 5 ---
    top5 = []
    n_records = len(lista_temp)
    for i in range(min(5, n_records)):
        top5.append(format_output(lista_temp[i]))
    
    bottom5 = []
    idx_inicio_bottom = max(0, n_records - 5)
    # Recorremos de atrás hacia adelante para que el más barato sea el primero del bottom
    for i in range(n_records - 1, idx_inicio_bottom - 1, -1):
        bottom5.append(format_output(lista_temp[i]))

    dtime = delta_time(inicio, get_time())
    
    return (catalog, dtime, total, os_count, min_year, max_year, 
            min_precio, max_precio, top5, bottom5)
    

    

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
