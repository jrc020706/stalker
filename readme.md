# Sistema de Gestión Integral de Inventario y Ventas

Este proyecto es un sistema de gestión de inventario y ventas simple implementado en Python. Permite llevar un registro de productos (libros), gestionar su stock, registrar ventas, y generar informes básicos sobre el rendimiento del inventario y los productos más vendidos.

## Características

*   **CRUD Básico** (Crear, Listar, Actualizar, Eliminar) para productos.
*   **Registro de Ventas** con cálculo automático de descuentos según el tipo de cliente.
*   **Control de Stock** que previene ventas de cantidades no disponibles.
*   **Informes** de los 3 productos más vendidos, ventas por autor y rendimiento del inventario.
*   **Validación de Entrada** mediante una función utilitaria (`safe_input`) para garantizar datos correctos (tipos de datos y rangos).

## Requisitos

El sistema utiliza únicamente la librería estándar de Python (`datetime` y `collections.Counter`). No requiere instalaciones externas.

*   **Python 3.x**

## Uso e Instalación

1.  Guarda el código proporcionado en un archivo llamado `inventario_ventas.py`.
2.  Ejecuta el archivo desde tu terminal:

```bash
python inventario_ventas.py

SISTEMA DE INVENTARIO Y VENTAS
1. Register Book         (Registrar nuevo libro/producto)
2. List Books            (Listar todos los productos disponibles)
3. Update Books          (Actualizar detalles de un producto existente o Crear uno nuevo en lugar de es)
4. Delete Book           (Eliminar un producto del inventario)
5. Register Book Sale    (Registrar una transacción de venta)
6. Sales History         (Ver el historial completo de ventas)
7. System Reports        (Generar informes y estadísticas del sistema)
8. Exit                  (Salir de la aplicación)
