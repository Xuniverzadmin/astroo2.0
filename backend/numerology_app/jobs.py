"""
Background jobs for precomputing panchangam data and caching.

This module provides scheduled jobs for precomputing panchangam data
for top cities to improve API response times.
"""

import logging
import os
from datetime import date, datetime, timedelta
from typing import List, Dict, Any, Optional
import json
import asyncio
from dataclasses import dataclass

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import redis.asyncio as redis

from .config import settings
from .panchangam.core import assemble_panchangam
from .festivals.service import festival_service
from .models import PanchangDay, FestivalDay
from .db import SessionLocal

logger = logging.getLogger(__name__)


@dataclass
class City:
    """City data for precomputation."""
    name: str
    state: str
    country: str
    latitude: float
    longitude: float
    timezone: str
    population: Optional[int] = None
    rank: Optional[int] = None


class PrecomputeJob:
    """Job for precomputing panchangam data for top cities."""
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self.scheduler: Optional[AsyncIOScheduler] = None
        self.cities: List[City] = []
        
    async def initialize(self):
        """Initialize the job system."""
        try:
            # Initialize Redis client
            if settings.REDIS_URL:
                self.redis_client = redis.from_url(
                    settings.REDIS_URL, 
                    encoding="utf-8", 
                    decode_responses=True
                )
                await self.redis_client.ping()
                logger.info("Redis client initialized for precompute jobs")
            
            # Load cities data
            self.cities = self._load_cities_data()
            logger.info(f"Loaded {len(self.cities)} cities for precomputation")
            
            # Initialize scheduler
            self.scheduler = AsyncIOScheduler()
            
        except Exception as e:
            logger.error(f"Error initializing precompute job: {e}")
            raise
    
    def _load_cities_data(self) -> List[City]:
        """Load cities data based on configuration."""
        all_cities = self._get_all_cities()
        
        # Filter cities based on configuration
        if settings.CITY_PRECOMPUTE == "IN_TOP10":
            return [city for city in all_cities if city.rank and city.rank <= 10]
        elif settings.CITY_PRECOMPUTE == "IN_TOP50":
            return [city for city in all_cities if city.rank and city.rank <= 50]
        elif settings.CITY_PRECOMPUTE == "IN_TOP200":
            return [city for city in all_cities if city.rank and city.rank <= 200]
        elif settings.CITY_PRECOMPUTE == "ALL":
            return all_cities
        else:
            # Default to top 200
            return [city for city in all_cities if city.rank and city.rank <= 200]
    
    def _get_all_cities(self) -> List[City]:
        """Get all cities data for India."""
        return [
            # Top 20 Indian cities by population
            City("Mumbai", "Maharashtra", "India", 19.0760, 72.8777, "Asia/Kolkata", 12478447, 1),
            City("Delhi", "Delhi", "India", 28.7041, 77.1025, "Asia/Kolkata", 11034555, 2),
            City("Bangalore", "Karnataka", "India", 12.9716, 77.5946, "Asia/Kolkata", 8443675, 3),
            City("Hyderabad", "Telangana", "India", 17.3850, 78.4867, "Asia/Kolkata", 6809970, 4),
            City("Ahmedabad", "Gujarat", "India", 23.0225, 72.5714, "Asia/Kolkata", 5570585, 5),
            City("Chennai", "Tamil Nadu", "India", 13.0827, 80.2707, "Asia/Kolkata", 4646732, 6),
            City("Kolkata", "West Bengal", "India", 22.5726, 88.3639, "Asia/Kolkata", 4496694, 7),
            City("Surat", "Gujarat", "India", 21.1702, 72.8311, "Asia/Kolkata", 4467797, 8),
            City("Pune", "Maharashtra", "India", 18.5204, 73.8567, "Asia/Kolkata", 3124458, 9),
            City("Jaipur", "Rajasthan", "India", 26.9124, 75.7873, "Asia/Kolkata", 3073350, 10),
            City("Lucknow", "Uttar Pradesh", "India", 26.8467, 80.9462, "Asia/Kolkata", 2817101, 11),
            City("Kanpur", "Uttar Pradesh", "India", 26.4499, 80.3319, "Asia/Kolkata", 2767031, 12),
            City("Nagpur", "Maharashtra", "India", 21.1458, 79.0882, "Asia/Kolkata", 2405665, 13),
            City("Indore", "Madhya Pradesh", "India", 22.7196, 75.8577, "Asia/Kolkata", 1964086, 14),
            City("Thane", "Maharashtra", "India", 19.2183, 72.9781, "Asia/Kolkata", 1841488, 15),
            City("Bhopal", "Madhya Pradesh", "India", 23.2599, 77.4126, "Asia/Kolkata", 1798218, 16),
            City("Visakhapatnam", "Andhra Pradesh", "India", 17.6868, 83.2185, "Asia/Kolkata", 1728128, 17),
            City("Pimpri-Chinchwad", "Maharashtra", "India", 18.6298, 73.7997, "Asia/Kolkata", 1727692, 18),
            City("Patna", "Bihar", "India", 25.5941, 85.1376, "Asia/Kolkata", 1684222, 19),
            City("Vadodara", "Gujarat", "India", 22.3072, 73.1812, "Asia/Kolkata", 1670806, 20),
            
            # Additional major cities
            City("Ghaziabad", "Uttar Pradesh", "India", 28.6692, 77.4538, "Asia/Kolkata", 1648643, 21),
            City("Ludhiana", "Punjab", "India", 30.9010, 75.8573, "Asia/Kolkata", 1618879, 22),
            City("Agra", "Uttar Pradesh", "India", 27.1767, 78.0081, "Asia/Kolkata", 1585704, 23),
            City("Nashik", "Maharashtra", "India", 19.9975, 73.7898, "Asia/Kolkata", 1486053, 24),
            City("Faridabad", "Haryana", "India", 28.4089, 77.3178, "Asia/Kolkata", 1414050, 25),
            City("Meerut", "Uttar Pradesh", "India", 28.9845, 77.7064, "Asia/Kolkata", 1305429, 26),
            City("Rajkot", "Gujarat", "India", 22.3039, 70.8022, "Asia/Kolkata", 1286678, 27),
            City("Kalyan-Dombivali", "Maharashtra", "India", 19.2403, 73.1305, "Asia/Kolkata", 1247327, 28),
            City("Vasai-Virar", "Maharashtra", "India", 19.4259, 72.8225, "Asia/Kolkata", 1222390, 29),
            City("Varanasi", "Uttar Pradesh", "India", 25.3176, 82.9739, "Asia/Kolkata", 1198491, 30),
            
            # South Indian cities
            City("Kochi", "Kerala", "India", 9.9312, 76.2673, "Asia/Kolkata", 677381, 31),
            City("Coimbatore", "Tamil Nadu", "India", 11.0168, 76.9558, "Asia/Kolkata", 1064238, 32),
            City("Madurai", "Tamil Nadu", "India", 9.9252, 78.1198, "Asia/Kolkata", 1017865, 33),
            City("Tiruchirappalli", "Tamil Nadu", "India", 10.7905, 78.7047, "Asia/Kolkata", 916857, 34),
            City("Salem", "Tamil Nadu", "India", 11.6643, 78.1460, "Asia/Kolkata", 829267, 35),
            City("Tirunelveli", "Tamil Nadu", "India", 8.7139, 77.7567, "Asia/Kolkata", 473637, 36),
            City("Erode", "Tamil Nadu", "India", 11.3410, 77.7172, "Asia/Kolkata", 521776, 37),
            City("Thiruvananthapuram", "Kerala", "India", 8.5241, 76.9366, "Asia/Kolkata", 752490, 38),
            City("Kozhikode", "Kerala", "India", 11.2588, 75.7804, "Asia/Kolkata", 431560, 39),
            City("Thrissur", "Kerala", "India", 10.5276, 76.2144, "Asia/Kolkata", 315596, 40),
            
            # North Indian cities
            City("Chandigarh", "Chandigarh", "India", 30.7333, 76.7794, "Asia/Kolkata", 960787, 41),
            City("Amritsar", "Punjab", "India", 31.6340, 74.8723, "Asia/Kolkata", 1132383, 42),
            City("Jalandhar", "Punjab", "India", 31.3260, 75.5762, "Asia/Kolkata", 862196, 43),
            City("Bathinda", "Punjab", "India", 30.2110, 74.9455, "Asia/Kolkata", 285813, 44),
            City("Patiala", "Punjab", "India", 30.3398, 76.3869, "Asia/Kolkata", 329224, 45),
            City("Gurgaon", "Haryana", "India", 28.4595, 77.0266, "Asia/Kolkata", 876824, 46),
            City("Panipat", "Haryana", "India", 29.3909, 76.9635, "Asia/Kolkata", 294292, 47),
            City("Ambala", "Haryana", "India", 30.3753, 76.7821, "Asia/Kolkata", 207934, 48),
            City("Hisar", "Haryana", "India", 29.1492, 75.7217, "Asia/Kolkata", 301249, 49),
            City("Rohtak", "Haryana", "India", 28.8955, 76.6066, "Asia/Kolkata", 374292, 50),
        ]
    
    async def precompute_panchangam(self):
        """Precompute panchangam data for all configured cities."""
        if not self.cities:
            logger.warning("No cities configured for precomputation")
            return
        
        logger.info(f"Starting panchangam precomputation for {len(self.cities)} cities")
        
        # Calculate date range
        today = date.today()
        end_date = today + timedelta(days=settings.PRECOMPUTE_DAYS)
        
        total_computations = 0
        successful_computations = 0
        failed_computations = 0
        
        for city in self.cities:
            try:
                logger.info(f"Precomputing for {city.name}, {city.state}")
                
                # Precompute panchangam data
                panchangam_count = await self._precompute_city_panchangam(city, today, end_date)
                
                # Precompute festival data
                festival_count = await self._precompute_city_festivals(city, today, end_date)
                
                total_computations += panchangam_count + festival_count
                successful_computations += panchangam_count + festival_count
                
                logger.info(f"Completed {city.name}: {panchangam_count} panchangam, {festival_count} festivals")
                
            except Exception as e:
                logger.error(f"Error precomputing for {city.name}: {e}")
                failed_computations += 1
                continue
        
        logger.info(f"Precomputation completed: {successful_computations} successful, {failed_computations} failed")
        
        # Store summary in Redis
        if self.redis_client:
            summary = {
                "last_run": datetime.now().isoformat(),
                "cities_processed": len(self.cities),
                "total_computations": total_computations,
                "successful_computations": successful_computations,
                "failed_computations": failed_computations,
                "date_range": {
                    "start": today.isoformat(),
                    "end": end_date.isoformat()
                }
            }
            await self.redis_client.set(
                "precompute:summary", 
                json.dumps(summary), 
                ex=86400  # 24 hours
            )
    
    async def _precompute_city_panchangam(self, city: City, start_date: date, end_date: date) -> int:
        """Precompute panchangam data for a specific city."""
        count = 0
        current_date = start_date
        
        while current_date <= end_date:
            try:
                # Generate cache key
                cache_key = f"panchangam:{city.name.lower().replace(' ', '_')}:{current_date.isoformat()}"
                
                # Check if already cached
                if self.redis_client:
                    cached = await self.redis_client.get(cache_key)
                    if cached:
                        current_date += timedelta(days=1)
                        continue
                
                # Compute panchangam data
                panchangam_data = assemble_panchangam(
                    current_date, 
                    city.latitude, 
                    city.longitude, 
                    city.timezone
                )
                
                # Store in Redis
                if self.redis_client:
                    await self.redis_client.set(
                        cache_key, 
                        json.dumps(panchangam_data, default=str), 
                        ex=86400 * 7  # 7 days
                    )
                
                # Store in database (optional)
                await self._store_panchangam_to_db(panchangam_data, city)
                
                count += 1
                current_date += timedelta(days=1)
                
            except Exception as e:
                logger.error(f"Error precomputing panchangam for {city.name} on {current_date}: {e}")
                current_date += timedelta(days=1)
                continue
        
        return count
    
    async def _precompute_city_festivals(self, city: City, start_date: date, end_date: date) -> int:
        """Precompute festival data for a specific city."""
        count = 0
        
        # Get festivals for the date range
        current_date = start_date
        while current_date <= end_date:
            try:
                # Generate cache key
                cache_key = f"festivals:{city.name.lower().replace(' ', '_')}:{current_date.year}:{current_date.month}"
                
                # Check if already cached
                if self.redis_client:
                    cached = await self.redis_client.get(cache_key)
                    if cached:
                        # Move to next month
                        if current_date.month == 12:
                            current_date = date(current_date.year + 1, 1, 1)
                        else:
                            current_date = date(current_date.year, current_date.month + 1, 1)
                        continue
                
                # Compute festival data
                festivals = festival_service.build_month(
                    current_date.year,
                    current_date.month,
                    city.latitude,
                    city.longitude,
                    city.timezone,
                    self._get_region_for_city(city)
                )
                
                # Store in Redis
                if self.redis_client:
                    await self.redis_client.set(
                        cache_key, 
                        json.dumps(festivals, default=str), 
                        ex=86400 * 30  # 30 days
                    )
                
                # Store in database
                if festivals:
                    festival_service.save_festivals_to_db(festivals)
                    count += len(festivals)
                
                # Move to next month
                if current_date.month == 12:
                    current_date = date(current_date.year + 1, 1, 1)
                else:
                    current_date = date(current_date.year, current_date.month + 1, 1)
                
            except Exception as e:
                logger.error(f"Error precomputing festivals for {city.name} on {current_date}: {e}")
                # Move to next month
                if current_date.month == 12:
                    current_date = date(current_date.year + 1, 1, 1)
                else:
                    current_date = date(current_date.year, current_date.month + 1, 1)
                continue
        
        return count
    
    def _get_region_for_city(self, city: City) -> str:
        """Get region code for a city."""
        region_mapping = {
            "Tamil Nadu": "TN",
            "Kerala": "KL", 
            "Karnataka": "KA",
            "Andhra Pradesh": "AP",
            "Telangana": "TS",
            "Maharashtra": "MH",
            "Gujarat": "GJ",
            "Rajasthan": "RJ",
            "Uttar Pradesh": "UP",
            "Madhya Pradesh": "MP",
            "West Bengal": "WB",
            "Odisha": "OR",
            "Assam": "AS",
            "Punjab": "PB",
            "Haryana": "HR",
            "Delhi": "DL",
            "Jammu and Kashmir": "JK",
            "Himachal Pradesh": "HP",
            "Uttarakhand": "UK",
            "Bihar": "BR",
            "Jharkhand": "JH",
            "Chhattisgarh": "CT",
            "Goa": "GA",
            "Manipur": "MN",
            "Mizoram": "MZ",
            "Nagaland": "NL",
            "Tripura": "TR",
            "Sikkim": "SK",
            "Arunachal Pradesh": "AR",
            "Meghalaya": "ML",
            "Chandigarh": "CH"
        }
        return region_mapping.get(city.state, "ALL")
    
    async def _store_panchangam_to_db(self, panchangam_data: Dict[str, Any], city: City):
        """Store panchangam data to database."""
        try:
            db = SessionLocal()
            try:
                # Check if already exists
                existing = db.query(PanchangDay).filter(
                    PanchangDay.date == date.fromisoformat(panchangam_data["date"]),
                    PanchangDay.latitude == city.latitude,
                    PanchangDay.longitude == city.longitude
                ).first()
                
                if not existing:
                    # Create PanchangDay object
                    panchang_day = PanchangDay(
                        date=date.fromisoformat(panchangam_data["date"]),
                        latitude=city.latitude,
                        longitude=city.longitude,
                        timezone=city.timezone,
                        sunrise=datetime.fromisoformat(panchangam_data["sunrise"]),
                        sunset=datetime.fromisoformat(panchangam_data["sunset"]),
                        tithi_number=panchangam_data["tithi"]["number"],
                        tithi_name=panchangam_data["tithi"]["name"],
                        tithi_progress=panchangam_data["tithi"]["progress"],
                        nakshatra_number=panchangam_data["nakshatra"]["number"],
                        nakshatra_name=panchangam_data["nakshatra"]["name"],
                        nakshatra_progress=panchangam_data["nakshatra"]["progress"],
                        yoga_number=panchangam_data["yoga"]["number"],
                        yoga_name=panchangam_data["yoga"]["name"],
                        yoga_progress=panchangam_data["yoga"]["progress"],
                        karana_name=panchangam_data["karana"]["name"],
                        karana_progress=panchangam_data["karana"]["progress"],
                        rahu_kalam=panchangam_data["rahu_kalam"],
                        yama_gandam=panchangam_data["yama_gandam"],
                        gulikai_kalam=panchangam_data["gulikai_kalam"],
                        horas=panchangam_data["horas"],
                        gowri_panchangam=panchangam_data["gowri_panchangam"]
                    )
                    
                    db.add(panchang_day)
                    db.commit()
                    
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Error storing panchangam to database: {e}")
    
    def start_scheduler(self):
        """Start the job scheduler."""
        if not self.scheduler:
            logger.error("Scheduler not initialized")
            return
        
        if not settings.SCHED_ENABLED:
            logger.info("Job scheduling is disabled")
            return
        
        try:
            # Parse time (format: "HH:MM")
            hour, minute = map(int, settings.PRECOMPUTE_TIME.split(":"))
            
            # Schedule precompute job at 02:30 IST daily
            self.scheduler.add_job(
                self.precompute_panchangam,
                trigger=CronTrigger(hour=hour, minute=minute, timezone="Asia/Kolkata"),
                id="precompute_panchangam",
                name="Precompute Panchangam Data",
                replace_existing=True
            )
            
            self.scheduler.start()
            logger.info(f"Job scheduler started. Precompute job scheduled for {settings.PRECOMPUTE_TIME} IST daily")
            
        except Exception as e:
            logger.error(f"Error starting scheduler: {e}")
    
    def stop_scheduler(self):
        """Stop the job scheduler."""
        if self.scheduler and self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Job scheduler stopped")
    
    async def cleanup(self):
        """Cleanup resources."""
        if self.redis_client:
            await self.redis_client.close()
        
        self.stop_scheduler()


# Global job instance
precompute_job = PrecomputeJob()


async def initialize_jobs():
    """Initialize the job system."""
    try:
        await precompute_job.initialize()
        precompute_job.start_scheduler()
        logger.info("Job system initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing job system: {e}")


async def cleanup_jobs():
    """Cleanup the job system."""
    try:
        await precompute_job.cleanup()
        logger.info("Job system cleaned up successfully")
    except Exception as e:
        logger.error(f"Error cleaning up job system: {e}")
