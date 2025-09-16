from etl.extract import DataExtractor
from etl.transform import DataTransformer
from etl.load import DataLoader
from datetime import datetime
import schedule
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler()
    ]
)

class ETLPipeline:
    def __init__(self):
        self.extractor = DataExtractor()
        self.transformer = DataTransformer()
        self.loader = DataLoader()
    
    def run_full_pipeline(self):
        """Run complete ETL pipeline"""
        try:
            logging.info("Starting ETL pipeline...")
            
            # Extract
            logging.info("Step 1: Extracting data...")
            raw_data = self.extractor.extract_from_files()
            
            # Transform
            logging.info("Step 2: Transforming data...")
            clean_data = self.transformer.transform_all_data(raw_data)
            
            # Load
            logging.info("Step 3: Loading data to database...")
            self.loader.create_database_schema()
            self.loader.load_all_data(clean_data)
            
            # Update summary
            logging.info("Step 4: Updating sales summary...")
            self.loader.update_sales_summary()
            
            logging.info("ETL pipeline completed successfully!")
            
        except Exception as e:
            logging.error(f"Pipeline failed: {e}")
            raise e
    
    def run_incremental_update(self):
        """Run incremental data update (simplified)"""
        try:
            logging.info("Running incremental update...")
            self.loader.update_sales_summary()
            logging.info("Incremental update completed!")
        except Exception as e:
            logging.error(f"Incremental update failed: {e}")
    
    def schedule_pipeline(self):
        """Schedule pipeline runs"""
        # Full pipeline daily at 2 AM
        schedule.every().day.at("02:00").do(self.run_full_pipeline)
        
        # Incremental updates every hour
        schedule.every().hour.do(self.run_incremental_update)
        
        logging.info("Pipeline scheduled. Running scheduler...")
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

if __name__ == "__main__":
    pipeline = ETLPipeline()
    
    # Run once immediately
    pipeline.run_full_pipeline()
    
    # Uncomment to run scheduler
    # pipeline.schedule_pipeline()
