# backend/numerology_app/models.py
from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, Text, func, Date, Float, Boolean, JSON, ForeignKey, Index
from datetime import date, datetime
from typing import Optional, Dict, Any
from .db import Base

class User(Base):
    """Basic user model for authentication and profile management."""
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text, default=None)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Profile(Base):
    """User profile for birth chart calculations."""
    __tablename__ = "profiles"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    birth_time: Mapped[str] = mapped_column(String(10), nullable=False)  # HH:MM format
    birth_place: Mapped[str] = mapped_column(String(200), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    timezone: Mapped[str] = mapped_column(String(50), default="Asia/Kolkata")
    gender: Mapped[str | None] = mapped_column(String(10), default=None)
    notes: Mapped[str | None] = mapped_column(Text, default=None)
    user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), default=None)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    birth_charts: Mapped[list["BirthChart"]] = relationship("BirthChart", back_populates="profile")
    dasha_timelines: Mapped[list["DashaTimeline"]] = relationship("DashaTimeline", back_populates="profile")
    readings: Mapped[list["Reading"]] = relationship("Reading", back_populates="profile")


class BirthChart(Base):
    """Stored birth chart calculations."""
    __tablename__ = "birth_charts"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    profile_id: Mapped[int] = mapped_column(Integer, ForeignKey("profiles.id"), nullable=False)
    chart_data: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    ascendant: Mapped[str] = mapped_column(String(20), nullable=False)
    moon_sign: Mapped[str] = mapped_column(String(20), nullable=False)
    sun_sign: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    profile: Mapped["Profile"] = relationship("Profile", back_populates="birth_charts")


class DashaTimeline(Base):
    """Stored dasha timeline calculations."""
    __tablename__ = "dasha_timelines"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    profile_id: Mapped[int] = mapped_column(Integer, ForeignKey("profiles.id"), nullable=False)
    timeline_data: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    current_dasha: Mapped[str] = mapped_column(String(20), nullable=False)
    current_antardasha: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    profile: Mapped["Profile"] = relationship("Profile", back_populates="dasha_timelines")


class Reading(Base):
    """AI-generated readings and interpretations."""
    __tablename__ = "readings"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    profile_id: Mapped[int] = mapped_column(Integer, ForeignKey("profiles.id"), nullable=False)
    reading_type: Mapped[str] = mapped_column(String(50), nullable=False)  # general, career, love, etc.
    language: Mapped[str] = mapped_column(String(10), default="en")
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    detailed_analysis: Mapped[str] = mapped_column(Text, nullable=False)
    strengths: Mapped[list[str]] = mapped_column(JSON, default=list)
    challenges: Mapped[list[str]] = mapped_column(JSON, default=list)
    recommendations: Mapped[list[str]] = mapped_column(JSON, default=list)
    predictions: Mapped[list[str]] = mapped_column(JSON, default=list)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    profile: Mapped["Profile"] = relationship("Profile", back_populates="readings")


