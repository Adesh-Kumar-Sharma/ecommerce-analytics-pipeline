import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
import json
import os

class DataExtractor:
    def __init__(self):
        self.base_path = 'data/raw'
        os.makedirs(self.base_path, exist_ok=True)
    
    def generate_synthetic_ecommerce_data(self):
        """Generate synthetic e-commerce data for demonstration"""
        np.random.seed(42)
        
        # Generate customers
        n_customers = 1000
        customers = []
        for i in range(n_customers):
            customers.append({
                'customer_id': i + 1,
                'customer_name': f'Customer {i + 1}',
                'email': f'customer{i+1}@email.com',
                'registration_date': (datetime.now() - timedelta(days=np.random.randint(1, 365))).date(),
                'country': np.random.choice(['USA', 'Canada', 'UK', 'Germany', 'France'], p=[0.4, 0.2, 0.15, 0.15, 0.1]),
                'city': np.random.choice(['New York', 'London', 'Toronto', 'Berlin', 'Paris']),
                'customer_segment': np.random.choice(['Premium', 'Regular', 'Bronze'], p=[0.2, 0.6, 0.2])
            })
        
        # Generate products
        categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books']
        subcategories = {
            'Electronics': ['Phones', 'Laptops', 'Accessories'],
            'Clothing': ['Men', 'Women', 'Kids'],
            'Home & Garden': ['Furniture', 'Decor', 'Tools'],
            'Sports': ['Fitness', 'Outdoor', 'Team Sports'],
            'Books': ['Fiction', 'Non-Fiction', 'Technical']
        }
        
        products = []
        product_id = 1
        for category in categories:
            for subcategory in subcategories[category]:
                for i in range(20):
                    products.append({
                        'product_id': product_id,
                        'product_name': f'{subcategory} Product {i+1}',
                        'category': category,
                        'subcategory': subcategory,
                        'unit_price': round(np.random.uniform(10, 500), 2),
                        'cost_price': round(np.random.uniform(5, 250), 2),
                        'brand': f'Brand {np.random.randint(1, 10)}',
                        'created_date': (datetime.now() - timedelta(days=np.random.randint(1, 180))).date()
                    })
                    product_id += 1
        
        # Generate orders and order items
        orders = []
        order_items = []
        order_id = 1
        item_id = 1
        
        for _ in range(2000):  # 2000 orders
            customer_id = np.random.randint(1, n_customers + 1)
            order_date = datetime.now() - timedelta(days=np.random.randint(1, 90))
            ship_date = order_date + timedelta(days=np.random.randint(1, 7))
            
            order = {
                'order_id': order_id,
                'customer_id': customer_id,
                'order_date': order_date.date(),
                'ship_date': ship_date.date(),
                'ship_mode': np.random.choice(['Standard', 'Express', 'Priority']),
                'order_status': np.random.choice(['Completed', 'Pending', 'Shipped'], p=[0.8, 0.1, 0.1]),
                'discount_amount': round(np.random.uniform(0, 50), 2)
            }
            
            # Generate order items
            n_items = np.random.randint(1, 5)
            total_amount = 0
            
            for _ in range(n_items):
                product = np.random.choice(products)
                quantity = np.random.randint(1, 4)
                unit_price = product['unit_price']
                total_price = quantity * unit_price
                total_amount += total_price
                
                order_items.append({
                    'item_id': item_id,
                    'order_id': order_id,
                    'product_id': product['product_id'],
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'total_price': total_price,
                    'discount_percentage': np.random.uniform(0, 15)
                })
                item_id += 1
            
            order['total_amount'] = round(total_amount - order['discount_amount'], 2)
            orders.append(order)
            order_id += 1
        
        # Save to CSV files
        pd.DataFrame(customers).to_csv(f'{self.base_path}/customers.csv', index=False)
        pd.DataFrame(products).to_csv(f'{self.base_path}/products.csv', index=False)
        pd.DataFrame(orders).to_csv(f'{self.base_path}/orders.csv', index=False)
        pd.DataFrame(order_items).to_csv(f'{self.base_path}/order_items.csv', index=False)
        
        print("Synthetic e-commerce data generated successfully!")
        return customers, products, orders, order_items
    
    def extract_from_api(self, api_url):
        """Extract data from API (placeholder for real API)"""
        try:
            response = requests.get(api_url, timeout=30)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API request failed with status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error extracting from API: {e}")
            return None
    
    def extract_from_files(self):
        """Extract data from CSV files"""
        data = {}
        files = ['customers.csv', 'products.csv', 'orders.csv', 'order_items.csv']
        
        for file in files:
            file_path = f'{self.base_path}/{file}'

            # Define table_name before the if/else block
            table_name = file.replace('.csv', '')

            if os.path.exists(file_path):
                table_name = file.replace('.csv', '')
                data[table_name] = pd.read_csv(file_path)
                print(f"Extracted {len(data[table_name])} records from {file}")
            else:
                print(f"File {file} not found. Generating synthetic data...")
                self.generate_synthetic_ecommerce_data()
                data[table_name] = pd.read_csv(file_path)
        
        return data

if __name__ == "__main__":
    extractor = DataExtractor()
    data = extractor.extract_from_files()
