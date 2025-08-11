import pandas as pd
from sqlalchemy import create_engine, text

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


# Подключение к postgresql
engine = create_engine("postgresql+psycopg2://postgres:This1is2just3a4test!@localhost:5432/sales_db")


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


# 6. Загрузка данных в БД
sales_clean.to_sql("sales", engine, if_exists="append", index=False)

print("\nДанные успешно загружены в PostgreSQL!")

