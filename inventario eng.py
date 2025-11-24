# Sistema de Gestión Integral de Inventario y Ventas
# Programa interactivo por consola en inglés (requisito), pero con comentarios explicativos en español
# Incluye: CRUD de inventario, registro de ventas, reportes, validaciones, modularidad,
# diccionarios anidados, listas, manejo de errores y uso de lambda.

from datetime import datetime
from collections import defaultdict, Counter
import sys

# --- Estructuras de Datos ---
# Lista de productos, cada uno con un ID único y sus atributos
products = [
    {"id": 1, "name": "Smartphone X100", "brand": "Apex", "category": "Mobile", "unit_price": 450.00, "stock": 20, "warranty_months": 24},
    {"id": 2, "name": "Laptop Pro 15", "brand": "Nexis", "category": "Computers", "unit_price": 1200.00, "stock": 10, "warranty_months": 12},
    {"id": 3, "name": "Wireless Headset", "brand": "Apex", "category": "Audio", "unit_price": 85.50, "stock": 50, "warranty_months": 6},
    {"id": 4, "name": "4K Monitor 27in", "brand": "Viewza", "category": "Peripherals", "unit_price": 330.00, "stock": 8, "warranty_months": 18},
    {"id": 5, "name": "External SSD 1TB", "brand": "Storix", "category": "Storage", "unit_price": 140.00, "stock": 25, "warranty_months": 36}
]

# Se registra el stock inicial para calcular rendimiento del inventario
initial_stock = {p['id']: p['stock'] for p in products}

# Lista que almacenará las ventas registradas
sales = []

# Generación automática del siguiente ID de producto
next_product_id = max(p['id'] for p in products) + 1

# Tipos de cliente y descuentos aplicados
CLIENT_DISCOUNTS = {
    'regular': 0.00,
    'member': 0.05,
    'vip': 0.10
}

# --- Funciones Utilitarias y de Validación ---

def safe_input(prompt, cast=str, validate=None, error_msg="Invalid input, try again."):
    """
    Solicita entrada al usuario, la convierte al tipo requerido y valida.
    Repite hasta recibir un valor válido.
    """
    while True:
        try:
            raw = input(prompt).strip()
            if raw == "":
                print("Input cannot be empty.")
                continue
            value = cast(raw)
            if validate and not validate(value):
                print(error_msg)
                continue
            return value
        except ValueError:
            print(error_msg)


def find_product_by_id(pid):
    """
    Busca un producto por ID y lo retorna si existe.
    """
    for p in products:
        if p['id'] == pid:
            return p
    return None


def print_product(p):
    """
    Imprime los datos formateados de un producto.
    """
    print(f"ID: {p['id']} | Name: {p['name']} | Brand: {p['brand']} | Category: {p['category']} | Price: ${p['unit_price']:.2f} | Stock: {p['stock']} | Warranty: {p['warranty_months']} months")

# --- CRUD del Inventario ---

def add_product():
    print('\n--- Add Product ---')
    # Se recopilan datos con validaciones
    name = safe_input("Product name: ")
    brand = safe_input("Brand: ")
    category = safe_input("Category: ")
    unit_price = safe_input("Unit price: ", cast=float, validate=lambda x: x >= 0)
    stock = safe_input("Stock quantity: ", cast=int, validate=lambda x: x >= 0)
    warranty = safe_input("Warranty months: ", cast=int, validate=lambda x: x >= 0)

    global next_product_id
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
    print(f"Product added with ID {product['id']}")


def list_products():
    print('\n--- Product List ---')
    if not products:
        print("No products registered.")
        return
    for p in products:
        print_product(p)


def update_product():
    print('\n--- Update Product ---')
    pid = safe_input("Enter product ID to update: ", cast=int, validate=lambda x: x > 0)
    p = find_product_by_id(pid)
    if not p:
        print("Product not found.")
        return

    print("Current values (leave blank to keep current):")
    print_product(p)

    # Permite modificar sólo campos deseados
    try:
        name = input("New name: ").strip() or p['name']
        brand = input("New brand: ").strip() or p['brand']
        category = input("New category: ").strip() or p['category']
        unit_price_raw = input("New unit price: ").strip()
        unit_price = float(unit_price_raw) if unit_price_raw != "" else p['unit_price']
        stock_raw = input("New stock quantity: ").strip()
        stock = int(stock_raw) if stock_raw != "" else p['stock']
        warranty_raw = input("New warranty months: ").strip()
        warranty = int(warranty_raw) if warranty_raw != "" else p['warranty_months']

        if unit_price < 0 or stock < 0 or warranty < 0:
            print("Values must be non-negative. Update cancelled.")
            return

        p.update({'name': name, 'brand': brand, 'category': category, 'unit_price': unit_price, 'stock': stock, 'warranty_months': warranty})
        print("Product updated successfully.")
    except ValueError:
        print("Invalid numeric input. Update cancelled.")


def delete_product():
    print('\n--- Delete Product ---')
    pid = safe_input("Enter product ID to delete: ", cast=int, validate=lambda x: x > 0)
    p = find_product_by_id(pid)
    if not p:
        print("Product not found.")
        return

    confirm = input(f"Are you sure you want to delete '{p['name']}'? (y/n): ").strip().lower()
    if confirm == 'y':
        products.remove(p)
        initial_stock.pop(pid, None)
        print("Product removed.")
    else:
        print("Deletion cancelled.")

# --- Registro de Ventas ---

def register_sale():
    print('\n--- Register Sale ---')
    client_name = safe_input("Client name: ")
    print("Client types: regular, member, vip")
    client_type = safe_input("Client type: ", validate=lambda x: x.lower() in CLIENT_DISCOUNTS).lower()

    pid = safe_input("Product ID to sell: ", cast=int, validate=lambda x: x > 0)
    product = find_product_by_id(pid)
    if not product:
        print("Product not found.")
        return

    print_product(product)
    qty = safe_input("Quantity to sell: ", cast=int, validate=lambda x: x > 0)

    # Validación de stock
    if qty > product['stock']:
        print(f"Insufficient stock. Available: {product['stock']}")
        return

    # Cálculos de totales y descuento
    unit_price = product['unit_price']
    gross = unit_price * qty
    discount_rate = CLIENT_DISCOUNTS.get(client_type, 0.0)
    discount_amount = gross * discount_rate
    total_after_discount = gross - discount_amount

    # Actualiza inventario
    product['stock'] -= qty

    sale = {
        'timestamp': datetime.now().isoformat(timespec='seconds'),
        'client': client_name,
        'client_type': client_type,
        'product_id': pid,
        'product_name': product['name'],
        'brand': product['brand'],
        'quantity': qty,
        'unit_price': unit_price,
        'gross': round(gross, 2),
        'discount_rate': discount_rate,
        'discount_amount': round(discount_amount, 2),
        'total_after_discount': round(total_after_discount, 2)
    }
    sales.append(sale)

    print(f"Sale recorded. Total: ${sale['total_after_discount']:.2f}")


def show_sales_history():
    print('\n--- Sales History ---')
    if not sales:
        print("No sales recorded yet.")
        return
    for i, s in enumerate(sales, 1):
        print(f"{i}. {s['timestamp']} | Client: {s['client']} ({s['client_type']}) | Product: {s['product_name']} x{s['quantity']} | Total: ${s['total_after']})