CREATE TABLE IF NOT EXISTS sales (
    sale_id INT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT,
    price NUMERIC(10,2),
    quantity INT,
    sale_date DATE,
    total NUMERIC(10,2)
);
