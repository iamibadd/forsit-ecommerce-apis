CREATE DATABASE IF NOT EXISTS forsit_ecommerce;

USE forsit_ecommerce;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_users_email ON users(email);

CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE INDEX idx_category_name ON categories(name);

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT,
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
);

CREATE INDEX idx_product_category_id ON products(category_id);

CREATE TABLE IF NOT EXISTS inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    quantity INT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

CREATE INDEX idx_inventory_product_id ON inventory(product_id);

CREATE TABLE IF NOT EXISTS sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    quantity INT NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    sale_date DATE NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

CREATE INDEX idx_sales_product_id ON sales(product_id);

CREATE INDEX idx_sales_sale_date ON sales(sale_date);

CREATE TABLE IF NOT EXISTS revenue (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sale_id INT,
    revenue_amount DECIMAL(10, 2) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE
);

CREATE INDEX idx_revenue_sale_id ON revenue(sale_id);

CREATE INDEX idx_revenue_created_at ON revenue(created_at);
