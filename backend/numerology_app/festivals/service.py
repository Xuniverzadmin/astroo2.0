"""
Festival service for building festival calendars and muhurtham periods.

This module provides services to build monthly festival calendars and
calculate auspicious times (muhurtham) based on panchangam data.
"""

import logging
from datetime import date, datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from calendar import monthrange

from ..models import FestivalDay, PanchangDay, MuhurthamPeriod
from ..db import SessionLocal
from .rules import FestivalRule, FestivalRuleEvaluator, get_festivals_for_region, FestivalType, Importance

logger = logging.getLogger(__name__)


class FestivalService:
    """Service for building festival calendars and muhurtham calculations."""
    
    def __init__(self):
        self.rule_evaluator = FestivalRuleEvaluator()
    
    def build_month(self, year: int, month: int, lat: float, lon: float, tz: str, region: str = "ALL") -> List[Dict[str, Any]]:
        """
        Build a festival calendar for a specific month.
        
        Args:
            year: Year (e.g., 2024)
            month: Month (1-12)
            lat: Latitude
            lon: Longitude
            tz: Timezone
            region: Region code (ALL, TN, KL, KA, AP, etc.)
            
        Returns:
            List of festival day dictionaries
        """
        try:
            logger.info(f"Building festival calendar for {year}-{month:02d} in region {region}")
            
            # Get festival rules for the region
            festival_rules = get_festivals_for_region(region)
            
            # Get all days in the month
            days_in_month = monthrange(year, month)[1]
            festival_days = []
            
            # Check each day for festivals
            for day in range(1, days_in_month + 1):
                date_obj = date(year, month, day)
                
                # Check for festivals on this day
                day_festivals = self._check_festivals_for_date(
                    date_obj, lat, lon, tz, festival_rules
                )
                
                if day_festivals:
                    festival_days.extend(day_festivals)
            
            logger.info(f"Found {len(festival_days)} festivals for {year}-{month:02d}")
            return festival_days
            
        except Exception as e:
            logger.error(f"Error building festival calendar: {e}")
            return []
    
    def _check_festivals_for_date(self, date_obj: date, lat: float, lon: float, tz: str, 
                                 festival_rules: List[FestivalRule]) -> List[Dict[str, Any]]:
        """Check which festivals occur on a specific date."""
        festivals = []
        
        for rule in festival_rules:
            try:
                # Evaluate the festival rule
                if self.rule_evaluator.evaluate_rule(rule, date_obj, lat, lon, tz):
                    # Create festival day data
                    festival_data = self._create_festival_data(rule, date_obj, lat, lon, tz)
                    if festival_data:
                        festivals.append(festival_data)
                        
            except Exception as e:
                logger.warning(f"Error evaluating rule {rule.name} for {date_obj}: {e}")
                continue
        
        return festivals
    
    def _create_festival_data(self, rule: FestivalRule, date_obj: date, lat: float, lon: float, tz: str) -> Optional[Dict[str, Any]]:
        """Create festival data dictionary from a rule."""
        try:
            # Get panchangam data for the date
            from ..panchangam.core import assemble_panchangam
            panchangam = assemble_panchangam(date_obj, lat, lon, tz)
            
            # Create festival data
            festival_data = {
                "date": date_obj.isoformat(),
                "lunar_date": rule.lunar_date or self._get_lunar_date(panchangam),
                "name": rule.name,
                "name_local": None,  # Could be added to rules
                "description": rule.description or f"Festival: {rule.name}",
                "festival_type": rule.festival_type.value,
                "importance": rule.importance.value,
                "regions": [rule.region] if rule.region != "ALL" else ["ALL"],
                "states": self._get_states_for_region(rule.region),
                "is_public_holiday": rule.is_public_holiday,
                "is_bank_holiday": rule.is_bank_holiday,
                "is_optional_holiday": rule.is_optional_holiday,
                "rituals": rule.rituals or self._get_default_rituals(rule),
                "customs": rule.customs or self._get_default_customs(rule),
                "auspicious_times": self._get_auspicious_times(rule, panchangam),
                "puja_times": self._get_puja_times(rule, panchangam),
                "panchangam": {
                    "tithi": panchangam.get("tithi", {}),
                    "nakshatra": panchangam.get("nakshatra", {}),
                    "yoga": panchangam.get("yoga", {}),
                    "karana": panchangam.get("karana", {})
                }
            }
            
            return festival_data
            
        except Exception as e:
            logger.error(f"Error creating festival data for {rule.name}: {e}")
            return None
    
    def _get_lunar_date(self, panchangam: Dict[str, Any]) -> str:
        """Get lunar date string from panchangam data."""
        tithi_data = panchangam.get("tithi", {})
        tithi_name = tithi_data.get("name", "")
        return tithi_name
    
    def _get_states_for_region(self, region: str) -> List[str]:
        """Get state names for a region code."""
        region_mapping = {
            "ALL": ["All States"],
            "TN": ["Tamil Nadu"],
            "KL": ["Kerala"],
            "KA": ["Karnataka"],
            "AP": ["Andhra Pradesh", "Telangana"],
            "TS": ["Telangana"],
            "MH": ["Maharashtra"],
            "GJ": ["Gujarat"],
            "RJ": ["Rajasthan"],
            "UP": ["Uttar Pradesh"],
            "MP": ["Madhya Pradesh"],
            "WB": ["West Bengal"],
            "OR": ["Odisha"],
            "AS": ["Assam"],
            "PB": ["Punjab"],
            "HR": ["Haryana"],
            "DL": ["Delhi"],
            "JK": ["Jammu and Kashmir"],
            "HP": ["Himachal Pradesh"],
            "UK": ["Uttarakhand"],
            "BR": ["Bihar"],
            "JH": ["Jharkhand"],
            "CT": ["Chhattisgarh"],
            "GA": ["Goa"],
            "MN": ["Manipur"],
            "MZ": ["Mizoram"],
            "NL": ["Nagaland"],
            "TR": ["Tripura"],
            "SK": ["Sikkim"],
            "AR": ["Arunachal Pradesh"],
            "ML": ["Meghalaya"]
        }
        return region_mapping.get(region, [region])
    
    def _get_default_rituals(self, rule: FestivalRule) -> Dict[str, Any]:
        """Get default rituals for a festival."""
        default_rituals = {
            "Maha Shivaratri": {
                "fasting": "Fasting throughout the day",
                "puja": "Shiva puja with bilva leaves",
                "japa": "Om Namah Shivaya mantra",
                "timing": "Night puja is most important"
            },
            "Diwali": {
                "cleaning": "Clean and decorate the house",
                "puja": "Lakshmi puja in the evening",
                "lights": "Light diyas and candles",
                "sweets": "Prepare and share sweets"
            },
            "Holi": {
                "bonfire": "Holika dahan the night before",
                "colors": "Play with colors the next day",
                "sweets": "Prepare gujiya and other sweets",
                "music": "Sing and dance"
            },
            "Dussehra": {
                "ramlila": "Watch or perform Ramlila",
                "burning": "Burn effigy of Ravana",
                "puja": "Worship weapons and tools",
                "timing": "Evening is most auspicious"
            }
        }
        return default_rituals.get(rule.name, {"general": "Follow traditional customs"})
    
    def _get_default_customs(self, rule: FestivalRule) -> Dict[str, Any]:
        """Get default customs for a festival."""
        default_customs = {
            "Maha Shivaratri": {
                "clothing": "Wear white or light colors",
                "food": "Simple vegetarian food",
                "behavior": "Stay awake and meditate"
            },
            "Diwali": {
                "clothing": "Wear new clothes",
                "food": "Prepare festive meals",
                "gifts": "Exchange gifts with family"
            },
            "Holi": {
                "clothing": "Wear old clothes",
                "food": "Prepare special sweets",
                "social": "Visit friends and family"
            }
        }
        return default_customs.get(rule.name, {"general": "Follow regional traditions"})
    
    def _get_auspicious_times(self, rule: FestivalRule, panchangam: Dict[str, Any]) -> Dict[str, Any]:
        """Get auspicious times for a festival."""
        # This would typically involve complex muhurtham calculations
        # For now, return basic timing based on the rule's observe setting
        
        observe_times = {
            "sunrise": "Early morning (6:00 AM - 8:00 AM)",
            "sunset": "Evening (6:00 PM - 8:00 PM)",
            "midnight": "Late night (11:00 PM - 1:00 AM)"
        }
        
        return {
            "best_time": observe_times.get(rule.observe, "Morning"),
            "avoid_times": "Avoid Rahu Kalam, Yama Gandam, Gulikai Kalam",
            "duration": "2-3 hours for main rituals"
        }
    
    def _get_puja_times(self, rule: FestivalRule, panchangam: Dict[str, Any]) -> Dict[str, Any]:
        """Get puja times for a festival."""
        # Get Gowri panchangam for auspicious times
        gowri_data = panchangam.get("gowri_panchangam", {})
        auspicious_periods = gowri_data.get("auspicious", [])
        
        return {
            "auspicious_periods": auspicious_periods,
            "main_puja": rule.observe,
            "duration": "1-2 hours"
        }
    
    def build_muhurtham_periods(self, date_obj: date, lat: float, lon: float, tz: str, 
                               event_type: str = "general") -> List[Dict[str, Any]]:
        """
        Build muhurtham (auspicious time) periods for a specific date and event.
        
        Args:
            date_obj: Date for muhurtham calculation
            lat: Latitude
            lon: Longitude
            tz: Timezone
            event_type: Type of event (marriage, house_warming, business_opening, etc.)
            
        Returns:
            List of muhurtham period dictionaries
        """
        try:
            logger.info(f"Building muhurtham periods for {date_obj} - {event_type}")
            
            # Get panchangam data
            from ..panchangam.core import assemble_panchangam
            panchangam = assemble_panchangam(date_obj, lat, lon, tz)
            
            # Calculate auspicious periods based on event type
            muhurtham_periods = self._calculate_muhurtham_periods(
                event_type, panchangam, date_obj
            )
            
            logger.info(f"Found {len(muhurtham_periods)} muhurtham periods")
            return muhurtham_periods
            
        except Exception as e:
            logger.error(f"Error building muhurtham periods: {e}")
            return []
    
    def _calculate_muhurtham_periods(self, event_type: str, panchangam: Dict[str, Any], 
                                   date_obj: date) -> List[Dict[str, Any]]:
        """Calculate muhurtham periods based on event type and panchangam."""
        periods = []
        
        # Get Gowri panchangam periods
        gowri_data = panchangam.get("gowri_panchangam", {})
        gowri_periods = gowri_data.get("periods", {})
        auspicious_periods = gowri_data.get("auspicious", [])
        
        # Event-specific muhurtham rules
        event_rules = self._get_event_muhurtham_rules(event_type)
        
        for period_name, period_data in gowri_periods.items():
            if period_name in auspicious_periods:
                # Check if this period is suitable for the event type
                if self._is_period_suitable_for_event(period_name, event_type, event_rules):
                    muhurtham_period = {
                        "name": period_name,
                        "start": period_data.get("start"),
                        "end": period_data.get("end"),
                        "duration_hours": period_data.get("duration_hours", 1.5),
                        "suitability": self._get_period_suitability(period_name, event_type),
                        "recommended_activities": self._get_recommended_activities(period_name, event_type),
                        "avoid_activities": self._get_avoid_activities(period_name, event_type)
                    }
                    periods.append(muhurtham_period)
        
        return periods
    
    def _get_event_muhurtham_rules(self, event_type: str) -> Dict[str, Any]:
        """Get muhurtham rules for specific event types."""
        rules = {
            "marriage": {
                "preferred_periods": ["amrutha", "siddha", "laabha", "dhanam"],
                "avoid_periods": ["marana", "rogam", "kantaka"],
                "timing": "Morning or evening",
                "duration": "2-4 hours"
            },
            "house_warming": {
                "preferred_periods": ["amrutha", "siddha", "laabha"],
                "avoid_periods": ["marana", "rogam"],
                "timing": "Morning",
                "duration": "1-2 hours"
            },
            "business_opening": {
                "preferred_periods": ["amrutha", "siddha", "laabha", "dhanam"],
                "avoid_periods": ["marana", "rogam"],
                "timing": "Morning",
                "duration": "1-2 hours"
            },
            "vehicle_purchase": {
                "preferred_periods": ["amrutha", "siddha", "laabha"],
                "avoid_periods": ["marana", "rogam", "kantaka"],
                "timing": "Morning",
                "duration": "1 hour"
            },
            "general": {
                "preferred_periods": ["amrutha", "siddha", "laabha", "dhanam", "sugam"],
                "avoid_periods": ["marana", "rogam", "kantaka"],
                "timing": "Any auspicious time",
                "duration": "1-2 hours"
            }
        }
        return rules.get(event_type, rules["general"])
    
    def _is_period_suitable_for_event(self, period_name: str, event_type: str, event_rules: Dict[str, Any]) -> bool:
        """Check if a period is suitable for a specific event type."""
        preferred_periods = event_rules.get("preferred_periods", [])
        avoid_periods = event_rules.get("avoid_periods", [])
        
        if period_name in avoid_periods:
            return False
        
        return period_name in preferred_periods
    
    def _get_period_suitability(self, period_name: str, event_type: str) -> str:
        """Get suitability level for a period."""
        suitability_mapping = {
            "amrutha": "Excellent",
            "siddha": "Very Good",
            "laabha": "Good",
            "dhanam": "Good",
            "sugam": "Moderate",
            "marana": "Avoid",
            "rogam": "Avoid",
            "kantaka": "Avoid"
        }
        return suitability_mapping.get(period_name, "Moderate")
    
    def _get_recommended_activities(self, period_name: str, event_type: str) -> List[str]:
        """Get recommended activities for a period and event type."""
        activities = {
            "amrutha": ["All auspicious activities", "Starting new ventures", "Important decisions"],
            "siddha": ["Spiritual practices", "Learning", "Creative work"],
            "laabha": ["Financial activities", "Business transactions", "Investments"],
            "dhanam": ["Charity", "Donations", "Helping others"],
            "sugam": ["Travel", "Communication", "Social activities"]
        }
        return activities.get(period_name, ["General activities"])
    
    def _get_avoid_activities(self, period_name: str, event_type: str) -> List[str]:
        """Get activities to avoid during a period."""
        avoid_activities = {
            "marana": ["All important activities", "Starting new projects", "Major decisions"],
            "rogam": ["Health-related activities", "Medical procedures", "Stressful work"],
            "kantaka": ["Sharp objects", "Cutting activities", "Conflicts"]
        }
        return avoid_activities.get(period_name, ["None"])
    
    def save_festivals_to_db(self, festivals: List[Dict[str, Any]]) -> bool:
        """Save festival data to database."""
        try:
            db = SessionLocal()
            try:
                for festival_data in festivals:
                    # Check if festival already exists
                    existing = db.query(FestivalDay).filter(
                        FestivalDay.date == date.fromisoformat(festival_data["date"]),
                        FestivalDay.name == festival_data["name"]
                    ).first()
                    
                    if not existing:
                        festival_day = FestivalDay(**festival_data)
                        db.add(festival_day)
                
                db.commit()
                logger.info(f"Saved {len(festivals)} festivals to database")
                return True
                
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Error saving festivals to database: {e}")
            return False
    
    def get_festivals_from_db(self, year: int, month: int, region: str = "ALL") -> List[Dict[str, Any]]:
        """Get festivals from database for a specific month."""
        try:
            db = SessionLocal()
            try:
                # Get start and end dates for the month
                start_date = date(year, month, 1)
                if month == 12:
                    end_date = date(year + 1, 1, 1) - timedelta(days=1)
                else:
                    end_date = date(year, month + 1, 1) - timedelta(days=1)
                
                # Query festivals
                festivals = db.query(FestivalDay).filter(
                    FestivalDay.date >= start_date,
                    FestivalDay.date <= end_date
                ).all()
                
                # Convert to dictionaries
                festival_data = []
                for festival in festivals:
                    festival_dict = {
                        "id": festival.id,
                        "date": festival.date.isoformat(),
                        "name": festival.name,
                        "description": festival.description,
                        "festival_type": festival.festival_type,
                        "importance": festival.importance,
                        "is_public_holiday": festival.is_public_holiday,
                        "is_bank_holiday": festival.is_bank_holiday,
                        "is_optional_holiday": festival.is_optional_holiday,
                        "rituals": festival.rituals,
                        "customs": festival.customs,
                        "auspicious_times": festival.auspicious_times,
                        "puja_times": festival.puja_times
                    }
                    festival_data.append(festival_dict)
                
                return festival_data
                
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Error getting festivals from database: {e}")
            return []


# Global service instance
festival_service = FestivalService()
