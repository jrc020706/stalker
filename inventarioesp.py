# ===============================================================
# Sistema Integral de Gestión de Inventario y Ventas
# Interacciones en ESPAÑOL (requisito solicitado)
# Comentarios explicativos en español
# ===============================================================

from datetime import datetime
from collections import Counter

# --- Estructuras de Datos ---
products = [
    {"id": 1, "name": "Smartphone X100", "brand": "Apex", "category": "Móvil", "unit_price": 450.00, "stock": 20, "warranty_months": 24},
    {"id": 2, "name": "Laptop Pro 15", "brand": "Nexis", "category": "Computador", "unit_price": 1200.00, "stock": 10, "warranty_months": 12},
    {"id": 3, "name": "Audífonos Wireless", "brand": "Apex", "category": "Audio", "unit_price": 85.50, "stock": 50, "warranty_months": 6},
    {"id": 4, "name": "Monitor 4K 27\"", "brand": "Viewza", "category": "Periférico", "unit_price": 330.00, "stock": 8, "warranty_months": 18},
    {"id": 5, "name": "SSD Externo 1TB", "brand": "Storix", "category": "Almacenamiento", "unit_price": 140.00, "stock": 25, "warranty_months": 36}
]

initial_stock = {p['id']: p['stock'] for p in products}
sales = []
next_product_id = max(p['id'] for p in products) + 1

CLIENT_DISCOUNTS = {
    'regular': 0.00,
    'miembro': 0.05,
    'vip': 0.10
}

# --------------------------------------------------------------
# Funciones Utilitarias
# --------------------------------------------------------------

def safe_input(prompt, cast=str, validate=None, error_msg="Entrada inválida, intenta de nuevo."):
    while True:
        try:
            raw = input(prompt).strip()
            if raw == "":
                print("El valor no puede estar vacío.")
                continue
            value = cast(raw)
            if validate and not validate(value):
                print(error_msg)
                continue
            return value
        except ValueError:
            print(error_msg)


def find_product_by_id(pid):
    return next((p for p in products if p['id'] == pid), None)


def print_product(p):
    print(f"ID: {p['id']} | Nombre: {p['name']} | Marca: {p['brand']} | Categoría: {p['category']} | Precio: ${p['unit_price']:.2f} | Stock: {p['stock']} | Garantía: {p['warranty_months']} meses")


# --------------------------------------------------------------
# CRUD del Inventario
# --------------------------------------------------------------

def add_product():
    print("\n📦 --- Registrar Producto ---")
    global next_product_id
    name = safe_input("Nombre: ")
    brand = safe_input("Marca: ")
    category = safe_input("Categoría: ")
    unit_price = safe_input("Precio unitario: ", cast=float, validate=lambda x: x >= 0)
    stock = safe_input("Cantidad en stock: ", cast=int, validate=lambda x: x >= 0)
    warranty = safe_input("Garantía (meses): ", cast=int, validate=lambda x: x >= 0)

    product = {
        'id': next_product_id,
        'name': name,
        'brand': brand,
        'category': category,
        'unit_price': float(unit_price),
        'stock': int(stock),
        'warranty_months': int(warranty)
    }
    products.append(product)
    initial_stock[product['id']] = product['stock']
    next_product_id += 1
    print("✅ Producto registrado con éxito.")


def list_products():
    print("\n📋 --- Lista de Productos ---")
    if not products:
        print("No hay productos registrados.")
        return
    for p in products:
        print_product(p)


def update_product():
    print("\n✏️ --- Actualizar Producto ---")
    pid = safe_input("ID del producto a actualizar: ", cast=int)
    p = find_product_by_id(pid)
    if not p:
        print("Producto no encontrado.")
        return

    print("\nValores actuales (ENTER para mantener):")
    print_product(p)

    try:
        name = input("Nuevo nombre: ").strip() or p['name']
        brand = input("Nueva marca: ").strip() or p['brand']
        category = input("Nueva categoría: ").strip() or p['category']

        unit_price_raw = input("Nuevo precio unitario: ").strip()
        unit_price = float(unit_price_raw) if unit_price_raw else p['unit_price']

        stock_raw = input("Nueva cantidad en stock: ").strip()
        stock = int(stock_raw) if stock_raw else p['stock']

        warranty_raw = input("Nueva garantía (meses): ").strip()
        warranty = int(warranty_raw) if warranty_raw else p['warranty_months']

        if unit_price < 0 or stock < 0 or warranty < 0:
            print("Valores inválidos. Cancelado.")
            return

        p.update({'name': name, 'brand': brand, 'category': category, 'unit_price': unit_price, 'stock': stock, 'warranty_months': warranty})
        print("✅ Producto actualizado.")

    except ValueError:
        print("Entrada numérica inválida.")


