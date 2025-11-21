def agregar_producto(inventario, nombre, precio, cantidad):
    inventario.append({
        "nombre": nombre,
        "precio": precio,
        "cantidad": cantidad
        })
    print("Producto agregado correctamente.")

def mostrar_inventario(inventario):
    if not inventario:
        print("El inventario esta vacio")
        return
    print("=== INVENTARIO ===")
    for producto in inventario:
        print(f"Nombre:{producto['nombre']},Precio: {producto['precio']},Cantidad:{producto['cantidad']}")

def buscar_producto(inventario, nombre):
    for producto in inventario:
        if producto["nombre"].lower() == nombre.lower():
            print("Producto encontrado:")
            print(f"Nombre: {producto['nombre']}")
            print(f"Precio: {producto['precio']}") 
            print(f"Cantidad: {producto['cantidad']}")
            return producto         
    print("Producto no encontrado.")
    return None

def actualizar_producto(inventario, nombre, nuevo_precio=None,nueva_cantidad=None):
    for producto in inventario:
        if producto["nombre"] == nombre:
            nuevo_precio=input("Ingresa nuevo precio: ")
            nueva_cantidad=input("Ingresa nueva cantidad: ")
            try:
                producto["precio"]=float(nuevo_precio)
                producto["cantidad"]=int(nueva_cantidad)
                print("Producto actualizado.")
            except ValueError:
                print("Datos del producto incorectos")
            return
    print("Producto no encontrado")

def eliminar_producto(inventario, nombre):
    for producto in inventario:
        if producto["nombre"]==nombre:
            inventario.remove(producto)
            print("Producto removido.")
            return
        print("Producto no encontrado")

def calcular_estadisticas(inventario):
    if not inventario:
        return None
    unidades_totales = sum(p["cantidad"] for p in inventario)
    valor_total = sum((lambda p: p["precio"] * p["cantidad"])(p) for p in inventario)
    producto_mas_caro = max(inventario, key=lambda p: p["precio"])
    producto_mayor_stock = max(inventario, key=lambda p: p["cantidad"])

    return {
        "unidades_totales": unidades_totales,
        "valor_total": valor_total,
        "producto_mas_caro": producto_mas_caro,
        "producto_mayor_stock": producto_mayor_stock
    }
inventario=[]
estad = calcular_estadisticas(inventario)
if estad:
    print("\n=== ESTADÍSTICAS ===")
    print(f"Unidades totales: {estad['unidades_totales']}")
    print(f"Valor total del inventario: {estad['valor_total']}")
    print(f"Producto más caro: {estad['producto_mas_caro']}")
    print(f"Producto con mayor stock: {estad['producto_mayor_stock']}")
else:
    print("Inventario vacío.")