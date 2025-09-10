"""
Management commands for the numerology application.

This module provides command-line utilities for managing the application,
including manual precomputation and maintenance tasks.
"""

import asyncio
import argparse
import logging
from datetime import date, timedelta
from typing import Optional

from .jobs import precompute_job
from .config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def run_precompute(days: Optional[int] = None, cities: Optional[str] = None):
    """Run precomputation manually."""
    try:
        # Override settings if provided
        if days:
            settings.PRECOMPUTE_DAYS = days
        if cities:
            settings.CITY_PRECOMPUTE = cities
        
        # Initialize job system
        await precompute_job.initialize()
        
        # Run precomputation
        await precompute_job.precompute_panchangam()
        
        logger.info("Precomputation completed successfully")
        
    except Exception as e:
        logger.error(f"Precomputation failed: {e}")
        raise
    finally:
        await precompute_job.cleanup()


async def check_cache_status():
    """Check the status of cached data."""
    try:
        await precompute_job.initialize()
        
        if not precompute_job.redis_client:
            logger.error("Redis client not available")
            return
        
        # Get summary
        summary = await precompute_job.redis_client.get("precompute:summary")
        if summary:
            import json
            data = json.loads(summary)
            logger.info(f"Last precomputation: {data.get('last_run')}")
            logger.info(f"Cities processed: {data.get('cities_processed')}")
            logger.info(f"Total computations: {data.get('total_computations')}")
        else:
            logger.info("No precomputation summary found")
        
        # Count cached panchangam entries
        panchangam_keys = await precompute_job.redis_client.keys("panchangam:*")
        logger.info(f"Cached panchangam entries: {len(panchangam_keys)}")
        
        # Count cached festival entries
        festival_keys = await precompute_job.redis_client.keys("festivals:*")
        logger.info(f"Cached festival entries: {len(festival_keys)}")
        
    except Exception as e:
        logger.error(f"Error checking cache status: {e}")
    finally:
        await precompute_job.cleanup()


async def clear_cache():
    """Clear all cached data."""
    try:
        await precompute_job.initialize()
        
        if not precompute_job.redis_client:
            logger.error("Redis client not available")
            return
        
        # Clear panchangam cache
        panchangam_keys = await precompute_job.redis_client.keys("panchangam:*")
        if panchangam_keys:
            await precompute_job.redis_client.delete(*panchangam_keys)
            logger.info(f"Cleared {len(panchangam_keys)} panchangam cache entries")
        
        # Clear festival cache
        festival_keys = await precompute_job.redis_client.keys("festivals:*")
        if festival_keys:
            await precompute_job.redis_client.delete(*festival_keys)
            logger.info(f"Cleared {len(festival_keys)} festival cache entries")
        
        # Clear summary
        await precompute_job.redis_client.delete("precompute:summary")
        logger.info("Cleared precomputation summary")
        
        logger.info("Cache cleared successfully")
        
    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
    finally:
        await precompute_job.cleanup()


def main():
    """Main entry point for management commands."""
    parser = argparse.ArgumentParser(description="Astrooverz Management Commands")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Precompute command
    precompute_parser = subparsers.add_parser("precompute", help="Run precomputation")
    precompute_parser.add_argument("--days", type=int, help="Number of days to precompute")
    precompute_parser.add_argument("--cities", help="Cities to precompute (IN_TOP10, IN_TOP50, IN_TOP200, ALL)")
    
    # Status command
    subparsers.add_parser("status", help="Check cache status")
    
    # Clear command
    subparsers.add_parser("clear", help="Clear cache")
    
    args = parser.parse_args()
    
    if args.command == "precompute":
        asyncio.run(run_precompute(args.days, args.cities))
    elif args.command == "status":
        asyncio.run(check_cache_status())
    elif args.command == "clear":
        asyncio.run(clear_cache())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
