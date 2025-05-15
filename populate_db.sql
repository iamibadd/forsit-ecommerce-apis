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
