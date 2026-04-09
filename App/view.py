import sys
from tabulate import tabulate
from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as lp
from DataStructures.Set import set as s
from DataStructures.Map import map_separate_chaining as sc

from App import logic as l

def new_logic():
    """
        Se crea una instancia del controlador
    """
    return l.new_logic()

def print_menu():
    print("Bienvenido")
    print("0- Cargar información")
    print("1- Ejecutar Requerimiento 1")
    print("2- Ejecutar Requerimiento 2")
    print("3- Ejecutar Requerimiento 3")
    print("4- Ejecutar Requerimiento 4")
    print("5- Ejecutar Requerimiento 5")
    print("6- Ejecutar Requerimiento 6")
    print("7- Salir")

def load_data(control):
    """
    Gestiona la carga de datos y muestra los resultados estadísticos.
    """
    while True:
        opcion = input("\nIngrese el tamaño de la muestra (ej: 10, 20, 100): ")
        if opcion.isdigit():
            break
        print("Error: Por favor ingrese un número válido.")

    print("\nCargando información de los archivos... ")
    
    # Llamado a la lógica optimizada
    data = l.load_data(control, opcion)

    (catalog, dtime, total, os_count, min_year, max_year, 
     min_precio, max_precio, top5, bottom5) = data

    # 1. RESUMEN DE CARGA
    print("\n" + "=" * 80)
    print("                 RESUMEN DE CARGA DE DATOS")
    print("=" * 80)

    resumen = [
        ["Tiempo de carga", f"{round(dtime, 2)} ms"],
        ["Total registros", f"{total:,}"],
        ["Año mínimo", min_year],
        ["Año máximo", max_year],
        ["Precio mínimo", f"${float(min_precio['price']):,.2f}"],
        ["Precio máximo", f"${float(max_precio['price']):,.2f}"]
    ]
    print(tabulate(resumen, headers=["Campo", "Valor"], tablefmt="fancy_grid"))

    # 2. TABLA DE LOS PRIMEROS 5 (TOP)
    print("\nPrimeros cinco computadores cargados (en orden descendente por precio):")
    if top5:
        print(tabulate(top5, headers="keys", tablefmt="fancy_grid"))
    else:
        print("No hay datos para mostrar.")

    # 3. TABLA DE LOS ÚLTIMOS 5 (BOTTOM)
    print("\nÚltimos cinco computadores cargados (en orden descendente por precio):")
    if bottom5:
        print(tabulate(bottom5, headers="keys", tablefmt="fancy_grid"))
    else:
        print("No hay datos para mostrar.")

    # 4. DISTRIBUCIÓN OS
    print("\nDISTRIBUCIÓN POR SISTEMA OPERATIVO")
    rows_os = []
    for os_name in ["macOS","Windows","ChromeOS","Linux"]:
        rows_os.append([os_name, lp.get(os_count, os_name)])
    
    # Ordenar por cantidad de mayor a menor
    print(tabulate(rows_os, headers=["OS", "Cantidad"], tablefmt="fancy_grid"))

    return catalog

def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    while True:
        brand = input("Ingrese la marca: ").strip().lower()
        form_factor = input("Ingrese el factor de forma: ").strip().lower()
        if sc.contains(control['brand'], brand) and sc.contains(control['form_factor'], form_factor):
            break
        print("Marca o factor de forma no encontrada, vuelva a ingresar.\n")
    
    lista_resultado, lista_computadores = l.req_1(control, brand, form_factor)
    print("\n" + "=" * 80)
    print(f"RESULTADO REQUERIMIENTO 1 - Marca: {brand} | Factor de forma: {form_factor}")
    print("=" * 80)
    print(tabulate(lista_resultado, headers=["Campo", "Valor"], tablefmt="fancy_grid"))
    print("\n" + "=" * 80)
    print("COMPUTADORAS FILTRADAS")
    print("=" * 80)
    print(tabulate(lista_computadores, headers=["Computadora", "Detalles"], tablefmt="fancy_grid"))

    return control

