import csv

def guardar_csv(inventario,ruta, incluir_header=True):
    if not inventario:
        print("Inventario vacio")
        return
    try:
        with open(ruta, "w", newline="") as f:
        
            writer = csv.DictWriter(f)
            if incluir_header:
                writer.writeheader(["nombre", "precio", "cantidad"])
            for p in inventario:
                writer.writerow([p["nombre"],p["precio"], p["cantidad"]])

            print(f"Inventario guardado en:{ruta}")
    except PermissionError:
        print("Error: no tienes permiso para escribir en esta ubicación.")
    
    except Exception as e:
        print(f"Error inesperado al guardar csv:{e}")

def cargar_csv(ruta):
    productos=[]
    filas_invalidas=0
   
    try:
    
        with open(ruta, "r", newline="") as file:
                reader = csv.DictReader(file)
                
                encabezado = (reader, None)
                if encabezado != ["nombre", "precio", "cantidad"]:
                    print("Error encabezado invalido.")
                    return[],0
                for fila in reader:
                    if len(fila) !=3:
                        filas_invalidas +=1
                        continue
                    nombre, precio, cantidad = fila

                    try:
                        precio=float(precio)
                        cantidad=int(cantidad)

                        if precio<0 or cantidad<0:
                            raise ValueError
                        
                        productos.append({
                                "nombre": nombre,
                                "precio": precio,
                                "cantidad": cantidad
                            })
                    except ValueError:
                        filas_invalidas+=1

                    return productos, filas_invalidas
    except FileNotFoundError:
            print("Arcgivo no encotrado")
    except UnicodeDecodeError:
            print("Codificacion erronea")
    except Exception as e:
            print(f"Error al cargar: {e}")

    return [], 0
        
        
    
