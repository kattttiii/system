

from auth_register import UserAuthentication
from shop import JewelryShop,Cart



def main():
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            # Регистрация нового пользователя
            username = input("Enter username: ")
            password = input("Enter password: ")
            role = input("Enter role (client, employee, admin): ")
            user_auth.register_user(username, password, role)


        elif choice == "2":
            # Аутентификация пользователя
            username = input("Enter username: ")
            password = input("Enter password: ")
            role = input("Enter role (client, employee, admin): ")
            if user_auth.authenticate_user(username, password,role):
                print("Authentication successful!")
                if role == 'client':
                    # Создание объекта Cart для корзины пользователя
                    cart = Cart()

                    while True:
                        print("\n1. View Available Products\n2. Add Product to Cart\n3. View Cart\n4. Checkout\n5. Logout")
                        user_choice = input("Enter your choice: ")

                        if user_choice == "1":
                            # Просмотр доступных продуктов
                            available_products = jewelry_shop.get_available_products()
                            print("\nAvailable Products:")
                            for product in available_products:
                                print(product)

                        elif user_choice == "2":
                            # Добавление товара в корзину
                            product_name = input("Enter product name: ")
                            quantity = int(input("Enter quantity: "))
                            cart.add_item(product_name, quantity)
                            print(f"{quantity} {product_name}(s) added to cart.")

                        elif user_choice == "3":
                            # Просмотр корзины
                            current_cart = cart.get_cart()
                            print("\nCurrent Cart:")
                            for item, quantity in current_cart.items():
                                print(f"{item}: {quantity}")

                        elif user_choice == "4":
                            # Оформление заказа
                            jewelry_shop.create_order(username, cart.get_cart())
                            print("Order placed successfully!")

                            # Очистка корзины после оформления заказа
                            cart.clear_cart()

                        elif user_choice == "5":
                            # Выход из учетной записи
                            break
                        else:
                            print("Invalid choice. Please try again.")
                elif role == "employee":
                    while True:
                        # Дополнительные действия для сотрудника
                        print("\nEmployee Actions:")
                        print("1. Add Product\n2. Delete Product\n3. Update Product\n4. View Available Products\n5. Configure own user's data\n6. Logout")

                        employee_choice = input("Enter your choice: ")

                        if employee_choice == "1":
                            # Добавление нового товара
                            new_product_name = input("Enter product name: ")
                            new_product_price = float(input("Enter product price: "))
                            new_product_quantity = int(input("Enter product quantity: "))
                            jewelry_shop.add_product(new_product_name, new_product_price, new_product_quantity)

                        elif employee_choice == "2":
                            # Удаление товара
                            product_to_delete = input("Enter product name to delete: ")
                            jewelry_shop.delete_product(product_to_delete)

                        elif employee_choice == "3":
                            # Изменение параметров товара
                            product_to_update = input("Enter product name to update: ")
                            new_price = float(input("Enter new price (press Enter to keep current price): "))
                            new_quantity = int(input("Enter new quantity (press Enter to keep current quantity): "))
                            jewelry_shop.update_product(product_to_update, new_price, new_quantity)

                        elif employee_choice == "4":
                            # Просмотр доступных продуктов
                            available_products = jewelry_shop.get_available_products()
                            print("\nAvailable Products:")
                            for product in available_products:
                                print(product)
                        elif employee_choice == "5":
                            # Изменение данных пользователя
                            username_from_login = username
                            user_id_to_update = user_auth.get_id_by_name(username=username_from_login)
                            new_name = input("Enter username  to update: ")
                            new_password = input("Enter new password (press Enter to keep current password): ")
                            new_role = input("Enter new role (press Enter to keep current role): ")
                            user_auth.update_user(user_id_to_update,new_name, new_password, new_role)
                            print(f"User with ID {user_id_to_update} updated successfully.")
                        elif employee_choice == "6":
                            # Выход из учетной записи
                            break

                        else:
                            print("Invalid choice. Please try again.")            
                elif role == "admin":
                    while True:
                        # Дополнительные действия для администратора
                        print("\nAdmin Actions:")
                        print("1. View All Users\n2. Delete User\n3. Update User\n4. Configure user's data\n5. Exit Admin Panel")

                        admin_choice = input("Enter your choice: ")

                        if admin_choice == "1":
                            # Просмотр всех пользователей
                            all_users = user_auth.get_all_users()
                            print("\nAll Users:")
                            for user in all_users:
                                print(user)

                        elif admin_choice == "2":
                            # Удаление пользователя
                            user_id_to_delete = int(input("Enter user ID to delete: "))
                            user_auth.delete_user(user_id_to_delete)
                            print(f"User with ID {user_id_to_delete} deleted successfully.")

                        elif admin_choice == "3":
                            # Изменение данных пользователя
                            user_id_to_update = input("Enter user ID to update: ")
                            new_name = input("Enter username  to update: ")
                            new_password = input("Enter new password (press Enter to keep current password): ")
                            new_role = input("Enter new role (press Enter to keep current role): ")
                            user_auth.update_user(user_id_to_update,new_name, new_password, new_role)
                            print(f"User with ID {user_id_to_update} updated successfully.")

                        elif admin_choice == "4":
                            # Добавление нового пользователя
                            new_username = input("Enter username: ")
                            new_password = input("Enter password: ")
                            new_role = input("Enter role (client, employee, admin): ")
                            user_auth.register_user( new_username, new_password, new_role)
                            
                            print(f"User '{new_username}' is added successfully.")

                        elif admin_choice == "5":
                            # Выход из админ-панели
                            print("Exiting Admin Panel.")
                            break

                        else:
                            print("Invalid choice. Please try again.")

            else:
                print("Authentication failed. Please try again.")

        elif choice == "3":
            # Выход из программы
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    jewelry_shop = JewelryShop()
    user_auth = UserAuthentication()
    main()
