-- Key Business Intelligence Queries

-- 1. Daily Sales Performance
CREATE OR REPLACE VIEW sales_summary AS
SELECT 
    order_date,
    COUNT(DISTINCT order_id) as total_orders,
    COUNT(DISTINCT customer_id) as total_customers,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_order_value,
    SUM(discount_amount) as total_discounts
FROM orders 
GROUP BY order_date 
ORDER BY order_date DESC;

-- 2. Customer Segmentation Analysis
CREATE OR REPLACE VIEW customer_analysis AS
SELECT 
    c.customer_segment,
    COUNT(DISTINCT c.customer_id) as total_customers,
    AVG(cm.order_count) as avg_orders_per_customer,
    AVG(cm.avg_order_value) as avg_order_value,
    SUM(cm.total_spent) as total_segment_revenue,
    AVG(cm.customer_lifetime_days) as avg_customer_lifetime_days
FROM customers c
LEFT JOIN customer_metrics cm ON c.customer_id = cm.customer_id
GROUP BY c.customer_segment;

-- 3. Product Performance by Category
CREATE OR REPLACE VIEW category_performance AS
SELECT 
    p.category,
    p.subcategory,
    COUNT(DISTINCT p.product_id) as product_count,
    SUM(pm.total_quantity_sold) as total_units_sold,
    SUM(pm.total_revenue) as total_revenue,
    AVG(p.profit_margin) as avg_profit_margin,
    COUNT(DISTINCT pm.unique_orders) as unique_orders
FROM products p
LEFT JOIN product_metrics pm ON p.product_id = pm.product_id
GROUP BY p.category, p.subcategory
ORDER BY total_revenue DESC;

-- 4. Monthly Growth Analysis
CREATE OR REPLACE VIEW monthly_summary AS
WITH monthly_stats AS (
    SELECT 
        DATE_TRUNC('month', order_date) as month,
        COUNT(DISTINCT order_id) as orders,
        SUM(total_amount) as revenue,
        COUNT(DISTINCT customer_id) as customers
    FROM orders 
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT 
    month,
    orders,
    revenue,
    customers,
    LAG(revenue) OVER (ORDER BY month) as prev_month_revenue,
    ((revenue - LAG(revenue) OVER (ORDER BY month)) / LAG(revenue) OVER (ORDER BY month) * 100)::DECIMAL(5,2) as revenue_growth_pct,
    ((orders - LAG(orders) OVER (ORDER BY month)) / LAG(orders) OVER (ORDER BY month) * 100)::DECIMAL(5,2) as orders_growth_pct
FROM monthly_stats
ORDER BY month DESC;

-- 5. Top Products Analysis
CREATE OR REPLACE VIEW product_metrics AS
SELECT 
    p.product_name,
    p.category,
    p.subcategory,
    pm.total_quantity_sold,
    pm.total_revenue,
    pm.unique_orders,
    p.unit_price,
    p.profit_margin
FROM products p
JOIN product_metrics pm ON p.product_id = pm.product_id
ORDER BY pm.total_revenue DESC
LIMIT 20;

-- 6. Customer Retention Analysis
CREATE OR REPLACE VIEW customer_retention AS
WITH customer_orders AS (
    SELECT 
        customer_id,
        order_date,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) as order_number
    FROM orders
),
retention_cohort AS (
    SELECT 
        DATE_TRUNC('month', first_order.order_date) as cohort_month,
        COUNT(DISTINCT first_order.customer_id) as cohort_size,
        COUNT(DISTINCT CASE WHEN subsequent_orders.order_date IS NOT NULL THEN first_order.customer_id END) as retained_customers
    FROM (SELECT customer_id, order_date FROM customer_orders WHERE order_number = 1) first_order
    LEFT JOIN (SELECT customer_id, order_date FROM customer_orders WHERE order_number > 1) subsequent_orders
        ON first_order.customer_id = subsequent_orders.customer_id
        AND subsequent_orders.order_date > first_order.order_date + INTERVAL '30 days'
    GROUP BY DATE_TRUNC('month', first_order.order_date)
)
SELECT 
    cohort_month,
    cohort_size,
    retained_customers,
    (retained_customers::DECIMAL / cohort_size * 100)::DECIMAL(5,2) as retention_rate
FROM retention_cohort
ORDER BY cohort_month DESC;
