filename = "IEE3702/TAREA2/data/el_principito.md"

with open(filename, "r", encoding="utf-8") as f:
    content = f.read()

num_chars = len(content)
file_size = len(content.encode("utf-8"))  # tamano en bytes

if file_size > 0:
    avg_length_per_symbol = num_chars / file_size
    print(f"Numero de caracteres: {num_chars}")
    print(f"Tamano del archivo (bytes): {file_size}")
    print(f"Largo promedio por simbolo: {avg_length_per_symbol}")
else:
    print("El archivo esta vacio.")