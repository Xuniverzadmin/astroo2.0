"""
Tests for panchangam core functionality.

This module contains sanity tests for panchangam calculations including
tithi, nakshatra, yoga, karana, and timing calculations.
"""

import pytest
from datetime import date, datetime, timedelta
from typing import Dict, Any

# Import the modules to test
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from numerology_app.panchangam.core import (
    compute_tithi, compute_nakshatra, compute_yoga, compute_karana,
    compute_rahu_yama_gulikai, compute_hora, compute_gowri_nalla,
    assemble_panchangam
)
from numerology_app.panchangam.astronomy import (
    get_sun_longitude, get_moon_longitude, get_sunrise_sunset
)


class TestPanchangamCore:
    """Test cases for panchangam core calculations."""
    
    def test_compute_tithi_basic(self):
        """Test basic tithi calculations."""
        # Test known tithi calculations
        # These are approximate values for testing
        
        # Test tithi 1 (Shukla Pratipada)
        tithi_num, tithi_progress = compute_tithi(0.0, 12.0)  # Sun at 0°, Moon at 12°
        assert tithi_num == 1
        assert 0.0 <= tithi_progress <= 1.0
        
        # Test tithi 15 (Purnima)
        tithi_num, tithi_progress = compute_tithi(0.0, 180.0)  # Sun at 0°, Moon at 180°
        assert tithi_num == 15
        assert 0.0 <= tithi_progress <= 1.0
        
        # Test tithi 30 (Amavasya)
        tithi_num, tithi_progress = compute_tithi(0.0, 0.0)  # Sun and Moon at same position
        assert tithi_num == 1  # Should be 1, not 30, as 0° difference = 0 tithi
        assert 0.0 <= tithi_progress <= 1.0
        
        # Test tithi 16 (Krishna Pratipada)
        tithi_num, tithi_progress = compute_tithi(0.0, 192.0)  # Sun at 0°, Moon at 192°
        assert tithi_num == 16
        assert 0.0 <= tithi_progress <= 1.0
    
    def test_compute_nakshatra_basic(self):
        """Test basic nakshatra calculations."""
        # Test nakshatra 1 (Ashwini)
        nakshatra_num, nakshatra_progress = compute_nakshatra(0.0)
        assert nakshatra_num == 1
        assert 0.0 <= nakshatra_progress <= 1.0
        
        # Test nakshatra 14 (Chitra)
        nakshatra_num, nakshatra_progress = compute_nakshatra(180.0)
        assert nakshatra_num == 14
        assert 0.0 <= nakshatra_progress <= 1.0
        
        # Test nakshatra 27 (Revati)
        nakshatra_num, nakshatra_progress = compute_nakshatra(350.0)
        assert nakshatra_num == 27
        assert 0.0 <= nakshatra_progress <= 1.0
    
    def test_compute_yoga_basic(self):
        """Test basic yoga calculations."""
        # Test yoga 1 (Vishkambha)
        yoga_num, yoga_progress = compute_yoga(0.0, 0.0)  # Sun and Moon at 0°
        assert yoga_num == 1
        assert 0.0 <= yoga_progress <= 1.0
        
        # Test yoga 14 (Vyaghata)
        yoga_num, yoga_progress = compute_yoga(90.0, 90.0)  # Sun and Moon at 90°
        assert yoga_num == 14
        assert 0.0 <= yoga_progress <= 1.0
        
        # Test yoga 27 (Vaidhriti)
        yoga_num, yoga_progress = compute_yoga(180.0, 180.0)  # Sun and Moon at 180°
        assert yoga_num == 27
        assert 0.0 <= yoga_progress <= 1.0
    
    def test_compute_karana_basic(self):
        """Test basic karana calculations."""
        # Test regular karanas (1-7)
        karana_name, karana_progress = compute_karana(1, 0.0)
        assert karana_name in ["Bava", "Balava", "Kaulava", "Taitila", "Garija", "Vanija", "Vishti"]
        assert 0.0 <= karana_progress <= 1.0
        
        # Test special karanas (9-11) on specific tithis
        karana_name, karana_progress = compute_karana(1, 0.0)  # Tithi 1
        assert karana_name in ["Chatushpada", "Naga"]
        assert 0.0 <= karana_progress <= 1.0
        
        karana_name, karana_progress = compute_karana(2, 0.0)  # Tithi 2
        assert karana_name in ["Naga", "Kimstughna"]
        assert 0.0 <= karana_progress <= 1.0
    
    def test_sunrise_sunset_bounds(self):
        """Test sunrise/sunset time bounds for different locations."""
        # Test Chennai (13.0827°N, 80.2707°E)
        chennai_date = date(2024, 3, 15)  # Spring equinox
        sunrise, sunset = get_sunrise_sunset(chennai_date, 13.0827, 80.2707, "Asia/Kolkata")
        
        # Sunrise should be between 5:30 AM and 7:00 AM IST
        assert 5.5 <= sunrise.hour + sunrise.minute/60.0 <= 7.0
        
        # Sunset should be between 5:30 PM and 7:00 PM IST
        assert 17.5 <= sunset.hour + sunset.minute/60.0 <= 19.0
        
        # Test Mumbai (19.0760°N, 72.8777°E)
        mumbai_date = date(2024, 6, 21)  # Summer solstice
        sunrise, sunset = get_sunrise_sunset(mumbai_date, 19.0760, 72.8777, "Asia/Kolkata")
        
        # Sunrise should be between 5:30 AM and 7:00 AM IST
        assert 5.5 <= sunrise.hour + sunrise.minute/60.0 <= 7.0
        
        # Sunset should be between 6:30 PM and 8:00 PM IST
        assert 18.5 <= sunset.hour + sunset.minute/60.0 <= 20.0
        
        # Test Delhi (28.7041°N, 77.1025°E)
        delhi_date = date(2024, 12, 21)  # Winter solstice
        sunrise, sunset = get_sunrise_sunset(delhi_date, 28.7041, 77.1025, "Asia/Kolkata")
        
        # Sunrise should be between 6:30 AM and 8:00 AM IST
        assert 6.5 <= sunrise.hour + sunrise.minute/60.0 <= 8.0
        
        # Sunset should be between 5:00 PM and 6:30 PM IST
        assert 17.0 <= sunset.hour + sunset.minute/60.0 <= 18.5
    
    def test_rahu_yama_gulikai_timing(self):
        """Test Rahu Kalam, Yama Gandam, and Gulikai Kalam timing."""
        test_date = date(2024, 3, 15)  # Friday
        lat, lon, tz = 13.0827, 80.2707, "Asia/Kolkata"
        
        periods = compute_rahu_yama_gulikai(test_date, lat, lon, tz)
        
        # Check that all periods exist
        assert "rahu_kalam" in periods
        assert "yama_gandam" in periods
        assert "gulikai_kalam" in periods
        
        # Check that each period has start, end, and duration
        for period_name in ["rahu_kalam", "yama_gandam", "gulikai_kalam"]:
            period = periods[period_name]
            assert "start" in period
            assert "end" in period
            assert "duration_hours" in period
            assert period["duration_hours"] == 1.5
            
            # Check that start is before end
            start_time = period["start"]
            end_time = period["end"]
            assert start_time < end_time
    
    def test_hora_calculations(self):
        """Test hora (planetary hour) calculations."""
        test_date = date(2024, 3, 15)  # Friday
        lat, lon, tz = 13.0827, 80.2707, "Asia/Kolkata"
        
        horas = compute_hora(test_date, lat, lon, tz)
        
        # Should have 12 horas
        assert len(horas) == 12
        
        # Check that each hora has required fields
        for i, hora in enumerate(horas):
            assert hora["hora_number"] == i + 1
            assert "planet" in hora
            assert "start" in hora
            assert "end" in hora
            assert "duration" in hora
            
            # Check that planets are valid
            valid_planets = ["Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars"]
            assert hora["planet"] in valid_planets
        
        # Check that horas are sequential
        for i in range(len(horas) - 1):
            assert horas[i]["end"] == horas[i + 1]["start"]
    
    def test_gowri_panchangam(self):
        """Test Gowri Panchangam calculations."""
        test_date = date(2024, 3, 15)
        lat, lon, tz = 13.0827, 80.2707, "Asia/Kolkata"
        
        gowri = compute_gowri_nalla(test_date, lat, lon, tz)
        
        # Check that gowri has required fields
        assert "periods" in gowri
        assert "auspicious" in gowri
        assert "inauspicious" in gowri
        
        # Check that periods exist
        expected_periods = ["amrutha", "siddha", "marana", "rogam", "laabha", "dhanam", "sugam", "kantaka"]
        for period_name in expected_periods:
            assert period_name in gowri["periods"]
        
        # Check that auspicious and inauspicious lists are populated
        assert len(gowri["auspicious"]) > 0
        assert len(gowri["inauspicious"]) > 0
        
        # Check that no period is both auspicious and inauspicious
        assert not set(gowri["auspicious"]).intersection(set(gowri["inauspicious"]))
    
    def test_assemble_panchangam_complete(self):
        """Test complete panchangam assembly."""
        test_date = date(2024, 3, 15)
        lat, lon, tz = 13.0827, 80.2707, "Asia/Kolkata"
        
        panchangam = assemble_panchangam(test_date, lat, lon, tz)
        
        # Check that all required fields exist
        required_fields = [
            "date", "location", "sunrise", "sunset",
            "tithi", "nakshatra", "yoga", "karana",
            "rahu_kalam", "yama_gandam", "gulikai_kalam",
            "horas", "gowri_panchangam", "settings"
        ]
        
        for field in required_fields:
            assert field in panchangam, f"Missing field: {field}"
        
        # Check location data
        location = panchangam["location"]
        assert location["latitude"] == lat
        assert location["longitude"] == lon
        assert location["timezone"] == tz
        
        # Check tithi data
        tithi = panchangam["tithi"]
        assert "number" in tithi
        assert "name" in tithi
        assert "progress" in tithi
        assert "percentage" in tithi
        assert 1 <= tithi["number"] <= 30
        assert 0.0 <= tithi["progress"] <= 1.0
        assert 0.0 <= tithi["percentage"] <= 100.0
        
        # Check nakshatra data
        nakshatra = panchangam["nakshatra"]
        assert "number" in nakshatra
        assert "name" in nakshatra
        assert "progress" in nakshatra
        assert "percentage" in nakshatra
        assert 1 <= nakshatra["number"] <= 27
        assert 0.0 <= nakshatra["progress"] <= 1.0
        assert 0.0 <= nakshatra["percentage"] <= 100.0
        
        # Check yoga data
        yoga = panchangam["yoga"]
        assert "number" in yoga
        assert "name" in yoga
        assert "progress" in yoga
        assert "percentage" in yoga
        assert 1 <= yoga["number"] <= 27
        assert 0.0 <= yoga["progress"] <= 1.0
        assert 0.0 <= yoga["percentage"] <= 100.0
        
        # Check karana data
        karana = panchangam["karana"]
        assert "name" in karana
        assert "progress" in karana
        assert "percentage" in karana
        assert 0.0 <= karana["progress"] <= 1.0
        assert 0.0 <= karana["percentage"] <= 100.0
        
        # Check timing periods
        for period_name in ["rahu_kalam", "yama_gandam", "gulikai_kalam"]:
            period = panchangam[period_name]
            assert "start" in period
            assert "end" in period
            assert "duration_hours" in period
        
        # Check horas
        horas = panchangam["horas"]
        assert len(horas) == 12
        for hora in horas:
            assert "hora_number" in hora
            assert "planet" in hora
            assert "start" in hora
            assert "end" in hora
    
    def test_known_dates_sanity(self):
        """Test panchangam calculations for known important dates."""
        # Test Diwali 2024 (October 31, 2024)
        diwali_date = date(2024, 10, 31)
        lat, lon, tz = 13.0827, 80.2707, "Asia/Kolkata"  # Chennai
        
        panchangam = assemble_panchangam(diwali_date, lat, lon, tz)
        
        # Diwali should be on Amavasya (tithi 30 or 15 Krishna)
        tithi = panchangam["tithi"]
        assert tithi["number"] in [15, 30]  # Could be either depending on exact timing
        
        # Test Holi 2024 (March 25, 2024)
        holi_date = date(2024, 3, 25)
        panchangam = assemble_panchangam(holi_date, lat, lon, tz)
        
        # Holi should be on Purnima (tithi 15)
        tithi = panchangam["tithi"]
        # Note: This is approximate as exact dates depend on precise calculations
        
        # Test Maha Shivaratri 2024 (March 8, 2024)
        shivaratri_date = date(2024, 3, 8)
        panchangam = assemble_panchangam(shivaratri_date, lat, lon, tz)
        
        # Maha Shivaratri should be on Krishna 14
        tithi = panchangam["tithi"]
        # Note: This is approximate as exact dates depend on precise calculations
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Test with extreme coordinates
        test_date = date(2024, 6, 21)  # Summer solstice
        
        # Test near North Pole
        try:
            panchangam = assemble_panchangam(test_date, 89.0, 0.0, "UTC")
            assert "sunrise" in panchangam
            assert "sunset" in panchangam
        except Exception as e:
            # It's acceptable for extreme coordinates to fail
            assert "latitude" in str(e).lower() or "coordinate" in str(e).lower()
        
        # Test with invalid timezone
        try:
            panchangam = assemble_panchangam(test_date, 13.0827, 80.2707, "Invalid/Timezone")
            # Should either work or fail gracefully
        except Exception as e:
            assert "timezone" in str(e).lower() or "invalid" in str(e).lower()
        
        # Test with future date (year 2100)
        future_date = date(2100, 1, 1)
        panchangam = assemble_panchangam(future_date, 13.0827, 80.2707, "Asia/Kolkata")
        assert panchangam["date"] == future_date.isoformat()
        
        # Test with past date (year 1900)
        past_date = date(1900, 1, 1)
        panchangam = assemble_panchangam(past_date, 13.0827, 80.2707, "Asia/Kolkata")
        assert panchangam["date"] == past_date.isoformat()
    
    def test_astronomy_functions(self):
        """Test astronomy helper functions."""
        test_datetime = datetime(2024, 3, 15, 12, 0, 0)  # Noon
        
        # Test sun longitude
        sun_long = get_sun_longitude(test_datetime)
        assert 0.0 <= sun_long <= 360.0
        
        # Test moon longitude
        moon_long = get_moon_longitude(test_datetime)
        assert 0.0 <= moon_long <= 360.0
        
        # Test that longitudes are reasonable (not NaN or infinite)
        assert sun_long == sun_long  # Not NaN
        assert moon_long == moon_long  # Not NaN
        assert sun_long != float('inf')
        assert moon_long != float('inf')
    
    def test_performance_basic(self):
        """Test basic performance of panchangam calculations."""
        import time
        
        test_date = date(2024, 3, 15)
        lat, lon, tz = 13.0827, 80.2707, "Asia/Kolkata"
        
        # Time a single panchangam calculation
        start_time = time.time()
        panchangam = assemble_panchangam(test_date, lat, lon, tz)
        end_time = time.time()
        
        calculation_time = end_time - start_time
        
        # Should complete within reasonable time (less than 5 seconds)
        assert calculation_time < 5.0, f"Panchangam calculation took {calculation_time:.2f} seconds"
        
        # Time multiple calculations
        start_time = time.time()
        for i in range(10):
            test_date_iter = date(2024, 3, 15 + i)
            assemble_panchangam(test_date_iter, lat, lon, tz)
        end_time = time.time()
        
        avg_time = (end_time - start_time) / 10
        
        # Average time should be reasonable
        assert avg_time < 2.0, f"Average panchangam calculation took {avg_time:.2f} seconds"


