import sqlite3




class Cart:
    def __init__(self):
        """
        Инициализация объекта Cart.
        """
        self.items = {}

    def add_item(self, product_name: str, quantity: int):
        """
        Добавление товара в корзину.
        """
        if product_name in self.items:
            self.items[product_name] += quantity
        else:
            self.items[product_name] = quantity

    def clear_cart(self):
        """
        Очистка корзины.
        """
        self.items = {}

    def get_cart(self) -> dict:
        """
        Получение текущего состояния корзины.
        return: Словарь товаров в корзине {название товара: количество}.
        """
        return self.items
class JewelryShop:
    def __init__(self, database_path: str = "jewelry_shop.db"):
        self.conn = sqlite3.connect(database_path)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,  -- Добавлено UNIQUE constraint
                price REAL NOT NULL,
                quantity INTEGER NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                total_price REAL NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                product_id INTEGER,
                quantity INTEGER NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        ''')

        self.conn.commit()


    def add_product(self, name: str, price: float, quantity: int):
        # Проверяем, есть ли товар с таким именем уже в базе данных
        self.cursor.execute("SELECT * FROM products WHERE name=?", (name,))
        existing_product = self.cursor.fetchone()

        if existing_product:
            # Если товар с таким именем уже существует, обновляем количество
            updated_quantity = existing_product[3] + quantity
            self.cursor.execute("UPDATE products SET quantity=? WHERE name=?", (updated_quantity, name))
            self.conn.commit()
            print(f"Количество товара '{name}' успешно обновлено.")
        else:
            # Если товара с таким именем нет, выполняем вставку
            self.cursor.execute("INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)", (name, price, quantity))
            self.conn.commit()
            print(f"Товар '{name}' успешно добавлен.")

    def delete_product(self, product_name: str):
        # Проверяем, существует ли товар с указанным именем
        self.cursor.execute("SELECT * FROM products WHERE name=?", (product_name,))
        existing_product = self.cursor.fetchone()

        if existing_product:
            # Удаляем товар из таблицы products
            self.cursor.execute("DELETE FROM products WHERE name=?", (product_name,))

            # Удаляем связанные записи из таблицы order_items
            self.cursor.execute("DELETE FROM order_items WHERE product_id=?", (existing_product[0],))

            self.conn.commit()
            print(f"Товар '{product_name}' успешно удален.")
        else:
            print(f"Товар с именем '{product_name}' не найден.")
    def update_product(self, product_name: str, new_price: float = None, new_quantity: int = None):
        # Проверяем, существует ли товар с указанным именем
        self.cursor.execute("SELECT * FROM products WHERE name=?", (product_name,))
        existing_product = self.cursor.fetchone()

        if existing_product:
            current_price, current_quantity = existing_product[2], existing_product[3]

            # Подготавливаем новые значения или оставляем текущие, если они не были указаны
            updated_price = new_price if new_price is not None else current_price
            updated_quantity = new_quantity if new_quantity is not None else current_quantity

            # Обновляем запись о товаре
            self.cursor.execute("UPDATE products SET price=?, quantity=? WHERE name=?",
                                (updated_price, updated_quantity, product_name))
            self.conn.commit()

            print(f"Параметры товара '{product_name}' успешно обновлены.")
        else:
            print(f"Товар с именем '{product_name}' не найден.")
    def filter_products(self, min_price=None, max_price=None, min_quantity=None, max_quantity=None):
        # Подготавливаем SQL-запрос с условиями фильтрации
        try:
            query = "SELECT * FROM products "
            params = []

            if min_price is not None:
                query += " AND price >= ?"
                params.append(min_price)

            if max_price is not None:
                query += " AND price <= ?"
                params.append(max_price)

            if min_quantity is not None:
                query += " AND quantity >= ?"
                params.append(min_quantity)

            if max_quantity is not None:
                query += " AND quantity <= ?"
                params.append(max_quantity)

            # Выполняем запрос
            self.cursor.execute(query, tuple(params))
            return self.cursor.fetchall()
        except Exception as e:
            print('e')
    
    def get_available_products(self):
        self.cursor.execute('SELECT * FROM products WHERE quantity > 0')
        return self.cursor.fetchall()
    def get_orders(self):
        self.cursor.execute('SELECT * FROM orders ')
        return self.cursor.fetchall()
    def create_order(self, customer_name: str, products: dict):
        total_price = 0
        for product_name, order_quantity in products.items():
            self.cursor.execute("SELECT name, price, quantity FROM products WHERE name=?", (product_name,))
            product_data = self.cursor.fetchone()

            if product_data and product_data[2] >= order_quantity:
                product_name, product_price, available_quantity = product_data
                total_price += product_price * order_quantity

                # Уменьшение количества товара в таблице products
                updated_quantity = available_quantity - order_quantity
                self.cursor.execute("UPDATE products SET quantity=? WHERE name=?", (updated_quantity, product_name))

        if total_price > 0:
            # Создание записи о заказе в таблице orders
            self.cursor.execute("INSERT INTO orders (customer_name, total_price) VALUES (?, ?)", (customer_name, total_price))
            order_id = self.cursor.lastrowid

            # Добавление товаров в заказ в таблицу order_items
            for product_name, order_quantity in products.items():
                self.cursor.execute("SELECT id FROM products WHERE name=?", (product_name,))
                product_id = self.cursor.fetchone()[0]

                # Добавление записи о товаре в заказ в таблицу order_items
                self.cursor.execute("INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)",
                                    (order_id, product_id, order_quantity))

            self.conn.commit()

    def delete_order(self, order_id: int):
        # Проверяем, существует ли заказ с указанным идентификатором
        self.cursor.execute("SELECT * FROM orders WHERE id=?", (order_id,))
        existing_order = self.cursor.fetchone()

        if existing_order:
            # Удаляем заказ из таблицы orders
            self.cursor.execute("DELETE FROM orders WHERE id=?", (order_id,))

            # Удаляем связанные записи из таблицы order_items
            self.cursor.execute("DELETE FROM order_items WHERE order_id=?", (order_id,))

            self.conn.commit()
            print(f"Заказ с идентификатором {order_id} успешно удален.")
        else:
            print(f"Заказ с идентификатором {order_id} не найден.")


# # Пример использования
#
jewelry_shop = JewelryShop()
# # Добавление товаров в магазин с ограниченным количеством
# jewelry_shop.add_product("Gold Necklace", 500, 10)
# jewelry_shop.add_product("Silver Earrings", 150, 20)
# jewelry_shop.add_product("Diamond Ring", 1000, 5)

# for item in jewelry_shop.get_available_products():
#     print(item)

# # Создание заказа
# order_products = {"Gold Necklace": 2, "Diamond Ring": 1}
# jewelry_shop.create_order("John Doe", order_products)


# cart = Cart()

# # # Добавляем товары в корзину
# cart.add_item("Gold Necklace", 2)


# # Выводим текущее состояние корзины
# print("Текущее состояние корзины:")
# print(cart.get_cart())
# for item in jewelry_shop.get_available_products():
#     print(item)
# print('---Заказ---')
# jewelry_shop.create_order(customer_name='lol',products=cart.get_cart())
# for item in jewelry_shop.get_available_products():
#     print(item)
