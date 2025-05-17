CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT,
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    sale_date DATE NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS revenue (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sale_id INT NOT NULL,
    revenue_amount DECIMAL(10, 2) NOT NULL,
    created_at DATE NOT NULL,
    FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE
);

-- Data Insertion
INSERT INTO categories (name) VALUES 
('Electronics'), 
('Books'), 
('Clothing'), 
('Home'), 
('Toys');

INSERT INTO products (name, price, description, category_id)
SELECT 
  CONCAT('Product_', LPAD(FLOOR(RAND() * 10000), 4, '0')),
  ROUND(5 + (RAND() * 495), 2),
  'Sample product description.',
  FLOOR(1 + (RAND() * 5))
FROM 
  information_schema.columns LIMIT 1000;

INSERT INTO inventory (product_id, quantity)
SELECT 
  id, FLOOR(1 + (RAND() * 100))
FROM 
  products;

INSERT INTO sales (product_id, quantity, total_price, sale_date)
SELECT 
  id,
  FLOOR(1 + (RAND() * 10)),
  ROUND(10 + (RAND() * 490), 2),
  CURDATE() - INTERVAL FLOOR(RAND() * 365) DAY
FROM 
  products
ORDER BY RAND()
LIMIT 1000;

INSERT INTO revenue (sale_id, revenue_amount, created_at)
SELECT 
  id,
  total_price,
  sale_date
FROM 
  sales;
