"""
Festival rules DSL (Domain Specific Language) for defining festival conditions.

This module provides a simple DSL for defining when festivals occur based on
panchangam elements like tithi, nakshatra, yoga, and timing conditions.
"""

import re
from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum

from ..panchangam.core import assemble_panchangam


class FestivalType(Enum):
    """Types of festivals."""
    RELIGIOUS = "religious"
    NATIONAL = "national"
    REGIONAL = "regional"
    SEASONAL = "seasonal"
    PERSONAL = "personal"


class Importance(Enum):
    """Importance levels for festivals."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


@dataclass
class FestivalRule:
    """
    A festival rule definition using the DSL.
    
    Example:
        FestivalRule(
            name="Maha Shivaratri",
            when="tithi=14 krishna & pradosha_kala",
            observe="sunset",
            region="ALL",
            festival_type=FestivalType.RELIGIOUS,
            importance=Importance.HIGH
        )
    """
    name: str
    when: str  # DSL condition string
    observe: str = "sunrise"  # When to observe: sunrise, sunset, midnight
    region: str = "ALL"  # Region code: ALL, TN, KL, KA, AP, etc.
    festival_type: FestivalType = FestivalType.RELIGIOUS
    importance: Importance = Importance.MEDIUM
    description: Optional[str] = None
    lunar_date: Optional[str] = None  # e.g., "Krishna 14"
    is_public_holiday: bool = False
    is_bank_holiday: bool = False
    is_optional_holiday: bool = False
    rituals: Optional[Dict[str, Any]] = None
    customs: Optional[Dict[str, Any]] = None


class FestivalRuleEvaluator:
    """
    Evaluates festival rules against computed panchangam data.
    
    The DSL supports the following operators and conditions:
    - tithi=N (shukla|krishna) - Tithi number and paksha
    - nakshatra=N - Nakshatra number (1-27)
    - yoga=N - Yoga number (1-27)
    - karana=NAME - Karana name
    - weekday=NAME - Day of week (monday, tuesday, etc.)
    - pradosha_kala - Pradosha time (1.5 hours before sunset)
    - brahma_muhurta - Brahma muhurta (1.5 hours before sunrise)
    - amavasya - New moon day
    - purnima - Full moon day
    - ekadashi - 11th tithi
    - & (AND), | (OR), ! (NOT) - Logical operators
    - () - Grouping
    """
    
    def __init__(self):
        self.operators = {
            '&': self._and_operator,
            '|': self._or_operator,
            '!': self._not_operator
        }
        
        # Special time periods
        self.special_periods = {
            'pradosha_kala': self._is_pradosha_kala,
            'brahma_muhurta': self._is_brahma_muhurta,
            'amavasya': self._is_amavasya,
            'purnima': self._is_purnima,
            'ekadashi': self._is_ekadashi
        }
    
    def _and_operator(self, left: bool, right: bool) -> bool:
        """Logical AND operator."""
        return left and right
    
    def _or_operator(self, left: bool, right: bool) -> bool:
        """Logical OR operator."""
        return left or right
    
    def _not_operator(self, operand: bool) -> bool:
        """Logical NOT operator."""
        return not operand
    
    def evaluate_rule(self, rule: FestivalRule, date_obj: date, lat: float, lon: float, tz: str) -> bool:
        """
        Evaluate a festival rule against a specific date and location.
        
        Args:
            rule: FestivalRule to evaluate
            date_obj: Date to check
            lat: Latitude
            lon: Longitude
            tz: Timezone
            
        Returns:
            True if the rule matches, False otherwise
        """
        try:
            # Get panchangam data for the date
            panchangam = assemble_panchangam(date_obj, lat, lon, tz)
            
            # Parse and evaluate the condition
            return self._evaluate_condition(rule.when, panchangam, date_obj)
            
        except Exception as e:
            print(f"Error evaluating rule {rule.name}: {e}")
            return False
    
    def _evaluate_condition(self, condition: str, panchangam: Dict[str, Any], date_obj: date) -> bool:
        """Evaluate a DSL condition string."""
        # Clean the condition string
        condition = condition.strip().lower()
        
        # Handle parentheses and logical operators
        return self._parse_logical_expression(condition, panchangam, date_obj)
    
    def _parse_logical_expression(self, expr: str, panchangam: Dict[str, Any], date_obj: date) -> bool:
        """Parse logical expressions with parentheses."""
        # Simple implementation - can be enhanced with proper parser
        expr = expr.strip()
        
        # Handle NOT operator
        if expr.startswith('!'):
            return not self._parse_logical_expression(expr[1:].strip(), panchangam, date_obj)
        
        # Handle parentheses
        if expr.startswith('(') and expr.endswith(')'):
            return self._parse_logical_expression(expr[1:-1].strip(), panchangam, date_obj)
        
        # Handle AND operator
        if ' & ' in expr:
            parts = expr.split(' & ')
            return all(self._parse_logical_expression(part.strip(), panchangam, date_obj) for part in parts)
        
        # Handle OR operator
        if ' | ' in expr:
            parts = expr.split(' | ')
            return any(self._parse_logical_expression(part.strip(), panchangam, date_obj) for part in parts)
        
        # Handle atomic conditions
        return self._evaluate_atomic_condition(expr, panchangam, date_obj)
    
    def _evaluate_atomic_condition(self, condition: str, panchangam: Dict[str, Any], date_obj: date) -> bool:
        """Evaluate atomic conditions like 'tithi=14 krishna'."""
        condition = condition.strip()
        
        # Check for special periods first
        if condition in self.special_periods:
            return self.special_periods[condition](panchangam, date_obj)
        
        # Parse equality conditions
        if '=' in condition:
            left, right = condition.split('=', 1)
            left = left.strip()
            right = right.strip()
            
            if left == 'tithi':
                return self._check_tithi_condition(right, panchangam)
            elif left == 'nakshatra':
                return self._check_nakshatra_condition(right, panchangam)
            elif left == 'yoga':
                return self._check_yoga_condition(right, panchangam)
            elif left == 'karana':
                return self._check_karana_condition(right, panchangam)
            elif left == 'weekday':
                return self._check_weekday_condition(right, date_obj)
        
        return False
    
    def _check_tithi_condition(self, condition: str, panchangam: Dict[str, Any]) -> bool:
        """Check tithi conditions like '14 krishna' or '1 shukla'."""
        tithi_data = panchangam.get('tithi', {})
        tithi_number = tithi_data.get('number', 0)
        tithi_name = tithi_data.get('name', '')
        
        # Parse condition like "14 krishna" or "1 shukla"
        parts = condition.split()
        if len(parts) == 2:
            number_str, paksha = parts
            try:
                target_number = int(number_str)
                target_paksha = paksha.lower()
                
                # Check if tithi matches
                if target_paksha == 'shukla':
                    return tithi_number == target_number and 'shukla' in tithi_name.lower()
                elif target_paksha == 'krishna':
                    return tithi_number == (target_number + 15) and 'krishna' in tithi_name.lower()
                else:
                    return tithi_number == target_number
                    
            except ValueError:
                return False
        
        # Simple number check
        try:
            target_number = int(condition)
            return tithi_number == target_number
        except ValueError:
            return False
    
    def _check_nakshatra_condition(self, condition: str, panchangam: Dict[str, Any]) -> bool:
        """Check nakshatra conditions."""
        nakshatra_data = panchangam.get('nakshatra', {})
        nakshatra_number = nakshatra_data.get('number', 0)
        
        try:
            target_number = int(condition)
            return nakshatra_number == target_number
        except ValueError:
            return False
    
    def _check_yoga_condition(self, condition: str, panchangam: Dict[str, Any]) -> bool:
        """Check yoga conditions."""
        yoga_data = panchangam.get('yoga', {})
        yoga_number = yoga_data.get('number', 0)
        
        try:
            target_number = int(condition)
            return yoga_number == target_number
        except ValueError:
            return False
    
    def _check_karana_condition(self, condition: str, panchangam: Dict[str, Any]) -> bool:
        """Check karana conditions."""
        karana_data = panchangam.get('karana', {})
        karana_name = karana_data.get('name', '').lower()
        
        return karana_name == condition.lower()
    
    def _check_weekday_condition(self, condition: str, date_obj: date) -> bool:
        """Check weekday conditions."""
        weekdays = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
            'friday': 4, 'saturday': 5, 'sunday': 6
        }
        
        target_weekday = weekdays.get(condition.lower(), -1)
        if target_weekday == -1:
            return False
        
        return date_obj.weekday() == target_weekday
    
    def _is_pradosha_kala(self, panchangam: Dict[str, Any], date_obj: date) -> bool:
        """Check if it's Pradosha kala (1.5 hours before sunset)."""
        # This is a simplified check - in reality, Pradosha kala is more complex
        # and depends on the specific tithi and timing
        tithi_data = panchangam.get('tithi', {})
        tithi_number = tithi_data.get('number', 0)
        
        # Pradosha kala typically occurs on 13th tithi
        return tithi_number == 13
    
    def _is_brahma_muhurta(self, panchangam: Dict[str, Any], date_obj: date) -> bool:
        """Check if it's Brahma muhurta (1.5 hours before sunrise)."""
        # Brahma muhurta is typically the last 1.5 hours before sunrise
        # This is a simplified implementation
        return True  # Placeholder - would need more complex timing logic
    
    def _is_amavasya(self, panchangam: Dict[str, Any], date_obj: date) -> bool:
        """Check if it's Amavasya (new moon day)."""
        tithi_data = panchangam.get('tithi', {})
        tithi_number = tithi_data.get('number', 0)
        
        # Amavasya is the 15th tithi of Krishna paksha
        return tithi_number == 30  # 15th Krishna = 30th tithi
    
    def _is_purnima(self, panchangam: Dict[str, Any], date_obj: date) -> bool:
        """Check if it's Purnima (full moon day)."""
        tithi_data = panchangam.get('tithi', {})
        tithi_number = tithi_data.get('number', 0)
        
        # Purnima is the 15th tithi of Shukla paksha
        return tithi_number == 15
    
    def _is_ekadashi(self, panchangam: Dict[str, Any], date_obj: date) -> bool:
        """Check if it's Ekadashi (11th tithi)."""
        tithi_data = panchangam.get('tithi', {})
        tithi_number = tithi_data.get('number', 0)
        
        # Ekadashi is the 11th tithi of either paksha
        return tithi_number == 11 or tithi_number == 26  # 11th Shukla or 11th Krishna


