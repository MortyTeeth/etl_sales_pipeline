import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение данных из переменных окружения
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Подключение к PostgreSQL
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Загрузка данных
sales = pd.read_csv(
    "data/sales.csv",
    dtype={"sale_id": int, "product_name": str, "category": str, "price": float, "quantity": int},
    parse_dates=["sale_date"]
)

# Очистка данных
sales_clean = sales.dropna().copy()

# Вычисление total
sales_clean["total"] = sales_clean["price"] * sales_clean["quantity"]

# Создание таблицы (если её нет)
create_table_sql = """
CREATE TABLE IF NOT EXISTS sales (
    sale_id INT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT,
    price NUMERIC(10,2),
    quantity INT,
    sale_date DATE,
    total NUMERIC(10,2)
);
"""

with engine.connect() as conn:
    conn.execute(text(create_table_sql))

# Загрузка данных в БД
sales_clean.to_sql("sales", engine, if_exists="append", index=False)

print("\nДанные успешно загружены в PostgreSQL!")