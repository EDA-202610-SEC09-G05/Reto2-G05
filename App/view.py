import sys
from tabulate import tabulate
from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as lp
from DataStructures.Set import set as s
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
        if brand in control['brand'] and form_factor in control['form_factor']:
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

    # Llamado a la lógica
    dtime, total, promedio_peso, lista_resultados = l.req_2(
        control, num_nucleos, anio_lanzamiento
    )

    # Resumen del requerimiento (según PDF)
    resumen_req = [
        ["Total encontrados", total],
        ["Peso promedio (kg)", round(promedio_peso, 2)],
        ["Tiempo de ejecución", f"{round(dtime, 2)} ms"]
    ]
    print(tabulate(resumen_req, headers=["Campo", "Valor"], tablefmt="fancy_grid"))

    if total > 0:
        # Convertir array_list a lista de Python
        resultados_py = []
        for i in range(al.size(lista_resultados)):
            resultados_py.append(al.get_element(lista_resultados, i))

        # Construir tabla SOLO con las columnas pedidas en el PDF
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
        if key in control["brand_gpu"]:
            break
        print("Combinación Marca + GPU no encontrada.\n")

    n = int(input("Ingrese el número de equipos a listar (N): "))

    tiempo, total, promedio_ram, resultados = l.req_3(
        control, n, brand, gpu_model
    )

    print(f"\nTiempo: {round(tiempo, 2)} ms")
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

    print(tabulate(tabla, headers=headers, tablefmt="fancy_grid"))
    return control

def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    while True:
        cpu_brand = input("Ingrese la marca del CPU: ").strip().lower()
        gpu_model = input("Ingrese el modelo de GPU: ").strip().lower()
        if gpu_model in control['gpu_model'] and cpu_brand in control['brandCPU']:
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
    Función que imprime la solución del Requerimiento 5 en consola
    """
    while True:
        brand = input("Ingrese la marca del equipo: ").strip().lower()
        form_factor = input("Ingrese el factor de forma (ej: ultrabook): ").strip().lower()
        
        # Validar usando la llave compuesta Marca + Forma
        llave_busqueda = (brand + form_factor).strip()
        if llave_busqueda in control['brand_form_map']:
            break
        print("Combinación de Marca y Factor de Forma no encontrada, vuelva a ingresar.\n")
    
    y_init = int(input("Ingrese el año de lanzamiento inicial: "))
    y_end = int(input("Ingrese el año de lanzamiento final: "))
    n = int(input("Ingrese el número de computadores a listar (N): "))

    # Llamado a la lógica
    tiempo, total, intel, amd, lista_top = l.req_5(control, n, y_init, y_end, brand, form_factor)

    # Formateo de la tabla para tabulate
    tabla_top = []
    for c in lista_top:
        tabla_top.append([
            c['model'], c['ram_gb'], c['cpu_boost_ghz'], 
            c['release_year'], c['cpu_brand'], c['cpu_model'], 
            f"${float(c['price']):,.2f}"
        ])

    print("\n" + "=" * 100)
    print(f"RESULTADO REQUERIMIENTO 5 - MARCA: {brand.upper()} | FORMA: {form_factor.upper()}")
    print(f"Años: {y_init}-{y_end} | Intel: {intel} | AMD: {amd} | Tiempo: {tiempo:.2f} ms")
    print("=" * 100)
    
    headers = ["Modelo", "RAM", "Boost", "Año", "CPU Brand", "CPU Model", "Precio"]
    print(tabulate(tabla_top, headers=headers, tablefmt="fancy_grid"))
    
    return control


def print_req_6(control):
    """
    Función que imprime la solución del Requerimiento 6 en consola.
    Muestra el Top N de eficiencia energética con filtros de pantalla y forma.
    """
    print("\n" + "=" * 80)
    print("      REQUERIMIENTO 6: TOP N EQUIPOS CON MEJOR EFICIENCIA ENERGÉTICA")
    print("=" * 80)

    # 1. Captura de parámetros de entrada
    try:
        n_top = input("Ingrese el número de equipos a listar (N): ")
        f_forma = input("Ingrese el Factor de forma (ej: Laptop, 2-in-1): ")
        s_type = input("Ingrese el Tipo de pantalla (ej: IPS, OLED, LED): ")
        
        print("\n--- Rango de años ---")
        y_min = int(input("Ingrese el año inicial: "))
        y_max = int(input("Ingrese el año final: "))
    except ValueError:
        print("\nError: Los años y el valor N deben ser números enteros.")
        return

    print(f"\nProcesando eficiencia para {f_forma} con pantalla {s_type} ({y_min}-{y_max})...")

    # 2. Llamado a la función de lógica
    # res es el diccionario que retorna tu función req_6
    res = l.req_6(control, n_top, f_forma, s_type, y_min, y_max)

    # 3. Mostrar Resumen de la ejecución (según pide el PDF)
    resumen_ejecucion = [
        ["Tiempo de ejecución", f"{round(res['tiempo'], 2)} ms"],
        ["Total equipos que cumplieron filtro", res["total"]],
        ["Equipos con OS Windows", res["windows"]],
        ["Equipos con OS Linux", res["linux"]]
    ]
    
    print("\n" + tabulate(resumen_ejecucion, headers=["Concepto", "Valor"], tablefmt="fancy_grid"))

    # 4. Mostrar el Top N de equipos
    if len(res["top"]) > 0:
        print(f"\nTOP {n_top} DE EQUIPOS CON MEJOR PUNTAJE DE EFICIENCIA:")
        # Imprimimos la lista de diccionarios directamente con tabulate
        print(tabulate(res["top"], headers="keys", tablefmt="fancy_grid"))
        
        print("\n* Puntaje calculado como: (Batería * CPU Boost) / Watts Cargador")
        print("* En caso de empate en eficiencia, se ordena por precio (menor a mayor).")
    else:
        print("\nNo se encontraron computadores que cumplan con todos los filtros aplicados.")

    print("\n" + "=" * 80)

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
