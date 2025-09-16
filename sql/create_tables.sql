-- Drop tables if they exist
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS sales_summary CASCADE;

-- Create customers table
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    registration_date DATE NOT NULL,
    country VARCHAR(50),
    city VARCHAR(50),
    customer_segment VARCHAR(20) DEFAULT 'Regular'
);

-- Create products table
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,
    category VARCHAR(50) NOT NULL,
    subcategory VARCHAR(50),
    unit_price DECIMAL(10, 2) NOT NULL,
    cost_price DECIMAL(10, 2),
    brand VARCHAR(50),
    created_date DATE DEFAULT CURRENT_DATE,
    profit_margin DECIMAL(10, 2)
);

-- Create orders table
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    order_date DATE NOT NULL,
    ship_date DATE,
    ship_mode VARCHAR(20),
    order_status VARCHAR(20) DEFAULT 'Pending',
    total_amount DECIMAL(12, 2),
    discount_amount DECIMAL(10, 2) DEFAULT 0,
    shipping_days INTEGER,
    order_month VARCHAR(7),
    order_year INTEGER,
    day_of_week VARCHAR(10)
);

-- Create order_items table
CREATE TABLE order_items (
    item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    total_price DECIMAL(12, 2) NOT NULL,
    discount_percentage DECIMAL(5, 2) DEFAULT 0,
    discount_amount DECIMAL(10, 2),
    final_price DECIMAL(12, 2)
);

-- Create sales summary table for analytics
CREATE TABLE sales_summary (
    summary_id SERIAL PRIMARY KEY,
    summary_date DATE NOT NULL,
    total_orders INTEGER,
    total_revenue DECIMAL(15, 2),
    total_customers INTEGER,
    avg_order_value DECIMAL(10, 2),
    top_category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);
CREATE INDEX idx_customers_segment ON customers(customer_segment);
CREATE INDEX idx_products_category ON products(category);