# Predefined festival rules
FESTIVAL_RULES = [
    # Major festivals
    FestivalRule(
        name="Maha Shivaratri",
        when="tithi=14 krishna",
        observe="sunset",
        region="ALL",
        festival_type=FestivalType.RELIGIOUS,
        importance=Importance.HIGH,
        description="Great night of Lord Shiva",
        lunar_date="Krishna 14",
        is_public_holiday=True
    ),
    
    FestivalRule(
        name="Holi",
        when="tithi=15 krishna & nakshatra=1",
        observe="sunset",
        region="ALL",
        festival_type=FestivalType.RELIGIOUS,
        importance=Importance.HIGH,
        description="Festival of colors",
        lunar_date="Krishna 15",
        is_public_holiday=True
    ),
    
    FestivalRule(
        name="Diwali",
        when="tithi=15 krishna & nakshatra=1",
        observe="sunset",
        region="ALL",
        festival_type=FestivalType.RELIGIOUS,
        importance=Importance.VERY_HIGH,
        description="Festival of lights",
        lunar_date="Krishna 15",
        is_public_holiday=True,
        is_bank_holiday=True
    ),
    
    FestivalRule(
        name="Dussehra",
        when="tithi=10 shukla",
        observe="sunset",
        region="ALL",
        festival_type=FestivalType.RELIGIOUS,
        importance=Importance.HIGH,
        description="Victory of good over evil",
        lunar_date="Shukla 10",
        is_public_holiday=True
    ),
    
    FestivalRule(
        name="Ganesh Chaturthi",
        when="tithi=4 shukla",
        observe="sunset",
        region="ALL",
        festival_type=FestivalType.RELIGIOUS,
        importance=Importance.HIGH,
        description="Birth of Lord Ganesha",
        lunar_date="Shukla 4",
        is_public_holiday=True
    ),
    
    FestivalRule(
        name="Krishna Janmashtami",
        when="tithi=8 krishna",
        observe="midnight",
        region="ALL",
        festival_type=FestivalType.RELIGIOUS,
        importance=Importance.HIGH,
        description="Birth of Lord Krishna",
        lunar_date="Krishna 8",
        is_public_holiday=True
    ),
    
    FestivalRule(
        name="Rama Navami",
        when="tithi=9 shukla",
        observe="sunset",
        region="ALL",
        festival_type=FestivalType.RELIGIOUS,
        importance=Importance.MEDIUM,
        description="Birth of Lord Rama",
        lunar_date="Shukla 9"
    ),
    
    FestivalRule(
        name="Hanuman Jayanti",
        when="tithi=15 shukla",
        observe="sunset",
        region="ALL",
        festival_type=FestivalType.RELIGIOUS,
        importance=Importance.MEDIUM,
        description="Birth of Lord Hanuman",
        lunar_date="Shukla 15"
    ),
    
    # Regional festivals
    FestivalRule(
        name="Pongal",
        when="tithi=1 shukla & nakshatra=1",
        observe="sunrise",
        region="TN",
        festival_type=FestivalType.REGIONAL,
        importance=Importance.HIGH,
        description="Tamil harvest festival",
        lunar_date="Shukla 1",
        is_public_holiday=True
    ),
    
    FestivalRule(
        name="Onam",
        when="tithi=10 shukla & nakshatra=1",
        observe="sunset",
        region="KL",
        festival_type=FestivalType.REGIONAL,
        importance=Importance.HIGH,
        description="Kerala harvest festival",
        lunar_date="Shukla 10",
        is_public_holiday=True
    ),
    
    FestivalRule(
        name="Karva Chauth",
        when="tithi=4 krishna",
        observe="sunset",
        region="ALL",
        festival_type=FestivalType.RELIGIOUS,
        importance=Importance.MEDIUM,
        description="Fast for husband's longevity",
        lunar_date="Krishna 4"
    ),
    
    FestivalRule(
        name="Navratri",
        when="tithi=1 shukla",
        observe="sunrise",
        region="ALL",
        festival_type=FestivalType.RELIGIOUS,
        importance=Importance.HIGH,
        description="Nine nights of Goddess Durga",
        lunar_date="Shukla 1",
        is_public_holiday=True
    ),
    
    # Ekadashi festivals
    FestivalRule(
        name="Ekadashi",
        when="ekadashi",
        observe="sunrise",
        region="ALL",
        festival_type=FestivalType.RELIGIOUS,
        importance=Importance.MEDIUM,
        description="Fasting day for Lord Vishnu",
        lunar_date="Ekadashi"
    ),
    
    # Amavasya and Purnima
    FestivalRule(
        name="Amavasya",
        when="amavasya",
        observe="sunset",
        region="ALL",
        festival_type=FestivalType.RELIGIOUS,
        importance=Importance.MEDIUM,
        description="New moon day",
        lunar_date="Amavasya"
    ),
    
    FestivalRule(
        name="Purnima",
        when="purnima",
        observe="sunset",
        region="ALL",
        festival_type=FestivalType.RELIGIOUS,
        importance=Importance.MEDIUM,
        description="Full moon day",
        lunar_date="Purnima"
    )
]


def get_festivals_for_region(region: str) -> List[FestivalRule]:
    """Get all festival rules for a specific region."""
    return [rule for rule in FESTIVAL_RULES if rule.region == "ALL" or rule.region == region]


def get_festivals_by_type(festival_type: FestivalType) -> List[FestivalRule]:
    """Get all festival rules of a specific type."""
    return [rule for rule in FESTIVAL_RULES if rule.festival_type == festival_type]


def get_festivals_by_importance(importance: Importance) -> List[FestivalRule]:
    """Get all festival rules of a specific importance level."""
    return [rule for rule in FESTIVAL_RULES if rule.importance == importance]