def print_req_2(control):
    print("\n" + "=" * 80)
    print("      REQUERIMIENTO 2: EQUIPOS MÁS LIGEROS POR NÚCLEOS Y AÑO")
    print("=" * 80)

    num_nucleos = input("Ingrese el número de núcleos: ")
    anio_lanzamiento = input("Ingrese el año de lanzamiento: ")

    dtime, total, promedio_peso, lista_resultados = l.req_2(
        control, num_nucleos, anio_lanzamiento
    )

    resumen_req = [
        ["Total encontrados", total],
        ["Peso promedio (kg)", round(promedio_peso, 2)],
        ["Tiempo de ejecución", f"{round(dtime, 2)} ms"]
    ]
    print(tabulate(resumen_req, headers=["Campo", "Valor"], tablefmt="fancy_grid"))

    if total > 0:
        resultados_py = []
        for i in range(al.size(lista_resultados)):
            resultados_py.append(al.get_element(lista_resultados, i))

        tabla = []
        for c in resultados_py:
            tabla.append([
                c["device_type"],
                c["model"],
                c["os"],
                c["cpu_brand"],
                c["ram_gb"],
                c["storage_gb"],
                c["weight_kg"]
            ])

        headers = [
            "Tipo de dispositivo",
            "Modelo",
            "Sistema Operativo",
            "Marca CPU",
            "RAM (GB)",
            "Almacenamiento (GB)",
            "Peso (kg)"
        ]

        if total > 20:
            print("\n>>> Los 10 más livianos:")
            print(tabulate(tabla[:10], headers=headers, tablefmt="fancy_grid"))

            print("\n>>> Los 10 más pesados:")
            print(tabulate(tabla[-10:], headers=headers, tablefmt="fancy_grid"))
        else:
            print(tabulate(tabla, headers=headers, tablefmt="fancy_grid"))
    else:
        print("\nNo se encontraron resultados.")

def print_req_3(control):
    print("\n" + "=" * 90)
    print("      REQUERIMIENTO 3: TOP N EQUIPOS MÁS COSTOSOS POR MARCA Y GPU")
    print("=" * 90)

    while True:
        brand = input("Ingrese la marca del equipo: ").strip().lower()
        gpu_model = input("Ingrese el modelo de la GPU: ").strip().lower()
        key = (brand + gpu_model).strip()

        if sc.contains(control["brand_gpu"], key):
            break
        print("Combinación Marca + GPU no encontrada.\n")

    n = int(input("Ingrese el número de equipos a listar (N): "))

    tiempo, total, promedio_ram, resultados = l.req_3(
        control, n, brand, gpu_model
    )

    # ✅ AQUÍ estaba el problema: ahora SI se imprime siempre
    print(f"\nTiempo de ejecución: {round(tiempo, 2)} ms")
    print(f"Total equipos encontrados: {total}")
    print(f"Promedio RAM: {promedio_ram} GB\n")

    if total == 0:
        print("No hay resultados para mostrar.")
        return control

    tabla = []
    for c in resultados:
        tabla.append([
            c["device_type"],
            c["model"],
            c["ram_gb"],
            c["storage_gb"],
            c["gpu_brand"],
            c["gpu_model"],
            c["weight_kg"],
            f"${float(c['price']):,.2f}"
        ])

    headers = [
        "Tipo",
        "Modelo",
        "RAM (GB)",
        "Almacenamiento (GB)",
        "Marca GPU",
        "Modelo GPU",
        "Peso (kg)",
        "Precio"
    ]

    print(tabulate(tabla, headers=headers, tablefmt="grid", stralign="center"))
    return control


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    while True:
        cpu_brand = input("Ingrese la marca del CPU: ").strip().lower()
        gpu_model = input("Ingrese el modelo de GPU: ").strip().lower()
        if sc.contains(control['gpu_model'], gpu_model) and lp.contains(control['cpu_brand'], cpu_brand):
            break
        print("Modelo de GPU o marca de CPU no encontrado, vuelva a ingresar.\n")
        
    lista_resultado, lista_computadores = l.req_4(control, cpu_brand, gpu_model)
    print("\n" + "=" * 80)
    print(f"RESULTADO REQUERIMIENTO 4 - CPU: {cpu_brand} | GPU: {gpu_model}")
    print("=" * 80)
    print(tabulate(lista_resultado, headers=["Campo", "Valor"], tablefmt="fancy_grid", floatfmt=".2f"))
    print("\n" + "=" * 80)
    print("COMPUTADORAS MÁS CARAS")
    print("=" * 80)
    print(tabulate(lista_computadores, headers=["Computadora", "Detalles"], tablefmt="fancy_grid"))
    
    return control


