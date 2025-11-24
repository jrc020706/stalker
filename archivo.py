# Sistema de Gestión Integral de Inventario y Ventas
# Interacciones en ESPAÑOL (requisito solicitado)
# Comentarios explicativos en español
# Incluye persistencia en JSON y CSV: guardar y cargar INVENTARIO y VENTAS

from datetime import datetime
from collections import Counter
import json
import csv
import os

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

# Archivos por defecto
PRODUCTS_JSON = 'products.json'
SALES_JSON = 'sales.json'
PRODUCTS_CSV = 'products.csv'
SALES_CSV = 'sales.csv'

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
# Persistencia: JSON
# --------------------------------------------------------------

def save_to_json(products_path=PRODUCTS_JSON, sales_path=SALES_JSON):
    try:
        with open(products_path, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        with open(sales_path, 'w', encoding='utf-8') as f:
            json.dump(sales, f, ensure_ascii=False, indent=2)
        print(f"✅ Datos guardados en JSON: {products_path}, {sales_path}")
    except Exception as e:
        print(f"Error al guardar JSON: {e}")


def load_from_json(products_path=PRODUCTS_JSON, sales_path=SALES_JSON):
    global products, sales, initial_stock, next_product_id
    try:
        if os.path.exists(products_path):
            with open(products_path, 'r', encoding='utf-8') as f:
                products = json.load(f)
            # Asegurar tipos correctos (por si acaso)
            for p in products:
                p['id'] = int(p['id'])
                p['unit_price'] = float(p['unit_price'])
                p['stock'] = int(p['stock'])
                p['warranty_months'] = int(p.get('warranty_months', 0))
            initial_stock = {p['id']: p['stock'] for p in products}
            next_product_id = max(p['id'] for p in products) + 1
        if os.path.exists(sales_path):
            with open(sales_path, 'r', encoding='utf-8') as f:
                sales = json.load(f)
        print("✅ Datos cargados desde JSON (si existían archivos).")
    except Exception as e:
        print(f"Error al cargar JSON: {e}")

# --------------------------------------------------------------
# Persistencia: CSV
# --------------------------------------------------------------

def save_to_csv(products_path=PRODUCTS_CSV, sales_path=SALES_CSV):
    try:
        with open(products_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'name', 'brand', 'category', 'unit_price', 'stock', 'warranty_months'])
            for p in products:
                writer.writerow([p['id'], p['name'], p['brand'], p['category'], p['unit_price'], p['stock'], p['warranty_months']])
        with open(sales_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'client', 'client_type', 'product_id', 'product_name', 'brand', 'quantity', 'unit_price', 'gross', 'discount', 'total'])
            for s in sales:
                writer.writerow([s.get('timestamp'), s.get('client'), s.get('client_type'), s.get('product_id'), s.get('product_name'), s.get('brand'), s.get('quantity'), s.get('unit_price'), s.get('gross'), s.get('discount'), s.get('total')])
        print(f"✅ Datos guardados en CSV: {products_path}, {sales_path}")
    except Exception as e:
        print(f"Error al guardar CSV: {e}")


