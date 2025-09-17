import pandas as pd
from config.database import db_manager
import os
from sqlalchemy import text

class DataLoader:
    def __init__(self):
        self.db = db_manager
    
    def create_database_schema(self):
        """Create database tables"""
        try:
            self.db.execute_sql_file('sql/create_tables.sql')
            print("Database schema created successfully!")
        except Exception as e:
            print(f"Error creating schema: {e}")
    
    def load_table(self, df, table_name, if_exists='append'):
        """Load DataFrame to database table"""
        try:
            # Handle date columns
            date_columns = df.select_dtypes(include=['datetime64']).columns
            for col in date_columns:
                df[col] = df[col].dt.date
            
            self.db.insert_dataframe(df, table_name, if_exists=if_exists)
            print(f"Loaded {len(df)} records to {table_name}")
        except Exception as e:
            print(f"Error loading {table_name}: {e}")
    
    def load_all_data(self, data_dict):
        """Load all transformed data to database"""
        
        # Core tables first (due to foreign key constraints)
        table_order = ['customers', 'products', 'orders', 'order_items']
        
        for table_name in table_order:
            if table_name in data_dict:
                self.load_table(data_dict[table_name], table_name)
        
        # Load analytics tables
        analytics_tables = ['customer_metrics', 'product_metrics', 'monthly_summary']
        for table_name in analytics_tables:
            if table_name in data_dict:
                self.load_table(data_dict[table_name], table_name)
    
    def update_sales_summary(self):
        """Update daily sales summary table"""
        summary_query = '''
        INSERT INTO sales_summary (summary_date, total_orders, total_revenue, total_customers, avg_order_value, top_category)
        SELECT 
            o.order_date as summary_date,
            COUNT(DISTINCT o.order_id) as total_orders,
            SUM(o.total_amount) as total_revenue,
            COUNT(DISTINCT o.customer_id) as total_customers,
            AVG(o.total_amount) as avg_order_value,
            (SELECT p.category 
             FROM order_items oi 
             JOIN products p ON oi.product_id = p.product_id 
             WHERE oi.order_id IN (SELECT o2.order_id FROM orders o2 WHERE o2.order_date = o.order_date)
             GROUP BY p.category 
             ORDER BY SUM(oi.total_price) DESC 
             LIMIT 1) as top_category
        FROM orders o
        GROUP BY o.summary_date
        '''
        
        try:
            with self.db.engine.begin() as conn:
                conn.execute(text(summary_query))
            print("Sales summary updated successfully!")
        except Exception as e:
            print(f"Error updating sales summary: {e}")

if __name__ == "__main__":
    # For testing
    loader = DataLoader()
    loader.create_database_schema()
    
    # Load processed data
    processed_path = 'data/processed'
    data_to_load = {}
    
    for file in os.listdir(processed_path):
        if file.endswith('.csv'):
            table_name = file.replace('.csv', '')
            data_to_load[table_name] = pd.read_csv(f'{processed_path}/{file}')
    
    loader.load_all_data(data_to_load)
