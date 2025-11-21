import psycopg2


class Postgres:
    _instance = None
    _initialized = False
    _connection = None

    def __new__(cls, options=None):
        if cls._instance is None:
            cls._instance = super(Postgres, cls).__new__(cls)
        return cls._instance

    def __init__(self, options=None):
        if not Postgres._initialized:
            if options is None:
                self.dbname = "chat_run"
                self.user = "postgres"
                self.password = "root"
                self.host = "localhost"
                self.port = 5432
            else:
                self.dbname = getattr(options, "dbname", "chat_run")
                self.user = getattr(options, "user", "postgres")
                self.password = getattr(options, "password", "root")
                self.host = getattr(options, "host", "localhost")
                self.port = getattr(options, "port", 5432)

            print("Создан экземпляр класса для работы с PostgreSQL")
            Postgres._initialized = True

    def connect(self):
        try:
            connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
            )
            self._connection = connection
            print("Соединение с PostgreSQL установлено")
            return connection
        except Exception as e:
            print(f"Ошибка при подключении к PostgreSQL: {e}")
            return None

    def cursor(self):
        if self._connection is None:
            self._connection = self.connect()
        if self._connection is not None:
            return self._connection.cursor()
        else:
            return None

    def close(self):
        if self._connection is not None:
            self._connection.close()
            print("Соединение с PostgreSQL закрыто.")
            self._connection = None
            Postgres._initialized = False
            Postgres._instance = None

    def create_table(self, table_name, columns):
        cursor = self.cursor()
        if cursor is not None:
            columns_with_types = ", ".join(
                [f"{col} {dtype}" for col, dtype in columns.items()]
            )
            create_table_query = (
                f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types});"
            )
            try:
                cursor.execute(create_table_query)
                self._connection.commit()
                print(f"Таблица '{table_name}' создана или уже существует.")
            except Exception as e:
                print(f"Ошибка при создании таблицы '{table_name}': {e}")

    def insert_data(self, table_name, data):
        cursor = self.cursor()
        if cursor is not None:
            columns = ", ".join(data.keys())
            values_placeholders = ", ".join(["%s"] * len(data))
            insert_query = (
                f"INSERT INTO {table_name} ({columns}) VALUES ({values_placeholders});"
            )
            try:
                cursor.execute(insert_query, list(data.values()))
                self._connection.commit()
                print(f"Данные вставлены в таблицу '{table_name}'.")
            except Exception as e:
                print(f"Ошибка при вставке данных в таблицу '{table_name}': {e}")

    def get_tables(self):
        cursor = self.cursor()
        if cursor is not None:
            try:
                cursor.execute(
                    """
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public';
                    """
                )
                tables = cursor.fetchall()
                return [table[0] for table in tables]
            except Exception as e:
                print(f"Ошибка при получении списка таблиц: {e}")
                return None

    def get_data_table(self, table_name):
        cursor = self.cursor()
        if cursor is not None:
            select_query = f"SELECT * FROM {table_name};"
            try:
                cursor.execute(select_query)
                records = cursor.fetchall()
                return records
            except Exception as e:
                print(f"Ошибка при получении данных из таблицы '{table_name}': {e}")
                return None