def load_from_csv(products_path=PRODUCTS_CSV, sales_path=SALES_CSV):
    global products, sales, initial_stock, next_product_id
    try:
        if os.path.exists(products_path):
            with open(products_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                products = []
                for row in reader:
                    products.append({
                        'id': int(row['id']),
                        'name': row['name'],
                        'brand': row['brand'],
                        'category': row['category'],
                        'unit_price': float(row['unit_price']),
                        'stock': int(row['stock']),
                        'warranty_months': int(row.get('warranty_months', 0))
                    })
            initial_stock = {p['id']: p['stock'] for p in products}
            next_product_id = max(p['id'] for p in products) + 1
        if os.path.exists(sales_path):
            with open(sales_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                sales = []
                for row in reader:
                    sales.append({
                        'timestamp': row.get('timestamp'),
                        'client': row.get('client'),
                        'client_type': row.get('client_type'),
                        'product_id': int(row['product_id']) if row.get('product_id') else None,
                        'product_name': row.get('product_name'),
                        'brand': row.get('brand'),
                        'quantity': int(row['quantity']) if row.get('quantity') else 0,
                        'unit_price': float(row['unit_price']) if row.get('unit_price') else 0.0,
                        'gross': float(row['gross']) if row.get('gross') else 0.0,
                        'discount': float(row['discount']) if row.get('discount') else 0.0,
                        'total': float(row['total']) if row.get('total') else 0.0
                    })
        print("✅ Datos cargados desde CSV (si existían archivos).")
    except Exception as e:
        print(f"Error al cargar CSV: {e}")

# --------------------------------------------------------------
# Resto de funciones (CRUD, ventas, reportes)
# --------------------------------------------------------------

def add_product():
    print("
📦 --- Registrar Producto ---")
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
    print("
📋 --- Lista de Productos ---")
    if not products:
        print("No hay productos registrados.")
        return
    for p in products:
        print_product(p)


def update_product():
    print("
✏️ --- Actualizar Producto ---")
    pid = safe_input("ID del producto a actualizar: ", cast=int)
    p = find_product_by_id(pid)
    if not p:
        print("Producto no encontrado.")
        return

    print("
Valores actuales (ENTER para mantener):")
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
    print("
🗑️ --- Eliminar Producto ---")
    pid = safe_input("ID del producto a eliminar: ", cast=int)
    p = find_product_by_id(pid)
    if not p:
        print("Producto no encontrado.")
        return

    confirm = input(f"¿Eliminar '{p['name']}'? (s/n): ").strip().lower()
    if confirm == 's':
        products.remove(p)
        initial_stock.pop(pid, None)
        print("✅ Producto eliminado.")
    else:
        print("Cancelado.")


def register_sale():
    print("
💰 --- Registrar Venta ---")
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
        'product_id': pid,
        'product_name': product['name'],
        'brand': product['brand'],
        'quantity': qty,
        'unit_price': unit_price,
        'gross': round(gross,2),
        'discount': round(discount_amount,2),
        'total': round(total,2)
    }
    sales.append(sale)

    print(f"✅ Venta registrada. Total a pagar: ${total:.2f}")


def show_sales_history():
    print("
🧾 --- Historial de Ventas ---")
    if not sales:
        print("No hay ventas registradas.")
        return
    for i, s in enumerate(sales, 1):
        print(f"{i}. {s['timestamp']} | {s['client']} ({s['client_type']}) | {s['product_name']} x{s['quantity']} | Total: ${s['total']:.2f}")


def reports():
    print("
📊 --- Reportes del Sistema ---")

    if not sales:
        print("No hay ventas para generar reportes.")
        return

    print("
⭐ Top 3 productos más vendidos:")
    counts = Counter(s['product_name'] for s in sales).most_common(3)
    for product, qty in counts:
        print(f"- {product}: {qty} ventas")

    print("
🏷️ Ventas agrupadas por marca:")
    brand_counts = Counter(s['brand'] for s in sales)
    for brand, qty in brand_counts.items():
        print(f"- {brand}: {qty} ventas")

    print("
💵 Ingreso bruto y neto:")
    gross_total = sum(s['gross'] for s in sales)
    net_total = sum(s['total'] for s in sales)
    print(f"Bruto: ${gross_total:.2f} | Neto: ${net_total:.2f}")

    print("
📦 Rendimiento del inventario:")
    for p in products:
        init = initial_stock.get(p['id'], p['stock'])
        sold = init - p['stock']
        turnover = (sold / init * 100) if init > 0 else 0
        print(f"- {p['name']}: vendido {sold} unidades | Turnover: {turnover:.1f}%")

# --------------------------------------------------------------
# Menú Principal y opciones de persistencia
# --------------------------------------------------------------

def persistence_menu():
    while True:
        print("
--- Guardar / Cargar Datos ---")
        print("1. Guardar en JSON")
        print("2. Cargar desde JSON")
        print("3. Guardar en CSV")
        print("4. Cargar desde CSV")
        print("5. Volver")
        opt = safe_input("Seleccione una opción: ", cast=int)
        if opt == 1:
            save_to_json()
        elif opt == 2:
            load_from_json()
        elif opt == 3:
            save_to_csv()
        elif opt == 4:
            load_from_csv()
        elif opt == 5:
            return
        else:
            print("Opción inválida.")


def menu():
    # Intentar cargar automáticamente si existen archivos JSON al iniciar
    if os.path.exists(PRODUCTS_JSON) or os.path.exists(SALES_JSON):
        load_from_json()
    elif os.path.exists(PRODUCTS_CSV) or os.path.exists(SALES_CSV):
        load_from_csv()

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
8. Guardar / Cargar datos (JSON/CSV)
9. Salir
""")

        option = safe_input("Seleccione una opción: ", cast=int)

        if option == 1: add_product()
        elif option == 2: list_products()
        elif option == 3: update_product()
        elif option == 4: delete_product()
        elif option == 5: register_sale()
        elif option == 6: show_sales_history()
        elif option == 7: reports()
        elif option == 8: persistence_menu()
        elif option == 9:
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida.")

# Iniciar sistema
menu()
