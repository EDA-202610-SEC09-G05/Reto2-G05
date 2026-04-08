import sys
from tabulate import tabulate
from DataStructures.List import array_list as al
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

    # Verificación de seguridad por si no hay datos
    p_min = min_precio["price"] if min_precio else "N/A"
    p_max = max_precio["price"] if max_precio else "N/A"

    resumen = [
        ["Tiempo de carga (ms)", f"{round(dtime, 2)} ms"],
        ["Total registros", f"{total:,}"],
        ["Año mínimo", min_year],
        ["Año máximo", max_year],
        ["Precio mínimo", p_min],
        ["Precio máximo", p_max]
    ]

    print(tabulate(resumen, headers=["Campo", "Valor"], tablefmt="fancy_grid"))

    # 2. SISTEMAS OPERATIVOS
    print("\n" + "=" * 80)
    print("           DISTRIBUCIÓN POR SISTEMA OPERATIVO")
    print("=" * 80)

    rows_os = []
    for os_name in os_count:
        rows_os.append([os_name, os_count[os_name]])

    # Ordenar el conteo de OS por cantidad (opcional, pero se ve mejor)
    rows_os.sort(key=lambda x: x[1], reverse=True)
    print(tabulate(rows_os, headers=["OS", "Cantidad"], tablefmt="fancy_grid"))

    # 3. TOP 5 MÁS CAROS
    print("\n" + "=" * 80)
    print("                 TOP 5 COMPUTADORES MÁS CAROS")
    print("=" * 80)
    if top5:
        print(tabulate(top5, headers="keys", tablefmt="fancy_grid"))
    else:
        print("No hay datos suficientes para mostrar el Top 5.")

    # 4. TOP 5 MÁS BARATOS
    print("\n" + "=" * 80)
    print("                TOP 5 COMPUTADORES MÁS BARATOS")
    print("=" * 80)
    if bottom5:
        print(tabulate(bottom5, headers="keys", tablefmt="fancy_grid"))
    else:
        print("No hay datos suficientes para mostrar el Bottom 5.")

    return catalog


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    pass


def print_req_2(control):
    """
    Función que imprime la solución del Requerimiento 2 en consola.
    Filtra equipos por núcleos y año, ordenados por peso.
    """
    print("\n" + "=" * 80)
    print("      REQUERIMIENTO 2: EQUIPOS MÁS LIGEROS POR NÚCLEOS Y AÑO")
    print("=" * 80)

    # 1. Entrada de datos
    num_nucleos = input("Ingrese el número de núcleos (ej: 4, 8, 16): ")
    anio_lanzamiento = input("Ingrese el año de lanzamiento (ej: 2022): ")

    print(f"\nBuscando equipos del año {anio_lanzamiento} con {num_nucleos} núcleos...")

    # 2. Llamado a la lógica
    # La función req_2 devuelve: (tiempo, total, promedio, resultados)
    resultado_logica = l.req_2(control, num_nucleos, anio_lanzamiento)
    dtime, total, promedio_peso, lista_resultados = resultado_logica

    # 3. Mostrar estadísticas básicas
    resumen_req = [
        ["Total encontrados", f"{total}"],
        ["Peso promedio", f"{promedio_peso} kg"],
        ["Tiempo de ejecución", f"{round(dtime, 2)} ms"]
    ]
    print(tabulate(resumen_req, tablefmt="fancy_grid"))

    # 4. Mostrar tabla de resultados
    if total > 0:
        print("\nLista de equipos encontrados:")
        
        # Si hay más de 20 resultados, la lógica ya nos dio los 10 primeros y 10 últimos
        if total > 20:
            print("10 más livianos ")
            
            # Dividimos visualmente para que el usuario note el salto
            parte_1 = lista_resultados[:10]
            parte_2 = lista_resultados[10:]
            
            print(tabulate(parte_1, headers="keys", tablefmt="fancy_grid"))
            print("\n 10 más pesados\n")
            print(tabulate(parte_2, headers="keys", tablefmt="fancy_grid"))
        else:
            # Si son 20 o menos, se imprimen todos de una vez
            print(tabulate(lista_resultados, headers="keys", tablefmt="fancy_grid"))
    else:
        print("\nNo se encontraron computadores con esos criterios.")

    print("\n" + "=" * 80)


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


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
