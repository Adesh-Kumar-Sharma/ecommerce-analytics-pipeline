import pandas as pd
import numpy as np
from datetime import datetime
import os

class DataTransformer:
    def __init__(self):
        self.processed_path = 'data/processed'
        os.makedirs(self.processed_path, exist_ok=True)
    
    def clean_customers(self, df):
        """Clean and validate customer data"""
        # Remove duplicates
        df = df.drop_duplicates(subset=['email'])
        
        # Validate email format (basic)
        df = df[df['email'].str.contains('@', na=False)]
        
        # Standardize country names
        country_mapping = {
            'US': 'USA',
            'United States': 'USA',
            'UK': 'United Kingdom',
            'Deutschland': 'Germany'
        }
        df['country'] = df['country'].replace(country_mapping)
        
        # Validate dates
        df['registration_date'] = pd.to_datetime(df['registration_date'], errors='coerce')
        df = df.dropna(subset=['registration_date'])
        
        return df
    
    def clean_products(self, df):
        """Clean and validate product data"""
        # Remove products with invalid prices
        df = df[df['unit_price'] > 0]
        df = df[df['cost_price'] > 0]
        
        # Calculate profit margin
        df['profit_margin'] = ((df['unit_price'] - df['cost_price']) / df['unit_price'] * 100).round(2)
        
        # Standardize category names
        df['category'] = df['category'].str.title()
        df['subcategory'] = df['subcategory'].str.title()
        
        # Validate dates
        df['created_date'] = pd.to_datetime(df['created_date'], errors='coerce')
        
        return df
    
    def clean_orders(self, df):
        """Clean and validate order data"""
        # Convert date columns
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        df['ship_date'] = pd.to_datetime(df['ship_date'], errors='coerce')
        
        # Remove orders with invalid dates
        df = df.dropna(subset=['order_date'])
        
        # Calculate shipping days
        df['shipping_days'] = (df['ship_date'] - df['order_date']).dt.days
        
        # Validate amounts
        df = df[df['total_amount'] > 0]
        df['discount_amount'] = df['discount_amount'].fillna(0)
        
        # Add derived fields
        df['order_month'] = df['order_date'].dt.to_period('M').astype(str)
        df['order_year'] = df['order_date'].dt.year
        df['day_of_week'] = df['order_date'].dt.day_name()
        
        return df
    
    def clean_order_items(self, df):
        """Clean and validate order items data"""
        # Validate quantities and prices
        df = df[df['quantity'] > 0]
        df = df[df['unit_price'] > 0]
        
        # Recalculate total price to ensure consistency
        df['total_price'] = df['quantity'] * df['unit_price']
        
        # Apply discount
        df['discount_amount'] = df['total_price'] * df['discount_percentage'] / 100
        df['final_price'] = df['total_price'] - df['discount_amount']
        
        return df
    
    def create_business_metrics(self, orders_df, order_items_df, customers_df, products_df):
        """Create business intelligence metrics"""
        
        # Ensure data is consistent
        # Get all valid order IDs from the (already filtered) orders_df
        valid_order_ids = orders_df['order_id'].unique()

        # Filter order_items_df to only include items for those valid orders
        order_items_df_cleaned = order_items_df[order_items_df['order_id'].isin(valid_order_ids)].copy()

        # Customer metrics
        customer_metrics = orders_df.groupby('customer_id').agg({
            'order_id': 'count',
            'total_amount': ['sum', 'mean', 'max'],
            'order_date': ['min', 'max']
            #maybe summary_date
        }).round(2)
        
        customer_metrics.columns = ['order_count', 'total_spent', 'avg_order_value', 'max_order_value', 'first_order', 'last_order']
        customer_metrics['customer_lifetime_days'] = (customer_metrics['last_order'] - customer_metrics['first_order']).dt.days
        customer_metrics = customer_metrics.reset_index()
        
        # Product performance
        product_metrics = order_items_df_cleaned.groupby('product_id').agg({
            'quantity': 'sum',
            'total_price': 'sum',
            'order_id': 'nunique'
        }).round(2)
        
        product_metrics.columns = ['total_quantity_sold', 'total_revenue', 'unique_orders']
        product_metrics = product_metrics.reset_index()

        # Monthly sales summary
        monthly_summary = orders_df.groupby('order_month').agg({
            'order_id': 'count',
            'total_amount': 'sum',
            'customer_id': 'nunique'
        }).round(2)
        
        monthly_summary.columns = ['total_orders', 'total_revenue', 'total_customers']
        monthly_summary['avg_order_value'] = (monthly_summary['total_revenue'] / monthly_summary['total_orders']).round(2)
        monthly_summary = monthly_summary.reset_index()
        
        # Add order_items_df_cleaned to your return statement
        return customer_metrics, product_metrics, monthly_summary, order_items_df_cleaned
    
    def transform_all_data(self, data_dict):
        """Transform all extracted data"""
        transformed_data = {}
        
        # Transform each table
        transformed_data['customers'] = self.clean_customers(data_dict['customers'])
        transformed_data['products'] = self.clean_products(data_dict['products'])
        transformed_data['orders'] = self.clean_orders(data_dict['orders'])
        transformed_data['order_items'] = self.clean_order_items(data_dict['order_items'])
        
        # Create business metrics
        customer_metrics, product_metrics, monthly_summary, order_items_df_cleaned = self.create_business_metrics(
            transformed_data['orders'],
            transformed_data['order_items'],
            transformed_data['customers'],
            transformed_data['products']
        )
        
        transformed_data['customer_metrics'] = customer_metrics
        transformed_data['product_metrics'] = product_metrics
        transformed_data['monthly_summary'] = monthly_summary
        transformed_data['order_items'] = order_items_df_cleaned
        
        # Save processed data
        for table_name, df in transformed_data.items():
            df.to_csv(f'{self.processed_path}/{table_name}.csv', index=False)
            print(f"Saved {len(df)} records to {table_name}.csv")
        
        return transformed_data

if __name__ == "__main__":
    # For testing
    from extract import DataExtractor
    
    extractor = DataExtractor()
    raw_data = extractor.extract_from_files()
    
    transformer = DataTransformer()
    clean_data = transformer.transform_all_data(raw_data)
