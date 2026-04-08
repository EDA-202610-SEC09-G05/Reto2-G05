def new_set():
    """Crea un nuevo set vacío."""
    return {'size': 0, 'elements': []}

def add_element(my_set, element):
    """Agrega un elemento al set si no está presente."""
    if element not in my_set['elements']:
        my_set['elements'].append(element)
        my_set['size'] += 1
    return my_set

def remove_element(my_set, element):
    """Elimina un elemento del set si está presente."""
    if element in my_set['elements']:
        my_set['elements'].remove(element)
        my_set['size'] -= 1
    return my_set

def size(my_set):
    """Devuelve el tamaño del set."""
    return my_set['size']

def is_empty(my_set):
    """Devuelve True si el set está vacío, False en caso contrario."""
    return my_set['size'] == 0

def load_set(my_set, filename):
    """Carga elementos desde un archivo de texto, uno por línea."""
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            element = line.strip()
            add_element(my_set, element)
    return my_set

def is_in(my_set, element):
    """Devuelve True si el elemento está en el set, False en caso contrario."""
    return element in my_set['elements']