class Event(Base):
    """Astrological events and reminders."""
    __tablename__ = "events"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, default=None)
    event_date: Mapped[date] = mapped_column(Date, nullable=False)
    event_time: Mapped[str | None] = mapped_column(String(10), default=None)  # HH:MM format
    event_type: Mapped[str] = mapped_column(String(20), nullable=False)  # auspicious, inauspicious, neutral
    significance: Mapped[str] = mapped_column(Text, nullable=False)
    recommendations: Mapped[list[str]] = mapped_column(JSON, default=list)
    related_planets: Mapped[list[str]] = mapped_column(JSON, default=list)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Reminder(Base):
    """User reminders for astrological events."""
    __tablename__ = "reminders"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), default=None)
    event_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("events.id"), default=None)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    reminder_time: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    notification_type: Mapped[str] = mapped_column(String(20), default="email")  # email, sms, push
    is_sent: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class UserPreferences(Base):
    """User personalization settings."""
    __tablename__ = "user_preferences"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    language: Mapped[str] = mapped_column(String(10), default="en")
    timezone: Mapped[str] = mapped_column(String(50), default="Asia/Kolkata")
    calculation_method: Mapped[str] = mapped_column(String(20), default="Lahiri")
    chart_style: Mapped[str] = mapped_column(String(20), default="North Indian")
    show_degrees: Mapped[bool] = mapped_column(Boolean, default=True)
    show_nakshatras: Mapped[bool] = mapped_column(Boolean, default=True)
    show_divisions: Mapped[bool] = mapped_column(Boolean, default=False)
    notification_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    email_notifications: Mapped[bool] = mapped_column(Boolean, default=True)
    sms_notifications: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class PanchangDay(Base):
    """
    Model for storing daily panchangam data.
    
    This table stores pre-calculated panchangam information for each day
    to improve performance and enable caching of complex calculations.
    """
    __tablename__ = "panchang_days"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Date and location
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    timezone: Mapped[str] = mapped_column(String(50), nullable=False, default="Asia/Kolkata")
    
    # Sunrise and sunset times
    sunrise: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    sunset: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    
    # Panchangam elements
    tithi_number: Mapped[int] = mapped_column(Integer, nullable=False)
    tithi_name: Mapped[str] = mapped_column(String(50), nullable=False)
    tithi_progress: Mapped[float] = mapped_column(Float, nullable=False)
    
    nakshatra_number: Mapped[int] = mapped_column(Integer, nullable=False)
    nakshatra_name: Mapped[str] = mapped_column(String(50), nullable=False)
    nakshatra_progress: Mapped[float] = mapped_column(Float, nullable=False)
    
    yoga_number: Mapped[int] = mapped_column(Integer, nullable=False)
    yoga_name: Mapped[str] = mapped_column(String(50), nullable=False)
    yoga_progress: Mapped[float] = mapped_column(Float, nullable=False)
    
    karana_name: Mapped[str] = mapped_column(String(50), nullable=False)
    karana_progress: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Timing periods (stored as JSON for flexibility)
    rahu_kalam: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    yama_gandam: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    gulikai_kalam: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    
    # Horas (12 planetary hours)
    horas: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    
    # Gowri Panchangam
    gowri_panchangam: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    
    # Metadata
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Indexes for efficient querying
    __table_args__ = (
        Index('idx_panchang_date_location', 'date', 'latitude', 'longitude', 'timezone'),
        Index('idx_panchang_tithi', 'tithi_number', 'date'),
        Index('idx_panchang_nakshatra', 'nakshatra_number', 'date'),
        Index('idx_panchang_yoga', 'yoga_number', 'date'),
    )


class FestivalDay(Base):
    """
    Model for storing festival and important dates.
    
    This table stores information about festivals, religious observances,
    and other important dates in the Hindu calendar.
    """
    __tablename__ = "festival_days"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Date information
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    lunar_date: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # e.g., "Shukla 15"
    
    # Festival details
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    name_local: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)  # Local language name
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Festival type and importance
    festival_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # e.g., "religious", "national", "regional"
    importance: Mapped[str] = mapped_column(String(20), nullable=False, default="medium")  # low, medium, high
    
    # Regional information
    regions: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)  # List of regions where this festival is observed
    states: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)  # List of states
    
    # Observance details
    is_public_holiday: Mapped[bool] = mapped_column(Boolean, default=False)
    is_bank_holiday: Mapped[bool] = mapped_column(Boolean, default=False)
    is_optional_holiday: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Rituals and customs
    rituals: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    customs: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    
    # Timing information
    auspicious_times: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    puja_times: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    
    # Related panchangam data
    panchang_day_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("panchang_days.id"), nullable=True)
    panchang_day: Mapped[Optional[PanchangDay]] = relationship("PanchangDay", backref="festivals")
    
    # Metadata
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Indexes for efficient querying
    __table_args__ = (
        Index('idx_festival_date_type', 'date', 'festival_type'),
        Index('idx_festival_importance', 'importance', 'date'),
        Index('idx_festival_holiday', 'is_public_holiday', 'date'),
        Index('idx_festival_name', 'name'),
    )


class MuhurthamPeriod(Base):
    """
    Model for storing auspicious time periods (muhurtham).
    
    This table stores pre-calculated auspicious times for various events
    like marriages, house warming, business openings, etc.
    """
    __tablename__ = "muhurtham_periods"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Date and location
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    timezone: Mapped[str] = mapped_column(String(50), nullable=False, default="Asia/Kolkata")
    
    # Event information
    event_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # marriage, house_warming, etc.
    event_subtype: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Auspicious periods
    auspicious_periods: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    
    # Panchangam conditions
    required_tithi: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    required_nakshatra: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    required_yoga: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    avoided_tithi: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    avoided_nakshatra: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    
    # Related panchangam data
    panchang_day_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("panchang_days.id"), nullable=True)
    panchang_day: Mapped[Optional[PanchangDay]] = relationship("PanchangDay", backref="muhurtham_periods")
    
    # Metadata
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Indexes for efficient querying
    __table_args__ = (
        Index('idx_muhurtham_date_type', 'date', 'event_type'),
        Index('idx_muhurtham_location', 'latitude', 'longitude', 'timezone'),
    )