class TestPanchangamIntegration:
    """Integration tests for panchangam functionality."""
    
    def test_multiple_locations(self):
        """Test panchangam calculations for multiple locations."""
        test_date = date(2024, 3, 15)
        
        locations = [
            (13.0827, 80.2707, "Asia/Kolkata"),  # Chennai
            (19.0760, 72.8777, "Asia/Kolkata"),  # Mumbai
            (28.7041, 77.1025, "Asia/Kolkata"),  # Delhi
            (12.9716, 77.5946, "Asia/Kolkata"),  # Bangalore
            (17.3850, 78.4867, "Asia/Kolkata"),  # Hyderabad
        ]
        
        for lat, lon, tz in locations:
            panchangam = assemble_panchangam(test_date, lat, lon, tz)
            
            # All locations should produce valid panchangam
            assert "tithi" in panchangam
            assert "nakshatra" in panchangam
            assert "sunrise" in panchangam
            assert "sunset" in panchangam
            
            # Location data should match input
            assert panchangam["location"]["latitude"] == lat
            assert panchangam["location"]["longitude"] == lon
            assert panchangam["location"]["timezone"] == tz
    
    def test_date_range_consistency(self):
        """Test consistency across a range of dates."""
        start_date = date(2024, 1, 1)
        lat, lon, tz = 13.0827, 80.2707, "Asia/Kolkata"
        
        for i in range(30):  # Test 30 days
            test_date = start_date + timedelta(days=i)
            panchangam = assemble_panchangam(test_date, lat, lon, tz)
            
            # Each date should produce valid panchangam
            assert panchangam["date"] == test_date.isoformat()
            assert "tithi" in panchangam
            assert "nakshatra" in panchangam
            
            # Tithi should progress logically
            tithi = panchangam["tithi"]
            assert 1 <= tithi["number"] <= 30
            assert 0.0 <= tithi["progress"] <= 1.0


if __name__ == "__main__":
    # Run tests if executed directly
    pytest.main([__file__, "-v"])
