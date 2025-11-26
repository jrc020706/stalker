# Sistema de Gestión Integral de Inventario y Ventas
from datetime import datetime
from collections import Counter
# --- Estructuras de Datos ---
products = [
    {"id": 1, "title": "Don quijote de la mancha", "author": "Miguel de cervantes", "category": "Fantasy", "price": 25.00, "stock": 28},
    {"id": 2, "title": "The Bible", "author": "Unknown", "category": "History", "price": 50.00, "stock": 10},
    {"id": 3, "title": "100 años de soledad", "author": "Gabriel Garcia Marquez", "category": "Novel", "price": 15.50, "stock": 50},
    {"id": 4, "title": "La divina comedia", "author": "Dante Alighieri", "category": "Epic", "price": 30.00, "stock": 8},
    {"id": 5, "title": "The  little prince", "author": "Antoine", "category": "For Kids", "price": 40.00, "stock": 25}
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
def safe_input(prompt, cast=str, validate=None, error_message="Invalid input, try again."):
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
                print(error_message)
                continue
            return value
        except ValueError:
            print(error_message)

def find_product_by_id(pid):
     """
    Busca un producto por ID y lo retorna si existe.
    """
     return next((p for p in products if p['id'] == pid), None)

def print_product(p):
    """
    Imprime los datos formateados de un producto.
    """
    print(f"ID: {p["id"]} | Title: {p['title']} | Author: {p['author']} | Category: {p['category']} | Price: ${p['price']:.2f} | Stock: {p['stock']}")
# --- CRUD del Inventario ---
def add_product():
    """
    Agregar un nuevo libro/producto
    """
    print("--- Add book ---")
     # Se recopilan datos con validaciones
    title = safe_input("Title: ")
    author = safe_input("Author: ")
    category = safe_input("Category: ")
    price = safe_input("Price: ", cast=float, validate=lambda x: x >= 0)
    stock = safe_input("Stock: ", cast=int, validate=lambda x: x >= 0)
    global next_product_id
    product = {
        'id': next_product_id,
        'title': title,
        'author': author,
        'category': category,
        'price': float(price),
        'stock': int(stock),   
    }
    products.append(product)
    initial_stock[product['id']] = product['stock']
    next_product_id += 1
    print(f"Product added with ID {product['id']}")

def list_products():
    """
    Crear una lista de los productos registrados
    """
    print("--- List Product ---")
    if not products:
        print("No products registered.")
        return
    for p in products:
        print_product(p)


def update_product():
    """
    Actualizar/Editar un producto de la lista
    """
    print("--- Update Product ---")
    pid = safe_input("Enter product ID to update: ", cast=int)
    p = find_product_by_id(pid)
    if not p:
        print("Product not found.")
        return
    print("Current values (leave blank to keep current):")
    print_product(p)
# Permite modificar sólo campos deseados
    try:
        title = input("New Title: ").strip() or p['title']
        author = input("New Author: ").strip() or p['author']
        category = input("New category: ").strip() or p['category']
        unit_price_raw = input("New price: ").strip()
        price = float(unit_price_raw) if unit_price_raw else p['price']
        stock_raw = input("New stock: ").strip()
        stock = int(stock_raw) if stock_raw else p['stock']
        if price < 0 or stock < 0 :
            print("Values must be non-negative. Update cancelled.")
            return
        p.update({'title': title, 'author': author, 'category': category, 'price': price, 'stock': stock})
        print(" Product updated successfully.")
    except ValueError:
        print("Invalid numeric input. Update cancelled.")

def delete_product():
    """
    Borrar un producto de la lista
    """
    print("--- Delete Book ---")
    pid = safe_input("Enter product ID to delete: ", cast=int)
    p = find_product_by_id(pid)
    if not p:
        print("Product not found.")
        return
    confirm = input(f"¿Delete '{p['title']}'? (yes/no): ").strip().lower()
    if confirm == 'yes':
        products.remove(p)
        initial_stock.pop(pid, None)
        print(" Product removed.")
    else:
        print("Cancelled.")
# --- Registro de Ventas ---
def register_sale():
    """
    Registrar una o varias ventas
    """
    print("--- Register Sale---")
    client = safe_input("Client name: ")
    print("Client types: regular, member, vip")
    #Aplicar descuentos a los tipos de clientes
    client_type = safe_input("Client Type: ", validate=lambda x: x.lower() in CLIENT_DISCOUNTS).lower()
    pid = safe_input("Product ID to sell: ", cast=int)
    product = find_product_by_id(pid)
    if not product:
        print("Product not found.")
        return
    print_product(product)
    quantity = safe_input("Quantity to sell: ", cast=int, validate=lambda x: x > 0)
    if quantity > product['stock']:
        print(f" Insufficient stock. Available: {product['stock']}")
        return
    unit_price = product['price']
    gross = unit_price * quantity
    discount_rate = CLIENT_DISCOUNTS[client_type]
    discount_amount = gross * discount_rate
    total = gross - discount_amount
    product['stock'] -= quantity
    sale = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'client': client,
        'client_type': client_type,
        'product_id': pid,
        'product_title': product['title'],
        'author': product['author'],
        'quantity': quantity,
        'price': unit_price,
        'gross': round(gross,2),
        'discount': round(discount_amount,2),
        'total': round(total,2)
    }
    sales.append(sale)
    print(f" Sale recorded. Total: ${total:.2f}")

def show_sales_history():
    """
    Mostrar historial de ventas con las fecha de las ventas
    """
    print("--- Sales History ---")
    if not sales:
        print("No sales recorded yet.")
        return
    for i, s in enumerate(sales, 1):
        print(f"{i}. {s['timestamp']} | {s['client']} ({s['client_type']}) | {s['product_title']} x{s['quantity']} | Total: ${s['total']:.2f}")

def reports():
    """
    Reporte de ventas y estadiscticas
    """
    print("--- Module reports ---")
    if not sales:
        print("There are no sales to generate reports.")
        return
    print("Top 3 best sell books:")
    counts = Counter(s.get('product_title') for s in sales).most_common(3)
    for books, quantity in counts:
        print(f"- {books}: {quantity} sales")
    print("Sales grouped by author:")
    author_counts = Counter(s['author'] for s in sales)
    for author, quantity in author_counts.items():
        print(f"- {author}: {quantity} sales")
    print("Inventory performance:")
    for p in products:
        init = initial_stock.get(p['id'], p['stock'])
        sold = init - p['stock']
        print(f"- {p['title']}: sold {sold} units ")

def menu():
    """
    Funcion de menu para iniciar el sistema
    """
    while True:
        print("""
INVENTORY AND SALES SYSTEM
1. Register Book
2. List Books
3. Update Books
4. Delete Book
5. Register Book Sale
6. Sales History
7. System Reports
8. Exit
""")
        option = safe_input("Choose an Option: ", cast=int)
        if option == 1: add_product()
        elif option == 2: list_products()
        elif option == 3: update_product()
        elif option == 4: delete_product()
        elif option == 5: register_sale()
        elif option == 6: show_sales_history()
        elif option == 7: reports()
        elif option == 8: 
            print("¡See you!")
            break
        else:
            print("Wrong Option.")
# Iniciar sistema
menu()