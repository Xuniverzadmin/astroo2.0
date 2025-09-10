"""
Initial database schema migration.

This module contains the initial database schema setup for the panchangam engine.
It creates all necessary tables for PanchangDay, FestivalDay, and MuhurthamPeriod models.
"""

import logging
from sqlalchemy import text
from ..db import engine, Base, check_database_connection

logger = logging.getLogger(__name__)

def create_initial_schema():
    """
    Create the initial database schema.
    
    This function creates all tables defined in the models.
    It's safe to run multiple times as it won't recreate existing tables.
    """
    try:
        # Check database connection first
        if not check_database_connection():
            raise Exception("Database connection failed")
        
        logger.info("Creating initial database schema...")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        # Create additional indexes for better performance
        _create_additional_indexes()
        
        logger.info("Initial database schema created successfully")
        
    except Exception as e:
        logger.error(f"Error creating initial schema: {str(e)}")
        raise

def _create_additional_indexes():
    """Create additional indexes for better query performance."""
    try:
        with engine.connect() as connection:
            # Additional indexes for panchang_days table
            additional_indexes = [
                # Composite index for date range queries
                "CREATE INDEX IF NOT EXISTS idx_panchang_date_range ON panchang_days (date DESC)",
                
                # Index for location-based queries
                "CREATE INDEX IF NOT EXISTS idx_panchang_location ON panchang_days (latitude, longitude)",
                
                # Index for timezone queries
                "CREATE INDEX IF NOT EXISTS idx_panchang_timezone ON panchang_days (timezone, date)",
                
                # Additional indexes for festival_days table
                "CREATE INDEX IF NOT EXISTS idx_festival_date_range ON festival_days (date DESC)",
                "CREATE INDEX IF NOT EXISTS idx_festival_type_importance ON festival_days (festival_type, importance)",
                
                # Additional indexes for muhurtham_periods table
                "CREATE INDEX IF NOT EXISTS idx_muhurtham_date_range ON muhurtham_periods (date DESC)",
                "CREATE INDEX IF NOT EXISTS idx_muhurtham_event_subtype ON muhurtham_periods (event_type, event_subtype)",
            ]
            
            for index_sql in additional_indexes:
                try:
                    connection.execute(text(index_sql))
                    logger.debug(f"Created index: {index_sql}")
                except Exception as e:
                    logger.warning(f"Index creation failed (may already exist): {e}")
            
            connection.commit()
            logger.info("Additional indexes created successfully")
            
    except Exception as e:
        logger.error(f"Error creating additional indexes: {str(e)}")
        # Don't raise here as the main schema creation was successful

def drop_all_tables():
    """
    Drop all tables (use with caution!).
    
    This function is useful for development and testing.
    It will remove all data from the database.
    """
    try:
        logger.warning("Dropping all database tables...")
        Base.metadata.drop_all(bind=engine)
        logger.warning("All database tables dropped successfully")
    except Exception as e:
        logger.error(f"Error dropping tables: {str(e)}")
        raise

def get_table_info():
    """Get information about existing tables."""
    try:
        with engine.connect() as connection:
            # Get list of tables
            result = connection.execute(text("""
                SELECT table_name, table_type 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            
            tables = result.fetchall()
            logger.info(f"Found {len(tables)} tables in database:")
            for table_name, table_type in tables:
                logger.info(f"  - {table_name} ({table_type})")
            
            return tables
            
    except Exception as e:
        logger.error(f"Error getting table info: {str(e)}")
        return []

if __name__ == "__main__":
    # Run schema creation if this file is executed directly
    create_initial_schema()
    get_table_info()