def print_req_5(control):
    """
    Función que imprime la solución del Requerimiento 5 en consola.
    """

    print("\n" + "=" * 100)
    print("      REQUERIMIENTO 5: TOP N EQUIPOS MEJOR EQUIPADOS")
    print("=" * 100)

    # -------------------------------
    # 1. Captura y validación de datos
    # -------------------------------
    while True:
        brand = input("Ingrese la marca del equipo: ").strip().lower()
        form_factor = input("Ingrese el factor de forma (ej: gaming, atx): ").strip().lower()
        key = (brand + form_factor).strip()

        if sc.contains(control["brand_form_map"], key):
            break
        print("Combinación Marca + Factor de Forma no encontrada.\n")

    try:
        y_init = int(input("Ingrese el año de lanzamiento inicial: "))
        y_end = int(input("Ingrese el año de lanzamiento final: "))
        n = int(input("Ingrese el número de computadores a listar (N): "))
    except ValueError:
        print("Error: Los valores deben ser numéricos.")
        return control

    # -------------------------------
    # 2. Llamado a la lógica
    # -------------------------------
    tiempo, total, intel, amd, resultados = l.req_5(
        control, n, y_init, y_end, brand, form_factor
    )

    # -------------------------------
    # 3. Resumen
    # -------------------------------
    print("\n" + "=" * 100)
    print(f"RESULTADOS REQ 5 | Marca: {brand.upper()} | Forma: {form_factor.upper()}")
    print("=" * 100)

    resumen = [
        ["Tiempo de ejecución (ms)", round(tiempo, 2)],
        ["Total de computadores", total],
        ["Computadores con CPU Intel", intel],
        ["Computadores con CPU AMD", amd]
    ]

    print(tabulate(resumen, headers=["Campo", "Valor"], tablefmt="grid"))

    if total == 0:
        print("\nNo se encontraron computadores que cumplan los criterios.")
        return control

    # -------------------------------
    # 4. Construcción de la tabla (UNA SOLA VEZ)
    # -------------------------------
    tabla = []
    for comp in resultados:
        tabla.append([
            comp["device_type"],
            comp["model"],
            comp["ram_gb"],
            comp["cpu_boost_ghz"],
            f"${float(comp['price']):,.2f}",
            comp["release_year"],
            comp["cpu_brand"],
            comp["cpu_model"]
        ])

    headers = [
        "Tipo",
        "Modelo",
        "RAM (GB)",
        "Boost CPU (GHz)",
        "Precio",
        "Año",
        "CPU Brand",
        "CPU Model"
    ]

    print("\nTOP N DE EQUIPOS MEJOR EQUIPADOS:\n")
    print(tabulate(tabla, headers=headers, tablefmt="grid", stralign="center"))

    return control



def print_req_6(control):
    print("\n" + "=" * 80)
    print("      REQUERIMIENTO 6: TOP N EQUIPOS CON MEJOR EFICIENCIA ENERGÉTICA")
    print("=" * 80)

    try:
        n_top = int(input("Ingrese el número de equipos a listar (N): "))
        form_factor = input("Ingrese el factor de forma (ej: laptop, ultrabook): ").strip().lower()
        screen_type = input("Ingrese el tipo de pantalla (ej: IPS, OLED): ").strip().lower()
        y_min = int(input("Ingrese el año inicial: "))
        y_max = int(input("Ingrese el año final: "))
    except ValueError:
        print("Error: Los valores deben ser numéricos.")
        return control

    res = l.req_6(control, n_top, form_factor, screen_type, y_min, y_max)

    resumen = [
        ["Tiempo de ejecución (ms)", round(res["tiempo"], 2)],
        ["Total de equipos", res["total"]],
        ["Equipos con Windows", res["windows"]],
        ["Equipos con Linux", res["linux"]]
    ]

    print("\nRESUMEN DE RESULTADOS:\n")
    print(tabulate(resumen, headers=["Campo", "Valor"], tablefmt="grid"))

    if len(res["top"]) == 0:
        print("\nNo se encontraron equipos que cumplan los criterios.")
        return control

    tabla = []
    for c in res["top"]:
        tabla.append([
            c["model"],
            c["ram_gb"],
            c["cpu_model"],
            c["cpu_boost_ghz"],
            round(c["efficient_score"], 3)
        ])

    headers = [
        "Modelo",
        "RAM (GB)",
        "Modelo CPU",
        "CPU Boost (GHz)",
        "Puntaje de eficiencia"
    ]

    print("\nTOP N DE EQUIPOS MÁS EFICIENTES:\n")
    print(tabulate(tabla, headers=headers, tablefmt="grid", stralign="center"))

    return control


# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 0:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 1:
            print_req_1(control)

        elif int(inputs) == 2:
            print_req_2(control)

        elif int(inputs) == 3:
            print_req_3(control)

        elif int(inputs) == 4:
            print_req_4(control)

        elif int(inputs) == 5:
            print_req_5(control)

        elif int(inputs) == 6:
            print_req_6(control)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
