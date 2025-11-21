from servicios import *
from archivos import *

inventario=[]

def menu():
    while True:
        print("==MENU PRINCIPAL==")
        print("1.Agregar producto")
        print("2.Mostrar inventario")
        print("3.Buscar producto")
        print("4.Actualizar producto")
        print("5.Eliminar producto")
        print("6.Estadisticas")
        print("7.Guardar CSV")
        print("8.Cargar CSV")
        print("9. Salir")

        opciones= input("Elige una opcion: ")

        if opciones == "1":
            nombre = input("Nombre: ")
            try:
                precio = float(input("Precio: "))
                cantidad = int(input ("Cantidad: "))
            except ValueError:
                print("Precio o cantidad invalidos.")
                continue
            
            agregar_producto(inventario, nombre, precio, cantidad)
        
        elif opciones == "2":
            mostrar_inventario(inventario)

        elif opciones == "3":
            nombre = input("Nombre a buscar: ")
            producto = buscar_producto(inventario, nombre)
            if producto:
                print("Producto encontrado:", producto)
            else:
                print("No existe el producto.")

        elif opciones == "4":
            nombre = input("Producto a actualizar: ")
            actualizar_producto(inventario, nombre)
        
        elif opciones == "5":
            nombre = input("Producto a eliminar: ")
            eliminar_producto(inventario, nombre)

        elif opciones == "6":
            estad=calcular_estadisticas(inventario)

            if estad is None:
                print("Inventario vacío. No hay estadísticas.")
            else:
                print("\n=== ESTADÍSTICAS DEL INVENTARIO ===")
                print(f"Unidades totales: {estad['unidades_totales']}")
                print(f"Valor total: {estad['valor_total']}")
                print(f"Producto más caro: {estad['producto_mas_caro']}")
                print(f"Producto con mayor stock: {estad['producto_mayor_stock']}")


        elif opciones == "7":
            ruta = input("Ruta para guardar archivo CSV:")
            guardar_csv (inventario, ruta)

        elif opciones == "8":
            ruta = input("Ruta del CSV a cargar: ")
            productos_cargados, errores = cargar_csv (ruta)
            print(f"\n✔ Productos cargados: {len(productos_cargados)}")
            print(f"⚠ Filas inválidas omitidas: {errores}")

            if productos_cargados:
                decision = input("¿Sobrescribir inventario actual? (S/N): ").upper()

                if decision == "S":
                    inventario.clear()
                    inventario.extend(productos_cargados)
                    print("Inventario reemplazado.")
                else:
                    print("Fusionando inventarios...")
                    for nuevo in productos_cargados:
                        existente = buscar_producto(inventario, nuevo["nombre"])
                        if existente:
                            existente["cantidad"] += nuevo["cantidad"]
                            existente["precio"] = nuevo["precio"]
                        else:
                            inventario.append(nuevo)

        elif opciones == "9":
            print("Salir")
            break

        else:
            print("Opcion invalida.")

if __name__ == "__main__":
    menu()