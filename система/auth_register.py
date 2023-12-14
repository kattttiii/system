import sqlite3

class UserAuthentication:
    def __init__(self, database_path: str = "users.db") -> None:
        """
        Инициализация объекта UserAuthentication.

        :param database_path: Путь к файлу базы данных SQLite.
        """
        self.conn = sqlite3.connect(database_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self) -> None:
        """
        Создание таблицы users в базе данных, если её нет.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def register_user(self, username: str, password: str, role: str) -> None:
        """
        Регистрация нового пользователя.
        role: Роль пользователя (client, employee, admin).
        """
        # Проверяем, существует ли пользователь с таким именем
        self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = self.cursor.fetchone()

        if existing_user:
            print(f"Пользователь с именем '{username}' уже существует. Выберите другое имя.")
        else:
            # Регистрируем нового пользователя
            self.cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
            self.conn.commit()
            print("Registration successful!")

    def authenticate_user(self, username: str, password: str,role:str) -> bool:
        try:
            """
            Проверка аутентификации пользователя.
            return: True, если пользователь прошел аутентификацию, иначе False.
            """
            self.cursor.execute("SELECT * FROM users WHERE username=? AND password=? AND role=?", (username, password,role))
            user = self.cursor.fetchone()
            return user is not None
        except Exception as e:
            print(e)

    def get_all_users(self) -> list:
        """
        Получение списка всех зарегистрированных пользователей.

        :return: Список пользователей в виде кортежей (id, username, password, role).
        """
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def delete_user(self, user_id: int) -> None:
        """
        Удаление пользователя по его идентификатору.

        :param user_id: Идентификатор пользователя.
        """
        try:
            self.cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
            self.conn.commit()
        except Exception as e:
            print(e)
    def update_user(self, user_id: int,new_name: str = None, new_password: str = None, new_role: str = None) -> None:
        """
        Изменение данных пользователя.
        """
        # Проверяем, существует ли пользователь с указанным идентификатором
        self.cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
        existing_user = self.cursor.fetchone()

        if existing_user:
            current_name, current_password, current_role = existing_user[1], existing_user[2], existing_user[3]

            # Подготавливаем новые значения или оставляем текущие, если они не были указаны
            updated_name = new_name if new_name is not None else current_name
            updated_password = new_password if new_password is not None else current_password
            updated_role = new_role if new_role is not None else current_role

            # Обновляем запись о пользователе
            self.cursor.execute("UPDATE users SET username=?,password=?, role=? WHERE id=?",
                                (updated_name,updated_password, updated_role, user_id))
            self.conn.commit()

            print(f"Данные пользователя с идентификатором {user_id} успешно обновлены.")
        else:
            print(f"Пользователь с идентификатором {user_id} не найден.")
    def get_id_by_name(self, username: str) -> int:
        """
        Получение идентификатора пользователя по его имени.
        """
        # Проверяем, существует ли пользователь с указанным именем
        self.cursor.execute("SELECT id FROM users WHERE username=?", (username,))
        user_id = self.cursor.fetchone()

        if user_id:
            return user_id[0]
        else:
            print(f"Пользователь с именем '{username}' не найден.")

# # Пример использования
# authenticator = UserAuthentication()

# # Регистрация пользователей
# authenticator.register_user("client1", "password123", "client")
# authenticator.register_user("employee1", "securepass", "employee")
# authenticator.register_user("admin1", "adminpass", "admin")

# # Получение списка всех пользователей
# all_users = authenticator.get_all_users()
# print("All Users:", all_users)






## Удаление пользователя (по выбору - замените user_id на фактический идентификатор)
# user_id_to_delete = 1
# authenticator.delete_user(user_id_to_delete)

# # Повторное получение списка всех пользователей после удаления
# all_users_after_deletion = authenticator.get_all_users()
# print("All Users After Deletion:", all_users_after_deletion)