def delete_product():
    print("\n🗑️ --- Eliminar Producto ---")
    pid = safe_input("ID del producto a eliminar: ", cast=int)
    p = find_product_by_id(pid)
    if not p:
        print("Producto no encontrado.")
        return

    confirm = input(f"¿Eliminar '{p['name']}'? (s/n): ").strip().lower()
    if confirm == 's':
        products.remove(p)
        print("✅ Producto eliminado.")
    else:
        print("Cancelado.")


# --------------------------------------------------------------
# Registro y Consulta de Ventas
# --------------------------------------------------------------

def register_sale():
    print("\n💰 --- Registrar Venta ---")
    client = safe_input("Nombre del cliente: ")
    print("Tipos de cliente: regular / miembro / vip")
    client_type = safe_input("Tipo de cliente: ", validate=lambda x: x.lower() in CLIENT_DISCOUNTS).lower()

    pid = safe_input("ID del producto vendido: ", cast=int)
    product = find_product_by_id(pid)
    if not product:
        print("Producto no encontrado.")
        return

    print_product(product)
    qty = safe_input("Cantidad vendida: ", cast=int, validate=lambda x: x > 0)

    if qty > product['stock']:
        print("❌ Stock insuficiente.")
        return

    unit_price = product['unit_price']
    gross = unit_price * qty
    discount_rate = CLIENT_DISCOUNTS[client_type]
    discount_amount = gross * discount_rate
    total = gross - discount_amount

    product['stock'] -= qty

    sale = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'client': client,
        'client_type': client_type,
        'product_name': product['name'],
        'brand': product['brand'],
        'quantity': qty,
        'gross': gross,
        'discount': discount_amount,
        'total': total
    }
    sales.append(sale)

    print(f"✅ Venta registrada. Total a pagar: ${total:.2f}")


def show_sales_history():
    print("\n🧾 --- Historial de Ventas ---")
    if not sales:
        print("No hay ventas registradas.")
        return
    for i, s in enumerate(sales, 1):
        print(f"{i}. {s['timestamp']} | {s['client']} ({s['client_type']}) | {s['product_name']} x{s['quantity']} | Total: ${s['total']:.2f}")


# --------------------------------------------------------------
# Reportes del Sistema
# --------------------------------------------------------------

def reports():
    print("\n📊 --- Reportes del Sistema ---")

    if not sales:
        print("No hay ventas para generar reportes.")
        return

    print("\n⭐ Top 3 productos más vendidos:")
    counts = Counter(s['product_name'] for s in sales).most_common(3)
    for product, qty in counts:
        print(f"- {product}: {qty} ventas")

    print("\n🏷️ Ventas agrupadas por marca:")
    brand_counts = Counter(s['brand'] for s in sales)
    for brand, qty in brand_counts.items():
        print(f"- {brand}: {qty} ventas")

    print("\n💵 Ingreso bruto y neto:")
    gross_total = sum(s['gross'] for s in sales)
    net_total = sum(s['total'] for s in sales)
    print(f"Bruto: ${gross_total:.2f} | Neto: ${net_total:.2f}")

    print("\n📦 Rendimiento del inventario:")
    for p in products:
        sold = initial_stock[p['id']] - p['stock']
        print(f"- {p['name']} vendido: {sold} unidades")


# --------------------------------------------------------------
# Menú Principal
# --------------------------------------------------------------

def menu():
    while True:
        print("""
=============================
🛒 SISTEMA DE INVENTARIO Y VENTAS
=============================
1. Registrar producto
2. Listar productos
3. Actualizar producto
4. Eliminar producto
5. Registrar venta
6. Ver historial de ventas
7. Reportes del sistema
8. Salir
""")

        option = safe_input("Seleccione una opción: ", cast=int)

        if option == 1: add_product()
        elif option == 2: list_products()
        elif option == 3: update_product()
        elif option == 4: delete_product()
        elif option == 5: register_sale()
        elif option == 6: show_sales_history()
        elif option == 7: reports()
        elif option == 8:
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida.")


# Iniciar sistema
menu()
